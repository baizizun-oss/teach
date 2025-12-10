#!/usr/bin/env python3
# uninstall_ubuntu_desktop.py

from common.utils import run_cmd

def uninstall_ubuntu_desktop():
    print("⚠️  此操作将移除 Ubuntu 桌面环境（GUI），仅保留命令行系统。")
    confirm = input("是否继续？(y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ 已取消卸载。")
        return

    print("\n🗑️  正在卸载 ubuntu-desktop 及相关 GUI 组件...")
    
    # 移除桌面元包（不会删除所有 GUI，但会移除主要组件）
    try:
        run_cmd([
            "sudo", "apt", "remove",
            "--purge", "-y",
            "ubuntu-desktop",
            "ubuntu-desktop-minimal",
            "gnome-shell",
            "gdm3",          # GNOME 显示管理器
            "lightdm",       # 备用显示管理器
            "xserver-xorg",
            "x11-common"
        ])
    except Exception as e:
        print(f"⚠️  卸载部分包失败（可能未安装）: {e}")

    print("\n🧹 正在清理无用依赖...")
    run_cmd(["sudo", "apt", "autoremove", "--purge", "-y"])

    print("\n🔌 禁用图形界面启动（切换到 multi-user.target）...")
    run_cmd(["sudo", "systemctl", "set-default", "multi-user.target"])
    run_cmd(["sudo", "systemctl", "isolate", "multi-user.target"])

    print("\n✅ Ubuntu 桌面环境已卸载！")
    print("💡 系统现在将以纯命令行模式启动。")
    print("   如需恢复 GUI，请重新安装 ubuntu-desktop。")

if __name__ == "__main__":
    uninstall_ubuntu_desktop()