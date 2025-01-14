import depthai as dai


class DepthAICameraHandler():
    def __init__(self):
        # Create pipeline
        pipeline = dai.Pipeline()

        # Define sources and outputs
        monoLeft = pipeline.create(dai.node.MonoCamera)
        monoRight = pipeline.create(dai.node.MonoCamera)
        # camRgb = pipeline.create(dai.node.ColorCamera)
        xoutLeft = pipeline.create(dai.node.XLinkOut)
        xoutRight = pipeline.create(dai.node.XLinkOut)

        xoutLeft.setStreamName('left')
        xoutRight.setStreamName('right')

        # Properties
        monoLeft.setCamera("left")
        monoLeft.setResolution(
            dai.MonoCameraProperties.SensorResolution.THE_720_P)
        monoRight.setCamera("right")
        monoRight.setResolution(
            dai.MonoCameraProperties.SensorResolution.THE_720_P)

        # Linking
        monoRight.out.link(xoutRight.input)
        monoLeft.out.link(xoutLeft.input)

        self.device = dai.Device(pipeline)

        # Defining data queue
        self.qLeft = self.device.getOutputQueue(
            name="left", maxSize=4, blocking=False)
        self.qRight = self.device.getOutputQueue(
            name="right", maxSize=4, blocking=False)

    def getFrame(self):
        inLeft = self.qLeft.tryGet()
        inRight = self.qRight.tryGet()
        if inLeft is None or inRight is None:
            return
        Lframe = inLeft.getCvFrame()
        Rframe = inRight.getCvFrame()

        return Lframe, Rframe
