import logging
import os
from typing import Annotated, Optional

import vtk

import slicer
from slicer.i18n import tr as _
from slicer.i18n import translate
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
from slicer.parameterNodeWrapper import (
    parameterNodeWrapper,
    WithinRange,
)

from slicer import vtkMRMLScalarVolumeNode, vtkMRMLIGTLConnectorNode, vtkMRMLWatchdogNode


#
# IVTutor
#


class IVTutor(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = _("IV Tutor")  # TODO: make this more human readable by adding spaces
        # TODO: set categories (folders where the module shows up in the module selector)
        self.parent.categories = [translate("qSlicerAbstractCoreModule", "QBiT")]
        self.parent.dependencies = []  # TODO: add here list of module names that this module requires
        self.parent.contributors = ["Andrew Kim (Queen's University)"]  # TODO: replace with "Firstname Lastname (Organization)"
        # TODO: update with short description of the module and a link to online module documentation
        # _() function marks text as translatable to other languages
        self.parent.helpText = _("""
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#IVTutor">module documentation</a>.
""")
        # TODO: replace with organization, grant and thanks
        self.parent.acknowledgementText = _("""
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""")

        # Additional initialization step after application startup is complete
        slicer.app.connect("startupCompleted()", registerSampleData)


#
# Register sample data sets in Sample Data module
#


def registerSampleData():
    """Add data sets to Sample Data module."""
    # It is always recommended to provide sample data for users to make it easy to try the module,
    # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

    import SampleData

    iconsPath = os.path.join(os.path.dirname(__file__), "Resources/Icons")

    # To ensure that the source code repository remains small (can be downloaded and installed quickly)
    # it is recommended to store data sets that are larger than a few MB in a Github release.

    # IVTutor1
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category="IVTutor",
        sampleName="IVTutor1",
        # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
        # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
        thumbnailFileName=os.path.join(iconsPath, "IVTutor1.png"),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        fileNames="IVTutor1.nrrd",
        # Checksum to ensure file integrity. Can be computed by this command:
        #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
        checksums="SHA256:998cb522173839c78657f4bc0ea907cea09fd04e44601f17c82ea27927937b95",
        # This node name will be used when the data set is loaded
        nodeNames="IVTutor1",
    )

    # IVTutor2
    SampleData.SampleDataLogic.registerCustomSampleDataSource(
        # Category and sample name displayed in Sample Data module
        category="IVTutor",
        sampleName="IVTutor2",
        thumbnailFileName=os.path.join(iconsPath, "IVTutor2.png"),
        # Download URL and target file name
        uris="https://github.com/Slicer/SlicerTestingData/releases/download/SHA256/1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        fileNames="IVTutor2.nrrd",
        checksums="SHA256:1a64f3f422eb3d1c9b093d1a18da354b13bcf307907c66317e2463ee530b7a97",
        # This node name will be used when the data set is loaded
        nodeNames="IVTutor2",
    )


#
# IVTutorParameterNode
#


@parameterNodeWrapper
class IVTutorParameterNode:
    """
    The parameters needed by module.

    """
    
    cameraConnectorNode: vtkMRMLIGTLConnectorNode
    markerConnectorNode: vtkMRMLIGTLConnectorNode
    watchDogNode: vtkMRMLWatchdogNode


#
# IVTutorWidget
#


class IVTutorWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)  # needed for parameter node observation
        self.logic = None
        self._parameterNode = None
        self._parameterNodeGuiTag = None
        slicer.mymod = self
        self.currentStep = None
        self.appliedTransforms = False # flag to check if transforms have been applied

    def setup(self) -> None:
        """Called when the user opens the module the first time and the widget is initialized."""
        ScriptedLoadableModuleWidget.setup(self)

        # Load widget from .ui file (created by Qt Designer).
        # Additional widgets can be instantiated manually and added to self.layout.
        uiWidget = slicer.util.loadUI(self.resourcePath("UI/IVTutor.ui"))
        self.layout.addWidget(uiWidget)
        self.ui = slicer.util.childWidgetVariables(uiWidget)

        # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
        # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
        # "setMRMLScene(vtkMRMLScene*)" slot.
        uiWidget.setMRMLScene(slicer.mrmlScene)

        # Create logic class. Logic implements all computations that should be possible to run
        # in batch mode, without a graphical user interface.
        self.logic = IVTutorLogic()

        # Connections
        self.logic.setUp()

        # These connections ensure that we update parameter node when scene is closed
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
        self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

        # Buttons
        self.ui.connectDeviceButton.connect("toggled(bool)", self.onConnectDeviceButton)
        self.ui.applyTransformsButton.connect("clicked(bool)", self.onApplyTransformsButton)
        self.ui.nextStepButton.connect("clicked(bool)", self.onNextStepButton)
        self.ui.prevStepButton.connect("clicked(bool)", self.onPrevStepButton)

        # Text box Displays
        self.initStepsTextDisplay()

        # Step number initialization for instructions
        self.currentStep = 0

        # Make sure parameter node is initialized (needed for module reload)
        self.initializeParameterNode()

    def cleanup(self) -> None:
        """Called when the application closes and the module widget is destroyed."""
        self.removeObservers()

    def enter(self) -> None:
        """Called each time the user opens this module."""
        # Make sure parameter node exists and observed
        self.initializeParameterNode()

    def exit(self) -> None:
        """Called each time the user opens a different module."""
        # Do not react to parameter node changes (GUI will be updated when the user enters into the module)
        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
            self._parameterNodeGuiTag = None

    def onSceneStartClose(self, caller, event) -> None:
        """Called just before the scene is closed."""
        # Parameter node will be reset, do not use it anymore
        self.setParameterNode(None)

    def onSceneEndClose(self, caller, event) -> None:
        """Called just after the scene is closed."""
        # If this module is shown while the scene is closed then recreate a new parameter node immediately
        if self.parent.isEntered:
            self.initializeParameterNode()

    def initializeParameterNode(self) -> None:
        """Ensure parameter node exists and observed."""
        # Parameter node stores all user choices in parameter values, node selections, etc.
        # so that when the scene is saved and reloaded, these settings are restored.

        self.setParameterNode(self.logic.getParameterNode())

    def setParameterNode(self, inputParameterNode: Optional[IVTutorParameterNode]) -> None:
        """
        Set and observe parameter node.
        Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
        """

        if self._parameterNode:
            self._parameterNode.disconnectGui(self._parameterNodeGuiTag)
        self._parameterNode = inputParameterNode
        if self._parameterNode:
            # Note: in the .ui file, a Qt dynamic property called "SlicerParameterName" is set on each
            # ui element that needs connection.
            self._parameterNodeGuiTag = self._parameterNode.connectGui(self.ui)
                
    def onConnectDeviceButton(self, toggled: bool) -> None:
        if toggled:
            logging.error(f"IGT connection started")
            self.logic.startIGTConnection(toggled)
            self.ui.connectDeviceButton.text = "Disconnect Device"
        else:
            logging.error(f"IGT connection stopped")
            self.logic.startIGTConnection(toggled)
            self.ui.connectDeviceButton.text = "Connect Device" 

    def onApplyTransformsButton(self) -> None:
        if not self.appliedTransforms:
            logging.error(f"Transforms applied")
            self.appliedTransforms = True
            
            # call logic function to create and apply transforms in correct hierarchy
            self.logic.setUpTransformHierarchy()
        else:
            logging.error(f"Transforms already applied")
            return

    def onNextStepButton(self) -> None:
        """Go to the next step in the instruction."""
        
        if self.currentStep == 10:
            return
        else:
            self.currentStep += 1
            self.stepsTextDisplay(self.currentStep)

    def onPrevStepButton(self) -> None:
        """Go to the previous step in the instruction."""
        
        if self.currentStep == 0:
            return
        else:
            self.currentStep -= 1
            self.stepsTextDisplay(self.currentStep)

    def initStepsTextDisplay(self):
        self.ui.stepsTextDisplay.setText("Click 'Connect Device' to start the connection with the IGT device. Then click 'Start Live Prediction' to start the live prediction of the IGT device. Click 'Stop Live Prediction' to stop the live prediction of the IGT device. Click 'Disconnect Device' to stop the connection with the IGT device.")
            
    def stepsTextDisplay(self, step):
        if step == 0:
            self.initStepsTextDisplay()
        elif step == 1:
            self.ui.stepsTextDisplay.setText("Step 1: Sanitize hands and place the patient’s arm in a comfortable position.")
        elif step == 2:
            self.ui.stepsTextDisplay.setText("Step 2: Identify the vein, choosing a vein 0.3-1.5cm from the skin surface with a diameter greater than 0.4cm, preferred veins are straight, distal, and non-branched.")
        elif step == 3:
            self.ui.stepsTextDisplay.setText("Step 3: Position the tourniquet (place under the arm, cross over sides of the band, tuck the front side under and tighten) 20-25cm proximally to the site.")
        elif step == 4:
            self.ui.stepsTextDisplay.setText("Step 4: Recheck the vein for the radial pulse, loosening the tourniquet if unsuccessful.")
        elif step == 5:
            self.ui.stepsTextDisplay.setText("Step 5: Clean the patient’s arm with an antibacterial wipe in the direction of blood flow, and remove the sterile, unopened needle from the package.")
        elif step == 6:
            self.ui.stepsTextDisplay.setText("Step 6: Prepare and inspect the catheter; remove the needle cap careful not to touch the needle.")
        elif step == 7:
            self.ui.stepsTextDisplay.setText("Step 7: Pull the skin taut by placing a thumb and forefinger at either end of the vein; another way is to pinch the skin on the underside of the arm, careful not to compress the vein during the placement attempt.")
        elif step == 8:
            self.ui.stepsTextDisplay.setText("Step 8: Insert the needle with the bevel facing up, at a 15-30° angle, moving slowly and stopping if any resistance is felt.")
        elif step == 9:
            self.ui.stepsTextDisplay.setText("Step 9: Advance the needle until a flashback (initial backflow of blood) is seen, then stop. Remove the tourniquet and advance the catheter into the vein.")
        elif step == 10:
            self.ui.stepsTextDisplay.setText("Step 10: Remove the needle and make a U-shaped loop with IV tubing so 1 strip of tape covers both vertical parts of the U; then secure the IV tubing about 6 inches proximally on the patient's arm.") 


