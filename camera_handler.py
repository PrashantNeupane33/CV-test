import depthai as dai
import time


class DepthAICameraHandler:
    def __init__(self):
        # Create pipeline
        pipeline = dai.Pipeline()

        # Define sources and outputs
        monoLeft = pipeline.create(dai.node.MonoCamera)
        monoRight = pipeline.create(dai.node.MonoCamera)
        xoutLeft = pipeline.create(dai.node.XLinkOut)
        xoutRight = pipeline.create(dai.node.XLinkOut)

        xoutLeft.setStreamName('left')
        xoutRight.setStreamName('right')

        # Properties
        monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
        monoLeft.setResolution(
            dai.MonoCameraProperties.SensorResolution.THE_720_P)
        monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
        monoRight.setResolution(
            dai.MonoCameraProperties.SensorResolution.THE_720_P)

        # Linking
        monoRight.out.link(xoutRight.input)
        monoLeft.out.link(xoutLeft.input)

        self.device = dai.Device(pipeline)

        # Start pipeline
        self.device.startPipeline()

        # Defining data queue
        self.qLeft = self.device.getOutputQueue(
            name="left", maxSize=10, blocking=False)
        self.qRight = self.device.getOutputQueue(
            name="right", maxSize=10, blocking=False)

    def getFrame(self):
        retry_count = 5
        while retry_count > 0:
            inLeft = self.qLeft.tryGet()
            inRight = self.qRight.tryGet()
            if inLeft and inRight:
                Lframe = inLeft.getCvFrame()
                Rframe = inRight.getCvFrame()
                return Lframe, Rframe
            retry_count -= 1
            time.sleep(0.05)  # Wait 50ms before retrying
        return None  # Return None if no frames are retrieved after retries
