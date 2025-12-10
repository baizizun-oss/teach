#!/usr/bin/env python3
# deploy.py
import sys
import os

# 添加当前目录到 Python 路径，以便导入子模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from services.uninstall_ssh import uninstall_ssh_with_prompt
    from projects.undeploy_sangao import undeploy_sangao
    from projects.undeploy_transaciton_manager import undeploy_transaction_manager
    from projects.uninstall_sangao import undeploy_sangao
    from services.uninstall_docker import uninstall_docker
    from services.uninstall_dnsmasq import uninstall_dnsmasq
    from services.uninstall_nginx import uninstall_nginx

except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    print("请确保目录结构正确，并在 /server-deploy/ 目录下运行此脚本。")
    sys.exit(1)

def main():
    print("=" * 60)
    print("🔧 服务器一键卸载系统（模块化版）")
    print("=" * 60)


    #项目卸载
    # undeploy_sangao()
    # undeploy_transaction_manager()
    # undeploy_sangao()

    #服务卸载
    # uninstall_docker()
    #uninstall_ssh_with_prompt()
    # uninstall_dnsmasq()
    # uninstall_nginx()



if __name__ == "__main__":
    main()