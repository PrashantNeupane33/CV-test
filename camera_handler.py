import depthai as dai
import time


class DepthAICameraHandler:
    def __init__(self):
        # Create pipeline
        pipeline = dai.Pipeline()

        # Define sources and outputs
        monoLeft = pipeline.create(dai.node.MonoCamera)
        monoRight = pipeline.create(dai.node.MonoCamera)
        stereo = pipeline.create(dai.node.StereoDepth)
        camRgb = pipeline.create(dai.node.ColorCamera)

        # Properties
        monoLeft.setResolution(
            dai.MonoCameraProperties.SensorResolution.THE_400_P)
        monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
        monoRight.setResolution(
            dai.MonoCameraProperties.SensorResolution.THE_400_P)
        monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
        monoLeft.setFps(60)
        monoRight.setFps(60)

        stereo.initialConfig.setConfidenceThreshold(255)
        stereo.setLeftRightCheck(True)
        stereo.setSubpixel(False)

        camRgb.setPreviewSize(600, 600)
        camRgb.setInterleaved(False)
        camRgb.setFps(60)

        # Linking
        monoLeft.out.link(stereo.left)
        monoRight.out.link(stereo.right)

        xoutDepth = pipeline.create(dai.node.XLinkOut)
        xoutDepth.setStreamName("depth")
        stereo.depth.link(xoutDepth.input)

        xoutDepth = pipeline.create(dai.node.XLinkOut)
        xoutDepth.setStreamName("disp")
        stereo.disparity.link(xoutDepth.input)

        xoutRgb = pipeline.create(dai.node.XLinkOut)
        xoutRgb.setStreamName("rgb")
        camRgb.preview.link(xoutRgb.input)

        self.device = dai.Device(pipeline, maxUsbSpeed=dai.UsbSpeed.SUPER_PLUS)

        # Start pipeline
        self.device.startPipeline()

        # Defining data queue
        # self.qLeft = self.device.getOutputQueue(
        #     name="left", maxSize=10, blocking=False)
        # self.qRight = self.device.getOutputQueue(
        #     name="right", maxSize=10, blocking=False)
        # self.qRgb = self.device.getOutputQueue(
        #     name="rgb", maxSize=10, blocking=False)
        self.depthQueue = self.device.getOutputQueue(name="depth")
        self.dispQ = self.device.getOutputQueue(name="disp")
        self.rgbQueue = self.device.getOutputQueue(
            name="rgb", maxSize=4, blocking=False)

    def getFrame(self):
        retry_count = 5
        while retry_count > 0:
            inDepth = self.depthQueue.tryGet()
            inDisp = self.dispQ.tryGet()
            inRgb = self.rgbQueue.tryGet()
            if inDepth and inDisp and inRgb:
                depthframe = inDepth.getCvFrame()
                dispframe = inDisp.getCvFrame()
                RgbFame = inRgb.getCvFrame()
                return depthframe, dispframe, RgbFame
            retry_count -= 1
            time.sleep(0.05)  # Wait 50ms before retrying
        return None  # Return None if no frames are retrieved after retries
