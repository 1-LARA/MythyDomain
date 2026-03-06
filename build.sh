#!/bin/bash

# 设置权限 - 使用正确的路径
chmod 755 listness-lite/usr/bin/listness-lite

# 构建包
dpkg-deb --build listness-lite

# 检查构建是否成功
if [ -f "listness-lite.deb" ]; then
    mv listness-lite.deb listness-lite_1.0.0_all.deb
    echo "构建成功: listness-lite_1.0.0_all.deb"
else
    echo "构建失败，请检查错误信息"
fi