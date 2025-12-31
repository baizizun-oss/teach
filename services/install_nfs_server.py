#!/usr/bin/env python3
# services/install_nfs_server.py

import os
import sys
import subprocess
from pathlib import Path

def run_cmd(cmd, check=True, cwd=None):
    """执行 shell 命令，支持错误检查"""
    cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
    print(f"▶️ 执行: {cmd_str}")
    result = subprocess.run(
        cmd,
        shell=isinstance(cmd, str),
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    if result.returncode != 0:
        if check:
            print(f"❌ 命令失败 (exit {result.returncode}):\n{result.stdout}")
            sys.exit(1)
        else:
            print(f"⚠️ 命令失败（已忽略）:\n{result.stdout}")
    else:
        output = result.stdout.strip()
        if output:
            print(output)
        else:
            print("✅ 成功")
    return result

def install_nfs_server(
    share_dir="/home/bgp1984/projects/nfs_server/server_181",
    client_spec="192.168.100.0/24",  # 可改为 "*" 表示所有
    options="rw,sync,no_subtree_check,no_root_squash"
):
    """
    安装并配置 NFS 服务器
    
    :param share_dir: 共享目录路径
    :param client_spec: 客户端访问规则（IP、网段或 *）
    :param options: NFS 导出选项
    """
    print("\n📦 安装 NFS 服务器...")

    # 1. 安装 nfs-utils（Ubuntu/Debian 用 nfs-kernel-server，此处假设为 CentOS/RHEL/Ubuntu 混合环境）
    # 先尝试 yum/dnf，再 fallback 到 apt
    pkg_manager = None
    if Path("/usr/bin/yum").exists() or Path("/usr/bin/dnf").exists():
        pkg_manager = "yum" if Path("/usr/bin/yum").exists() else "dnf"
        run_cmd(["sudo", pkg_manager, "install", "-y", "nfs-utils"])
    elif Path("/usr/bin/apt").exists():
        # run_cmd(["sudo", "apt", "update"])
        run_cmd(["sudo", "apt", "install", "-y", "nfs-kernel-server"])
        pkg_manager = "apt"
    else:
        print("❌ 不支持的包管理器，请手动安装 nfs-utils 或 nfs-kernel-server")
        sys.exit(1)

    # 2. 创建共享目录
    share_path = Path(share_dir)
    if not share_path.exists():
        print(f"📁 创建共享目录: {share_dir}")
        run_cmd(["sudo", "mkdir", "-p", str(share_path)])
    run_cmd(["sudo", "chmod", "755", str(share_path)])
    run_cmd(["sudo", "chown", "nobody:nogroup", str(share_path)])  # Ubuntu 默认用户；CentOS 可用 nfsnobody

    # 3. 配置 /etc/exports
    export_line = f"{share_dir} {client_spec}({options})"
    exports_path = Path("/etc/exports")
    
    # 备份原文件
    if exports_path.exists():
        run_cmd(["sudo", "cp", "/etc/exports", "/etc/exports.bak"])

    # 写入新配置（覆盖模式，简单起见）
    print(f"📝 配置 NFS 导出: {export_line}")
    with open("/tmp/exports.new", "w") as f:
        f.write(export_line + "\n")
    run_cmd(["sudo", "mv", "/tmp/exports.new", "/etc/exports"])
    run_cmd(["sudo", "chmod", "644", "/etc/exports"])

    # 4. 启动服务
    print("🔄 启动 NFS 服务...")
    if pkg_manager in ("yum", "dnf"):
        run_cmd(["sudo", "systemctl", "enable", "--now", "rpcbind"])
        run_cmd(["sudo", "systemctl", "enable", "--now", "nfs-server"])
    else:  # apt (Ubuntu/Debian)
        run_cmd(["sudo", "systemctl", "enable", "--now", "nfs-kernel-server"])

    # 5. 重新导出
    run_cmd(["sudo", "exportfs", "-arv"])

    # 6. （可选）配置防火墙（简化处理，实际生产需细化）
    if pkg_manager == "apt":
        run_cmd(["sudo", "ufw", "allow", "2049/tcp"], check=False)
    else:
        run_cmd(["sudo", "firewall-cmd", "--permanent", "--add-service=nfs"], check=False)
        run_cmd(["sudo", "firewall-cmd", "--reload"], check=False)

    print(f"\n✅ NFS 服务器配置完成！")
    print(f"   共享目录: {share_dir}")
    print(f"   客户端访问: {client_spec}")
    print(f"   挂载命令示例: sudo mount {os.uname().nodename}:{share_dir} /mnt")


# ==============================
# 供 deploy.py 调用的统一入口
# ==============================
def install_nfs():
    """标准接口函数，供 deploy.py 调用"""
    install_nfs_server(
        share_dir="/data/nfs_share",
        client_spec="192.168.100.0/24",  # 根据你的网络调整
        options="rw,sync,no_subtree_check,no_root_squash"
    )


if __name__ == "__main__":
    # 可独立运行测试
    install_nfs()