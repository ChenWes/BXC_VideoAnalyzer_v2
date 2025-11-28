# Linux 构建和运行指南

## 📋 问题解答

**问题：** 在项目根目录运行 `cmake .` 时提示找不到 CMakeLists.txt

**原因：** CMakeLists.txt 原本在 `Analyzer_v2` 子目录中，从根目录运行找不到

**解决方案：** 已创建根目录的 CMakeLists.txt，现在可以从根目录或子目录运行

---

## 🚀 快速开始

### 从项目子目录构建（推荐）



```bash
# 1. 进入项目根目录
cd ~/Analyzer_v2/Analyzer_v2

# 2. 创建构建目录
mkdir -p build && cd build

# 3. 配置CMake
cmake ..

# 4. 编译
make -j$(nproc)

# 5. 运行
./Analyzer_v2 -h
```

### 方式三：使用自动化脚本（最简单）

```bash
# 1. 进入项目根目录
cd ~/Analyzer_v2

# 2. 给脚本添加执行权限
chmod +x build_and_run_linux.sh

# 3. 运行脚本（会自动检查依赖、编译并提示运行）
./build_and_run_linux.sh
```

---



## 📦 依赖安装



### Ubuntu/Debian 系统

`验证过`

```bash
sudo apt update

sudo apt install -y \
    build-essential \
    cmake \
    git \
    pkg-config \
    libavcodec-dev \
    libavformat-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    libavdevice-dev \
    libcurl4-openssl-dev \
    libevent-dev \
    libjsoncpp-dev \
    libopencv-dev \
    libjpeg-turbo8-dev
```



### CentOS/RHEL 系统

```bash
sudo yum install -y \
    gcc-c++ \
    cmake \
    git \
    pkgconfig \
    ffmpeg-devel \
    libcurl-devel \
    libevent-devel \
    jsoncpp-devel \
    opencv-devel \
    turbojpeg-devel
```

---



## 🔧 编译选项

### Debug 模式（调试）

```bash
cd build
cmake .. -DCMAKE_BUILD_TYPE=Debug
make -j$(nproc)
```



### Release 模式（发布）

`验证过`

```bash
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j$(nproc)
```



### 指定编译线程数

```bash
make -j4  # 使用4个线程编译
make -j$(nproc)  # 使用所有可用CPU核心
```

---



## ▶️ 运行程序

### 基本运行

```bash
# 查看帮助信息
./Analyzer_v2 -h

# 使用默认配置运行
./Analyzer_v2

# 指定配置文件
./Analyzer_v2 -f config.json

# 指定API服务IP和端口
./Analyzer_v2 -f config.json -i 0.0.0.0 -p 9002
```



### 后台运行

```bash
# 使用 nohup 后台运行
nohup ./Analyzer_v2 -f config.json -i 0.0.0.0 -p 9002 > analyzer.log 2>&1 &

# 查看进程
ps aux | grep Analyzer_v2

# 查看日志
tail -f analyzer.log

# 停止进程
kill $(pgrep Analyzer_v2)
```



### 使用 systemd 服务（生产环境推荐）

创建服务文件 `/etc/systemd/system/analyzer_v2.service`：

```ini
[Unit]
Description=Analyzer_v2 Video Analyzer Service
After=network.target

[Service]
Type=simple
User=weschen
WorkingDirectory=/home/weschen/Analyzer_v2/build/bin
ExecStart=/home/weschen/Analyzer_v2/build/bin/Analyzer_v2 -f /home/weschen/Analyzer_v2/config.json -i 0.0.0.0 -p 9002
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```



然后：

```bash
# 重载systemd配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start analyzer_v2

# 查看状态
sudo systemctl status analyzer_v2

# 设置开机自启
sudo systemctl enable analyzer_v2

# 查看日志
sudo journalctl -u analyzer_v2 -f
```

---



## 🐛 常见问题

### 1. 找不到库文件

**错误信息：**
```
CMake Error: Could not find a package configuration file
```



**解决方案：**

```bash
# 检查库是否安装
pkg-config --exists libavformat && echo "已安装" || echo "未安装"

# 安装缺失的库（参考上面的依赖安装部分）
sudo apt install libavformat-dev
```



### 2. 运行时找不到动态库

**错误信息：**
```
error while loading shared libraries: libavcodec.so.58: cannot open shared object file
```

**解决方案：**

```bash
# 查找库文件位置
find /usr -name "libavcodec.so*" 2>/dev/null

# 临时设置库路径（当前会话）
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# 永久设置（添加到 ~/.bashrc）
echo 'export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```



### 3. OpenCV 版本不匹配

**错误信息：**
```
OpenCV version mismatch
```

**解决方案：**
```bash
# 检查OpenCV版本
pkg-config --modversion opencv4

# 如果版本不对，重新安装
sudo apt remove libopencv-dev
sudo apt install libopencv-dev
```



### 4. 端口被占用

**错误信息：**

```
bind error: Address already in use
```

**解决方案：**
```bash
# 查看端口占用
sudo netstat -tlnp | grep 9002

# 或使用 lsof
sudo lsof -i :9002

# 杀死占用进程
sudo kill -9 <PID>

# 或使用其他端口
./Analyzer_v2 -p 9003
```



### 5. 配置文件路径错误

**错误信息：**
```
failed to read config file
```

**解决方案：**
```bash
# 检查配置文件是否存在
ls -l config.json

# 使用绝对路径
./Analyzer_v2 -f /home/weschen/Analyzer_v2/config.json
```

---



## 📝 配置文件说明

配置文件 `config.json` 的路径问题：

```json
{
  "rootVideoDir": "/home/weschen/Analyzer_v2/data/alarm"  // 注意：Linux路径使用 / 而不是 \
}
```

**重要：** 如果是从Windows复制过来的配置文件，需要：
1. 修改路径分隔符：`\\` → `/`
2. 使用Linux风格的绝对路径

---



## ✅ 验证清单

编译和运行前请确认：

- [ ] 所有依赖库已安装
- [ ] CMakeLists.txt 存在于项目根目录或 Analyzer_v2 子目录
- [ ] 编译无错误无警告
- [ ] 可执行文件已生成
- [ ] 配置文件路径正确
- [ ] 配置文件中的路径已改为Linux格式
- [ ] 端口未被占用
- [ ] 有足够的磁盘空间（用于存储告警视频）

---



## 📚 相关文件

- `CMakeLists.txt` - 根目录的CMake配置（支持Windows和Linux）
- `Analyzer_v2/CMakeLists.txt` - 子目录的CMake配置（仅Linux）
- `build_and_run_linux.sh` - Linux自动化构建脚本
- `config.json` - 配置文件模板

---



## 💡 提示

1. **推荐使用根目录的 CMakeLists.txt**，它支持跨平台
2. **构建目录建议使用 `build`**，便于清理（`rm -rf build`）
3. **生产环境建议使用 systemd 服务管理**
4. **定期查看日志文件**，及时发现问题

