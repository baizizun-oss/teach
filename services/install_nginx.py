# services/install_nginx.py
import os
from common.utils import run_cmd

NGINX_SITES_AVAILABLE = "/etc/nginx/sites-available"
NGINX_SITES_ENABLED = "/etc/nginx/sites-enabled"

def install_nginx():
    print("\n🌐 安装并配置 Nginx 反向代理...")

    # run_cmd(["sudo", "apt", "update"])
    run_cmd(["sudo", "apt", "install", "nginx", "-y"])

    # === 主入口：花生壳域名 bgp1984.eicp.net ===
    main_conf = f"""
server {{
    listen 80;
    server_name 192.168.100.181 _;

    client_max_body_size 5G;

    location / {{
        proxy_pass http://192.168.100.182:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering on;
        proxy_buffering on;
        client_max_body_size 5G;
    }}

    # /organization → 192.168.100.182:9000
    location /organization {{
        proxy_pass http://192.168.100.182:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering on;
        proxy_buffering on;
        client_max_body_size 5G;
    }}

    location /static_jobs_recordings {{
        proxy_pass http://192.168.100.182:9000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering on;
        proxy_buffering on;
        client_max_body_size 5G;
    }}

    # /sangao → 192.168.100.184:8080
    location /sangao {{
        proxy_pass http://192.168.100.181:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /sangao_admin {{
        proxy_pass http://192.168.100.181:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /static_operation_question_files/ {{
        proxy_pass http://192.168.100.181:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /static_operation_question_images/ {{
        proxy_pass http://192.168.100.181:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /static_single_choice_question_images/ {{
        proxy_pass http://192.168.100.181:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /static_Answer_files/ {{
        proxy_pass http://192.168.100.181:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /static_operation_question_video/ {{
        proxy_pass http://192.168.100.181:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /board_pic/ {{
        proxy_pass http://192.168.100.181:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /static_Question_js/ {{
        proxy_pass http://192.168.100.181:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /static_js/ {{
        proxy_pass http://192.168.100.181:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /teacher_exam {{
        proxy_pass http://192.168.100.183:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /transaction_manager {{
        proxy_pass http://192.168.100.183:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /task {{
        proxy_pass http://192.168.100.183:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /task_develop {{
        proxy_pass http://192.168.100.183:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /task_develop_test {{
        proxy_pass http://192.168.100.183:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /myportal {{
        proxy_pass http://192.168.100.183:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /warehouse_manager {{
        proxy_pass http://192.168.100.183:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}
}}
"""

    # === 新增：NAT123 域名分流 ===
    nat123_conf = f"""
server {{
    listen 80;
    server_name 11101f92.nat123.top;

    client_max_body_size 5G;

    location / {{
        proxy_pass http://192.168.100.183:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
        client_max_body_size 5G;
    }}
    location /transaction_manager {{
        proxy_pass http://192.168.100.183:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /task {{
        proxy_pass http://192.168.100.183:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /task_develop {{
        proxy_pass http://192.168.100.183:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /task_develop_test {{
        proxy_pass http://192.168.100.183:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /myportal {{
        proxy_pass http://192.168.100.183:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}

    location /warehouse_manager {{
        proxy_pass http://192.168.100.183:8081;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_request_buffering off;
    }}
}}    
"""

    # 合并两个 server 块
    full_conf = main_conf.strip() + "\n\n" + nat123_conf.strip()

    conf_path = "/tmp/multi-sites.conf"
    with open(conf_path, "w") as f:
        f.write(full_conf)

    run_cmd(["sudo", "mv", conf_path, f"{NGINX_SITES_AVAILABLE}/multi-sites"])
    run_cmd(["sudo", "ln", "-sf", f"{NGINX_SITES_AVAILABLE}/multi-sites", f"{NGINX_SITES_ENABLED}/multi-sites"])
    run_cmd(["sudo", "rm", "-f", f"{NGINX_SITES_ENABLED}/default"], check=False)

    # 测试并重载
    run_cmd(["sudo", "nginx", "-t"])
    run_cmd(["sudo", "systemctl", "reload", "nginx"])
    run_cmd(["sudo", "ufw", "allow", "80/tcp"], check=False)

    print("✅ Nginx 配置完成！")
    print("   花生壳主站: http://bgp1984.eicp.net/...       → 多后端分流")
    print("   NAT123 分流: http://11101f92.nat123.top/      → 192.168.100.183:8081")