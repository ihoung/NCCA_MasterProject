import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr

class EditableToonShader(om.MPxNode):
    id = om.MTypeId(0x00070010)
    sDbClassification = "drawdb/shader/surface/editableToonShader"
    sRegistrantId = "EditableToonShaderPlugin"

    # Input attributes
    aBaseColor = None
    aNormalMap = None
    aShadeThreshold = None
    aShadeIntensityRatio = None
    aDiffuseSmoothness = None
    aShadowDepthBias = None
    aLinearSpaceLighting = None

    # Output attributes
    aOutColor = None

    @staticmethod
    def creator():
        return EditableToonShader()

    @staticmethod
    def initialize():
        nAttr = om.MFnNumericAttribute()

        # Create input attributes
        EditableToonShader.aBaseColor = nAttr.createColor("baseColor", "bc")
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.default = (1.0, 1.0, 1.0)

        EditableToonShader.aNormalMap = nAttr.createColor("normalMap", "nm")
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.default = (0.0, 0.0, 1.0)

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

        EditableToonShader.aShadowDepthBias = nAttr.create("shadowDepthBias", "sd", om.MFnNumericData.kFloat)
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.setMin(0.0)
        nAttr.setMax(1.0)
        nAttr.default = 0.2

        EditableToonShader.aLinearSpaceLighting = nAttr.create("linearSpaceLighting", "lsl", om.MFnNumericData.kBoolean)
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.default = True

        # Create output attributes
        EditableToonShader.aOutColor = nAttr.createColor("outColor", "oc")
        nAttr.keyable = False
        nAttr.storable = False
        nAttr.readable = True
        nAttr.writable = False

        om.MPxNode.addAttribute(EditableToonShader.aBaseColor)
        om.MPxNode.addAttribute(EditableToonShader.aNormalMap)
        om.MPxNode.addAttribute(EditableToonShader.aShadeThreshold)
        om.MPxNode.addAttribute(EditableToonShader.aShadeIntensityRatio)
        om.MPxNode.addAttribute(EditableToonShader.aDiffuseSmoothness)
        om.MPxNode.addAttribute(EditableToonShader.aShadowDepthBias)
        om.MPxNode.addAttribute(EditableToonShader.aLinearSpaceLighting)
        om.MPxNode.addAttribute(EditableToonShader.aOutColor)

        om.MPxNode.attributeAffects(EditableToonShader.aBaseColor, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aNormalMap, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aShadeThreshold, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aShadeIntensityRatio, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aDiffuseSmoothness, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aShadowDepthBias, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aLinearSpaceLighting, EditableToonShader.aOutColor)

    def __init__(self):
        om.MPxNode.__init__(self)

    def compute(self, plug, block):
        if (plug != EditableToonShader.aOutColor) and (plug.parent() != EditableToonShader.aOutColor):
            return None

    def postConstructor(self):
        self.setMPSafe(True)


class EditableToonShaderOverride(omr.MPxSurfaceShadingNodeOverride):
    @staticmethod
    def creator(obj):
        return omr.MPxSurfaceShadingNodeOverride(obj)

    def __init__(self, obj):
        omr.MPxSurfaceShadingNodeOverride.__init__(self, obj)

        # Register fragments with the manager

    def supportedDrawAPIs(self):
        return omr.MRenderer.kOpenGL | omr.MRenderer.kOpenGLCoreProfile | omr.MRenderer.kDirectX11

    def fragmentName(self):
        return ""