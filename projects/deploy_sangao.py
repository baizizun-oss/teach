# projects/deploy_sangao.py
import os
import yaml
import subprocess
from common.utils import run_cmd
from services.install_docker import install_docker

# === 阿里云 CR 配置（仅用于个人环境）===
ALIYUN_CR_REGISTRY = "crpi-3lvooynrry6ot6hx.cn-hangzhou.personal.cr.aliyuncs.com"
ALIYUN_CR_USERNAME = "special198412@hotmail.com"
ALIYUN_CR_PASSWORD = "founder#021665"
PRIVATE_UBUNTU_IMAGE = f"{ALIYUN_CR_REGISTRY}/baigaopeng/ubuntu:20.04"
TARGET_BASE_IMAGE = "ubuntu:20.04"


def ensure_aliyun_ubuntu_image():
    """确保 ubuntu:20.04 镜像存在（通过阿里云私有仓库）"""
    # 检查是否已有 ubuntu:20.04
    result = subprocess.run(
        ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"],
        capture_output=True, text=True
    )
    local_images = set(line.strip() for line in result.stdout.splitlines()) if result.stdout else set()

    if TARGET_BASE_IMAGE in local_images:
        print(f"✅ 本地已存在 {TARGET_BASE_IMAGE}，跳过拉取")
        return

    print(f"🔑 正在登录阿里云容器镜像服务 ({ALIYUN_CR_REGISTRY})...")
    login_cmd = [
        "docker", "login",
        "--username", ALIYUN_CR_USERNAME,
        "--password", ALIYUN_CR_PASSWORD,
        ALIYUN_CR_REGISTRY
    ]
    # 使用 run_cmd 但隐藏密码（避免日志泄露）
    subprocess.run(login_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("✅ 登录成功")

    print(f"📥 正在拉取私有镜像: {PRIVATE_UBUNTU_IMAGE}")
    run_cmd(["docker", "pull", PRIVATE_UBUNTU_IMAGE])

    print(f"🏷️  重命名镜像为 {TARGET_BASE_IMAGE}")
    run_cmd(["docker", "tag", PRIVATE_UBUNTU_IMAGE, TARGET_BASE_IMAGE])

    print(f"✅ 基础镜像 {TARGET_BASE_IMAGE} 已准备就绪")


def deploy_sangao():
    # 确保 Docker 已安装
    install_docker()

    # 确保 ubuntu:20.04 镜像可用（从私有源）
    ensure_aliyun_ubuntu_image()

    # ✅ 动态获取脚本所在目录，并定位到同级 projects/sangao
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    proj_dir = os.path.join(SCRIPT_DIR, "sangao")

    if not os.path.exists(proj_dir):
        print(f"⚠️  {proj_dir} 目录不存在，跳过部署")
        return

    print(f"\n🚀 部署 {proj_dir} 项目...")
    original_dir = os.getcwd()
    compose_file = os.path.join(proj_dir, "docker-compose.yml")
    temp_compose = os.path.join(proj_dir, "docker-compose.build.yml")

    try:
        os.chdir(proj_dir)

        # === 新增逻辑：检查并清理旧容器 ===
        print("🔍 检查是否存在旧的 sangao 容器...")
        result = subprocess.run(
            ["docker", "compose", "-f", compose_file, "ps", "-q"],
            capture_output=True,
            text=True
        )
        if result.stdout.strip():
            print("🛑 发现正在运行或已停止的容器，正在停止并删除...")
            run_cmd(["docker", "compose", "-f", compose_file, "down"])
        else:
            print("ℹ️  未发现旧容器，继续部署...")

        # 读取并修改 compose 文件（确保 build 不 pull）
        with open(compose_file, 'r', encoding='utf-8') as f:
            compose_config = yaml.safe_load(f)

        # 如果未来启用了 build，强制禁用 pull
        if compose_config.get('services', {}).get('app', {}).get('build') is not None:
            if 'build' not in compose_config['services']['app']:
                compose_config['services']['app']['build'] = {}
            compose_config['services']['app']['build']['pull'] = False
            compose_config['services']['app']['build']['no_cache'] = False  # 可选

            with open(temp_compose, 'w', encoding='utf-8') as f:
                yaml.dump(compose_config, f, default_flow_style=False, allow_unicode=True)
            compose_to_use = temp_compose
        else:
            # 当前未启用 build，直接使用原文件
            compose_to_use = compose_file
            print("ℹ️  docker-compose.yml 未启用 build，跳过构建配置修改")

        print("▶️  启动 sangao 容器...")
        run_cmd(["docker", "compose", "-f", compose_to_use, "up", "-d", "--build"])
    finally:
        os.chdir(original_dir)
        if os.path.exists(temp_compose):
            os.remove(temp_compose)

    print(f"✅ {proj_dir} 部署完成（端口: 80）")