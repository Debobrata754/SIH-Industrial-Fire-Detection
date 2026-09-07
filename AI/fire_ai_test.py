import cv2
from ultralytics import YOLO

print("🔥 Fire AI Test Started")

# Load AI model
model = YOLO("best_nano_111.pt")
print("✅ Model loaded successfully")

# Ask for image name
image_path = input("Enter image filename (example: fire.jpg): ")

# Load image
frame = cv2.imread(image_path)

if frame is None:
    print("❌ ERROR: Image could not be opened")
    exit()

print("✅ Image loaded")

# Run AI detection
results = model.predict(
    source=frame,
    conf=0.25,
    verbose=False
)

result = results[0]

fire_found = False

# Check detections
if result.boxes is not None and len(result.boxes) > 0:

    for box in result.boxes:

        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        if class_name.lower() == "fire":
            fire_found = True

            print(
                f"🔥 FIRE DETECTED | "
                f"Confidence: {confidence * 100:.2f}%"
            )

else:
    print("❌ No fire detected")

# Draw bounding boxes + labels
annotated_frame = result.plot()

# Save result
output_name = "fire_detection_result.jpg"
cv2.imwrite(output_name, annotated_frame)

print(f"✅ Result saved as {output_name}")

if fire_found:
    print("🔥 Fire detection test SUCCESSFUL!")
else:
    print("ℹ️ No fire found in this image.")
