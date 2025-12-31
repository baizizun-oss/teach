# services/install_dnsmasq.py
from common.utils import run_cmd, get_local_ip
import os
import subprocess

def install_dnsmasq():
    print("\n📡 安装并配置本地 DNS (dnsmasq)...")
    
    # === 彻底禁用 systemd-resolved ===
    print("🔧 停用并屏蔽 systemd-resolved 以释放 53 端口...")
    run_cmd(["sudo", "systemctl", "stop", "systemd-resolved"], check=False)
    run_cmd(["sudo", "systemctl", "disable", "systemd-resolved"], check=False)
    run_cmd(["sudo", "systemctl", "mask", "systemd-resolved"], check=False)

    if os.path.islink("/etc/resolv.conf"):
        print("🗑️  删除 /etc/resolv.conf 符号链接...")
        run_cmd(["sudo", "rm", "-f", "/etc/resolv.conf"])
    with open("/tmp/resolv.conf", "w") as f:
        f.write("nameserver 8.8.8.8\n")
    run_cmd(["sudo", "mv", "/tmp/resolv.conf", "/etc/resolv.conf"])

    # === 安装 dnsmasq ===
    run_cmd(["sudo", "apt", "install", "dnsmasq", "-y"])

    # === 自动获取主网卡（使用原生 subprocess 避免 run_cmd 限制）===
    try:
        result = subprocess.run(
            ["ip", "route", "show", "default"],
            capture_output=True, text=True, check=True
        )
        main_iface = result.stdout.split()[4]
    except Exception as e:
        print(f"⚠️  获取主网卡失败 ({e})，回退到 eth0")
        main_iface = "eth0"

    local_ip = get_local_ip()
    print(f"🌐 使用 IP {local_ip}，网卡 {main_iface}")

    # === 生成配置 ===
    dnsmasq_conf = f"""# 本地开发 DNS
interface={main_iface}
bind-interfaces
domain-needed
bogus-priv
address=/bgp1984.eicp.net/{local_ip}
address=/bgp1982.eicp.net/{local_ip}
address=/sangao.eicp.net/{local_ip}
server=114.114.114.114
server=8.8.8.8
cache-size=500
"""
    with open("/tmp/dnsmasq.conf", "w") as f:
        f.write(dnsmasq_conf.strip())
    run_cmd(["sudo", "mv", "/tmp/dnsmasq.conf", "/etc/dnsmasq.conf"])

    # === 启动服务 ===
    run_cmd(["sudo", "systemctl", "daemon-reload"])
    run_cmd(["sudo", "systemctl", "restart", "dnsmasq"])
    run_cmd(["sudo", "systemctl", "enable", "dnsmasq"])

    # === 防火墙 ===
    run_cmd(["sudo", "ufw", "allow", "53/tcp"], check=False)
    run_cmd(["sudo", "ufw", "allow", "53/udp"], check=False)

    # === 验证 ===
    print("\n🔍 检查 dnsmasq 状态...")
    try:
        result = subprocess.run(
            ["sudo", "systemctl", "is-active", "dnsmasq"],
            capture_output=True, text=True, check=True
        )
        if result.stdout.strip() == "active":
            print(f"✅ dnsmasq 已成功运行！客户端 DNS 请设为: {local_ip}")
        else:
            raise Exception("not active")
    except:
        print("❌ dnsmasq 启动失败！查看日志：")
        subprocess.run(["sudo", "journalctl", "-u", "dnsmasq", "-n", "30", "--no-pager"])
        raise RuntimeError("dnsmasq 未正常启动")