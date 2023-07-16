# 假设你使用Django的ORM来进行数据库操作
import sys
import time

import insightface
import torch
from PIL import Image
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
import cv2
import numpy as np
# import tensorflow as tf
import datetime

import face_recognition
from rest_framework.decorators import api_view

from ultralytics import YOLO
from ultralytics.yolo.utils.ops import non_max_suppression

from djangoProject import settings
# from fall_detection import FallDetection
# from falldetectioninterface import falldetection
from video_catch import models

sys.path.append("../face_Module")
from face_Module import FaceDepart

import threading
from queue import Queue

gpu_id = 0
face_db = './face_Module/face_db'
threshold = 1.24
det_thresh = 0.50
det_size = (640, 640)
# test thread control


# model1 = torch.hub.load('D:/work/mini/pyback/yolov5master', 'custom', 'D:/work/mini/pyback/best.pt',
#                         source='local')
#
# model3 = torch.hub.load('D:/work/mini/pyback/yolov5master', 'custom', 'D:/work/mini/pyback/best-firev5.pt',
#                         source='local')
#
# model2 = YOLO('D:/work/mini/pyback/best-violence.pt')

model_fall = torch.hub.load('./yolov5master', 'custom', './best.pt',
                            source='local')

model_fire = torch.hub.load('./yolov5master', 'custom', './best-firev5.pt',
                            source='local')

model_emotion = torch.hub.load('./yolov5master', 'custom', './best-emotion.pt',
                               source='local')

model2 = YOLO('./best-violence.pt')

# 从数据库查询已知人脸数据
# known_faces_data = models.OldpersonInfo.objects.all()
#
# for face_data in known_faces_data:
#     image_path = face_data.img_url
#     name = face_data.name
#     face_image = face_recognition.load_image_file(image_path)
#     face_encoding = face_recognition.face_encodings(face_image)[0]
#     known_faces_encodings.append(face_encoding)
#     known_faces_names.append(name)

model = insightface.app.FaceAnalysis(root='./',
                                     allowed_modules=None,
                                     providers=['CUDAExecutionProvider'])
model.prepare(ctx_id=gpu_id, det_thresh=det_thresh, det_size=det_size)
faces_embedding = list()
FaceDepart.load_faces(model, faces_embedding, face_db_path=face_db)


def video_generator(queueForGain, id):
    readCap = models.Cap.objects.get(id=id)
    if readCap.url == '0':
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(readCap.url)
    print("摄像头正在运行：id:", id)

    if cap.isOpened():
        print("ok")
    else:
        print("video_generator done")
    while not settings.GLOBULE_THREAD_STOP:
        queueForGain.put(cap.read()[1])
        queueForGain.get() if queueForGain.qsize() > 1 else time.sleep(0.01)


