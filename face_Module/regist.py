import cv2
import numpy as np

import FaceDepart
import insightface
import os

gpu_id = 0
face_db = './face_db'
threshold = 1.24
det_thresh = 0.50
det_size = (640, 640)

model = insightface.app.FaceAnalysis(root='../',
                                     allowed_modules=None,
                                     providers=['CUDAExecutionProvider'])
model.prepare(ctx_id=gpu_id, det_thresh=det_thresh, det_size=det_size)
faces_embedding = list()
FaceDepart.load_faces(model, faces_embedding, face_db_path=face_db)


def regist():
    folder_path = "./face_init"
    db_path = "./face_db"
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            # 仅处理图像文件
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                # 使用 cv2 读取图像
                image = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
                msg = FaceDepart.register(model, faces_embedding, threshold, image, db_path, os.path.splitext(filename)[0])
                if msg=='success':
                    os.remove(file_path)




if __name__ == '__main__':
    regist()