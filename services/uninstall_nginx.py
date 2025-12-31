# services/uninstall_nginx.py
from common.utils import run_cmd
import os

NGINX_SITES_AVAILABLE = "/etc/nginx/sites-available"
NGINX_SITES_ENABLED = "/etc/nginx/sites-enabled"

def uninstall_nginx():
    print("\n🗑️  正在卸载自定义 Nginx 配置...")

    # === 1. 删除启用的站点链接 ===
    enabled_link = f"{NGINX_SITES_ENABLED}/multi-sites"
    if os.path.exists(enabled_link) or os.path.islink(enabled_link):
        print(f"🔗 删除启用的站点: {enabled_link}")
        run_cmd(["sudo", "rm", "-f", enabled_link])

    # === 2. 删除可用站点配置文件 ===
    available_conf = f"{NGINX_SITES_AVAILABLE}/multi-sites"
    if os.path.exists(available_conf):
        print(f"🧹 删除站点配置: {available_conf}")
        run_cmd(["sudo", "rm", "-f", available_conf])

    # === 3. （可选）恢复 default 站点？===
    # 原安装脚本删除了 default，但卸载时一般不自动恢复
    # 如果你希望恢复，取消下面注释：
    #
    # default_enabled = f"{NGINX_SITES_ENABLED}/default"
    # if not os.path.exists(default_enabled):
    #     print("🔄 恢复默认站点配置...")
    #     run_cmd(["sudo", "ln", "-sf", f"{NGINX_SITES_AVAILABLE}/default", default_enabled])

    # === 4. 重载 Nginx 使配置生效 ===
    print("🔄 重载 Nginx 配置...")
    run_cmd(["sudo", "nginx", "-t"], desc="检查 Nginx 配置", check=False)
    run_cmd(["sudo", "systemctl", "reload", "nginx"], desc="重载 Nginx", check=False)

    # === 5. 清理 UFW 防火墙规则（忽略失败）===
    print("🛡️  尝试删除 UFW 中的 80/tcp 规则...")
    run_cmd(["sudo", "ufw", "delete", "allow", "80/tcp"], check=False)

    # === 6. （可选）彻底卸载 Nginx 软件包？===
    # 如果你确实想完全移除 Nginx（包括所有配置、日志等），取消下面注释：
    #
    # print("📦 彻底卸载 Nginx 软件包...")
    # run_cmd(["sudo", "apt", "remove", "--purge", "nginx", "-y"], check=False)
    # run_cmd(["sudo", "apt", "autoremove", "-y"], check=False)
    # # 注意：这会删除 /etc/nginx 整个目录！

    print("\n✅ 自定义 Nginx 配置已卸载！")
    print("   Nginx 服务仍在运行（如需完全移除，请手动卸载 nginx 包）")