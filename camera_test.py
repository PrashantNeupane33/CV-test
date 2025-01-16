import cv2 as cv
import numpy as np
from calc import HostSpatialsCalc
from camera_handler import DepthAICameraHandler

cam = DepthAICameraHandler()
hostSpatials = HostSpatialsCalc(cam.device)

x = 200
y = 300
step = 3
delta = 5
stereo = None

hostSpatials.setDeltaRoi(delta)

while True:
    frames = cam.getFrame()
    if frames is None:
        continue
    depthData, dispframe, RgbFrame = frames
    spatials, centroid = hostSpatials.calc_spatials(
        depthData, (int(x), int(y)))
    disp = (dispframe * (255 / cam.stereo.initialConfig.getMaxDisparity())
            ).astype(np.uint8)
    disp = cv.applyColorMap(disp, cv.COLORMAP_JET)
    # Show the frame
    cv.imshow("depth", disp)
    cv.imshow("RGB", RgbFrame)
    cv.waitKey(1)
