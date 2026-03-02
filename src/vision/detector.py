from ultralytics import YOLO
class YoloDetector:
    def __init__(self, config):
        self.config = config
        print("Initializing YOLO model with config:", config)
        self.model = YOLO(config.model_path)

    def infer(self, frame):
        results = self.model(frame)
        detections = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                score = box.conf.item()
                class_id = int(box.cls.item())
                detections.append([x1, y1, x2, y2, score, class_id])
        return detections