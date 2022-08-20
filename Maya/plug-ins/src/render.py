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
    aEditWorldPos = None
    aAnisotropy = None
    aSharpness = None
    aBend = None
    aBulge = None
    aRotation = None
    aNormalSmooth = None
    aIntensityGain = None
    aSoftness = None
    aEditLightSpace = None
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
        mAttr = om.MFnMatrixAttribute()

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

        aEditWorldPosX = nAttr.create('editWorldPositionX', 'wpx', om.MFnNumericData.kFloat)
        aEditWorldPosY = nAttr.create('editWorldPositionY', 'wpy', om.MFnNumericData.kFloat)
        aEditWorldPosZ = nAttr.create('editWorldPositionZ', 'wpz', om.MFnNumericData.kFloat)
        EditableToonShader.aEditWorldPos = nAttr.create('editWorldPosition', 'ewp', aEditWorldPosX, aEditWorldPosY, aEditWorldPosZ)
        nAttr.readable = False
        EditableToonShader.aEditLightSpace = mAttr.create('editLightSpace', 'els')
        nAttr.readable = False
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
        cmpAttr.addChild(EditableToonShader.aEditWorldPos)
        cmpAttr.addChild(EditableToonShader.aEditLightSpace)
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
        self.fEditWorldPos = []
        self.fAnisotropy = []
        self.fSharpness = []
        self.fBend = []
        self.fBulge = []
        self.fRotation = []
        self.fNormalSmooth = []
        self.fIntensityGain = []
        self.fSoftness = []
        self.fEditNum = 0
        self.fResolvedEditWorldPosName = ""
        self.fResolvedAnisotropyName = ""
        self.fResolvedSharpnessName = ""
        self.fResolvedBendName = ""
        self.fResolvedBulgeName = ""
        self.fResolvedRotationName = ""
        self.fResolvedNormalSmoothName = ""
        self.fResolvedIntensityGainName = ""
        self.fResolvedSoftnessName = ""
        self.fResolvedEditNumName = ""

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
        editMapping = omr.MAttributeParameterMapping('editWorldPosition', '', True, True)
        mappings.append(editMapping)
        editMapping = omr.MAttributeParameterMapping('anisotropy', '', True, True)
        mappings.append(editMapping)
        editMapping = omr.MAttributeParameterMapping('sharpness', '', True, True)
        mappings.append(editMapping)
        editMapping = omr.MAttributeParameterMapping('bend', '', True, True)
        mappings.append(editMapping)
        editMapping = omr.MAttributeParameterMapping('bulge', '', True, True)
        mappings.append(editMapping)
        editMapping = omr.MAttributeParameterMapping('rotation', '', True, True)
        mappings.append(editMapping)
        editMapping = omr.MAttributeParameterMapping('normalSmooth', '', True, True)
        mappings.append(editMapping)
        editMapping = omr.MAttributeParameterMapping('intensityGain', '', True, True)
        mappings.append(editMapping)
        editMapping = omr.MAttributeParameterMapping('softness', '', True, True)
        mappings.append(editMapping)
        editMapping = omr.MAttributeParameterMapping('editNum', '', True, True)
        mappings.append(editMapping)

    # def valueChangeRequiresFragmentRebuild(self, plug):
    #     return True

    def updateDG(self):
        node = om.MFnDependencyNode(self.fObject)
        editsPlug = node.findPlug('edits', True)
        del self.fEditWorldPos[:]
        del self.fAnisotropy[:]
        del self.fSharpness[:]
        del self.fBend[:]
        del self.fBulge[:]
        del self.fRotation[:]
        del self.fNormalSmooth[:]
        del self.fIntensityGain[:]
        del self.fSoftness[:]
        self.fEditNum = editsPlug.numConnectedElements()
        for i in range(self.fEditNum):
            elemPlug = editsPlug.elementByPhysicalIndex(i)
            for j in range(elemPlug.numChildren()):
                childPlug = elemPlug.child(j)
                childAttrName = om.MFnAttribute(childPlug.attribute()).name
                if childAttrName == 'editWorldPosition':
                    xPlugValue = childPlug.child(0).asFloat()
                    yPlugValue = childPlug.child(1).asFloat()
                    zPlugValue = childPlug.child(2).asFloat()
                    self.fEditWorldPos.append(xPlugValue)
                    self.fEditWorldPos.append(yPlugValue)
                    self.fEditWorldPos.append(zPlugValue)
                    continue
                childPlugValue = childPlug.asFloat()
                if childAttrName == 'anisotropy':
                    self.fAnisotropy.append(childPlugValue)
                elif childAttrName == 'sharpness':
                    self.fSharpness.append(childPlugValue)
                elif childAttrName == 'bend':
                    self.fBend.append(childPlugValue)
                elif childAttrName == 'bulge':
                    self.fBulge.append(childPlugValue)
                elif childAttrName == 'rotation':
                    self.fRotation.append(childPlugValue)
                elif childAttrName == 'normalSmooth':
                    self.fNormalSmooth.append(childPlugValue)
                elif childAttrName == 'intensityGain':
                    self.fIntensityGain.append(childPlugValue)
                elif childAttrName == 'softness':
                    self.fSoftness.append(childPlugValue)
        if self.fEditNum < data.EditManager.maxEditNum:
            self.fEditWorldPos += [0.0]*(data.EditManager.maxEditNum-self.fEditNum)*3
            self.fAnisotropy += [0.0]*(data.EditManager.maxEditNum-self.fEditNum)
            self.fSharpness += [0.0]*(data.EditManager.maxEditNum-self.fEditNum)
            self.fBend += [0.0]*(data.EditManager.maxEditNum-self.fEditNum)
            self.fBulge += [0.0]*(data.EditManager.maxEditNum-self.fEditNum)
            self.fRotation += [0.0]*(data.EditManager.maxEditNum-self.fEditNum)
            self.fNormalSmooth += [0.0]*(data.EditManager.maxEditNum-self.fEditNum)         
            self.fIntensityGain += [0.0]*(data.EditManager.maxEditNum-self.fEditNum)
            self.fSoftness += [0.0]*(data.EditManager.maxEditNum-self.fEditNum)

    def updateShader(self, shader, mappings):
        # Edit number
        if len(self.fResolvedEditNumName) == 0:
            mapping = mappings.findByParameterName("editNum")
            if mapping is not None:
                self.fResolvedEditNumName = mapping.resolvedParameterName()
        if len(self.fResolvedEditNumName) > 0:
            # print("editNum",self.fEditNum)
            shader.setParameter(self.fResolvedEditNumName, self.fEditNum)
        # EditWorldPosition
        if len(self.fResolvedEditWorldPosName) == 0:
            mapping = mappings.findByParameterName("editWorldPosition")
            if mapping is not None:
                self.fResolvedEditWorldPosName = mapping.resolvedParameterName()
        if len(self.fResolvedEditWorldPosName) > 0 :
            # print("editWorldPosition",self.fEditWorldPos)
            shader.setArrayParameter(self.fResolvedEditWorldPosName, self.fEditWorldPos, data.EditManager.maxEditNum*3)
        # Anisotropy
        if len(self.fResolvedAnisotropyName) == 0:
            mapping = mappings.findByParameterName("anisotropy")
            if mapping is not None:
                self.fResolvedAnisotropyName = mapping.resolvedParameterName()
        if len(self.fResolvedAnisotropyName) > 0 :
            # print("anisotropy",self.fAnisotropy)
            shader.setArrayParameter(self.fResolvedAnisotropyName, self.fAnisotropy, data.EditManager.maxEditNum)
        # sharpness
        if len(self.fResolvedSharpnessName) == 0:
            mapping = mappings.findByParameterName("sharpness")
            if mapping is not None:
                self.fResolvedSharpnessName = mapping.resolvedParameterName()
        if len(self.fResolvedSharpnessName) > 0:
            # print("sharpness",self.fSharpness)
            shader.setArrayParameter(self.fResolvedSharpnessName, self.fSharpness, data.EditManager.maxEditNum)
        # bend
        if len(self.fResolvedBendName) == 0:
            mapping = mappings.findByParameterName("bend")
            if mapping is not None:
                self.fResolvedBendName = mapping.resolvedParameterName()
        if len(self.fResolvedBendName) > 0:
            # print("bend",self.fBend)
            shader.setArrayParameter(self.fResolvedBendName, self.fBend, data.EditManager.maxEditNum)
        # bulge
        if len(self.fResolvedBulgeName) == 0:
            mapping = mappings.findByParameterName("bulge")
            if mapping is not None:
                self.fResolvedBulgeName = mapping.resolvedParameterName()
        if len(self.fResolvedBulgeName) > 0:
            # print("bulge",self.fBulge)
            shader.setArrayParameter(self.fResolvedBulgeName, self.fBulge, data.EditManager.maxEditNum)
        # rotation
        if len(self.fResolvedRotationName) == 0:
            mapping = mappings.findByParameterName("rotation")
            if mapping is not None:
                self.fResolvedRotationName = mapping.resolvedParameterName()
        if len(self.fResolvedRotationName) > 0:
            # print("rotation",self.fRotation)
            shader.setArrayParameter(self.fResolvedRotationName, self.fRotation, data.EditManager.maxEditNum)
        # normalSmooth
        if len(self.fResolvedNormalSmoothName) == 0:
            mapping = mappings.findByParameterName("normalSmooth")
            if mapping is not None:
                self.fResolvedNormalSmoothName = mapping.resolvedParameterName()
        if len(self.fResolvedNormalSmoothName) > 0:
            # print("normalSmooth",self.fNormalSmooth)
            shader.setArrayParameter(self.fResolvedNormalSmoothName, self.fNormalSmooth, data.EditManager.maxEditNum)
        # intensityGain
        if len(self.fResolvedIntensityGainName) == 0:
            mapping = mappings.findByParameterName("intensityGain")
            if mapping is not None:
                self.fResolvedIntensityGainName = mapping.resolvedParameterName()
        if len(self.fResolvedIntensityGainName) > 0:
            # print("intensityGain",self.fIntensityGain)
            shader.setArrayParameter(self.fResolvedIntensityGainName, self.fIntensityGain, data.EditManager.maxEditNum)
        # softness
        if len(self.fResolvedSoftnessName) == 0:
            mapping = mappings.findByParameterName("softness")
            if mapping is not None:
                self.fResolvedSoftnessName = mapping.resolvedParameterName()
        if len(self.fResolvedSoftnessName) > 0:
            # print("softness",self.fSoftness)
            shader.setArrayParameter(self.fResolvedSoftnessName, self.fSoftness, data.EditManager.maxEditNum)

