import cv2
import numpy as np
import face_recognition
import tensorflow as tf
from oldperson_info import models

# 启用TensorFlow GPU加速
# physical_devices = tf.config.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(physical_devices[0], True)


def detect_faces(frame, face_detector):
    # 构建输入图像的 blob
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104.0, 177.0, 123.0))
    # 通过人脸检测器模型进行前向传递
    face_detector.setInput(blob)
    detections = face_detector.forward()

    return detections


def recognize_faces(frame, detections, known_faces_encodings, known_faces_names):
    # 获取图像的高度和宽度
    height, width = frame.shape[:2]

    if len(detections) == 0:
        # 如果没有检测到人脸，直接返回原始帧
        return frame
    # 创建一个TensorFlow图，以便在GPU上运行人脸编码
    #with tf.device('/GPU:0'):
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        # 过滤掉置信度低于阈值的检测结果
        if confidence > 0.5:
            # 计算人脸框的坐标
            # TODO:
            # models.OldpersonInfo.objects.create()
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            (startX, startY, endX, endY) = box.astype(int)

            # 提取人脸区域
            face = frame[startY:endY, startX:endX]

            # 将人脸图像转换为RGB格式
            face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

            # 对人脸图像进行编码
            face_encodings = face_recognition.face_encodings(face_rgb)

            if len(face_encodings) > 0:
                face_encoding = face_encodings[0]

                # 在已知人脸编码中进行匹配
                matches = face_recognition.compare_faces(known_faces_encodings, face_encoding, tolerance=0.4)

                if True in matches:
                    # 获取匹配的人脸的索引
                    match_indices = [index for index, match in enumerate(matches) if match]
                    names = [known_faces_names[index] for index in match_indices]

                    # 在人脸框上绘制姓名
                    label = ", ".join(names)
                    cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                else:
                    # 如果没有匹配的人脸，标记为Unknown
                    cv2.putText(frame, 'Unknown', (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            # 在人脸框周围绘制边框
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)

    return frame
