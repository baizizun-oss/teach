#!/usr/bin/env python3
# deploy.py

import sys
import os
import subprocess

# ==============================
# 🔁 自动升级 Python 环境逻辑（仅限 Ubuntu/Debian）
# ==============================

REQUIRED_PYTHON = (3, 7)
IN_UPGRADED_ENV = os.environ.get("DEPLOY_IN_VENV") == "1"

def ensure_python38_and_venv():
    """确保使用 Python 3.8+ 虚拟环境运行"""
    print("🔍 检测到 Python 版本过低，正在自动配置 Python 3.8 环境...")

    # 1. 安装 Python 3.8 和必要工具
    try:
        print("📦 正在更新 apt 并安装 Python 3.8...")
        subprocess.run(["sudo", "apt", "update"], check=True)
        subprocess.run([
            "sudo", "apt", "install", "-y",
            "python3.8", "python3.8-venv", "python3.8-dev", "python3-pip"
        ], check=True)
    except subprocess.CalledProcessError:
        print("❌ 安装 Python 3.8 失败，请检查网络或权限。")
        sys.exit(1)

    # 2. 创建虚拟环境目录（在项目内）
    venv_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".deploy_venv")
    if not os.path.exists(venv_dir):
        print(f"🛠️  创建虚拟环境: {venv_dir}")
        subprocess.run([sys.executable.replace("python3", "python3.8"), "-m", "venv", venv_dir], check=True)

    # 3. 安装依赖
    pip_path = os.path.join(venv_dir, "bin", "pip")
    print("📥 安装依赖: pyyaml")
    subprocess.run([pip_path, "install", "pyyaml"], check=True)

    # 4. 用新环境重新运行自己
    python_path = os.path.join(venv_dir, "bin", "python")
    print(f"🔄 重启脚本使用新环境: {python_path}")
    env = os.environ.copy()
    env["DEPLOY_IN_VENV"] = "1"
    os.execve(python_path, [python_path, __file__] + sys.argv[1:], env)


# ==============================
# 🚦 主逻辑入口
# ==============================

if sys.version_info < REQUIRED_PYTHON and not IN_UPGRADED_ENV:
    # 自动修复环境（仅在非虚拟环境中触发）
    ensure_python38_and_venv()
    # 不会执行到这里（os.execve 替换了进程）

# ==============================
# ✅ 正常业务逻辑（此时已是 Python 3.7+）
# ==============================

import yaml  # 确保能导入（由 venv 安装）
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:

    from projects.deploy_sangao import deploy_sangao
    from services.install_rustdesk import install_rustdesk
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    print("请确保目录结构正确。")
    sys.exit(1)


def main():
    print("=" * 60)
    print("🔧 服务器一键部署系统（模块化版）")
    print("=" * 60)
    print(f"✅ 当前 Python 版本: {sys.version.split()[0]}")

    print("\n⚠️  注意：部署过程需要多次输入 sudo 密码以完成系统配置")
    
    install_rustdesk()
    deploy_sangao()


if __name__ == "__main__":
    main()