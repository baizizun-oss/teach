#!/usr/bin/env bash

set -e  # 遇错即停

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.deploy_venv"

echo "🗑️  开始卸载 deploy.py 部署的内容..."

# 1. 停止并卸载 NFS 客户端/服务（根据你的 install_nfs 实现调整）
echo "🔌 停止并卸载 NFS 相关组件..."
sudo systemctl stop nfs-client.target 2>/dev/null || true
sudo apt remove -y nfs-common nfs-kernel-server 2>/dev/null || true

# 2. 卸载 Docker（标准官方卸载方式）
echo "🐳 卸载 Docker..."
sudo systemctl stop docker 2>/dev/null || true
sudo apt remove -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin 2>/dev/null || true
sudo apt autoremove -y 2>/dev/null || true

# 3. 清理 Docker 残留（可选）
sudo rm -rf /var/lib/docker
sudo rm -rf /etc/docker

# 4. 移除 SSH 配置？（注意：不要卸载 openssh-server，否则可能断连！）
# deploy.py 中 install_ssh_with_prompt 很可能是配置而非安装
# 所以这里只清理自定义配置（假设你修改了 ~/.ssh/config 或 /etc/ssh/sshd_config）
# 如无特殊配置，可跳过
echo "🔑 跳过 SSH 卸载（避免断连）。如需重置 SSH，请手动操作。"

# 5. 删除部署的项目文件（假设 deploy_sangao 在 ~/sangao 或 /opt/sangao）
# 请根据你实际部署路径修改！
SANGAO_PATH="/opt/sangao"
if [ -d "$SANGAO_PATH" ]; then
    echo "📂 删除 Sangao 项目: $SANGAO_PATH"
    sudo rm -rf "$SANGAO_PATH"
fi

# 6. 删除虚拟环境
if [ -d "$VENV_DIR" ]; then
    echo "🧹 删除虚拟环境: $VENV_DIR"
    rm -rf "$VENV_DIR"
fi

# 7. 【可选】卸载 Python 3.8（⚠️ 谨慎！可能影响其他程序）
# 如果你确定是 deploy.py 安装的且无其他依赖，可取消注释：
# echo "🐍 卸载 Python 3.8（可选）..."
# sudo apt remove -y python3.8 python3.8-venv python3.8-dev
# sudo apt autoremove -y

echo ""
echo "✅ 卸载完成！"
echo "💡 提示：如需彻底清理 Python 3.8 或 SSH 配置，请手动确认后再操作。"