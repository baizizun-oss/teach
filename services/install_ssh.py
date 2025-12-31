# services/install_ssh.py
from common.utils import run_cmd
import os

def install_ssh():
    print("\n📦 安装 SSH 服务...")
    run_cmd(["sudo", "apt", "update"])
    run_cmd(["sudo", "apt", "install", "openssh-server", "-y"])
    print("✅ SSH 安装完成")

def configure_bash_prompt_with_ip():
    """向 ~/.bashrc 添加带 IP 的简洁命令提示符"""
    print("\n🎨 配置命令提示符显示 IP 地址...")
    
    bashrc_path = os.path.expanduser("~/.bashrc")
    marker = "# === Auto-added by install_ssh_rdp.py: show IP in prompt ==="

    # 检查是否已存在
    try:
        with open(bashrc_path, 'r') as f:
            if marker in f.read():
                print("ℹ️  命令提示符配置已存在，跳过")
                return
    except FileNotFoundError:
        pass

    # 新的片段：直接设置 PS1，不依赖原值
    snippet = f'''
{marker}
# 动态获取主 IP 并设置提示符
get_ip_for_prompt() {{
    local ip=$(hostname -I | awk '{{print $1}}')
    if [[ -z "$ip" ]]; then
        ip="no-ip"
    fi
    # 简洁格式: user@host(ip):path$
    PS1="\\u@\\h($ip):\\w\\$ "
}}
PROMPT_COMMAND=get_ip_for_prompt
# 初始化一次（对当前会话有效）
get_ip_for_prompt
# =========================================================
'''

    with open(bashrc_path, 'a') as f:
        f.write(snippet)

    print("✅ 命令提示符配置已写入 ~/.bashrc")
    print("💡 请重新登录 SSH 或运行: source ~/.bashrc")

def install_ssh_with_prompt():
    """组合任务：安装 SSH + 配置带 IP 的提示符"""
    install_ssh()
    configure_bash_prompt_with_ip()