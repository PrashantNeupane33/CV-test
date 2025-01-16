import cv2 as cv
from ultralytics import YOLO


class Detector:
    def __init__(self, model_path, conf_threshold=0.75):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.tracker = None

    def detect_objects(self, frame):
        results = self.model.predict(frame)
        for r in results:
            if r.boxes is None:
                continue
            for box in r.boxes:
                if float(box.conf) < self.conf_threshold:
                    continue
                bx = box.cpu().xywh.numpy()
                if bx.shape[0] == 0:
                    continue
                bbox = bx[0]
                x, y, w, h = bbox
                bbox_tracker = (int(x - w / 2), int(y - h / 2), int(w), int(h))
                self.initialize_tracker(frame, bbox_tracker)
                return bbox_tracker
        return None

    def initialize_tracker(self, frame, bbox_tracker):
        self.tracker = cv.TrackerCSRT_create()
        self.tracker.init(frame, bbox_tracker)

    def update_tracker(self, frame):
        if self.tracker:
            success, bbox = self.tracker.update(frame)
            if success:
                return bbox, True
        return None, False
