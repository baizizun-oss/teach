# services/install_rustdesk.py
import os
import subprocess
import getpass
from common.utils import run_cmd

def is_debian_based():
    """检测是否为 Debian/Ubuntu 系统"""
    return subprocess.run(['which', 'apt'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def enable_rustdesk_autostart():
    """启用 RustDesk 用户级开机自启"""
    user = getpass.getuser()
    try:
        # 1. 启用 linger（关键！允许无登录时启动）
        print("⚙️  启用 loginctl linger（支持无用户登录时启动）...")
        run_cmd(['sudo', 'loginctl', 'enable-linger', user])

        # 2. 尝试重载用户 systemd 配置
        print("🔄 重载用户级 systemd 配置...")
        run_cmd(['systemctl', '--user', 'daemon-reload'], check=False)

        # 3. 启用 rustdesk.service（如果存在）
        # 注意：首次安装后可能尚未生成 service 文件，需启动一次 GUI 才生成
        # 但我们仍尝试启用，避免后续手动操作
        print("🔌 启用 RustDesk 用户服务（开机自启）...")
        result = run_cmd(['systemctl', '--user', 'is-enabled', 'rustdesk.service'], capture_output=True, text=True, check=False)
        if "disabled" in result.stdout or result.returncode != 0:
            run_cmd(['systemctl', '--user', 'enable', 'rustdesk.service'], check=False)
        
        # 4. 确保 .config/autostart 也有桌面自启（兼容 GNOME/KDE）
        autostart_dir = os.path.expanduser("~/.config/autostart")
        desktop_file = os.path.join(autostart_dir, "rustdesk.desktop")
        if not os.path.exists(desktop_file):
            os.makedirs(autostart_dir, exist_ok=True)
            with open(desktop_file, "w") as f:
                f.write("""[Desktop Entry]
Name=RustDesk
Exec=rustdesk --tray
Terminal=false
Type=Application
X-GNOME-Autostart-enabled=true
""")
            print("✅ 已创建桌面环境自启项 (~/.config/autostart/rustdesk.desktop)")

        return True
    except Exception as e:
        print(f"⚠️  开机自启配置部分失败（可忽略）: {e}")
        return False

def install_rustdesk():
    """
    安装本地 RustDesk 并配置开机自启
    """
    print("\n🖥️  开始安装 RustDesk（开源远程桌面工具）...")

    if not is_debian_based():
        print("❌ 不支持的系统：仅支持 Debian/Ubuntu 等 apt 系统")
        return False

    try:
        # 安装依赖
        print("🔧 更新并安装依赖...")
        # run_cmd(['sudo', 'apt', 'update'])
        run_cmd(['sudo', 'apt', 'install', '-y', 'wget', 'curl', 'ca-certificates'])

        # 安装本地 deb
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        deb_path = os.path.join(project_root, 'rustdesk-1.4.4-x86_64.deb')
        if not os.path.isfile(deb_path):
            print(f"❌ 安装包不存在: {deb_path}")
            return False

        print(f"📦 安装 {os.path.basename(deb_path)} ...")
        run_cmd(['sudo', 'apt', 'install', '-y', deb_path])

        # 配置开机自启
        enable_rustdesk_autostart()

        print("")
        print("✅ RustDesk 安装与开机自启配置完成！")
        print("👉 首次使用请从应用菜单启动一次 RustDesk（生成配置和服务）")
        print("🔑 记下 ID 和密码，用于远程连接")
        print("📱 手机端下载: https://rustdesk.com/")
        print("💡 即使注销或重启，RustDesk 也会在后台运行（支持远程唤醒）")
        print("")

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ 安装失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return False


if __name__ == "__main__":
    install_rustdesk()