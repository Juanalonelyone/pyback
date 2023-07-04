from django.shortcuts import render

# Create your views here.

from django.http import StreamingHttpResponse
import cv2
import time


def video_catch(request):
    # 创建 VideoCapture 对象
    cap = cv2.VideoCapture(0)
    print(1111111)

    def generate_frames():
        print(2222)
        while True:
            # 读取摄像头帧
            ret, frame = cap.read()
            if ret:
                # 将帧转换为 JPEG 格式
                ret, frame = cv2.imencode('.jpeg', frame)
                if ret:
                    # 将 JPEG 数据作为流响应返回
                    print(3333)
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')
    # 返回 StreamingHttpResponse 响应
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
