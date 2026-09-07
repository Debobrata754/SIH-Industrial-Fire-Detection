from ultralytics import YOLO

print("1. Starting...")

model = YOLO("best_nano_111.pt")

print("2. Model loaded")

results = model.predict("fire.jpg", conf=0.25)

print("3. Prediction finished")

results[0].save(filename="result.jpg")

print("4. Result saved")