def stream_thread(queueForGain, queueForSend, id):
    # 读取算法权限
    cap = models.Cap.objects.get(id=id)
    has_face = cap.has_face
    has_emotion = cap.has_emotion
    has_fall = cap.has_fall
    has_fire = cap.has_fire
    has_violence = cap.has_violence

    fall_counter = 0
    violence_counter = 0
    fire_counter = 0
    unknown_counter = 0

    while not settings.GLOBULE_THREAD_STOP:
        frame = queueForGain.get()
        # 调用算法全加这里！！！！！！！！！！！！！！！！！！！！！！！！！！
        frame = cv2.resize(frame, (640, 480))
        if has_face == '1':
            frame, unknown = FaceDepart.cameraWithCap(model, faces_embedding, threshold, frame)
            if unknown:
                unknown_counter += 1
                if unknown_counter > 150:
                    add_img('./img/event-img/face/', frame, '识别到陌生人')
                    unknown_counter = 0

        if has_fall == '1':
            frame = model_fall(frame)
            predictions = frame.pandas().xyxy[0]
            frame.save(save_dir='runs/detect/fall' + id, exist_ok=True)
            # print(frame)
            # 遍历每个检测结果
            for index, row in predictions.iterrows():
                class_name = row['name']
                confidence = row['confidence']
                if class_name == 'fall detected' and confidence > 0.5:
                    fall_counter += 1
                    print(fall_counter)
                    if fall_counter >= 150:
                        # TODU 插入数据库
                        frame = cv2.imread('./runs/detect/fall' + id + '/image0.jpg', flags=1)
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        add_img('./img/event-img/fall/', frame, '摔倒了')
                        fall_counter = 0
            frame = cv2.imread('./runs/detect/fall' + id + '/image0.jpg', flags=1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if has_fire == '1':
            frame = model_fire(frame)
            # v5版本获取标签
            predictions = frame.pandas().xyxy[0]
            frame.save(save_dir='runs/detect/fire' + id, exist_ok=True)
            # 遍历每个检测结果
            for index, row in predictions.iterrows():
                class_name = row['name']
                confidence = row['confidence']
                if class_name == 'fire' and confidence > 0.3:
                    fire_counter += 1
                    print(fall_counter)
                    if fire_counter >= 150:
                        # TODU 插入数据库
                        frame = cv2.imread('./runs/detect/fire' + id + '/image0.jpg', flags=1)
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        add_img('./img/event-img/fire/', frame, '着火了')
                        fire_counter = 0

            frame = cv2.imread('./runs/detect/fire' + id + '/image0.jpg', flags=1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if has_violence == '1':
            frame = model2(frame)
            frame = frame[0].plot()

        if has_emotion == '1':
            frame = model_emotion(frame)
            predictions = frame.pandas().xyxy[0]
            frame.save(save_dir='runs/detect/emotion' + id, exist_ok=True)
            # print(frame)
            # 遍历每个检测结果
            for index, row in predictions.iterrows():
                class_name = row['name']
                confidence = row['confidence']
                if class_name == 'anger' and confidence > 0.5:
                    fall_counter += 1
                    print(fall_counter)
                    if fall_counter >= 150:
                        # TODU 插入数据库
                        frame = cv2.imread('./runs/detect/emotion' + id + '/image0.jpg', flags=1)
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        add_img('./img/event-img/emotion/', frame, '老人很生气')
                        fall_counter = 0
            frame = cv2.imread('./runs/detect/emotion' + id + '/image0.jpg', flags=1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        queueForSend.put(frame)


def video_stream(request, id):
    queueForGain = Queue()
    queueForSend = Queue()

    thread_generator = threading.Thread(target=video_generator, args=(queueForGain, id))
    thread_generator.daemon = True
    thread_generator.start()

    thread_stream = threading.Thread(target=stream_thread, args=(queueForGain, queueForSend, id))
    thread_stream.daemon = True
    thread_stream.start()

    def streamer():
        while not settings.GLOBULE_THREAD_STOP:
            frame = queueForSend.get()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        print("streamer停止")


    return StreamingHttpResponse(streamer(), content_type='multipart/x-mixed-replace; boundary=frame')


def video_catch(request, id):
    return StreamingHttpResponse(get_frame(id), content_type='multipart/x-mixed-replace; boundary=frame')


@api_view(['GET'])
def stop_video_stream(request):

    settings.GLOBULE_THREAD_STOP = True
    return JsonResponse({'message': '视频停止'})


@api_view(['GET'])
def enable_video_stream(request):
    global thread_stop
    settings.GLOBULE_THREAD_STOP = False
    return JsonResponse({'message': '视频停止'})


# no used
def get_frame(id):
    cap1 = models.Cap.objects.get(id=id)
    has_face = cap1.has_face
    has_emotion = cap1.has_emotion
    has_fall = cap1.has_fall
    has_fire = cap1.has_fire
    has_violence = cap1.has_violence
    # fall_detection = FallDetection(weights_path='D:\work\mini\pyback\yolov5s.pt')
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture('http://192.168.98.159/mjpeg/1')
    fall_counter = 0
    violence_counter = 0
    fire_counter = 0
    while True:
        # with tf.device('/GPU:0'):
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (640, 480))
        # 火灾检测
        # if fire_counter == '1':
        #     frame = model(frame)
        #     # v5版本获取标签
        #     predictions = frame.pandas().xyxy[0]
        #
        #     frame.save(exist_ok=True)
        #
        #     # 遍历每个检测结果
        #     for index, row in predictions.iterrows():
        #         class_name = row['name']
        #         confidence = row['confidence']
        #
        #         #
        #         if class_name == 'fire' and confidence > 0.3:
        #             fire_counter += 1
        #             print(fall_counter)
        #             if fire_counter >= 150:
        #                 # TODU 插入数据库
        #                 frame = cv2.imread('D:/work/mini/pyback/runs/detect/exp/image0.jpg', flags=1)
        #                 frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #                 add_img('C:/img/event-img/', frame, '着火了')
        #                 fire_counter = 0
        #
        #     frame = cv2.imread('D:/work/mini/pyback/runs/detect/exp/image0.jpg', flags=1)
        #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #
        # if fall_counter == '1':
        #     frame = model_fall(frame)
        #
        #     predictions = frame.pandas().xyxy[0]
        #
        #     frame.save(exist_ok=True)
        #
        #     # 遍历每个检测结果
        #     for index, row in predictions.iterrows():
        #         class_name = row['name']
        #         confidence = row['confidence']
        #
        #         #
        #         if class_name == 'fall detected' and confidence > 0.5:
        #             fall_counter += 1
        #             print(fall_counter)
        #             if fall_counter >= 150:
        #                 # TODU 插入数据库
        #                 frame = cv2.imread('D:/work/mini/pyback/runs/detect/exp/image0.jpg', flags=1)
        #                 frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #                 add_img('C:/img/event-img/', frame, '摔倒了')
        #                 fall_counter = 0
        #     frame = cv2.imread('D:/work/mini/pyback/runs/detect/exp/image0.jpg', flags=1)
        #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #
        # 暴力检测
        frame = model2(frame)
        # predictions = frame[0].boxes.xyxy
        # predictions = frame[0].boxes
        # predictions = predictions.cpu().numpy()
        # for i, box in enumerate(predictions):
        #     if box.conf[0] > 0.5:
        #         cls = int(box.cls[0])
        #         print(cls)

        frame = frame[0].plot()
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
    today_time = datetime.datetime.today()
    str_today_time = today_time.strftime("%Y/{month}/{day} %H:%M:%S".format(month=str(today_time.month).lstrip('0'),
                                                                            day=str(today_time.day).lstrip('0')))
    # 将本地时间转换为字符串
    today_time_string = today_time.strftime("%Y-{month}-{day}-%H-%M-%S".format(month=str(today_time.month).lstrip('0'),
                                                                               day=str(today_time.day).lstrip('0')))

    cv2.imwrite(path + today_time_string + '.jpg', frame)
    models.Event.objects.create(id=last_event, old_id=None, location='餐厅', time=str_today_time, desc=event_desc,
                                img_url=path + today_time_string + '.jpg')

    return True
