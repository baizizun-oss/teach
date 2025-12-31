# services/uninstall_dnsmasq.py
from common.utils import run_cmd
import os
import subprocess

def uninstall_dnsmasq():
    print("\n🗑️  正在卸载本地 DNS (dnsmasq) 并恢复系统默认 DNS...")

    # === 1. 停止并禁用 dnsmasq ===
    print("⏹️  停止 dnsmasq 服务...")
    run_cmd(["sudo", "systemctl", "stop", "dnsmasq"], check=False)
    run_cmd(["sudo", "systemctl", "disable", "dnsmasq"], check=False)

    # === 2. 卸载 dnsmasq 软件包（含配置）===
    print("📦 卸载 dnsmasq 软件包...")
    run_cmd(["sudo", "apt", "remove", "--purge", "dnsmasq", "-y"], check=False)
    run_cmd(["sudo", "apt", "autoremove", "-y"], check=False)

    # === 3. 删除配置文件（即使 purge 未删干净）===
    conf_path = "/etc/dnsmasq.conf"
    if os.path.exists(conf_path):
        print(f"🧹 删除配置文件: {conf_path}")
        run_cmd(["sudo", "rm", "-f", conf_path])

    # === 4. 恢复 systemd-resolved ===
    print("🔄 恢复 systemd-resolved 服务...")
    run_cmd(["sudo", "systemctl", "unmask", "systemd-resolved"], check=False)
    run_cmd(["sudo", "systemctl", "enable", "systemd-resolved"], check=False)
    run_cmd(["sudo", "systemctl", "start", "systemd-resolved"], check=False)

    # === 5. 恢复 /etc/resolv.conf 为标准符号链接 ===
    print("🔗 恢复 /etc/resolv.conf 为 systemd-resolved 的符号链接...")
    run_cmd(["sudo", "rm", "-f", "/etc/resolv.conf"], check=False)
    # 使用 stub-resolv.conf（支持本地解析 + 上游转发）
    run_cmd(["sudo", "ln", "-sf", "/run/systemd/resolve/stub-resolv.conf", "/etc/resolv.conf"], check=False)

    # === 6. 清理 UFW 防火墙规则（忽略失败）===
    print("🛡️  尝试删除 UFW 中的 DNS 规则（53/tcp, 53/udp）...")
    run_cmd(["sudo", "ufw", "delete", "allow", "53/tcp"], check=False)
    run_cmd(["sudo", "ufw", "delete", "allow", "53/udp"], check=False)

    # === 7. 验证恢复状态 ===
    print("\n🔍 验证恢复结果...")

    # 检查 systemd-resolved 是否活跃
    try:
        result = subprocess.run(
            ["sudo", "systemctl", "is-active", "systemd-resolved"],
            capture_output=True, text=True, check=True
        )
        if result.stdout.strip() == "active":
            print("✅ systemd-resolved 已成功恢复运行")
        else:
            print("⚠️  systemd-resolved 未激活（但已尝试启动）")
    except Exception as e:
        print(f"⚠️  检查 systemd-resolved 状态时出错: {e}")

    # 检查 resolv.conf 是否为符号链接
    if os.path.islink("/etc/resolv.conf"):
        target = os.readlink("/etc/resolv.conf")
        print(f"✅ /etc/resolv.conf 已恢复为符号链接 → {target}")
    else:
        print("⚠️  /etc/resolv.conf 不是符号链接，可能需要手动修复")

    print("\n🎉 dnsmasq 卸载完成！系统 DNS 已恢复为默认。")