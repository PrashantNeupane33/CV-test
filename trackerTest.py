import detector
import tracker
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
        detector = detector(model_path)
        detections = detector.preditct(frame)
        print(detections)
