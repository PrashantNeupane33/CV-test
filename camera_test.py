import cv2 as cv
from camera_handler import DepthAICameraHandler

camera = DepthAICameraHandler()

while True:
    frames = camera.getFrame()
    if frames is None:
        print("No frames retrieved, retrying...")
        continue

    Lframe, Rframe = frames
    cv.imshow("Left Frame", Lframe)
    cv.imshow("Right Frame", Rframe)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
