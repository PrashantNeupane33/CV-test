from ultralytics import YOLO


class detector:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = YOLO(model_path)
        self.conf_threshold = 0.7

    def setThreshold(self, threshold):
        self.conf_threshold = threshold

    def predict(self, frame):
        results = self.model.predict(self.model_path)
        detections = []
        for r in results:
            if r.boxes is None:
                continue
            for box in r.boxes:
                if float(box.conf) < self.conf_threshold:
                    continue
                bx = box.cpu().xywh.numpy()
                if bx.shape[0] < 0:
                    continue
                bbox = bx[0]
                conf = float(box.conf)
                detections.append((bbox, conf))
        return detections
