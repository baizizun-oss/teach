# services/uninstall_base.py
from common.utils import run_cmd
import os

def uninstall_base():
    print("\n🗑️  正在卸载基础软件：Google Chrome + VSCode + Fcitx5...")

    # ========================
    # 1. 卸载主程序
    # ========================
    print("▶️ 卸载 Google Chrome、VSCode 和 Fcitx5...")
    run_cmd([
        "sudo", "apt", "remove", "-y",
        "google-chrome-stable",
        "code",
        "fcitx5",
        "fcitx5-pinyin",
        "fcitx5-frontend-gtk3",
        "fcitx5-frontend-qt5"
    ], check=False)

    # ========================
    # 2. 删除 APT 源和 GPG 密钥
    # ========================
    print("🧹 清理 APT 源和密钥...")
    # Chrome
    run_cmd(["sudo", "rm", "-f", "/etc/apt/sources.list.d/google-chrome.list"], check=False)
    run_cmd(["sudo", "rm", "-f", "/etc/apt/trusted.gpg.d/google-chrome.gpg"], check=False)
    # VSCode
    run_cmd(["sudo", "rm", "-f", "/etc/apt/sources.list.d/vscode.list"], check=False)
    run_cmd(["sudo", "rm", "-f", "/etc/apt/trusted.gpg.d/microsoft.gpg"], check=False)

    # ========================
    # 3. 清理用户配置（可选）
    # ========================
    home = os.path.expanduser("~")
    
    # Fcitx5 用户数据
    fcitx5_dir = os.path.join(home, ".local", "share", "fcitx5")
    if os.path.exists(fcitx5_dir):
        print(f"🧹 删除 Fcitx5 用户配置: {fcitx5_dir}")
        run_cmd(["rm", "-rf", fcitx5_dir], check=False)

    # VSCode 用户配置（谨慎！会丢失设置、扩展等）
    vscode_config = os.path.join(home, ".config", "Code")
    if os.path.exists(vscode_config):
        print(f"🧹 删除 VSCode 用户配置: {vscode_config}")
        run_cmd(["rm", "-rf", vscode_config], check=False)

    # Chrome 用户数据（通常不建议自动删，这里跳过）
    # 如需清理，可手动删除 ~/.config/google-chrome

    # ========================
    # 4. 恢复输入法框架
    # ========================
    print("🔄 恢复默认输入法配置...")
    run_cmd(["im-config", "-n", "default"], check=False)

    # ========================
    # 5. 清理无用依赖
    # ========================
    run_cmd(["sudo", "apt", "autoremove", "-y"], check=False)

    print("✅ Google Chrome、VSCode 和 Fcitx5 已卸载，系统已回滚。")