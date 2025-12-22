# services/install_docker.py
import subprocess
import json
from common.utils import run_cmd, get_username

def install_docker():
    print("\n🐳 安装 Docker 并配置国内镜像...")
    run_cmd(["sudo", "apt", "install", "apt-transport-https", "ca-certificates", "curl", "software-properties-common", "-y"])

    # 添加阿里云 GPG 密钥
    run_cmd(
        'curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | '
        'sudo gpg --batch --yes --dearmor -o /usr/share/keyrings/docker-aliyun-keyring.gpg',
        shell=True
    )

    # 添加 Docker 源
    arch = subprocess.getoutput("dpkg --print-architecture")
    codename = subprocess.getoutput("lsb_release -cs")
    repo_line = f"deb [arch={arch} signed-by=/usr/share/keyrings/docker-aliyun-keyring.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu {codename} stable"
    run_cmd(f'echo "{repo_line}" | sudo tee /etc/apt/sources.list.d/docker-aliyun.list > /dev/null', shell=True)

    run_cmd(["sudo", "apt", "update"])
    run_cmd(["sudo", "apt", "install", "docker-ce", "docker-ce-cli", "containerd.io", "-y"])
    run_cmd(["sudo", "systemctl", "enable", "--now", "docker"])

    # 配置镜像加速
    docker_config = {"registry-mirrors": ["https://docker.m.daocloud.io"]}
    with open("/tmp/daemon.json", "w") as f:
        json.dump(docker_config, f, indent=2)
    run_cmd(["sudo", "mv", "/tmp/daemon.json", "/etc/docker/daemon.json"])
    run_cmd(["sudo", "systemctl", "daemon-reload"])
    run_cmd(["sudo", "systemctl", "restart", "docker"])

    # 将当前用户加入 docker 组
    username = get_username()
    run_cmd(["sudo", "usermod", "-aG", "docker", username])
    print("✅ Docker 安装并配置完成（请重新登录以生效）")