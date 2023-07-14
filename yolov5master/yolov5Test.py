import cv2
import detect
import os

video_capture = cv2.VideoCapture(0)
detect_api = detect.DetectAPI(exist_ok=True)

while True:
    k = cv2.waitKey(1)
    ret, frame = video_capture.read()

    path = 'D:/work/mini/pyback/yolov5master/data/myimages/'
    cv2.imwrite(os.path.join(path, 'test.jpg'), frame)

    label = detect_api.run()
    print(str(label))

    image = cv2.imread('D:/work/mini/pyback/yolov5master/runs/detect/myexp/test.jpg', flags=1)
    cv2.imshow("video", image)

    if k == 27:  # 按下ESC退出窗口
        break

video_capture.release()

