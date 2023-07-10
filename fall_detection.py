# import torch
# import cv2
# from torchvision import transforms
# from yolov5 import YOLOv5
# from yolov5.models.common import DetectMultiBackend
# from yolov5.models.experimental import attempt_load
#
#
# class FallDetection:
#     def __init__(self, weights_path, confidence_threshold=0.5):
#         self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#         self.model = DetectMultiBackend(weights_path, device=self.device, data='D:\work\mini\pyback\coco128.yaml')
#         self.model.eval()
#         self.confidence_threshold = confidence_threshold
#         self.transform = transforms.Compose([
#             transforms.ToPILImage(),
#             transforms.Resize((640, 480)),
#             transforms.ToTensor(),
#         ])
#
#     def detect_fall(self, frame):
#         image = self.transform(frame).unsqueeze(0).to(self.device)
#         with torch.no_grad():
#             output = self.model(image)
#
#         # 解析YOLOv5输出
#         detections = self.parse_output(output)
#
#         # 检测是否发生摔倒
#         is_fallen = False
#         is_collection = False
#         for detection in detections:
#             bbox = detection["bbox"]
#             x, y, w, h = bbox
#             if detection["class"] == "person":
#                 # 绘制边界框
#                 color = (0, 0, 255)  # 红色
#                 frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
#                 if detection["confidence"] >= self.confidence_threshold:
#                     is_fallen = True
#                 if 0 < x < 100 or 0 < x + w < 100 or 0 < y < 100 or 0 < y + h < 100 :
#                     is_collection = True
#                     cv2.putText(frame, 'is collection', (300, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
#
#         return is_fallen, frame
#
#     def parse_output(self, output):
#         detections = []
#         for detection in output[0]:
#             class_id = int(detection[5])
#             confidence = float(detection[4])
#             class_name = self.model.classes[class_id]
#             bbox = detection[:4]
#
#             detections.append({
#                 "class": class_name,
#                 "confidence": confidence,
#                 "bbox": bbox,
#             })
#
#         return detections