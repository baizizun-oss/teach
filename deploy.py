#!/usr/bin/env python3
# deploy.py


# ==============================
# ✅ 正常业务逻辑（此时已是 Python 3.7+）
# ==============================

import yaml  # 确保能导入（由 venv 安装）
import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from common.utils import run_cmd
    from projects.deploy_sangao import deploy_sangao
    from services.install_rustdesk import install_rustdesk
    from services.install_nfs_server import install_nfs_server
    from services.install_nginx import install_nginx
    from services.install_nfs import install_nfs
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
    

    run_cmd(['sudo', 'apt', 'update'])#在此处统一执行更新，各个模块中不再更新
    install_rustdesk()
    install_nginx()
    install_nfs_server()
    install_nfs()
    deploy_sangao()


if __name__ == "__main__":
    main()