import cv2 as cv
import numpy as np
from cam_handler import OAKD, HostSpatialsCalc

camera = OAKD()
hostSpatials = HostSpatialsCalc(camera.device)
x = 200
y = 200
step = 3
delta = 5

hostSpatials.setDeltaRoi(delta)

while True:
    frames = camera.get_frame()
    if frames is None:
        continue
    RGBframe, dispframe, depthData = frames

    if depthData is not None:
        spatials, centroid = hostSpatials.calc_spatials(
            depthData, (int(x), int(y)))

    disp = (dispframe * (255 /
            camera.stereo.initialConfig.getMaxDisparity())).astype(np.uint8)
    disp = cv.applyColorMap(disp, cv.COLORMAP_JET)

    if dispframe is not None:
        cv.imshow("Disparity Frame", dispframe)
    if RGBframe is not None:
        cv.imshow("RGB Preview", RGBframe)
    if dispframe is None or RGBframe is None:
        print("None")

    if disp is not None:
        cv.imshow("D Frame", disp)

    if cv.waitKey(1) & 0xFF == ord("q"):
        break

cv.destroyAllWindows()
