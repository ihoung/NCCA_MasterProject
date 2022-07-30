from distutils import command
import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds
import maya.mel as mel

import utils
import data

class EditableShadingShelf(object):
    SHELF_NAME = 'Editable Shading'
    shelf_instance = None

    @classmethod
    def initializeShelf(cls):
        if not (cls.shelf_instance and cmds.shelfLayout(cls.shelf_instance, q=1, ex=1)):
            cls.shelf_instance = cmds.shelfLayout(cls.SHELF_NAME, p="ShelfLayout")
            # Add buttons
            cmds.shelfButton(ann='Add a shading edit', i='locator.png', c=EditableShadingCmd.addEditLocator)
            cmds.shelfButton(ann='Assign toon shader', i='', c=EditableShadingCmd.assignToonShader)

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
            cmds.menuItem(label='Add Edit Locator', command=EditableShadingCmd.addEditLocator)
            cmds.menuItem(label='Assign Toon Shader', command=EditableShadingCmd.assignToonShader)
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
            print('No object selected!')
            return
        elif len(slist) != 1:
            print('More than one object selected')
            return
        print('Add edit locator')
        meshObj = slist[0]
        data.EditManager.createEdit(meshObj)
        
    @classmethod
    def assignToonShader(cls, *args):
        slist = cmds.ls(sl=1)
        if len(slist) == 0:
            print('No object selected!')
            return
        print('Assign toon shader')
        shaderNode = cmds.shadingNode('editableToonShader', asShader=1)
        sg = cmds.sets(renderable=1, noSurfaceShader=1, em=1, name='editableToonShader1SG')
        cmds.connectAttr(shaderNode+'.outColor', sg+'.surfaceShader', f=1)
        cmds.sets(slist, e=1, fe=sg)