#
# IVTutorLogic
#


class IVTutorLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    # IGT Connection Constants
    CONNECTION_HOSTNAME = "localhost"
    CAMERA_PORT = 18945 #45 for optical marker tracker config
    MARKER_PORT = 18944 #44 for optical marker tracker config

    def __init__(self) -> None:
        """Called when the logic class is instantiated. Can be used for initializing member variables."""
        ScriptedLoadableModuleLogic.__init__(self)

    def setUp(self):
        parameterNode = self.getParameterNode()
        cameraConnectorNode = parameterNode.cameraConnectorNode
        if not cameraConnectorNode:
            cameraConnectorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLIGTLConnectorNode")
            cameraConnectorNode.SetTypeClient(self.CONNECTION_HOSTNAME, self.CAMERA_PORT)
            parameterNode.cameraConnectorNode = cameraConnectorNode
        markerConnectorNode = parameterNode.markerConnectorNode
        if not markerConnectorNode:
            markerConnectorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLIGTLConnectorNode")
            markerConnectorNode.SetTypeClient(self.CONNECTION_HOSTNAME, self.MARKER_PORT)
            parameterNode.markerConnectorNode = markerConnectorNode
        # referenceMarker = slicer.util.getNode
            
    def setUpTransformHierarchy(self):
        # need to first create needle model
        """
        Hierarchy:
        Marker5(needle)ToTracker (linear transform)
            -> NeedleTipToNeedle (linear transform)
                -> NeedleModel (model)
        """
        
        pass

    def getParameterNode(self):
        return IVTutorParameterNode(super().getParameterNode())

    def process(self,
                inputVolume: vtkMRMLScalarVolumeNode,
                outputVolume: vtkMRMLScalarVolumeNode,
                imageThreshold: float,
                invert: bool = False,
                showResult: bool = True) -> None:
        """
        Run the processing algorithm.
        Can be used without GUI widget.
        :param inputVolume: volume to be thresholded
        :param outputVolume: thresholding result
        :param imageThreshold: values above/below this threshold will be set to 0
        :param invert: if True then values above the threshold will be set to 0, otherwise values below are set to 0
        :param showResult: show output volume in slice viewers
        """

        if not inputVolume or not outputVolume:
            raise ValueError("Input or output volume is invalid")

        import time

        startTime = time.time()
        logging.info("Processing started")

        # Compute the thresholded output volume using the "Threshold Scalar Volume" CLI module
        cliParams = {
            "InputVolume": inputVolume.GetID(),
            "OutputVolume": outputVolume.GetID(),
            "ThresholdValue": imageThreshold,
            "ThresholdType": "Above" if invert else "Below",
        }
        cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True, update_display=showResult)
        # We don't need the CLI module node anymore, remove it to not clutter the scene with it
        slicer.mrmlScene.RemoveNode(cliNode)

        stopTime = time.time()
        logging.info(f"Processing completed in {stopTime-startTime:.2f} seconds")
    
    def startIGTConnection(self, toggled):
        # def setLivePrediction(self, toggled):
        logging.info(f"startConnection({toggled})")
        # find how to set connector to active
        parameterNode = self.getParameterNode()
        cameraConnectorNode = parameterNode.cameraConnectorNode
        markerConnectorNode = parameterNode.markerConnectorNode
        if toggled:
            cameraConnectorNode.Start()
            markerConnectorNode.Start()

        else:
            cameraConnectorNode.Stop()
            markerConnectorNode.Stop()

    # def startWatchDog(self, toggled):
    #     logging.info(f"startWatchDog({toggled})")
    #     parameterNode = self.getParameterNode()
    #     watchDogNode = parameterNode.watchDogNode()
    #     if toggled:
            

    

