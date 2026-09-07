from ultralytics import YOLO

model = YOLO("models/best_nano_111.pt")

print("Fire Detection System Started!")

image_path = "fire.jpg"

results = model.predict(
    source=image_path,
    conf=0.25,
    save=True
)

for result in results:
    if result.boxes is not None and len(result.boxes) > 0:
        for box in result.boxes:
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            print(
                f"{class_name} detected with "
                f"{confidence * 100:.2f}% confidence"
            )
    else:
        print("No fire detected.")

print("Detection completed.")
