import maya.cmds as cmds
import maya.api.OpenMaya as om

import utils

class ShadingLocatorPair(object):
    def __init__(self, parent):
        self.edit = cmds.createNode('shadingLocatorNode')
        self.origin = cmds.createNode('shadingLocatorNode')

        centrePos = cmds.objectCenter(parent, gl=1)
        cmds.move(centrePos[0], centrePos[1], centrePos[2], self.origin, a=1)
        originTrans = cmds.listRelatives(self.origin, p=1, f=1, typ='transform')[0]
        self.originTrans = cmds.rename(originTrans, 'shadingPivot#')
        cmds.parentConstraint(parent, self.originTrans, mo=1)

        viewPos = utils.getMeshNearbyPosInView(parent, 0.5, 0.5)
        cmds.move(viewPos[0], viewPos[1], viewPos[2], self.edit, a=1)
        editTrans = cmds.listRelatives(self.edit, p=1, f=1, typ='transform')[0]
        self.editTrans = cmds.rename(editTrans, 'shadingEdit#')
        cmds.parentConstraint(parent, self.editTrans, mo=1)

        self.connectOrigin2Edit()

    def connectOrigin2Edit(self):
        # Record current selected object(s)
        curSlObj = cmds.ls(sl=1)

        MDGMod = om.MDGModifier() 
        # Get location plug from origin transformation node
        cmds.select(self.originTrans)
        mslList = om.MGlobal.getActiveSelectionList()
        originTransNode = mslList.getDependNode(0)
        originTransNode = om.MFnDependencyNode(originTransNode)
        srcPlug = originTransNode.findPlug('translate', False)
        # Find destination plug for origin location
        cmds.select(self.edit)
        mslList = om.MGlobal.getActiveSelectionList()
        editNode = mslList.getDependNode(0)
        editNode = om.MFnDependencyNode(editNode)
        desPlug = editNode.findPlug('originWorldPosition', False)
        MDGMod.connect(srcPlug, desPlug)
        # Get location plug from edit transformation node
        cmds.select(self.editTrans)
        mslList = om.MGlobal.getActiveSelectionList()
        editTransNode = mslList.getDependNode(0)
        editTransNode = om.MFnDependencyNode(editTransNode)
        srcPlug = editTransNode.findPlug('translate', False)
        # Find destination plug for edit location
        desPlug = editNode.findPlug('editWorldPosition', False)
        MDGMod.connect(srcPlug, desPlug)

        MDGMod.doIt()
        # Reselect previous object(s) after operation
        cmds.select(curSlObj)


class EditManager(object):
    editData = dict()
    maxEditNum = 50

    @classmethod
    def createEdit(cls, parent):
        locatorPair = ShadingLocatorPair(parent)
        if parent in cls.editData:
            cls.editData[parent].append(locatorPair)
        else:
            cls.editData[parent] = [locatorPair]
        return locatorPair

    @classmethod
    def getEditPairTransforms(cls, editLocator):
        pMesh = cmds.parentConstraint(editLocator, q=1, tl=1)[0]
        for pair in cls.editData[pMesh]:
            if pair.editTrans == editLocator or pair.originTrans == editLocator:
                return pair.editTrans, pair.originTrans

    @classmethod
    def getEditPairNodes(cls, editLocator):
        pMesh = cmds.parentConstraint(editLocator, q=1, tl=1)[0]
        for pair in cls.editData[pMesh]:
            if pair.editTrans == editLocator or pair.originTrans == editLocator:
                return pair.edit, pair.origin

    @classmethod
    def getConstraintedMesh(cls, editLocator):
        pMeshList = cmds.parentConstraint(editLocator, q=1, tl=1)
        pMesh = None
        if len(pMeshList) != 0:
            pMesh = pMeshList[0]
        return pMesh


class MaterialManager(object):
    materialData = dict()
    maxEditNum = 50

    @classmethod
    def createMeshMaterial(cls, meshTrans):
        if meshTrans in cls.materialData:
            material = cls.materialData[meshTrans]
            if cmds.objExists(material):
                return material
        shaderNode = cmds.shadingNode('editableToonShader', asShader=1)
        sg = cmds.sets(renderable=1, noSurfaceShader=1, em=1, name='editableToonShader1SG')
        cmds.connectAttr(shaderNode+'.outColor', sg+'.surfaceShader', f=1)
        cls.materialData[meshTrans] = sg
        return sg