#
# IVTutorTest
#


class IVTutorTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """Do whatever is needed to reset the state - typically a scene clear will be enough."""
        slicer.mrmlScene.Clear()

    def runTest(self):
        """Run as few or as many tests as needed here."""
        self.setUp()
        self.test_IVTutor1()

    def test_IVTutor1(self):
        """Ideally you should have several levels of tests.  At the lowest level
        tests should exercise the functionality of the logic with different inputs
        (both valid and invalid).  At higher levels your tests should emulate the
        way the user would interact with your code and confirm that it still works
        the way you intended.
        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on,
        your test should break so they know that the feature is needed.
        """

        self.delayDisplay("Starting the test")

        # Get/create input data

        import SampleData

        registerSampleData()
        inputVolume = SampleData.downloadSample("IVTutor1")
        self.delayDisplay("Loaded test data set")

        inputScalarRange = inputVolume.GetImageData().GetScalarRange()
        self.assertEqual(inputScalarRange[0], 0)
        self.assertEqual(inputScalarRange[1], 695)

        outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
        threshold = 100

        # Test the module logic

        logic = IVTutorLogic()

        # Test algorithm with non-inverted threshold
        logic.process(inputVolume, outputVolume, threshold, True)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], threshold)

        # Test algorithm with inverted threshold
        logic.process(inputVolume, outputVolume, threshold, False)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], inputScalarRange[1])

        self.delayDisplay("Test passed")
