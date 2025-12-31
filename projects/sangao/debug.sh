#!/bin/bash

# 停止并删除旧容器
docker stop sangao-app-1
docker rm sangao-app-1

# 构建新镜像
docker build -t sangao:1.0 \
  -f /home/bgp1984/projects/sangao/Dockerfile \
  /home/bgp1984/projects/sangao/

# 启动容器
docker compose up -d

# 等待容器启动（建议添加短暂延迟）
sleep 2

# 查看容器日志
docker logs sangao-app-1