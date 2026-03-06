#!/bin/bash

# 设置权限 - 使用正确的路径
chmod 755 firstpace/usr/bin/firstpace

# 构建包
dpkg-deb --build firstpace

# 检查构建是否成功
if [ -f "firstpace.deb" ]; then
    mv firstpace.deb firstpace_1.0.0_all.deb
    echo "构建成功: firstpace_1.0.0_all.deb"
else
    echo "构建失败，请检查错误信息"
fi