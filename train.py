from ultralytics import YOLO

# Load a pretrained model
model = YOLO("yolov8n.pt")

# Train
model.train(
    data="C:\\Users\\lenovo\\Desktop\\IbexServices\\Robotics\\office-1\\data.yaml",
    epochs=100,
    imgsz=640,
    batch=16,
    workers=4,
    name="office_detector"
)