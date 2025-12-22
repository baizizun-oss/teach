# services/install_base.py
from common.utils import run_cmd

def install_base():
    print("\n🔧 安装基础软件：Google Chrome + VSCode + Fcitx5 输入法...")

    # ========================
    # 1. 安装 Google Chrome（官方 APT 源）
    # ========================
    print("▶️ 配置 Google Chrome APT 源...")
    run_cmd([
        "sudo", "sh", "-c",
        "wget -qO- https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google-chrome.gpg && "
        "echo 'deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google-chrome.list"
    ], check=False)

    # ========================
    # 2. 安装 VSCode（微软官方 APT 源，非 Snap）
    # ========================
    print("▶️ 配置 VSCode APT 源...")
    run_cmd([
        "sudo", "sh", "-c",
        "apt install -y wget gpg && "
        "wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && "
        "echo 'deb [arch=amd64] https://packages.microsoft.com/repos/code stable main' > /etc/apt/sources.list.d/vscode.list"
    ], check=False)

    # ========================
    # 3. 更新并安装所有软件
    # ========================
    print("🔄 正在更新软件源并安装软件...")
    run_cmd(["sudo", "apt", "update"], check=False)
    run_cmd([
        "sudo", "apt", "install", "-y",
        "google-chrome-stable",
        "code",  # VSCode 的包名
        "fcitx5",
        "fcitx5-pinyin",
        "fcitx5-frontend-gtk3",
        "fcitx5-frontend-qt5",
        "fonts-wqy-microhei"
    ], check=False)

    # ========================
    # 4. 设置默认输入法为 fcitx5
    # ========================
    run_cmd(["im-config", "-n", "fcitx5"], check=False)

    print("✅ 基础软件安装完成：Google Chrome + VSCode + Fcitx5")