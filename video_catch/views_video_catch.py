from django.shortcuts import render

# Create your views here.

from django.http import StreamingHttpResponse
import cv2
import time



def video_catch(request):
    # 创建 VideoCapture 对象
    cap = cv2.VideoCapture(0)

    def generate_frames():
        while True:
            # 读取摄像头帧
            ret, frame = cap.read()

            # 将帧转换为 JPEG 格式
            ret, jpeg = cv2.imencode('.jpg', frame)

            # 将 JPEG 数据作为流响应返回
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')


    # 返回 StreamingHttpResponse 响应
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')




