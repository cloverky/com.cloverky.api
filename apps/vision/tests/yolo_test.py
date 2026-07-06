from ultralytics import YOLO

model = YOLO("yolo11n.pt")

results = model("https://ultralytics.com/images/bus.jpg", show=True)

for r in results:
    print(f"감지된 객체 수: {len(r.boxes)}")
    for box in r.boxes:
        cls_id = int(box.cls[0])
        label = model.names[cls_id]
        conf = float(box.conf[0])
        print(f"  {label}: {conf:.2%}")
