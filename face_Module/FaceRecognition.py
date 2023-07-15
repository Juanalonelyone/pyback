import os

import cv2
import insightface
import numpy as np
from sklearn import preprocessing


class FaceRecognition:
    def __init__(self, gpu_id=0, face_db='face_db', threshold=1.24, det_thresh=0.50, det_size=(640, 640)):
        """
        人脸识别工具类
        :param gpu_id: 正数为GPU的ID，负数为使用CPU
        :param face_db: 人脸库文件夹
        :param threshold: 人脸识别阈值
        :param det_thresh: 检测阈值
        :param det_size: 检测模型图片大小
        """
        self.gpu_id = gpu_id
        self.face_db = face_db
        self.threshold = threshold
        self.det_thresh = det_thresh
        self.det_size = det_size

        # 加载人脸识别模型，当allowed_modules=['detection', 'recognition']时，只单纯检测和识别
        self.model = insightface.app.FaceAnalysis(root='./',
                                                  allowed_modules=None,
                                                  providers=['CUDAExecutionProvider'])
        self.model.prepare(ctx_id=self.gpu_id, det_thresh=self.det_thresh, det_size=self.det_size)
        # 人脸库的人脸特征

        self.faces_embedding = list()
        # 加载人脸库中的人脸
        self.load_faces(self.face_db)

    # 加载人脸库中的人脸
    def load_faces(self, face_db_path):
        if not os.path.exists(face_db_path):
            os.makedirs(face_db_path)
        for root, dirs, files in os.walk(face_db_path):
            for file in files:
                input_image = cv2.imdecode(np.fromfile(os.path.join(root, file), dtype=np.uint8), 1)
                user_name = file.split(".")[0]
                face = self.model.get(input_image)[0]
                embedding = np.array(face.embedding).reshape((1, -1))
                embedding = preprocessing.normalize(embedding)
                self.faces_embedding.append({
                    "user_name": user_name,
                    "feature": embedding
                })

    def recognition(self, image):
        faces = self.model.get(image)

        results = list()
        for face in faces:
            # 开始人脸识别
            embedding = np.array(face.embedding).reshape((1, -1))
            embedding = preprocessing.normalize(embedding)
            user_name = "unknown"
            for com_face in self.faces_embedding:
                r = self.feature_compare(embedding, com_face["feature"], self.threshold)
                if r:
                    user_name = com_face["user_name"]
            results.append(user_name)
        return results

    @staticmethod
    def feature_compare(feature1, feature2, threshold):
        diff = np.subtract(feature1, feature2)
        dist = np.sum(np.square(diff), 1)
        if dist < threshold:
            return True
        else:
            return False

    def register(self, image, user_name):
        faces = self.model.get(image)
        if len(faces) != 1:
            return '图片检测不到人脸'
        # 判断人脸是否存在
        embedding = np.array(faces[0].embedding).reshape((1, -1))
        embedding = preprocessing.normalize(embedding)
        is_exits = False
        for com_face in self.faces_embedding:
            r = self.feature_compare(embedding, com_face["feature"], self.threshold)
            if r:
                is_exits = True
        if is_exits:
            return '该用户已存在'
        # 符合注册条件保存图片，同时把特征添加到人脸特征库中
        cv2.imencode('.png', image)[1].tofile(os.path.join(self.face_db, '%s.png' % user_name))
        self.faces_embedding.append({
            "user_name": user_name,
            "feature": embedding
        })
        return "success"

    def detect(self, image):
        faces = self.model.get(image)
        results = list()
        for face in faces:
            result = dict()
            # 获取人脸属性
            result["bbox"] = np.array(face.bbox).astype(np.int32).tolist()
            result["kps"] = np.array(face.kps).astype(np.int32).tolist()
            result["landmark_3d_68"] = np.array(face.landmark_3d_68).astype(np.int32).tolist()
            result["landmark_2d_106"] = np.array(face.landmark_2d_106).astype(np.int32).tolist()
            result["pose"] = np.array(face.pose).astype(np.int32).tolist()
            result["age"] = face.age
            gender = '男'
            if face.gender == 0:
                gender = '女'
            result["gender"] = gender
            # 开始人脸识别
            embedding = np.array(face.embedding).reshape((1, -1))
            embedding = preprocessing.normalize(embedding)
            result["embedding"] = embedding
            user_name = "unknown"
            for com_face in self.faces_embedding:
                r = self.feature_compare(embedding, com_face["feature"], self.threshold)
                if r:
                    user_name = com_face["user_name"]

            result["user_name"] = user_name
            results.append(result)
        return results

    # def camera(self):
    #     cap = cv2.VideoCapture(0)
    #
    #     ret, frame = cap.read()
    #     while True:
    #         ret, frame = cap.read()
    #         resultCamera = self.detect(frame)
    #         # x, y, w, h = resultCamera["bbox"]
    #         # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #         for result in resultCamera:
    #             print('人脸框坐标：{}'.format(resultCamera["bbox"]))
    #         cv2.imshow('out', frame)
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #     cap.release()
    def camera(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            resultCamera = self.detect(frame)
            for result in resultCamera:
                bbox = result["bbox"]
                x, y, w, h = bbox
                user_name = result["user_name"]
                # 绘制边界框
                cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)

                # 在框上显示人名
                cv2.putText(frame, user_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            cv2.imshow('Camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def cameraWithCap(self, frame):
        resultCamera = self.detect(frame)
        for result in resultCamera:
            bbox = result["bbox"]
            x, y, w, h = bbox
            user_name = result["user_name"]
            # 绘制边界框
            cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)

            # 在框上显示人名
            cv2.putText(frame, user_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        return frame


if __name__ == '__main__':
    img = cv2.imdecode(np.fromfile('dingzhen.jpg', dtype=np.uint8), -1)
    face_recognition = FaceRecognition()
    # result = face_recognition.register(img, user_name='dingzhen')
    # print(result)

    # results = face_recognition.detect(img)
    # print(results)
    #
    # print("-------------")
    # for result in results:
    #     print(format(result["user_name"]))
    #     print(format(result["bbox"]))

    # face_recognition.camera()

    # resultt = face_recognition.detect(img)
    # for result in resultt:
    #     # print('人脸框坐标：{}'.format(result["bbox"]))
    #     # print('人脸五个关键点：{}'.format(result["kps"]))
    #     # print('人脸3D关键点：{}'.format(result["landmark_3d_68"]))
    #     # print('人脸2D关键点：{}'.format(result["landmark_2d_106"]))
    #     # print('人脸姿态：{}'.format(result["pose"]))
    #     # print('年龄：{}'.format(result["age"]))
    #     # print('性别：{}'.format(result["gender"]))
    #     print(result)

    # print(resultt)

    face_recognition.camera()