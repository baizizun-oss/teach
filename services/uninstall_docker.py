# services/uninstall_docker.py
import subprocess
import os
from common.utils import run_cmd, get_username

def has_active_docker_resources():
    """检查是否存在容器、镜像、卷、网络等 Docker 资源"""
    try:
        # 检查运行中或已停止的容器
        containers = subprocess.run(
            ["docker", "ps", "-aq"],
            capture_output=True, text=True, timeout=5
        )
        if containers.stdout.strip():
            return True

        # 检查镜像（排除中间层镜像）
        images = subprocess.run(
            ["docker", "images", "-q"],
            capture_output=True, text=True, timeout=5
        )
        if images.stdout.strip():
            return True

        # 检查卷
        volumes = subprocess.run(
            ["docker", "volume", "ls", "-q"],
            capture_output=True, text=True, timeout=5
        )
        if volumes.stdout.strip():
            return True

        # 检查自定义网络
        networks = subprocess.run(
            ["docker", "network", "ls", "--filter", "type=custom", "-q"],
            capture_output=True, text=True, timeout=5
        )
        if networks.stdout.strip():
            return True

        return False
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        # Docker 命令不可用（可能已卸载），视为无资源
        return False

def is_docker_installed():
    """检测 Docker 是否已安装（与 install_docker.py 保持一致）"""
    try:
        result = subprocess.run(
            ["docker", "info"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def uninstall_docker():
    print("\n🗑️  准备卸载 Docker...")

    if not is_docker_installed():
        print("ℹ️  Docker 未安装，无需卸载")
        return

    # 🔍 检查是否有活跃资源
    if has_active_docker_resources():
        print("⚠️  检测到系统中存在 Docker 容器、镜像、卷或网络！")
        print("💡 为避免数据丢失，本次卸载将跳过清理操作。")
        print("📌 请手动执行以下命令确认并清理（如需要）：")
        print("    docker ps -a          # 查看所有容器")
        print("    docker images         # 查看镜像")
        print("    docker system df      # 查看磁盘使用")
        print("    docker-compose down   # （如使用 Compose）")
        print("\n🛑 卸载已中止。清理完成后，请重新运行卸载命令。")
        return

    # ✅ 确认无资源，继续卸载
    print("✅ 未检测到活跃的 Docker 资源，开始卸载...")

    # 1. 停止并禁用服务
    run_cmd(["sudo", "systemctl", "stop", "docker"], check=False)
    run_cmd(["sudo", "systemctl", "disable", "docker"], check=False)

    # 2. 卸载软件包
    run_cmd([
        "sudo", "apt", "remove", "--purge",
        "docker-ce", "docker-ce-cli", "containerd.io",
        "docker-buildx-plugin", "docker-compose-plugin",
        "-y"
    ], check=False)
    run_cmd(["sudo", "apt", "autoremove", "-y"], check=False)
    run_cmd(["sudo", "apt", "autoclean"], check=False)

    # 3. 删除仓库和密钥
    run_cmd(["sudo", "rm", "-f", "/etc/apt/sources.list.d/docker-aliyun.list"], check=False)
    run_cmd(["sudo", "rm", "-f", "/usr/share/keyrings/docker-aliyun-keyring.gpg"], check=False)

    # 4. 删除配置文件
    run_cmd(["sudo", "rm", "-f", "/etc/docker/daemon.json"], check=False)

    # 5. （可选）清理残留数据目录（这里不删，因为前面已确保无资源）
    # 如果用户后续想彻底清理，可手动执行：
    # sudo rm -rf /var/lib/docker

    # 6. 将当前用户从 docker 组移除（谨慎操作）
    username = get_username()
    try:
        groups_output = subprocess.getoutput(f"groups {username}")
        if "docker" in groups_output.split():
            # 获取除 docker 外的所有组
            current_groups = [g for g in groups_output.split() if g != "docker"]
            new_groups = ",".join(current_groups) if current_groups else username
            run_cmd(["sudo", "usermod", "-G", new_groups, username], check=False)
            print(f"✅ 用户 {username} 已从 docker 组移除")
    except Exception as e:
        print(f"⚠️  移除用户组时出错（可忽略）: {e}")

    print("✅ Docker 已成功卸载！")
    print("💡 提示：如需彻底删除所有历史数据，请手动执行：")
    print("    sudo rm -rf /var/lib/docker")