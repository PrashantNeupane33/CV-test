import cv2 as cv
from camera_handler import DepthAICameraHandler as dai

# Initialize the DepthAI camera handler
camera = dai()
print("Camera Initialized")

while True:
    # Fetch frames
    frames = camera.getFrame()

    # Check if frames are valid
    if frames is None:
        continue  # Skip this iteration if frames are not available

    Lframe, Rframe = frames

    # Display the frames
    cv.imshow("Left", Lframe)
    cv.imshow("Right", Rframe)

    # Break the loop if 'q' is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cv.destroyAllWindows()
