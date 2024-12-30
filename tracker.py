import cv2 as cv


class Tracker:
    def __init__(self, bbox):
        self.tracker = cv.TrackerCSRT_create()
        x, y, w, h = bbox
        self.bbox = (int(x-w/2), int(y-h/2), int(w), int(h))

    def trackerUpdate(self, frame):
        success, self.bbox = self.tracker.update(frame)
        if success:
            return self.bbox
        else:
            print("Tracker update failed")
