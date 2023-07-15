import os
import cv2
import insightface
import numpy as np
from sklearn import preprocessing

# gpu_id = 0
# face_db = 'face_db'
# threshold = 1.24
# det_thresh = 0.50
# det_size = (640, 640)
#
# model = insightface.app.FaceAnalysis(root='./',
#                                      allowed_modules=None,
#                                      providers=['CUDAExecutionProvider'])
# model.prepare(ctx_id=gpu_id, det_thresh=det_thresh, det_size=det_size)
#
# faces_embedding = list()


def load_faces(model, faces_embedding, face_db_path):
    if not os.path.exists(face_db_path):
        os.makedirs(face_db_path)
    for root, dirs, files in os.walk(face_db_path):
        for file in files:
            input_image = cv2.imdecode(np.fromfile(os.path.join(root, file), dtype=np.uint8), 1)
            user_name = file.split(".")[0]
            face = model.get(input_image)[0]
            embedding = np.array(face.embedding).reshape((1, -1))
            embedding = preprocessing.normalize(embedding)
            faces_embedding.append({
                "user_name": user_name,
                "feature": embedding
            })


def feature_compare(feature1, feature2, threshold):
    diff = np.subtract(feature1, feature2)
    dist = np.sum(np.square(diff), 1)
    if dist < threshold:
        return True
    else:
        return False


def recognition(model, faces_embedding, image, threshold):
    faces = model.get(image)

    results = list()
    for face in faces:
        # 开始人脸识别
        embedding = np.array(face.embedding).reshape((1, -1))
        embedding = preprocessing.normalize(embedding)
        user_name = "unknown"
        for com_face in faces_embedding:
            r = feature_compare(embedding, com_face["feature"], threshold)
            if r:
                user_name = com_face["user_name"]
        results.append(user_name)
    return results


def register(model, faces_embedding, threshold, image, face_db, user_name):
    faces = model.get(image)
    if len(faces) != 1:
        return '图片检测不到人脸'
    # 判断人脸是否存在
    embedding = np.array(faces[0].embedding).reshape((1, -1))
    embedding = preprocessing.normalize(embedding)
    is_exits = False
    for com_face in faces_embedding:
        r = feature_compare(embedding, com_face["feature"], threshold)
        if r:
            is_exits = True
    if is_exits:
        return '该用户已存在'
    # 符合注册条件保存图片，同时把特征添加到人脸特征库中
    cv2.imencode('.png', image)[1].tofile(os.path.join(face_db, '%s.png' % user_name))
    faces_embedding.append({
        "user_name": user_name,
        "feature": embedding
    })
    return "success"


def detect(model, faces_embedding, threshold,image):
    faces = model.get(image)
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
        for com_face in faces_embedding:
            r = feature_compare(embedding, com_face["feature"], threshold)
            if r:
                user_name = com_face["user_name"]

        result["user_name"] = user_name
        results.append(result)
    return results


def camera():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        resultCamera = detect(frame)
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


def cameraWithCap(model, faces_embedding, threshold,frame):
    resultCamera = detect(model, faces_embedding, threshold,frame)
    for result in resultCamera:
        bbox = result["bbox"]
        x, y, w, h = bbox
        user_name = result["user_name"]
        # 绘制边界框
        cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 2)
        # 在框上显示人名
        cv2.putText(frame, user_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame,


