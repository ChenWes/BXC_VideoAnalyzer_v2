# Algorithm 视频行为分析系统v2 算法服务





## 开发



### 运行环境要求

| 程序         | 版本      |
| ---------- | ------- |
| python     | 3.7+    |
| 依赖库      | requirements.txt |



### 安装依赖库

~~~bash

# 创建虚拟环境
python -m venv venv

# 切换到虚拟环境
venv\Scripts\activate

# 更新虚拟环境的pip版本
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

# 在虚拟环境中安装依赖库
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

~~~



### 启动

~~~bash
python AlgorithmApiServer.py --port 9003
~~~



#### Anconda环境接管

2025-11-27修改脚本


```bash


# 建议使用Anaconda Prompt命令行运行项目
# 进入至项目目录

d:
cd D:\report\other\BXC_VideoAnalyzer_v2\Algorithm_v2







# 1、创建环境
conda create -n algorithm-py37 python=3.7

# 2、启动环境
conda activate algorithm-py37


# 3、升级pip及安装依赖
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple



# 4、启动服务器
python AlgorithmApiServer.py --port 9003


# 5、不再需要运行时删除环境
conda remove -n algorithm-py37

```





### 识别模型

目前使用的是Yolo转换成OpenVINO

1. **关系定位**：OpenVINO是Intel开发的模型优化部署工具套件，可将YOLO模型转换为中间表示(IR)格式，在Intel CPU/GPU/NPU等硬件上实现数倍的推理加速。

2. **转换流程**：

   ```bash
   # 第1步：训练PyTorch模型
   # 第2步：转换成ONNX格式
   # 第3步：转换成OpenVINO格式
   PyTorch模型 → ONNX格式 → OpenVINO IR格式 (.xml + .bin)
   ```



关于`yolov5n.bin`文件：这确实是YOLOv5n模型转换后的OpenVINO文件之一

**完整格式**：OpenVINO IR格式包含**两个配套文件**：

- `.xml`：网络结构定义文件（计算图、层参数等）
- `.bin`：二进制权重文件（存储模型参数）

**操作确认**：

```bash
# 典型转换命令会生成一对文件
mo --input_model yolov5n.onnx  # 生成 yolov5n.xml + yolov5n.bin
```

**使用提示**：部署时必须同时加载这两个文件，缺一不可。

