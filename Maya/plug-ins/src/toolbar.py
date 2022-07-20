from distutils import command
import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds
import maya.mel as mel

import utils

class EditableShadingShelf(object):
    SHELF_NAME = 'Editable Shading'
    shelf_instance = None

    @classmethod
    def initializeShelf(cls):
        if not (cls.shelf_instance and cmds.shelfLayout(cls.shelf_instance, q=1, ex=1)):
            cls.shelf_instance = cmds.shelfLayout(cls.SHELF_NAME, p="ShelfLayout")
            # Add buttons
            cmds.shelfButton(ann='Add a shading edit', i='locator.png', c=EditableShadingCmd.addEditLocator)

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
        print('Add edit locator')
        cmds.createNode('shadingLocatorNode')