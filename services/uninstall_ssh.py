# services/install_ssh.py
from common.utils import run_cmd
import os



# ========================
# 🔁 反向操作：卸载 + 清理
# ========================

def uninstall_ssh():
    print("\n🗑️  卸载 SSH 服务...")
    # 停止服务（避免卸载时警告）
    run_cmd(["sudo", "systemctl", "stop", "ssh"], ignore_error=True)
    run_cmd(["sudo", "apt", "remove", "--purge", "openssh-server", "-y"])
    run_cmd(["sudo", "apt", "autoremove", "-y"])
    print("✅ SSH 已卸载")

def remove_bash_prompt_config():
    """从 ~/.bashrc 中移除自动添加的带 IP 提示符配置"""
    print("\n🧹 清理命令提示符 IP 显示配置...")
    
    bashrc_path = os.path.expanduser("~/.bashrc")
    marker_start = "# === Auto-added by install_ssh_rdp.py: show IP in prompt ==="
    marker_end = "# ========================================================="

    try:
        with open(bashrc_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("ℹ️  ~/.bashrc 不存在，跳过清理")
        return

    # 过滤掉标记之间的所有行（包括标记行本身）
    new_lines = []
    skip = False
    for line in lines:
        if marker_start in line:
            skip = True
            continue
        if skip and marker_end in line:
            skip = False
            continue
        if not skip:
            new_lines.append(line)

    # 如果内容有变化，写回文件
    if len(new_lines) != len(lines):
        with open(bashrc_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("✅ IP 提示符配置已从 ~/.bashrc 移除")
        print("💡 请重新登录 SSH 或运行: source ~/.bashrc 使更改生效")
    else:
        print("ℹ️  未找到自动添加的配置，跳过清理")

def uninstall_ssh_with_prompt():
    """组合任务：卸载 SSH + 清理提示符配置"""
    uninstall_ssh()
    remove_bash_prompt_config()


    