import cv2


def capture_camera():

        # 创建摄像头对象
    cap = cv2.VideoCapture(0)
    try:
        while True:
            # 读取摄像头画面
            ret, frame = cap.read()

            # 显示画面
            cv2.imshow('Camera1', frame)

            # 等待按键事件
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # 释放摄像头对象和关闭窗口
        cap.release()
        cv2.destroyAllWindows()

    except Exception as e:
        return f"Error: {str(e)}"


# 调用捕获摄像头函数
result = capture_camera()

# 检查是否有错误发生
if result.startswith("Error"):
    print(result)
