import Detector
import cv2 as cv
import sys
sys.path.append('../depthPY')

conf_threshold = 0.75
detect = True
model_path = "/home/pnnp/Robocon2025CV/Resource/model/best.pt"
cap = cv.VideoCapture(0)
count = 0

while True:
    isTrue, frame = cap.read()
    if not isTrue:
        break
    if detect:
        detect = Detector.detector(model_path)
        detections = detect.predict(frame)
        print(detections)
        if detections is not None:
            cx, cy, w, h = detections
            cv.rectangle(frame, (int(cx-w/2), int(cy-h/2)),
                         (int(cx+w/2), int(cy+h/2)), (0, 255, 0), 2)
            detect = False
            tracker = cv.TrackerCSRT_create()
            bbox_tracker = (
                int(cx - w / 2), int(cy - h / 2), int(w), int(h))
            tracker.init(frame, bbox_tracker)
            break

    else:
        cv.imshow("Balls", frame)
        success, bbox = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in bbox]
            cv.rectangle(frame, (x, y),
                         (x + w, y + h), (0, 255, 0), 2)
            count += 1
            if count > 100:
                detect = True
                count = 0
