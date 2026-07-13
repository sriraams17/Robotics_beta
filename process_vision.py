import cv2
import json
from datetime import datetime
from ultralytics import YOLO

def analyze_inspection_image(image_path, output_json_path="mock_robot_telemetry.json"):
    # 1. Load a pre-trained general-purpose AI model
    # This automatically downloads a lightweight (nano) model on first run
    model = YOLO("yolov8n.pt") 
    
    # 2. Run the image through the neural network
    results = model(image_path)
    
    detected_objects = []
    highest_risk = "Low"
    compliance_passed = True
    
    # 3. Process the AI detections
    for box in results[0].boxes:
        class_id = int(box.cls[0])
        label = model.names[class_id]
        confidence = float(box.conf[0])
        
        # Core QHSE Hazard Mapping Logic
        # (YOLO natively recognizes everyday items like 'fire hydrant', 'backpack', 'person', 'bottle')
        risk_level = "Low"
        action_required = "None"
        
        # Mocking an industrial scenario mapping:
        if label in ["fire hydrant", "extinguisher"]:
            label = "Fire Safety Equipment"
        elif label == "person":
            # For a real factory, we'd check if they have safety vests/helmets
            label = "Personnel in Workzone"
        elif label in ["bottle", "cup", "backpack"]:
            label = "Tripping Hazard / Foreign Object Debris"
            risk_level = "Medium"
            action_required = "Clear pathway immediately"
            highest_risk = "Medium"
            compliance_passed = False

        detected_objects.append({
            "element": label,
            "confidence_score": round(confidence * 100, 2),
            "risk_assessment": risk_level,
            "corrective_action": action_required
        })
    
    # 4. Construct the standardized telemetry JSON envelope
    telemetry_payload = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "robot_id": "QHSE-ROBOT-BETA-01",
            "inspection_type": "Optical Hazard Scanning",
            "overall_status": "PASS" if compliance_passed else "FAIL",
            "max_risk_level": highest_risk
        },
        "findings": detected_objects
    }
    
    # 5. Overwrite the telemetry file so the report engine can instantly read it
    with open(output_json_path, "w") as f:
        json.dump(telemetry_payload, f, indent=4)
        
    print(f"✅ Image processed! JSON telemetry packet written to {output_json_path}")
    return telemetry_payload

# Quick local test loop
if __name__ == "__main__":
    # Place any sample photo (e.g., a messy desk with cups/bottles) named 'test.jpg' in your folder to test it
    try:
        analyze_inspection_image("test.jpg")
    except Exception as e:
        print(f"Put a file named 'test.jpg' in your folder to test locally: {e}")