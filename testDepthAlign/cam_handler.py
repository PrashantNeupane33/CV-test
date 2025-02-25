import depthai as dai


class OAKD:
    def __init__(self, model=None, preview_size=(640, 480), fps=60, conf_threshold=0.75):
        self.timeout = 1/fps
        pipeline = dai.Pipeline()
        device = dai.Device()

        # Define sources and outputs
        monoLeft = pipeline.create(dai.node.MonoCamera)
        monoRight = pipeline.create(dai.node.MonoCamera)
        self.stereo = pipeline.create(dai.node.StereoDepth)
        camRgb = pipeline.create(dai.node.Camera)

        # Properties
        monoLeft.setResolution(
            dai.MonoCameraProperties.SensorResolution.THE_400_P)
        monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)
        monoRight.setResolution(
            dai.MonoCameraProperties.SensorResolution.THE_400_P)
        monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)
        monoLeft.setFps(fps)
        monoRight.setFps(fps)

        camRgb.setBoardSocket(dai.CameraBoardSocket.CAM_A)
        camRgb.setPreviewSize(preview_size)
        camRgb.setInterleaved(False)
        camRgb.setFps(fps)

        try:
            calibData = device.readCalibration2()
            lensPosition = calibData.getLensPosition(
                dai.CameraBoardSocket.CAM_A)
            if lensPosition:
                camRgb.initialControl.setManualFocus(lensPosition)
        except:
            raise

        self.stereo.setDefaultProfilePreset(
            dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
        self.stereo.initialConfig.setConfidenceThreshold(255)
        self.stereo.setLeftRightCheck(True)
        self.stereo.setSubpixel(False)
        self.stereo.setDepthAlign(dai.CameraBoardSocket.CAM_A)

        # Linking
        monoLeft.out.link(self.stereo.left)
        monoRight.out.link(self.stereo.right)

        xoutDepth = pipeline.create(dai.node.XLinkOut)
        xoutDepth.setStreamName("disp")
        self.stereo.disparity.link(xoutDepth.input)

        xoutRgb = pipeline.create(dai.node.XLinkOut)
        xoutRgb.setStreamName("rgb")
        camRgb.video.link(xoutRgb.input)

        camRgb.setMeshSource(dai.CameraProperties.WarpMeshSource.CALIBRATION)
        camRgb.setCalibrationAlpha(1)
        self.stereo.setAlphaScaling(1)

        # Start pipeline
        self.device.startPipeline(pipeline)

        self.dispQ = self.device.getOutputQueue(
            name="disp", maxSize=4, blocking=False)
        self.rgbQueue = self.device.getOutputQueue(
            name="rgb", maxSize=4, blocking=False
        )

    def get_frame(self):
        inRgb = self.rgbQueue.get()
        inDisp = self.dispQ.get()
        (rgbFrame, dispFrame) = (None, None)
        if inRgb:
            rgbFrame = inRgb.getCvFrame()
        if inDisp:
            dispFrame = inDisp.getCvFrame()
        return (rgbFrame, dispFrame)
