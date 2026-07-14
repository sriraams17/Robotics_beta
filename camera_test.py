import cv2
from ultralytics import YOLO

# 1. Load the model ONCE, outside the loop
model = YOLO('yolov8n.pt') 

def start_camera_feed(camera_source):
    cap = cv2.VideoCapture(camera_source)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    print("Camera active. Press 'q' to exit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 2. Run inference inside the loop
        results = model(frame) 

        # 3. Process detections
        for r in results:
            for box in r.boxes:
                class_id = int(box.cls[0])
                label = model.names[class_id]
                confidence = float(box.conf[0])
                
                # Print to terminal to verify it's working
                print(f"Detected: {label} ({confidence:.2f})")

        cv2.imshow('Robot Camera Feed', frame)
        
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    smartphone_url = "http://192.168.0.72:8080/video"
    start_camera_feed(smartphone_url)