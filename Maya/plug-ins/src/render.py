from pyexpat import native_encoding
import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr

import utils
import fragments
import data

class EditableToonShader(om.MPxNode):
    id = om.MTypeId(0x00070010)
    sDbClassification = "drawdb/shader/surface/editableToonShader"
    sRegistrantId = "EditableToonShaderPlugin"

    # Input attributes
    aBaseColor = None
    aShadeThreshold = None
    aShadeIntensityRatio = None
    aDiffuseSmoothness = None
    aLightDirection = None
    aLightIntensity = None
    # aLightDiffuse = None
    # aLightShadowFraction = None
    # aPreShadowIntensity = None
    # aLightData = None
    aUVCoord = None
    aNormalCamera = None
    # aShadowDepthBias = None
    # aLinearSpaceLighting = None
    aAnisotropy = None
    aSharpness = None
    aBend = None
    aBulge = None
    aRotation = None
    aNormalSmooth = None
    aIntensityGain = None
    aSoftness = None
    aEdits = None

    # Output attributes
    aOutColor = None

    @staticmethod
    def creator():
        return EditableToonShader()

    @staticmethod
    def initialize():
        nAttr = om.MFnNumericAttribute()
        lAttr = om.MFnLightDataAttribute()
        cmpAttr = om.MFnCompoundAttribute()
        uAttr = om.MFnUnitAttribute()

        # Create input attributes
        EditableToonShader.aBaseColor = nAttr.createColor("baseColor", "bc")
        nAttr.keyable = True
        nAttr.storable = True
        nAttr.readable = True
        nAttr.writable = True
        nAttr.default = (1.0, 1.0, 1.0)

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

        EditableToonShader.aLightIntensity = nAttr.createColor( "lightIntensity", "li" )
        nAttr.storable = False
        nAttr.hidden = True
        nAttr.readable = True
        nAttr.writable = False

        # EditableToonShader.aLightDiffuse = nAttr.create( "lightDiffuse", "ldf", om.MFnNumericData.kBoolean)
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

        aUCoord = nAttr.create("uCoord", "u", om.MFnNumericData.kFloat)
        aVCoord = nAttr.create("vCoord", "v", om.MFnNumericData.kFloat)
        EditableToonShader.aUVCoord = nAttr.create("uvCoord", "uv", aUCoord, aVCoord)
        nAttr.hidden = True

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

        EditableToonShader.aAnisotropy = nAttr.create('anisotropy', 'a', om.MFnNumericData.kFloat)
        nAttr.readable = False
        EditableToonShader.aSharpness = nAttr.create('sharpness', 's', om.MFnNumericData.kFloat)
        nAttr.readable = False
        EditableToonShader.aBend = nAttr.create('bend', 'wy', om.MFnNumericData.kFloat)
        nAttr.readable = False
        EditableToonShader.aBulge = nAttr.create('bulge', 'wx', om.MFnNumericData.kFloat)
        nAttr.readable = False
        EditableToonShader.aRotation = uAttr.create('rotation', 'rot', om.MFnUnitAttribute.kAngle)
        nAttr.readable = False
        EditableToonShader.aNormalSmooth = nAttr.create('normalSmooth', 'ns', om.MFnNumericData.kFloat)
        nAttr.readable = False
        EditableToonShader.aIntensityGain = nAttr.create('intensityGain', 'G', om.MFnNumericData.kFloat)
        nAttr.readable = False
        EditableToonShader.aSoftness = nAttr.create('softness', 'd', om.MFnNumericData.kFloat)
        nAttr.readable = False

        EditableToonShader.aEdits = cmpAttr.create("edits", "es")
        cmpAttr.array = True
        cmpAttr.addChild(EditableToonShader.aAnisotropy)
        cmpAttr.addChild(EditableToonShader.aSharpness)
        cmpAttr.addChild(EditableToonShader.aBend)
        cmpAttr.addChild(EditableToonShader.aBulge)
        cmpAttr.addChild(EditableToonShader.aRotation)
        cmpAttr.addChild(EditableToonShader.aNormalSmooth)
        cmpAttr.addChild(EditableToonShader.aIntensityGain)
        cmpAttr.addChild(EditableToonShader.aSoftness)
        cmpAttr.readable = False
        cmpAttr.usesArrayDataBuilder = True

        # Create output attributes
        EditableToonShader.aOutColor = nAttr.createColor("outColor", "oc")
        nAttr.keyable = False
        nAttr.storable = False
        nAttr.readable = True
        nAttr.writable = False

        om.MPxNode.addAttribute(EditableToonShader.aBaseColor)
        om.MPxNode.addAttribute(EditableToonShader.aShadeThreshold)
        om.MPxNode.addAttribute(EditableToonShader.aShadeIntensityRatio)
        om.MPxNode.addAttribute(EditableToonShader.aDiffuseSmoothness)
        om.MPxNode.addAttribute(EditableToonShader.aLightDirection)
        om.MPxNode.addAttribute(EditableToonShader.aLightIntensity)
        # om.MPxNode.addAttribute(EditableToonShader.aLightDiffuse)
        # om.MPxNode.addAttribute(EditableToonShader.aLightShadowFraction)
        # om.MPxNode.addAttribute(EditableToonShader.aPreShadowIntensity)
        # om.MPxNode.addAttribute(EditableToonShader.aLightData)
        om.MPxNode.addAttribute(EditableToonShader.aUVCoord)
        om.MPxNode.addAttribute(EditableToonShader.aNormalCamera)
        # om.MPxNode.addAttribute(EditableToonShader.aShadowDepthBias)
        # om.MPxNode.addAttribute(EditableToonShader.aLinearSpaceLighting)
        om.MPxNode.addAttribute(EditableToonShader.aEdits)
        om.MPxNode.addAttribute(EditableToonShader.aOutColor)

        om.MPxNode.attributeAffects(EditableToonShader.aBaseColor, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aShadeThreshold, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aShadeIntensityRatio, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aDiffuseSmoothness, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aLightDirection, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aLightIntensity, EditableToonShader.aOutColor)
        # om.MPxNode.attributeAffects(EditableToonShader.aLightDiffuse, EditableToonShader.aOutColor)
        # om.MPxNode.attributeAffects(EditableToonShader.aLightShadowFraction, EditableToonShader.aOutColor)
        # om.MPxNode.attributeAffects(EditableToonShader.aPreShadowIntensity, EditableToonShader.aOutColor)
        # om.MPxNode.attributeAffects(EditableToonShader.aLightData, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aUVCoord, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aNormalCamera, EditableToonShader.aOutColor)
        # om.MPxNode.attributeAffects(EditableToonShader.aShadowDepthBias, EditableToonShader.aOutColor)
        # om.MPxNode.attributeAffects(EditableToonShader.aLinearSpaceLighting, EditableToonShader.aOutColor)
        om.MPxNode.attributeAffects(EditableToonShader.aEdits, EditableToonShader.aOutColor)

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
        self.fEdits = []
        self.fResolvedEditName = []

        # Register fragments with the manager
        shaderMgr = omr.MRenderer.getShaderManager()
        fragmentMgr = omr.MRenderer.getFragmentManager()
        if shaderMgr and fragmentMgr:
            shaderMgr.addShaderPath(utils.getShaderDirPath())
            fragmentMgr.addFragmentPath(utils.getFragmentDirPath())
            # if not fragmentMgr.hasFragment("ETS_ShadingMapFragment"):
            #     fragmentMgr.addShadeFragmentFromFile("ETS_ShadingMapFragment.xml", False)
            # if not fragmentMgr.hasFragment("ETS_ToonFragment"):
            #     fragmentMgr.addShadeFragmentFromFile("ETS_ToonFragment.xml", False)
            if not fragmentMgr.hasFragment("ETS_ShaderSurface"):
                fragmentMgr.addFragmentGraphFromFile("ETS_ShaderSurface.xml")
            # if not fragmentMgr.hasFragment("ETS_ToonFragment"):
            #     fragmentBody = fragments.getShaderSurfaceFragment(0)
            #     fragmentMgr.addShadeFragmentFromBuffer(fragmentBody, False)
    
    def primaryColorParameter(self):
        return "baseColor"

    def bumpAttribute(self):
        return "normalCamera"

    def supportedDrawAPIs(self):
        return omr.MRenderer.kOpenGL | omr.MRenderer.kOpenGLCoreProfile | omr.MRenderer.kDirectX11

    def fragmentName(self):
        return "ETS_ShaderSurface"

    def getCustomMappings(self, mappings):
        for i in range(data.EditManager.maxEditNum):
            editMapping = omr.MAttributeParameterMapping('edit{}'.format(i), '', True, True)
            mappings.append(editMapping)

    def valueChangeRequiresFragmentRebuild(self, plug):
        return True

    def updateDG(self):
        node = om.MFnDependencyNode(self.fObject)
        # sharpnessPlug = node.findPlug('sharpness', True)
        # del self.fSharpness[:]
        # elementNum = sharpnessPlug.numElements()
        # for i in range(elementNum):
        #     sharpnessElem = sharpnessPlug.elementByPhysicalIndex(i)
        #     self.fSharpness.append(sharpnessElem)
        # fragmentMgr = omr.MRenderer.getFragmentManager()
        # if fragmentMgr:
        #     fragmentMgr.removeFragment("ETS_ToonFragment")
        #     print("hasFragment ETS_ToonFragment " ,fragmentMgr.hasFragment("ETS_ToonFragment"))
        #     surfaceShaderBody = fragments.getShaderSurfaceFragment(elementNum)
        #     fragmentMgr.addShadeFragmentFromBuffer(surfaceShaderBody, False)
        #     print(fragmentMgr.getFragmentXML("ETS_ToonFragment"))
        #     print('fragment update')        
        editsPlug = node.findPlug('edits', True)
        del self.fEdits[:]
        connectedElemNum = editsPlug.numConnectedElements()
        for i in range(connectedElemNum):
            elemPlug = editsPlug.elementByPhysicalIndex(i)
            plugValues = []
            for j in range(elemPlug.numChildren()):
                childValue = elemPlug.child(j).asFloat()
                plugValues.append(childValue)
            self.fEdits.append(plugValues)
        print(self.fEdits)


    def updateShader(self, shader, mappings):
        # for i in range(len(mappings)):
        #     mapping = mappings[i]
        #     print(mapping.attributeName(), mapping.parameterName(), mapping.resolvedParameterName())
        #     print(shader.parameterType(mapping.resolvedParameterName()))
        if len(self.fResolvedEditName) == 0:
            for i in range(data.EditManager.maxEditNum):
                mapping = mappings.findByParameterName("edit{}".format(i))
                if mappings is not None:
                    self.fResolvedEditName.append(mapping.resolvedParameterName())
        if len(self.fResolvedEditName) > 0:
            dataNum = min(data.EditManager.maxEditNum, len(self.fEdits))
            for i in range(dataNum):
                shader.setArrayParameter(self.fResolvedEditName[i], self.fEdits[i], 8)


