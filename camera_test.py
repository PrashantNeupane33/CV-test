import cv2 as cv
import time
from camera_handler import DepthAICameraHandler

# Initialize camera handler
camera = DepthAICameraHandler()

# Initialize variables for frame rate calculation
prev_time_disp = time.time()
prev_time_rgb = time.time()
frame_count_disp = 0
frame_count_rgb = 0

while True:
    # Get frames
    frames = camera.getFrame()
    if frames is None:
        continue
    depthframe, dispframe, RGBframe = frames
    # Get current time for frame rate calculation
    current_time_disp = time.time()
    current_time_rgb = time.time()

    # Count frames for disparity frame
    if dispframe is not None:
        frame_count_disp += 1
        if current_time_disp - prev_time_disp >= 1.0:  # Every second, print FPS for disparity frame
            fps_disp = frame_count_disp / (current_time_disp - prev_time_disp)
            print(f"Disparity FPS: {fps_disp:.2f}")
            prev_time_disp = current_time_disp
            frame_count_disp = 0

    # Count frames for RGB frame
    if RGBframe is not None:
        frame_count_rgb += 1
        if current_time_rgb - prev_time_rgb >= 1.0:  # Every second, print FPS for RGB frame
            fps_rgb = frame_count_rgb / (current_time_rgb - prev_time_rgb)
            print(f"RGB FPS: {fps_rgb:.2f}")
            prev_time_rgb = current_time_rgb
            frame_count_rgb = 0

    # Display frames if available
    if dispframe is not None:
        cv.imshow("Disparity Frame", dispframe)
    if RGBframe is not None:
        cv.imshow("RGB Preview", RGBframe)

    # Exit on 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()

