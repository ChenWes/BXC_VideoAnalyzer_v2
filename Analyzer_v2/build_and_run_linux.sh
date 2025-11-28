#!/bin/bash
# Linux编译和运行脚本

set -e  # 遇到错误立即退出

echo "======================================"
echo "  Analyzer_v2 Linux编译和运行脚本"
echo "======================================"
echo

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否安装了必要的工具
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}[错误] 未找到 $1，请先安装${NC}"
        echo "安装方法: sudo apt install $2"
        exit 1
    fi
}

echo "[1] 检查依赖工具..."
check_command cmake cmake
check_command g++ build-essential
check_command pkg-config pkg-config

echo -e "${GREEN}✓ 基础工具检查通过${NC}"
echo

# 检查库依赖
echo "[2] 检查库依赖..."
LIBS_NEEDED=(libavformat libavcodec libavutil libswscale libcurl libevent jsoncpp opencv4)
MISSING_LIBS=()

for lib in "${LIBS_NEEDED[@]}"; do
    if ! pkg-config --exists $lib 2>/dev/null; then
        MISSING_LIBS+=($lib)
    fi
done

if [ ${#MISSING_LIBS[@]} -ne 0 ]; then
    echo -e "${YELLOW}[警告] 缺少以下库: ${MISSING_LIBS[*]}${NC}"
    echo
    echo "请运行以下命令安装："
    echo "  sudo apt update"
    echo "  sudo apt install -y \\"
    echo "    libavcodec-dev libavformat-dev libavutil-dev \\"
    echo "    libswscale-dev libswresample-dev libavdevice-dev \\"
    echo "    libcurl4-openssl-dev libevent-dev libjsoncpp-dev \\"
    echo "    libopencv-dev libjpeg-turbo8-dev"
    echo
    read -p "是否继续编译？(y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✓ 库依赖检查通过${NC}"
fi
echo

# 创建构建目录
echo "[3] 配置CMake..."
mkdir -p build
cd build

# 检查根目录是否有CMakeLists.txt
if [ -f "../CMakeLists.txt" ]; then
    echo "使用根目录的 CMakeLists.txt"
    cmake .. || {
        echo -e "${RED}[错误] CMake配置失败${NC}"
        exit 1
    }
else
    echo "使用子目录的 CMakeLists.txt"
    cmake ../Analyzer_v2 || {
        echo -e "${RED}[错误] CMake配置失败${NC}"
        exit 1
    }
fi

echo -e "${GREEN}✓ CMake配置成功${NC}"
echo

# 编译
echo "[4] 编译项目..."
make -j$(nproc) || {
    echo -e "${RED}[错误] 编译失败${NC}"
    exit 1
}

echo -e "${GREEN}✓ 编译成功${NC}"
echo

# 复制配置文件
if [ -f "../config.json" ]; then
    cp ../config.json ./
fi

echo "======================================"
echo -e "${GREEN}  编译完成！${NC}"
echo "======================================"
echo
echo "可执行文件: $(pwd)/Analyzer_v2"
echo
echo "运行方法："
echo "  ./Analyzer_v2 -h                    # 查看帮助"
echo "  ./Analyzer_v2 -f config.json -i 0.0.0.0 -p 9002"
echo
read -p "是否立即运行？(y/N) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo
    echo "======================================"
    echo "  启动 Analyzer_v2"
    echo "======================================"
    echo
    ./Analyzer_v2 -f config.json -i 0.0.0.0 -p 9002
fi

