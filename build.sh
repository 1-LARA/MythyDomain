#!/bin/bash

# 设置权限
chmod 755 usr/bin/listness-lite

# 构建包
dpkg-deb --build listness-lite

# 重命名包
mv listness-lite.deb listness-lite_1.0.0_all.deb

echo "构建完成: listness-lite_1.0.0_all.deb"