import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds
import maya.mel as mel

import utils
import data
from render import EditableToonShader
from locator import ShadingLocatorNode

class EditableShadingShelf(object):
    SHELF_NAME = 'Editable Shading'
    shelf_instance = None

    @classmethod
    def initializeShelf(cls):
        if not (cls.shelf_instance and cmds.shelfLayout(cls.shelf_instance, q=1, ex=1)):
            cls.shelf_instance = cmds.shelfLayout(cls.SHELF_NAME, p="ShelfLayout")
            # Add buttons
            cmds.shelfButton(ann='Assign toon shader', i='', c=EditableShadingCmd.assignToonShader)
            cmds.shelfButton(ann='Add a shading edit', i='locator.png', c=EditableShadingCmd.addEditLocator)
            cmds.shelfButton(ann='Delete current shading edit', i='locator.png', c=EditableShadingCmd.deleteEditLocator)
            cmds.shelfButton(ann='Edit shading projection pivot', i='', c=EditableShadingCmd.editProjectPivot)

    @classmethod
    def createShelf(cls, args):
        cls.initializeShelf()
        shelfTab = cmds.shelfLayout(cls.shelf_instance, q=1, p=1)
        cmds.shelfTabLayout(shelfTab, e=1, selectTab=cls.shelf_instance)

    @classmethod
    def deleteShelf(cls):
        if cls.shelf_instance and cmds.shelfLayout(cls.shelf_instance, q=1, ex=1): 
            cmds.deleteUI(cls.shelf_instance)
            cls.shelf_instance = None


class EditableShadingMenu(object):
    MENU_NAME = 'Editable Shading'
    menu_instance = None

    @classmethod
    def initializeMenu(cls):
        if not cls.menu_instance:
            rendering_menuset = mel.eval('findMenuSetFromLabel("Rendering")')
            cls.menu_instance = cmds.menu(label=cls.MENU_NAME, parent='MayaWindow', visible=cmds.menuSet(q=1, label=1)=='Rendering')
            # Add menu items
            cmds.menuItem(label='Assign Toon Shader', command=EditableShadingCmd.assignToonShader)
            cmds.menuItem(label='Add Edit Locator', command=EditableShadingCmd.addEditLocator)
            cmds.menuItem(label='Edit shading projection pivot', command=EditableShadingCmd.editProjectPivot)
            cmds.menuItem(label='Open Shelf', command=EditableShadingShelf.createShelf)
            # Add menu to rendering menu set
            cmds.menuSet(rendering_menuset, addMenu=cls.menu_instance)

    @classmethod
    def deleteMenu(cls):
        if cls.menu_instance: 
            cmds.deleteUI(cls.menu_instance)
            cls.menu_instance = None


class EditableShadingCmd(object):
    EDIT_GROUP_NAME = ''

    def __init__(self):
        pass

    @classmethod
    def addEditLocator(cls, *args):
        slist = cmds.ls(sl=1)
        if len(slist) == 0:
            OpenMaya.MGlobal.displayError('No mesh object selected!')
            return
        elif len(slist) != 1:
            OpenMaya.MGlobal.displayError('More than one object selected')
            return
        slObj = slist[0]
        material = EditableShadingCmd.getAssignedToonShader(slObj)
        if not material:
            OpenMaya.MGlobal.displayError('No mesh object selected!')
            return
        print('Add edit locator')
        edit = data.EditManager.createEdit(slObj)
        # Connect attributes
        if cmds.nodeType(material) == 'editableToonShader':
            # cmds.connectAttr(edit.locator+'.sharpness', material+'.sharpness')
            cmds.select(edit.locator)
            mslList = OpenMaya.MGlobal.getActiveSelectionList()
            editNode = mslList.getDependNode(0)
            cmds.select(edit.locTrans)
            mslList = OpenMaya.MGlobal.getActiveSelectionList()
            editTransNode = mslList.getDependNode(0)
            cmds.select(material)
            mslList = OpenMaya.MGlobal.getActiveSelectionList()
            materialNode = mslList.getDependNode(0)
            utils.connect2CmpAttrByName(editNode, editTransNode, materialNode, EditableToonShader.aEdits)
        else:
            OpenMaya.MGlobal.displayWarning('No specific toon material assgined!')
        # Add to group
        groupName = cmds.ls(slObj, sn=1)[0] + '_shadingEdits'
        if not cmds.objExists(groupName):
            cmds.group(n=groupName, em=1)
        cmds.parent([edit.locTrans, edit.pivotTrans], groupName)
        cmds.select(edit.locTrans)

    @classmethod
    def deleteEditLocator(cls, *arg):
        slist = cmds.ls(sl=1)
        if len(slist) == 0:
            OpenMaya.MGlobal.displayError('No edit locator selected!')
            return
        for slObj in slist:
            slChildList = cmds.listRelatives(slObj, typ=['shadingLocatorNode', 'shadingPivotNode'])
            if slChildList is None or len(slChildList) == 0:
                OpenMaya.MGlobal.displayWarning('Current selected object is not a edit locator!')
                continue
            edit, pivot = data.EditManager.getEditPairNodes(slObj)
            cmds.select(edit)
            mslList = OpenMaya.MGlobal.getActiveSelectionList()
            editNode = mslList.getDependNode(0)
            utils.disconnectCmpAttr(editNode)
            editTrans, pivotTrans = data.EditManager.getEditPairTransforms(slObj)
            cmds.delete(editTrans)
            cmds.delete(pivotTrans)

    @classmethod
    def editProjectPivot(cls, *args):
        slist = cmds.ls(sl=1)
        if len(slist) > 1:
            OpenMaya.MGlobal.displayError('More than one edit selected')
            return
        elif len(slist) == 0:
            OpenMaya.MGlobal.displayError('No edit selected!')
            return
        elif len(cmds.listRelatives(slist[0], typ='shadingLocatorNode')) == 0:
            OpenMaya.MGlobal.displayError('No edit locator selected!')
            return
        editTrans, pivotTrans = data.EditManager.getEditPairTransforms(slist[0])
        cmds.select(pivotTrans)
        cmds.setToolTo('Move')
        
    @classmethod
    def assignToonShader(cls, *args):
        slist = cmds.ls(sl=1)
        if len(slist) == 0:
            OpenMaya.MGlobal.displayError('No object selected!')
            return
        meshTransList = []
        for slObj in slist:
            relativeList = cmds.listRelatives(slObj, typ='mesh')
            if len(relativeList) != 0:
                meshTransList.append(slObj)
        if len(meshTransList) == 0:
            OpenMaya.MGlobal.displayError('No mesh object selected!')
            return
        print('Assign toon shader')
        for meshTrans in meshTransList:
            sg = data.MaterialManager.createMeshMaterial(meshTrans)
            cmds.sets([meshTrans], e=1, fe=sg)
        cmds.select(slist)
    
    @staticmethod
    def getAssignedToonShader(meshTransform):
        # Check the assigned toon shader
        relativeList = cmds.listRelatives(meshTransform)
        if relativeList is None or len(relativeList) == 0 or cmds.nodeType(relativeList[0]) != 'mesh':
            OpenMaya.MGlobal.displayError('No mesh object selected!')
            return
        meshName = relativeList[0]
        shadingGroup = cmds.listConnections(meshName)[0]
        if shadingGroup is not None:
        # Get the material attached to the shader group
            material = [x for x in cmds.ls(cmds.listConnections(shadingGroup), materials=1)][0]
        return material

