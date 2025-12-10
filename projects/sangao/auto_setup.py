import subprocess
import os

# 获取当前用户名
username = os.environ.get("USER") or os.getlogin()


pkgs=[
    # "qemu-kvm",

      ]
# pkgs = ["filezilla","openssh-server"]


commands= [["sudo","apt","install",pkg,"-y"] for pkg in pkgs ]


#构建容器
#docker build -t sangao:1.0 -f /home/bgp1984/projects/sangao/Dockerfile /home/bgp1984/projects/sangao/
commands = commands+ [["docker","build","-t","sangao:1.0","-f","/home/bgp1984/projects/sangao/Dockerfile","/home/bgp1984/projects/sangao/"],["docker","compose","up","-d"]]


for cmd in commands:
    subprocess.run(cmd)

# ✅ 成功完成，输出提示
print("已经构建容器，项目在容器中运行")