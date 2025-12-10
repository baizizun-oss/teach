# services/install_ssh_rdp.py
from common.utils import run_cmd

def install_ssh_rdp():
    print("\n📦 安装 SSH 与远程桌面服务...")
    run_cmd(["sudo", "apt", "update"])
    run_cmd(["sudo", "apt", "install", "openssh-server", "xrdp", "sqlitebrowser", "-y"])
    run_cmd(["sudo", "adduser", "xrdp", "ssl-cert"], desc="修复 xrdp 权限")
    run_cmd(["sudo", "ufw", "allow", "22/tcp"], check=False)
    run_cmd(["sudo", "ufw", "allow", "3389/tcp"], check=False)
    print("✅ SSH 和 RDP 安装完成")