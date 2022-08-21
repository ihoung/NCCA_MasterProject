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
# ShadingLocatorNode starts

class ShadingLocatorNode(OMUI.MPxLocatorNode):
    id = OM.MTypeId(0x00070001)
    drawDbClassification = "drawdb/geometry/shadinglocator"
    drawRegistrantId = "ShadingLocatorNodePlugin"

    # Attributes
    aEditWorldPos = None
    aOriginWorldPos = None
    aAnisotropy = None
    aSharpness = None
    aBend = None
    aBulge = None
    aRotation = None
    aNormalSmooth = None
    aIntensityGain = None
    aSoftness = None
    aEditType = None
    aEditLightSpace = None

    @staticmethod
    def creator():
        return ShadingLocatorNode()

    @staticmethod
    def initialize():
        nAttr = OM.MFnNumericAttribute()
        uAttr = OM.MFnUnitAttribute()
        mAttr = OM.MFnMatrixAttribute()
        eAttr = OM.MFnEnumAttribute()

        aEditWorldPosX = nAttr.create('editWorldPositionX', 'ewpx', OM.MFnNumericData.kFloat)
        aEditWorldPosY = nAttr.create('editWorldPositionY', 'ewpy', OM.MFnNumericData.kFloat)
        aEditWorldPosZ = nAttr.create('editWorldPositionZ', 'ewpz', OM.MFnNumericData.kFloat)
        ShadingLocatorNode.aEditWorldPos = nAttr.create('editWorldPosition', 'ewp', 
                                            aEditWorldPosX, aEditWorldPosY, aEditWorldPosZ)
        nAttr.keyable = False
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.hidden = True

        aOriginWorldPosX = nAttr.create('originWorldPositionX', 'owpx', OM.MFnNumericData.kFloat)
        aOriginWorldPosY = nAttr.create('originWorldPositionY', 'owpy', OM.MFnNumericData.kFloat)
        aOriginWorldPosZ = nAttr.create('originWorldPositionZ', 'owpz', OM.MFnNumericData.kFloat)
        ShadingLocatorNode.aOriginWorldPos = nAttr.create('originWorldPosition', 'owp', 
                                            aOriginWorldPosX, aOriginWorldPosY, aOriginWorldPosZ)
        nAttr.keyable = False
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.hidden = True

        ShadingLocatorNode.aAnisotropy = nAttr.create('anisotropy', 'a', OM.MFnNumericData.kFloat)
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        nAttr.default = 0.0

        ShadingLocatorNode.aSharpness = nAttr.create('sharpness', 's', OM.MFnNumericData.kFloat)
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        nAttr.default = 0.0

        ShadingLocatorNode.aBend = nAttr.create('bend', 'wy', OM.MFnNumericData.kFloat)
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.setMin(-0.5)
        nAttr.setMax(0.5)
        nAttr.default = 0.0

        ShadingLocatorNode.aBulge = nAttr.create('bulge', 'wx', OM.MFnNumericData.kFloat)
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.setMin(-0.1)
        nAttr.setMax(0.1)
        nAttr.default = 0.0

        ShadingLocatorNode.aRotation = uAttr.create('rotation', 'rot', OM.MFnUnitAttribute.kAngle)
        uAttr.keyable = True
        uAttr.storable = True
        uAttr.readable = True
        uAttr.writable = True
        uAttr.setMin(OM.MAngle(-180.0, OM.MAngle.kDegrees))
        uAttr.setMax(OM.MAngle(180.0, OM.MAngle.kDegrees))
        uAttr.default = OM.MAngle(0.0, OM.MAngle.kDegrees)

        ShadingLocatorNode.aNormalSmooth = nAttr.create('normalSmooth', 'ns', OM.MFnNumericData.kFloat)
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        nAttr.default = 0.0

        ShadingLocatorNode.aIntensityGain = nAttr.create('intensityGain', 'G', OM.MFnNumericData.kFloat)
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.setSoftMin(-10.0)
        nAttr.setSoftMax(10.0)
        nAttr.default = 0.0

        ShadingLocatorNode.aSoftness = nAttr.create('softness', 'd', OM.MFnNumericData.kFloat)
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.setMin(0.0)
        nAttr.setSoftMax(10.0)
        nAttr.default = 0.1

        ShadingLocatorNode.aEditType = eAttr.create('editType', 'et')
        eAttr.addField('Intensity', 0)
        eAttr.addField('Mask', 1)
        eAttr.keyable = False
        eAttr.storable = True
        eAttr.readable = True
        eAttr.writable = True

        ShadingLocatorNode.aEditLightSpace = mAttr.create('editLightSpace', 'els')
        mAttr.keyable = False
        mAttr.storable = True
        mAttr.readable = True
        mAttr.writable = False
        mAttr.hidden = True

        ShadingLocatorNode.addAttribute(ShadingLocatorNode.aEditLightSpace)
        ShadingLocatorNode.addAttribute(ShadingLocatorNode.aEditWorldPos)
        ShadingLocatorNode.addAttribute(ShadingLocatorNode.aOriginWorldPos)
        ShadingLocatorNode.addAttribute(ShadingLocatorNode.aAnisotropy)
        ShadingLocatorNode.addAttribute(ShadingLocatorNode.aSharpness)
        ShadingLocatorNode.addAttribute(ShadingLocatorNode.aBend)
        ShadingLocatorNode.addAttribute(ShadingLocatorNode.aBulge)
        ShadingLocatorNode.addAttribute(ShadingLocatorNode.aRotation)
        ShadingLocatorNode.addAttribute(ShadingLocatorNode.aNormalSmooth)
        ShadingLocatorNode.addAttribute(ShadingLocatorNode.aIntensityGain)
        ShadingLocatorNode.addAttribute(ShadingLocatorNode.aSoftness)
        ShadingLocatorNode.addAttribute(ShadingLocatorNode.aEditType)

        ShadingLocatorNode.attributeAffects(ShadingLocatorNode.aEditWorldPos, ShadingLocatorNode.aEditLightSpace)
        ShadingLocatorNode.attributeAffects(ShadingLocatorNode.aOriginWorldPos, ShadingLocatorNode.aEditLightSpace)
        # ShadingLocatorNode.attributeAffects(ShadingLocatorNode.aAnisotropy, ShadingLocatorNode.aOutputData)
        # ShadingLocatorNode.attributeAffects(ShadingLocatorNode.aSharpness, ShadingLocatorNode.aOutputData)
        # ShadingLocatorNode.attributeAffects(ShadingLocatorNode.aBend, ShadingLocatorNode.aOutputData)
        # ShadingLocatorNode.attributeAffects(ShadingLocatorNode.aBulge, ShadingLocatorNode.aOutputData)
        # ShadingLocatorNode.attributeAffects(ShadingLocatorNode.aRotation, ShadingLocatorNode.aOutputData)
        # ShadingLocatorNode.attributeAffects(ShadingLocatorNode.aNormalSmooth, ShadingLocatorNode.aOutputData)
        # ShadingLocatorNode.attributeAffects(ShadingLocatorNode.aIntensityGain, ShadingLocatorNode.aOutputData)
        # ShadingLocatorNode.attributeAffects(ShadingLocatorNode.aSoftness, ShadingLocatorNode.aOutputData)
    
    def __init__(self):
        OMUI.MPxLocatorNode.__init__(self)

    def compute(self, plug, data):
        OMUI.MPxLocatorNode.compute(self, plug, data)

        if plug != self.aEditLightSpace:
            return None

        originLocation = data.inputValue(self.aOriginWorldPos).asFloatVector()
        originLocation = OM.MFloatPoint(originLocation)
        editLocation = data.inputValue(self.aEditWorldPos).asFloatVector()
        editLocation = OM.MFloatPoint(editLocation)

        lightZ = (editLocation - originLocation).normalize()
        worldUp = OM.MFloatVector(0.0, 1.0, 0.0)
        lightX = (worldUp ^ lightZ).normalize()
        lightY = (lightZ ^ lightX).normalize()

        mData = [
            lightX.x, lightY.x, lightZ.x, 0.0,
            lightX.y, lightY.y, lightZ.y, 0.0,
            lightX.z, lightY.z, lightZ.z, 0.0,
            0.0, 0.0, 0.0, 0.0
        ]
        # print("mData: ", mData)
        lsMatrix = OM.MFloatMatrix(mData)

        lightSpaceHandle = data.outputValue(self.aEditLightSpace)
        lightSpaceHandle.setMFloatMatrix(lsMatrix)
        lightSpaceHandle.setClean()

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

        # print('linelist: {}'.format(drawdata.fLineList))
        drawManager.beginDrawable()
        drawManager.setColor(drawdata.fColor)
        drawManager.setDepthPriority(5)
        drawManager.mesh(OMR.MUIDrawManager.kLines, drawdata.fLineList)
        drawManager.endDrawable()

# ShadingLocatorNode ends
######################################################################################

######################################################################################
# ShadingPivotNode starts

class ShadingPivotNode(OM.MPxNode):
    id = OM.MTypeId(0x00070002)
    drawDbClassification = "drawdb/geometry/shadingpivot"
    drawRegistrantId = "ShadingPivotNodePlugin"

    @staticmethod
    def creator():
        return ShadingPivotNode()

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
# ShadingPivotNode ends
######################################################################################
