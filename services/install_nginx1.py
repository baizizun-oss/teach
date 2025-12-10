# services/install_nginx.py
import os
from common.utils import run_cmd, get_local_ip

NGINX_SITES_AVAILABLE = "/etc/nginx/sites-available"
NGINX_SITES_ENABLED = "/etc/nginx/sites-enabled"

def install_nginx():
    print("\n🌐 安装并配置 Nginx 反向代理...")
    
    # 1. 安装 Nginx
    run_cmd(["sudo", "apt", "update"])
    run_cmd(["sudo", "apt", "install", "nginx", "-y"])
    
    # 2. 创建站点配置
    nginx_conf = f"""
# transaction (外网域名:bgp1984.eicp.net:12310,内网域名:192.168.100.182:8001)
server {{
    listen 12310;
    server_name bgp1984.eicp.net _;

    location / {{
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}

# sangao (外网域名暂时没有,内网为192.168.100.182:8083)
server {{
    listen 80;
    server_name sangao.eicp.net;

    location / {{
        proxy_pass http://127.0.0.1:8083;  
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
}}

# sangao → (外网域名:bgp1984.eicp.net,内网域名:192.168.100.182:9000)
server {{
    listen 80;
    server_name bgp1984.eicp.net _;

    location / {{
        proxy_pass http://127.0.0.1:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
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
    
    print("✅ Nginx 配置完成！请确保花生壳映射 80 → 此服务器 80 端口")