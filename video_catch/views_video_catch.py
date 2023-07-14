# 假设你使用Django的ORM来进行数据库操作
import torch
from PIL import Image
from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
import numpy as np
import tensorflow as tf
import datetime

import face_recognition

from ultralytics import YOLO
from ultralytics.yolo.utils.ops import non_max_suppression

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
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

# # 加载人脸检测器模型
# face_detector = cv2.dnn.readNetFromCaffe('deploy.prototxt',
#                                          'D:\\work\\mini\\pyback\\video_catch\\res10_300x300_ssd_iter_140000_fp16.caffemodel')
#
# # 加载人脸识别模型
# known_faces_encodings = []
# known_faces_names = []
# i = 0
#
# # 从数据库查询已知人脸数据
# known_faces_data = models.OldpersonInfo.objects.all()
#
# for face_data in known_faces_data:
#     image_path = face_data.img_url
#     name = face_data.name
#     face_image = face_recognition.load_image_file(image_path)
#     face_encoding = face_recognition.face_encodings(face_image)[0]
#     known_faces_encodings.append(face_encoding)
#     known_faces_names.append(name)

model1 = torch.hub.load('./yolov5master', 'custom', './best-emotion.pt',
                        source='local')

model = torch.hub.load('./yolov5master', 'custom', './best-firev5.pt',
                       source='local')

model2 = YOLO('./best-violence.pt')


def video_catch(request, id):
    return StreamingHttpResponse(get_frame(id), content_type='multipart/x-mixed-replace; boundary=frame')


def get_frame(id):
    cap = models.Cap.objects.get(id=id)
    has_face = cap.has_face
    has_emotion = cap.has_emotion
    has_fall = cap.has_fall
    has_fire = cap.has_fire
    has_violence = cap.has_violence
    # fall_detection = FallDetection(weights_path='D:\work\mini\pyback\yolov5s.pt')
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture('http://192.168.98.159/mjpeg/1')
    fall_counter = 0
    violence_counter = 0
    fire_counter = 0
    while True:
        with tf.device('/GPU:0'):
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (640, 480))
            # 火灾检测
            if fire_counter == '1':
                frame = model(frame)
                # v5版本获取标签
                predictions = frame.pandas().xyxy[0]

                frame.save(exist_ok=True)

                # 遍历每个检测结果
                for index, row in predictions.iterrows():
                    class_name = row['name']
                    confidence = row['confidence']

                    #
                    if class_name == 'fire' and confidence > 0.3:
                        fire_counter += 1
                        print(fall_counter)
                        if fire_counter >= 150:
                            # TODU 插入数据库
                            frame = cv2.imread('D:/work/mini/pyback/runs/detect/exp/image0.jpg', flags=1)
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            add_img('C:/img/event-img/', frame, '着火了')
                            fire_counter = 0

                frame = cv2.imread('D:/work/mini/pyback/runs/detect/exp/image0.jpg', flags=1)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if fall_counter == '1':
                frame = model1(frame)

                predictions = frame.pandas().xyxy[0]

                frame.save(exist_ok=True)

                # 遍历每个检测结果
                for index, row in predictions.iterrows():
                    class_name = row['name']
                    confidence = row['confidence']

                    #
                    if class_name == 'fall detected' and confidence > 0.5:
                        fall_counter += 1
                        print(fall_counter)
                        if fall_counter >= 150:
                            # TODU 插入数据库
                            frame = cv2.imread('D:/work/mini/pyback/runs/detect/exp/image0.jpg', flags=1)
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            add_img('C:/img/event-img/', frame, '摔倒了')
                            fall_counter = 0
                frame = cv2.imread('D:/work/mini/pyback/runs/detect/exp/image0.jpg', flags=1)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            #
            # 暴力检测
            # frame = model2(frame)
            # predictions = frame[0].boxes.xyxy
            # predictions = frame[0].boxes
            # predictions = predictions.cpu().numpy()
            # for i, box in enumerate(predictions):
            #     if box.conf[0] > 0.5:
            #         cls = int(box.cls[0])
            #         print(cls)

            # frame = frame[0].plot()
            # predictions = predictions.shape
            # print(predictions)
            # for index, row in predictions:
            #     class_name = row['name']
            #     confidence = row['confidence']
            #
            #     #
            #     print(class_name)
            #     if class_name == 'violence' and confidence > 0.5:
            #         violence_counter += 1
            #         print(violence_counter)
            #         if violence_counter >= 150:
            #             # TODU 插入数据库
            #             add_img('C:/img/event-img/', frame, '摔倒了')
            #             violence_counter = 0
            # labels = frame.names[1]  # 类别标签
            # print(counter)
            # for label in zip(labels):
            #     print(label)
            #     if label == 'f':
            #         print("success")
            #         counter += 1



            # # 遍历检测结果
            # detection = frame.pred  # 获取单个预测结果
            #
            # label = detection['label']
            # confidence = detection['confidence']
            # bbox = detection['bbox']
            #
            # # 判断是否为你希望预测的事物，例如 'sitting'
            # if label == 'sitting' and confidence > 0.5:
            #     # 在这里可以执行你希望的操作，比如计数器加一
            #     counter += 1
            #
            # # 打印计数器的值
            # print("计数器值：", counter)

            # REadin('摔倒'，)
            # models.Event.objects.create()


            # 将帧转换为字节流
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    print(fall_counter)

    cap.release()


def add_img(path, frame, event_desc):
    last_event = models.Event.objects.last()
    if last_event is None:
        last_event = 0
    else:
        last_event = int(last_event.id + 1)
    current_time = datetime.datetime.now().time()
    today_time = datetime.datetime.today()
    today_time = today_time.strftime("%Y/{month}/{day} %H:%M:%S".format(month=str(today_time.month).lstrip('0'),
                                                                        day=str(today_time.day).lstrip('0')))
    # 将本地时间转换为字符串
    time_string = current_time.strftime("%H-%M-%S")
    cv2.imwrite(path + time_string + '.jpg', frame)
    models.Event.objects.create(id=last_event, old_id=None, location='餐厅', time=today_time, desc=event_desc,
                                img_url=path + time_string + '.jpg')

    return True
