# common/utils.py
import subprocess
import os

def run_cmd(cmd, shell=False, check=True, desc=""):
    """执行系统命令，支持描述信息"""
    if desc:
        print(f"▶️ {desc}")
    else:
        cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
        print(f"▶️ 执行: {cmd_str}")
    try:
        result = subprocess.run(cmd, shell=shell, check=check, text=True, capture_output=False)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        raise

def get_local_ip():
    """获取本机局域网 IPv4 地址"""
    try:
        result = subprocess.run(
            "ip -4 addr show scope global | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}' | head -1",
            shell=True, capture_output=True, text=True
        )
        ip = result.stdout.strip()
        return ip if ip else "192.168.100.182"
    except Exception:
        return "192.168.100.182"

def get_username():
    """获取当前用户名"""
    return os.environ.get("USER") or os.getlogin()