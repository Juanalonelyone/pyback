# 假设你使用Django的ORM来进行数据库操作
from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
import numpy as np
import tensorflow as tf

import face_recognition

from face_recognition_utils import detect_faces, recognize_faces
# from fall_detection import FallDetection
from falldetectioninterface import falldetection
from video_catch import models
from tensorflow.python.client import device_lib

# gpus = tf.config.experimental.list_physical_devices('GPU')
# print(gpus)
# if gpus:
#     try:
#         tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
#         tf.config.experimental.set_memory_growth(gpus[0], True)
#         print('GPU run')
#     except RuntimeError as e:
#         print(e)

# 启用TensorFlow GPU加速
# physical_devices = tf.config.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(physical_devices[0], True)

# 加载人脸检测器模型
face_detector = cv2.dnn.readNetFromCaffe('deploy.prototxt',
                                         'D:\\work\\mini\\pyback\\video_catch\\res10_300x300_ssd_iter_140000_fp16.caffemodel')

# 加载人脸识别模型
known_faces_encodings = []
known_faces_names = []
i = 0


# 从数据库查询已知人脸数据
known_faces_data = models.OldpersonInfo.objects.all()

for face_data in known_faces_data:
    image_path = face_data.img_url
    name = face_data.name
    face_image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(face_image)[0]
    known_faces_encodings.append(face_encoding)
    known_faces_names.append(name)


def video_catch(request, id):
    return StreamingHttpResponse(get_frame(id), content_type='multipart/x-mixed-replace; boundary=frame')


def get_frame(id):
    global i
    # fall_detection = FallDetection(weights_path='D:\work\mini\pyback\yolov5s.pt')
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (640, 480))

        # 设置 TensorFlow 使用 GPU 加速

        # print(device_lib.list_local_devices())

        # is_fall = fall_detection.detect_fall(frame)
        #
        # if is_fall:
        #     frame = cv2.putText(frame, 'Fall Detected', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
        #                         cv2.LINE_AA)

        # 人脸检测
        detections = detect_faces(frame, face_detector)

        # 人脸识别
        frame = recognize_faces(frame, detections, known_faces_encodings, known_faces_names)
        frame = falldetection(True, frame)
        # 将帧转换为字节流
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    cap.release()
