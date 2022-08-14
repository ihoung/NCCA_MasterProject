from pyexpat import native_encoding
import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr

import utils
import fragments

class EditableToonShader(om.MPxNode):
    id = om.MTypeId(0x00070010)
    sDbClassification = "drawdb/shader/surface/editableToonShader"
    sRegistrantId = "EditableToonShaderPlugin"

    # Input attributes
    aBaseColor = None
    # aNormalMap = None
    aShadeThreshold = None
    aShadeIntensityRatio = None
    aDiffuseSmoothness = None
    aLightDirection = None
    # aLightIntensity = None
    # aLightShadowFraction = None
    # aPreShadowIntensity = None
    # aLightData = None
    aNormalCamera = None
    # aShadowDepthBias = None
    # aLinearSpaceLighting = None
    aSharpness = None

    # Output attributes
    aOutColor = None

    @staticmethod
    def creator():
        return EditableToonShader()

    @staticmethod
    def initialize():
        nAttr = om.MFnNumericAttribute()
        lAttr = om.MFnLightDataAttribute()

        # Create input attributes
        EditableToonShader.aBaseColor = nAttr.createColor("baseColor", "bc")
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.default = (1.0, 1.0, 1.0)

        # EditableToonShader.aNormalMap = nAttr.createColor("normalMap", "nm")
        # nAttr.keyable = True
        # nAttr.storable = True
        # nAttr.readable = True
        # nAttr.writable = True
        # nAttr.default = (0.0, 0.0, 1.0)

        EditableToonShader.aShadeThreshold= nAttr.create("shadeThreshold", "st", om.MFnNumericData.kFloat)
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        nAttr.default = 0.5

        EditableToonShader.aShadeIntensityRatio = nAttr.create("shadeIntensityRatio", "sir", om.MFnNumericData.kFloat)
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        nAttr.default = 0.2

        EditableToonShader.aDiffuseSmoothness = nAttr.create("diffuseSmoothness", "ds", om.MFnNumericData.kFloat)
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        nAttr.default = 0.4

        EditableToonShader.aLightDirection = nAttr.createPoint( "lightDirection", "ld" )
        nAttr.storable = False
        nAttr.hidden = True
        nAttr.readable = True
        nAttr.writable = False

        # EditableToonShader.aLightIntensity = nAttr.createColor( "lightIntensity", "li" )
        # nAttr.storable = False
        # nAttr.hidden = True
        # nAttr.readable = True
        # nAttr.writable = False

        # EditableToonShader.aLightShadowFraction = nAttr.create( "lightShadowFraction", "lsf", om.MFnNumericData.kFloat)
        # nAttr.storable = False
        # nAttr.hidden = True

        # EditableToonShader.aPreShadowIntensity = nAttr.create( "preShadowIntensity", "psi", om.MFnNumericData.kFloat)
        # nAttr.storable = False
        # nAttr.hidden = True

        # EditableToonShader.aLightData = lAttr.create("lightDataArray", "ltd",
		# EditableToonShader.aLightDirection,
		# EditableToonShader.aLightIntensity)
        # lAttr.array = True
        # lAttr.storable = False
        # lAttr.hidden = True
        # lAttr.default = (1.0, 1.0, 1.0, 1.0, 1.0, 1.0)

        EditableToonShader.aNormalCamera = nAttr.createPoint("normalCamera", "n")
        nAttr.storable = False

        # EditableToonShader.aShadowDepthBias = nAttr.create("shadowDepthBias", "sd", om.MFnNumericData.kFloat)
        # nAttr.keyable = True
        # nAttr.storable = True
        # nAttr.readable = True
        # nAttr.writable = True
        # nAttr.setMin(0.0)
        # nAttr.setMax(1.0)
        # nAttr.default = 0.2

        # EditableToonShader.aLinearSpaceLighting = nAttr.create("linearSpaceLighting", "lsl", om.MFnNumericData.kBoolean)
        # nAttr.keyable = True
        # nAttr.storable = True
        # nAttr.readable = True
        # nAttr.writable = True
        # nAttr.default = True

        EditableToonShader.aSharpness = nAttr.create("sharpness", "s", om.MFnNumericData.kFloat)
        nAttr.array = True
        nAttr.keyable = False
        nAttr.storable = True
        nAttr.readable = False
        nAttr.writable = True
        nAttr.usesArrayDataBuilder = True

        # Create output attributes
        EditableToonShader.aOutColor = nAttr.createColor("outColor", "oc")
        nAttr.keyable = False
        nAttr.storable = False
        nAttr.readable = True
        nAttr.writable = False

        om.MPxNode.addAttribute(EditableToonShader.aBaseColor)
        # om.MPxNode.addAttribute(EditableToonShader.aNormalMap)
        om.MPxNode.addAttribute(EditableToonShader.aShadeThreshold)
        om.MPxNode.addAttribute(EditableToonShader.aShadeIntensityRatio)
        om.MPxNode.addAttribute(EditableToonShader.aDiffuseSmoothness)
        om.MPxNode.addAttribute(EditableToonShader.aLightDirection)
        # om.MPxNode.addAttribute(EditableToonShader.aLightIntensity)
        # om.MPxNode.addAttribute(EditableToonShader.aLightShadowFraction)
        # om.MPxNode.addAttribute(EditableToonShader.aPreShadowIntensity)
        # om.MPxNode.addAttribute(EditableToonShader.aLightData)
        om.MPxNode.addAttribute(EditableToonShader.aNormalCamera)
        # om.MPxNode.addAttribute(EditableToonShader.aShadowDepthBias)
        # om.MPxNode.addAttribute(EditableToonShader.aLinearSpaceLighting)
        om.MPxNode.addAttribute(EditableToonShader.aSharpness)
        om.MPxNode.addAttribute(EditableToonShader.aOutColor)

        om.MPxNode.attributeAffects(EditableToonShader.aBaseColor, EditableToonShader.aOutColor)
        # om.MPxNode.attributeAffects(EditableToonShader.aNormalMap, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aShadeThreshold, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aShadeIntensityRatio, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aDiffuseSmoothness, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aLightDirection, EditableToonShader.aOutColor)
        # om.MPxNode.attributeAffects(EditableToonShader.aLightIntensity, EditableToonShader.aOutColor)
        # om.MPxNode.attributeAffects(EditableToonShader.aLightShadowFraction, EditableToonShader.aOutColor)
        # om.MPxNode.attributeAffects(EditableToonShader.aPreShadowIntensity, EditableToonShader.aOutColor)
        # om.MPxNode.attributeAffects(EditableToonShader.aLightData, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aNormalCamera, EditableToonShader.aOutColor)
        # om.MPxNode.attributeAffects(EditableToonShader.aShadowDepthBias, EditableToonShader.aOutColor)
        # om.MPxNode.attributeAffects(EditableToonShader.aLinearSpaceLighting, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aSharpness, EditableToonShader.aOutColor)

    def __init__(self):
        om.MPxNode.__init__(self)

    def compute(self, plug, block):
        if (plug != EditableToonShader.aOutColor) and (plug.parent() != EditableToonShader.aOutColor):
            return None

        baseColor = block.inputValue(EditableToonShader.aBaseColor).asFloatVector()

        resultColor = baseColor

        outColorHandle = block.outputValue(EditableToonShader.aOutColor)
        outColorHandle.setMFloatVector(resultColor)
        outColorHandle.setClean()

    # def postConstructor(self):
    #     self.setMPSafe(True)


