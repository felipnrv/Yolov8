#! pip install ultralytics --quiet
from ultralytics import YOLO

model = YOLO("yolov8n.yaml")

results= model.train(data="/content/drive/MyDrive/FotosFrutasYOLO/data.yaml",epochs=500)