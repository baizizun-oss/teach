# services/install_nginx.py
import os
from common.utils import run_cmd

NGINX_SITES_AVAILABLE = "/etc/nginx/sites-available"
NGINX_SITES_ENABLED = "/etc/nginx/sites-enabled"

def install_nginx():
    print("\n🌐 安装并配置 Nginx 反向代理...")
    
    # 1. 安装 Nginx
    run_cmd(["sudo", "apt", "update"])
    run_cmd(["sudo", "apt", "install", "nginx", "-y"])
    
    # 2. 创建站点配置：统一使用 bgp1984.eicp.net 的路径路由
    nginx_conf = f"""
server {{
    listen 80;
    server_name bgp1984.eicp.net _;

    # /sangao → 192.168.100.181:80
    location /sangao {{
        proxy_pass http://192.168.100.181:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }}

    # /sangao → 192.168.100.182:80
    location /sangao {{
        proxy_pass http://192.168.100.182:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }}

    # /transaction_manager → 192.168.100.183:80
    location /transaction_manager {{
        proxy_pass http://192.168.100.183:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }}

    # 可选：根路径跳转或返回欢迎页
    location = / {{
        return 200 'Welcome to bgp1984.eicp.net\\nUse /sangao, /sangao, or /transaction_manager\\n';
        add_header Content-Type text/plain;
    }}
}}
"""
    
    # 3. 写入配置文件
    conf_path = "/tmp/multi-sites.conf"
    with open(conf_path, "w") as f:
        f.write(nginx_conf.strip())
    
    run_cmd(["sudo", "mv", conf_path, f"{NGINX_SITES_AVAILABLE}/multi-sites"])
    run_cmd(["sudo", "ln", "-sf", f"{NGINX_SITES_AVAILABLE}/multi-sites", f"{NGINX_SITES_ENABLED}/multi-sites"])
    
    # 4. 删除 default 站点（避免冲突）
    run_cmd(["sudo", "rm", "-f", f"{NGINX_SITES_ENABLED}/default"], check=False)
    
    # 5. 重载 Nginx
    run_cmd(["sudo", "nginx", "-t"], desc="检查 Nginx 配置")
    run_cmd(["sudo", "systemctl", "reload", "nginx"], desc="重载 Nginx")
    run_cmd(["sudo", "ufw", "allow", "80/tcp"], check=False)
    
    print("✅ Nginx 配置完成！请确保花生壳将公网 80 端口映射到此服务器的 80 端口")
    print("   访问示例：")
    print("     http://bgp1984.eicp.net/sangao")
    print("     http://bgp1984.eicp.net/sangao")
    print("     http://bgp1984.eicp.net/transaction_manager")