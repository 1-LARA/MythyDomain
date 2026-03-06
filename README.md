# FirstPace

轻量级 GTK+ 3 计划清单应用。该项目使用 Python 3 和 PyGObject（`gi`）构建，目标是提供简单的任务管理功能。

## 目录结构

```
firstpace/          # 打包目录，包含应用安装结构
  DEBIAN/               # Debian 包控制文件
  usr/
    bin/firstpace   # 主执行脚本
    share/
      applications/     # 桌面文件
      icons/            # 应用图标
```

根目录还有一个 `build.sh` 用于生成 `.deb` 包。

## 依赖

- Python 3
- `python3-gi` 和 GTK+ 3（`gir1.2-gtk-3.0`）

## 开发与运行

1. 确保安装依赖：
   ```bash
   sudo apt install python3-gi gir1.2-gtk-3.0
   ```

2. 直接运行脚本（开发模式）：
   ```bash
   python3 firstpace/usr/bin/firstpace
   ```

3. 编译生成 Debian 包：
   ```bash
   ./build.sh
   ```
   生成的包在根目录下，如 `firstpace_1.0.0_all.deb`。

## 发布

使用 `dpkg -i` 安装生成的 `.deb` 包，或者将包上传到 APT 仓库。

## 未来展望

当前这是一个个人试验性项目，还没有指定许可证。我的目标是将它发展成一个既复杂又轻量的任务和时间管理工具，提供更多高级功能的同时保持简洁。此 README 会随着项目的发展逐步更新。


