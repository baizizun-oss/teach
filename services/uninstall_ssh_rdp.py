# services/uninstall_ssh_rdp.py
import os
from common.utils import run_cmd

def uninstall_ssh_rdp():
    '''
    回滚 install_ssh_rdp.py 所做的更改：
    - 卸载 xrdp、xfce4 等远程桌面相关组件
    - 恢复 xrdp 配置文件
    - 移除用户组和防火墙规则（可选）
    '''
    print("\n🗑️  正在回滚 SSH 与远程桌面服务配置...")

    # 1. 停止并禁用 xrdp 服务
    run_cmd(["sudo", "systemctl", "stop", "xrdp"], check=False)
    run_cmd(["sudo", "systemctl", "disable", "xrdp"], check=False)

    # 2. 恢复 /etc/xrdp/startwm.sh（如果存在备份）
    startwm_path = "/etc/xrdp/startwm.sh"
    backup_path = "/etc/xrdp/startwm.sh.bak"

    if os.path.exists(backup_path):
        print("🔄 正在恢复原始 xrdp 启动脚本...")
        run_cmd(["sudo", "mv", backup_path, startwm_path], check=True)
    else:
        print("ℹ️  未找到 startwm.sh 备份，跳过恢复。")

    # 3. 从 ssl-cert 组中移除 xrdp 用户（如果存在）
    run_cmd(["sudo", "deluser", "xrdp", "ssl-cert"], check=False)

    # 4. 卸载远程桌面相关软件（保留 openssh-server！）
    print("🗑️  正在卸载 xrdp、XFCE4 及相关组件...")
    packages_to_remove = [
        "xrdp",
        "xfce4",
        "xfce4-goodies",
        "xorg",
        "dbus-x11",
        "sqlitebrowser"
    ]
    run_cmd(["sudo", "apt", "remove", "-y"] + packages_to_remove, check=False)
    # 可选：清理不再需要的依赖（自动标记为 auto-installed 的包）
    run_cmd(["sudo", "apt", "autoremove", "-y"], check=False)

    # 5. 【可选】删除 xrdp 配置目录（谨慎！）
    # 如果你确定不再使用 xrdp，可取消注释以下行：
    # run_cmd(["sudo", "rm", "-rf", "/etc/xrdp"], check=False)

    # 6. 【可选】移除防火墙规则（默认保留，避免误断网）
    # 如果你希望彻底清理，可启用以下命令：
    # run_cmd(["sudo", "ufw", "delete", "allow", "3389/tcp"], check=False)
    # run_cmd(["sudo", "ufw", "delete", "allow", "22/tcp"], check=False)  # ⚠️ 别删 SSH！

    print("✅ xrdp 和 XFCE4 已卸载，配置已回滚。")
    print("💡 SSH 服务（openssh-server）已保留，如需卸载请手动操作。")