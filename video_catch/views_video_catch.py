from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2

# 加载人脸识别模型
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def video_catch(request):
    cap = cv2.VideoCapture(0)

    def generate_frames():
        while True:
            ret, frame = cap.read()
            if ret:
                # 将帧转换为灰度图像
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # 进行人脸检测
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                # 绘制人脸框
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # 将帧转换为 JPEG 格式
                ret, jpeg = cv2.imencode('.jpeg', frame)
                if ret:
                    # 将 JPEG 数据作为流响应返回
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')