class EditableToonShaderOverride(omr.MPxSurfaceShadingNodeOverride):
    @staticmethod
    def creator(obj):
        return EditableToonShaderOverride(obj)

    def __init__(self, obj):
        omr.MPxSurfaceShadingNodeOverride.__init__(self, obj)

        self.fObject = obj
        self.fSharpness = []
        self.fResolvedSharpnessName = ''

        # Register fragments with the manager
        shaderMgr = omr.MRenderer.getShaderManager()
        fragmentMgr = omr.MRenderer.getFragmentManager()
        if shaderMgr and fragmentMgr:
            # shaderMgr.addShaderPath(utils.getShaderDirPath())
            fragmentMgr.addFragmentPath(utils.getFragmentDirPath())
            if not fragmentMgr.hasFragment("ETS_ShadingMapFragment"):
                fragmentMgr.addShadeFragmentFromFile("ETS_ShadingMapFragment.xml", False)
            if not fragmentMgr.hasFragment("ETS_ToonFragment"):
                fragmentMgr.addShadeFragmentFromFile("ETS_ToonFragment.xml", False)
            if not fragmentMgr.hasFragment("ETS_ShaderSurface"):
                fragmentMgr.addFragmentGraphFromFile("ETS_ShaderSurface.xml")
    
    def __del__(self):
        fragmentMgr = omr.MRenderer.getFragmentManager()
        if fragmentMgr:
            fragmentMgr.removeFragment("ETS_ShaderSurface")
            fragmentMgr.removeFragment("ETS_ShadingMapFragment")
            fragmentMgr.removeFragment("ETS_ToonFragment")

    def primaryColorParameter(self):
        return "baseColor"

    def bumpAttribute(self):
        return "normalCamera"

    def supportedDrawAPIs(self):
        return omr.MRenderer.kOpenGL | omr.MRenderer.kOpenGLCoreProfile | omr.MRenderer.kDirectX11

    def fragmentName(self):
        return "ETS_ShaderSurface"

    # def getCustomMappings(self, mappings):
    #     sharpnessMapping = omr.MAttributeParameterMapping('sharpness', '', True, True)
    #     mappings.append(sharpnessMapping)

    def updateDG(self):
        node = om.MFnDependencyNode(self.fObject)
        sharpnessPlug = node.findPlug('sharpness', True)
        # del self.fSharpness[:]
        # for i in range(sharpnessPlug.numElements()):
        #     sharpnessElem = sharpnessPlug.elementByPhysicalIndex(i)
        #     self.fSharpness.append(sharpnessElem)
        elementNum = sharpnessPlug.numElements()
        fragmentMgr = omr.MRenderer.getFragmentManager()
        if fragmentMgr:
            fragmentMgr.removeFragment("ETS_ShaderSurface")
            surfaceShaderBody = fragments.getShaderSurfaceFragment(elementNum)
            fragmentMgr.addShadeFragmentFromBuffer(surfaceShaderBody, False)


    # def updateShader(self, shader, mappings):
    #     if len(self.fResolvedSharpnessName) == 0:
    #         mapping = mappings.findByParameterName("sharpness[2]")
    #         if mappings is not None:
    #             self.fResolvedSharpnessName = mapping.resolvedParameterName()
    #     if len(self.fResolvedSharpnessName) > 0:
    #         shader.setParameter(self.fResolvedSharpnessName, tuple(self.fSharpness))
