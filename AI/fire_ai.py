from ultralytics import YOLO
import sys
import cv2

# ==============================
# FIRE DETECTION AI MODEL
# ==============================

MODEL_PATH = "models/best_nano_111.pt"

# Load trained Fire Detection model
model = YOLO(MODEL_PATH)

print("🔥 Fire AI Model Loaded Successfully!")


def detect_fire(frame, confidence_threshold=0.25):

    results = model.predict(
        source=frame,
        conf=confidence_threshold,
        verbose=False
    )

    result = results[0]

    fire_detected = False
    highest_confidence = 0.0

    if result.boxes is not None:

        for box in result.boxes:

            confidence = float(box.conf[0])
            class_id = int(box.cls[0])

            class_name = model.names[class_id]

            if class_name.lower() == "fire":

                fire_detected = True

                if confidence > highest_confidence:
                    highest_confidence = confidence

    annotated_frame = result.plot()

    return annotated_frame, fire_detected, highest_confidence


# ==============================
# IMAGE TEST
# ==============================

if len(sys.argv) < 2:

    print("❌ Please provide an image name.")
    print("Example: python fire_ai.py test.jpg")
    sys.exit()

image_path = sys.argv[1]

print("📷 Detecting:", image_path)

image = cv2.imread(image_path)

if image is None:

    print("❌ Image not found:", image_path)
    sys.exit()

annotated_frame, fire_detected, confidence = detect_fire(image)


# ==============================
# RESULT
# ==============================

output_path = "fire_detection_result.jpg"

cv2.imwrite(output_path, annotated_frame)

if fire_detected:

    print("🔥 FIRE DETECTED!")
    print(f"Confidence: {confidence * 100:.2f}%")

else:

    print("✅ No Fire Detected.")


print("📁 Result saved as:", output_path)
