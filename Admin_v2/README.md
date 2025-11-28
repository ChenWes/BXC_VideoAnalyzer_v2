#Admin 视频行为分析系统v2 后台管理

#### 环境
| 程序         | 版本      |
| ---------- | ------- |
| python     | 3.7+    |
| 依赖库      | requirements.txt |

### 安装依赖库
~~~

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

~~~
//启动后台管理服务
python manage.py runserver 0.0.0.0:9001

//默认用户
用户名：admin 密码：admin888

~~~



#### Anconda环境接管


修改参数


* BXC_VideoAnalyzer_v2\Admin_v2\framework\settings.py：修改对应的视频分析器及ZLMediaKit的地址
* BXC_VideoAnalyzer_v2\Admin_v2\app\utils\ZLMediaKit.py：修改ZLMediaKit的密钥



2025-11-27修改脚本

```bash

# 建议使用Anaconda Prompt命令行运行项目
# 进入至项目目录

d:
cd D:\report\other\BXC_VideoAnalyzer_v2\Admin_v2

# 1、创建环境
conda create -n admin-py37 python=3.7

# 2、启动环境
conda activate admin-py37


# 3、升级pip及安装依赖
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


# 4、启动服务器
python manage.py runserver 0.0.0.0:9001


# 5、不再需要运行时删除环境
conda remove -n admin-py37


```