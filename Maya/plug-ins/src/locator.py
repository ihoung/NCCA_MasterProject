import maya.api.OpenMaya as OM
import maya.api.OpenMayaUI as OMUI
import maya.api.OpenMayaRender as OMR

import utils


# Draw data of locator nodes
nodeLineList = [
    [-0.5, 0.0, 0.0],
    [0.5, 0.0, 0.0],
    [0.0, -0.5, 0.0],
    [0.0, 0.5, 0.0],
    [0.0, 0.0, -0.5],
    [0.0, 0.0, 0.5]
]

######################################################################################
# ShadingLocatorNode start

class ShadingLocatorNode(OMUI.MPxLocatorNode):
    id = OM.MTypeId(0x00070001)
    drawDbClassification = "drawdb/geometry/shadinglocator"
    drawRegistrantId = "ShadingLocatorNodePlugin"

    @staticmethod
    def creator():
        return ShadingLocatorNode()

    @staticmethod
    def initialize():
        pass
    
    def __init__(self):
        OMUI.MPxLocatorNode.__init__(self)

    def compute(self, plug, data):
        OMUI.MPxLocatorNode.compute(self, plug, data)

    def draw(self, view, path, style, status):
        global nodeLineList
        view.beginGL()
        ## drawing in VP1 views will be done using V1 Python APIs:
        import maya.OpenMayaRender as v1omr      
        glRenderer = v1omr.MHardwareRenderer.theRenderer()
        glFT = glRenderer.glFunctionTable()
        
        if status == OMUI.M3dView.kActive:
            view.setDrawColor( 13, OMUI.M3dView.kActiveColors )
        else:
            view.setDrawColor( 13, OMUI.M3dView.kDormantColors )
        glFT.glBegin(v1omr.MGL_LINES)
        glFT.glVertex3f(nodeLineList[0][0], nodeLineList[0][1], nodeLineList[0][2])
        glFT.glVertex3f(nodeLineList[1][0], nodeLineList[1][1], nodeLineList[1][2])
        glFT.glVertex3f(nodeLineList[2][0], nodeLineList[2][1], nodeLineList[2][2])
        glFT.glVertex3f(nodeLineList[3][0], nodeLineList[3][1], nodeLineList[3][2])
        glFT.glVertex3f(nodeLineList[4][0], nodeLineList[4][1], nodeLineList[4][2])
        glFT.glVertex3f(nodeLineList[5][0], nodeLineList[5][1], nodeLineList[5][2])
        glFT.glEnd()
    
        view.endGL()


## Viewport 2.0 override implementation
class ShadingLocatorNodeDrawData(OM.MUserData):
    def __init__(self):
        OM.MUserData.__init__(self, False)
        self.fColor = OM.MColor()
        self.fLineList = OM.MPointArray()


class ShadingLocatorNodeDrawOverride(OMR.MPxDrawOverride):
    @staticmethod
    def creator(obj):
        return ShadingLocatorNodeDrawOverride(obj)

    def __init__(self, obj):
        OMR.MPxDrawOverride.__init__(self, obj, None, False)

    def supportedDrawAPIs(self):
        return OMR.MRenderer.kOpenGL | OMR.MRenderer.kDirectX11 | OMR.MRenderer.kOpenGLCoreProfile

    def prepareForDraw(self, objPath, cameraPath, frameContext, oldData):
        data = oldData
        if not isinstance(data, ShadingLocatorNodeDrawData):
            data = ShadingLocatorNodeDrawData()

        global nodeLineList
        data.fLineList.clear()
        for lineData in nodeLineList:
            data.fLineList.append(OM.MPoint(lineData[0], lineData[1], lineData[2]))

        data.fColor = OMR.MGeometryUtilities.wireframeColor(objPath) 

        return data

    def hasUIDrawables(self):
        return True

    def addUIDrawables(self, objPath, drawManager, frameContext, data):
        drawdata = data
        if not isinstance(drawdata, ShadingLocatorNodeDrawData):
            return

        print('linelist: {}'.format(drawdata.fLineList))
        drawManager.beginDrawable()
        drawManager.setColor(drawdata.fColor)
        drawManager.setDepthPriority(5)
        drawManager.mesh(OMR.MUIDrawManager.kLines, drawdata.fLineList)
        drawManager.endDrawable()

# ShadingLocatorNode end
######################################################################################
