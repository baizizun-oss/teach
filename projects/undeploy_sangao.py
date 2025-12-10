# projects/undeploy_sangao.py
import os
from common.utils import run_cmd

def undeploy_sangao():
    proj_dir = "/home/bgp1984/projects/server_20_04/projects/sangao"
    if not os.path.exists(proj_dir):
        print(f"ℹ️  {proj_dir} 不存在，跳过卸载")
        return

    print(f"\n⏹️  卸载 sangao 项目...")
    original_dir = os.getcwd()
    compose_file = os.path.join(proj_dir, "docker-compose.yml")

    try:
        os.chdir(proj_dir)
        if os.path.exists(compose_file):
            # run_cmd(
            #     ["docker", "compose", "-f", compose_file, "down", "--volumes", "--remove-orphans"],
            #     desc="停止并删除 sangao 容器及关联卷",
            #     check=False  # 允许失败（如已停止）
            # )
            print("停止并删除 sangao 容器及关联卷")
            run_cmd(["docker", "compose", "-f", compose_file, "down", "--volumes", "--remove-orphans"])
        else:
            print("⚠️  docker-compose.yml 不存在，无法卸载")
    finally:
        os.chdir(original_dir)

    print("✅ sangao 项目已卸载")