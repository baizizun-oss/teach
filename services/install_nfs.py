#!/usr/bin/env python3
# services/install_nfs.py

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common.utils import run_cmd

def check_nfs_mount(mount_point):
    """检查NFS是否已经挂载"""
    try:
        with open("/proc/mounts", "r") as f:
            mounts = f.read()
            return mount_point in mounts
    except Exception:
        return False

def install_nfs_utils():
    """安装NFS客户端工具"""
    print("📦 正在安装NFS客户端工具...")
    try:
        run_cmd(["sudo", "apt", "update"])
        run_cmd(["sudo", "apt", "install", "-y", "nfs-common"])
        print("✅ NFS客户端工具安装完成")
    except Exception as e:
        print(f"❌ NFS客户端工具安装失败: {e}")
        return False
    return True

def create_mount_point(mount_point):
    """创建挂载点目录"""
    try:
        # 先检查目录是否存在
        if os.path.exists(mount_point):
            print(f"✅ 挂载点目录 {mount_point} 已存在")
            return True
            
        # 尝试创建目录，如果权限不足则使用sudo
        try:
            os.makedirs(mount_point, exist_ok=True)
            print(f"✅ 挂载点目录 {mount_point} 创建成功")
            return True
        except PermissionError:
            print(f"⚠️  权限不足，正在使用sudo创建挂载点目录 {mount_point}...")
            run_cmd(["sudo", "mkdir", "-p", mount_point])
            # 更改目录所有者为当前用户
            user = os.getenv("USER")
            if user:
                run_cmd(["sudo", "chown", f"{user}:{user}", mount_point])
            print(f"✅ 挂载点目录 {mount_point} 创建成功")
            return True
    except Exception as e:
        print(f"❌ 创建挂载点目录失败: {e}")
        return False

def mount_nfs(server_ip, server_path, mount_point):
    """挂载NFS目录"""
    try:
        # 构建挂载命令，需要sudo权限
        cmd = ["sudo", "mount", "-t", "nfs", f"{server_ip}:{server_path}", mount_point]
        run_cmd(cmd)
        print(f"✅ 成功挂载 {server_ip}:{server_path} 到 {mount_point}")
        return True
    except Exception as e:
        print(f"❌ NFS挂载失败: {e}")
        return False

def install_nfs():
    """主函数：安装并挂载NFS目录"""
    # NFS服务器配置
    NFS_SERVER_IP = "192.168.100.184"
    NFS_SERVER_PATH = "/home/bgp1984/projects/server_184/sangao/Answer/upload"
    LOCAL_MOUNT_POINT = os.path.join(os.path.dirname(__file__),"..","sangao","sangao","templates","Answer","upload")

    print(f"🔧 开始配置NFS挂载: {NFS_SERVER_IP}:{NFS_SERVER_PATH} -> {LOCAL_MOUNT_POINT}")
    
    # 1. 安装NFS客户端工具
    if not install_nfs_utils():
        return False
    
    # 2. 创建挂载点
    if not create_mount_point(LOCAL_MOUNT_POINT):
        return False
    
    # 3. 检查是否已经挂载
    if check_nfs_mount(LOCAL_MOUNT_POINT):
        print(f"✅ {LOCAL_MOUNT_POINT} 已经挂载，无需重复挂载")
        return True
    
    # 4. 执行挂载
    if not mount_nfs(NFS_SERVER_IP, NFS_SERVER_PATH, LOCAL_MOUNT_POINT):
        return False
    
    # 5. 验证挂载
    if not check_nfs_mount(LOCAL_MOUNT_POINT):
        print("❌ 挂载验证失败")
        return False
        
    print("✅ NFS挂载配置完成")
    return True

if __name__ == "__main__":
    success = install_nfs()
    if not success:
        sys.exit(1)