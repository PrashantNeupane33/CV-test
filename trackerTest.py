import cv2 as cv
from ultralytics import YOLO

conf_threshold = 0.75
detect = True

model = YOLO("/home/pnnp/Robocon2025CV/Resource/model/best.pt")
cap = cv.VideoCapture(0)
cout = 0
tracker = None

while True:
    isTrue, frame = cap.read()
    if not isTrue:
        print("Failed to grab frame")
        break

    if detect:
        results = model.predict(frame)
        for r in results:
            if r.boxes is None:
                continue
            for box in r.boxes:
                if float(box.conf) < conf_threshold:
                    continue
                bx = box.cpu().xywh.numpy()
                if bx.shape[0] == 0:
                    continue
                bbox = bx[0]
                x, y, w, h = bbox
                cv.rectangle(frame, (int(x - w / 2), int(y - h / 2)),
                             (int(x + w / 2), int(y + h / 2)), (0, 255, 0), 2)
                detect = False

                # Initialize tracker
                tracker = cv.TrackerCSRT_create()
                bbox_tracker = (int(x - w / 2), int(y - h / 2), int(w), int(h))
                tracker.init(frame, bbox_tracker)
                break

    else:
        if tracker:
            success, bbox = tracker.update(frame)
            if success:
                x, y, w, h = [int(v) for v in bbox]
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cout += 1
            else:
                cv.putText(frame, "Tracking failed", (10, 50),
                           cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            if cout > 100:
                detect = True
                cout = 0

    cv.imshow("Test", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
