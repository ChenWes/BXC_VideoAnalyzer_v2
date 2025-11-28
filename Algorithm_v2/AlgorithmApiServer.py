import argparse
import sys
import numpy as np
import base64
import json
import cv2
# from turbojpeg import TurboJPEG

from lib.OpenVinoYoloV5Detector import OpenVinoYoloV5Detector

# turboJpeg = TurboJPEG()

from flask import Flask,request
app = Flask(__name__)
@app.route("/image/objectDetect",methods=['POST'])
def imageObjectDetect():
    data = {
        "code": 0,
        "msg": "unknown error",
    }
    try:
        params = request.get_json()
    except:
        params = request.form

    # 请求参数
    algorithm_str = params.get("algorithm")
    appKey = params.get("appKey")
    image_base64 = params.get("image_base64", None)  # 接收base64编码的图片并转换成cv2的图片格式


    if image_base64:
        if algorithm_str in ["openvino_yolov5", "yolo_v5"]:

            try:
                # 将Base64编码还原成图片
                print(f"[DEBUG] 收到Base64数据长度: {len(image_base64)}")
                
                # 处理 Data URI 格式 (例如: data:image/jpeg;base64,xxxxx)
                if image_base64.startswith('data:image'):
                    # 移除 Data URI 前缀，只保留实际的 Base64 数据
                    image_base64 = image_base64.split(',', 1)[1]                    
                    print(f"[DEBUG] 检测到Data URI格式，移除前缀后长度: {len(image_base64)}")
                
                # 修复可能在表单传输中被破坏的Base64字符
                # 空格可能是被转换的'+'号，需要还原
                image_base64 = image_base64.replace(' ', '+')
                
                encoded_image_byte = base64.b64decode(image_base64)
                print(f"[DEBUG] 解码后字节长度: {len(encoded_image_byte)}")
                
                # 
                image_array = np.frombuffer(encoded_image_byte, np.uint8)
                print(f"[DEBUG] numpy数组形状: {image_array.shape}, dtype: {image_array.dtype}")

                # turbojpeg 解码
                # image = turboJpeg.decode(image_array)  
                
                # opencv 解码
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                
                if image is None:
                    print("[ERROR] cv2.imdecode 返回 None，图像解码失败！")
                    data["code"] = 4001
                    data["msg"] = "图像解码失败，请检查Base64编码的图片是否为有效的JPG/PNG格式"
                    return json.dumps(data, ensure_ascii=False)
                
                print(f"[DEBUG] 解码成功！图像形状: {image.shape}")
                
            except Exception as e:
                print(f"[ERROR] Base64解码过程异常: {str(e)}")
                import traceback
                traceback.print_exc()
                data["code"] = 4002
                data["msg"] = f"Base64解码异常: {str(e)}"
                return json.dumps(data, ensure_ascii=False)

            if algorithm_str in ["openvino_yolov5", "yolo_v5"]:

                # 检测结果
                detect_num, detect_data = openVinoYoloV5Detector.detect(image)

                # 返回数据
                data["result"] = {
                    "detect_num": detect_num,
                    "detect_data": detect_data,
                }


            data["code"] = 1000
            data["msg"] = "success"
        else:
            data["msg"] = "algorithm=%s not supported"%algorithm_str
    else:
        data["msg"] = "image not uploaded"

    return json.dumps(data,ensure_ascii=False)


if __name__ == "__main__":

    parse = argparse.ArgumentParser()
    parse.add_argument("--debug", type=int, default=0, help="whether to turn on debugging mode default:0")
    parse.add_argument("--processes", type=int, default=1, help="number of open processes default:1")
    parse.add_argument("--port", type=int, default=9003, help="service port default:9003")
    parse.add_argument("--weights", type=str, default="weights", help="root directory of weight parameters")

    flags, unparsed = parse.parse_known_args(sys.argv[1:])

    debug = flags.debug
    processes = flags.processes
    port = flags.port
    weights_root_path = flags.weights
    debug = True if 1 == debug else False

    openVinoYoloV5Detector_IN_conf = {
        "weight_file": "weights/yolov5n_openvino_model/yolov5n.xml",
        "device": "CPU"
    }

    openVinoYoloV5Detector = OpenVinoYoloV5Detector(IN_conf=openVinoYoloV5Detector_IN_conf)


    app.run(host="0.0.0.0",port=port,debug=debug)



