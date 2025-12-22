# projects/deploy_sangao.py
import os
import sys
import shutil
from pathlib import Path

def run_cmd(cmd, cwd=None, check=True):
    import subprocess
    cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd
    print(f"▶️ 执行: {cmd_str}")
    result = subprocess.run(
        cmd,
        shell=isinstance(cmd, str),
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    if result.returncode != 0:
        if check:
            print(f"❌ 命令失败 (exit {result.returncode}):\n{result.stdout}")
            sys.exit(1)
        else:
            print(f"⚠️ 命令失败（已忽略）:\n{result.stdout}")
    else:
        output = result.stdout.strip()
        if output:
            print(output)
        else:
            print("✅ 成功")
    return result  # 返回结果用于检查

def deploy_sangao():
    SCRIPT_DIR = Path(__file__).parent.resolve()
    proj_dir = SCRIPT_DIR / "sangao"

    if not proj_dir.exists():
        print(f"⚠️  {proj_dir} 目录不存在，跳过部署")
        return

    print(f"\n🚀 非容器化部署 sangao（监听 8080）...")

    VENV_DIR = proj_dir / ".venv"
    VENV_PYTHON = VENV_DIR / "bin" / "python"
    # 注意：不再使用pip_bin变量，所有pip命令都通过python -m pip执行

    # 创建虚拟环境（总是重新创建以避免pip版本问题）
    print("🗑️  删除现有虚拟环境...")
    if VENV_DIR.exists():
        shutil.rmtree(VENV_DIR)
    print("🔧 正在创建新的虚拟环境...")
    run_cmd([sys.executable, "-m", "venv", str(VENV_DIR)])

    # 升级 pip（避免旧 pip 问题）
    run_cmd([str(VENV_PYTHON), "-m", "pip", "install", "--upgrade", "pip", 
             "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",
             "--trusted-host", "pypi.tuna.tsinghua.edu.cn"])

    # 安装依赖：优先使用项目根目录下的 requirements.txt
    req_file = proj_dir / "requirements.txt"
    if req_file.exists():
        print("📦 使用 requirements.txt 安装依赖...")
        run_cmd([str(VENV_PYTHON), "-m", "pip", "install", "-r", str(req_file),
                 "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",
                 "--trusted-host", "pypi.tuna.tsinghua.edu.cn"], cwd=proj_dir)
    else:
        print("ℹ️  未找到 requirements.txt，安装项目所需的所有依赖...")
        # 安装Dockerfile中指定的所有Python库
        packages = [
            "tornado",
            "requests", 
            "python-dateutil", 
            "psutil", 
            "docker", 
            "aiohttp", 
            "openpyxl"
        ]
        
        # 使用清华源安装
        for package in packages:
            print(f"📡 安装 {package}，使用源: https://pypi.tuna.tsinghua.edu.cn/simple")
            res = run_cmd([
                str(VENV_PYTHON), "-m", "pip", "install", package,
                "-i", "https://pypi.tuna.tsinghua.edu.cn/simple",
                "--trusted-host", "pypi.tuna.tsinghua.edu.cn"
            ], check=False)
            if res.returncode != 0:
                print(f"❌ 无法安装 {package}，请检查网络！")
                sys.exit(1)

    # === 验证关键模块是否可导入 ===
    print("🔍 验证关键模块是否安装成功...")
    modules_to_check = ["tornado", "requests"]
    for module in modules_to_check:
        if module == "tornado":
            verify_cmd = [str(VENV_PYTHON), "-c", f"import {module}; print('{module} version:', {module}.version)"]
        else:
            verify_cmd = [str(VENV_PYTHON), "-c", f"import {module}; print('{module} version:', {module}.__version__)"]
        verify_res = run_cmd(verify_cmd, check=False)
        if verify_res.returncode != 0:
            print(f"❌ {module} 未正确安装！")
            sys.exit(1)
        else:
            print(f"✅ {module} 已成功安装并可导入")

    # 停止旧服务
    service_name = "sangao"
    run_cmd(["sudo", "systemctl", "stop", service_name], check=False)
    run_cmd(["sudo", "systemctl", "disable", service_name], check=False)

    # systemd 服务
    current_user = os.getenv("USER")
    systemd_unit = f"""
[Unit]
Description=Sangao Web Application
After=network.target

[Service]
Type=simple
User={current_user}
WorkingDirectory={proj_dir}
ExecStart={VENV_PYTHON} app.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
"""

    service_path = Path(f"/tmp/{service_name}.service")
    with open(service_path, "w") as f:
        f.write(systemd_unit.strip())

    run_cmd(["sudo", "cp", str(service_path), f"/etc/systemd/system/{service_name}.service"])
    run_cmd(["sudo", "systemctl", "daemon-reload"])
    run_cmd(["sudo", "systemctl", "enable", "--now", service_name])

    print(f"✅ sangao 服务已启动（监听 8080）")
    print(f"   日志: sudo journalctl -u {service_name} -f")