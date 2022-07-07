from distutils import cmd
import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds


class EditableShadingShelf(object):
    SHELF_NAME = 'EditableShading'

    def __init__(self):
        pass

    @classmethod
    def initializeShelf(cls):
        cmds.shelfLayout(cls.SHELF_NAME, p="ShelfLayout")
        cls.addButtons()

    @classmethod
    def deleteShelf(cls):
        if cmds.shelfLayout(cls.SHELF_NAME, ex=1): 
            cmds.deleteUI(cls.SHELF_NAME)

    @classmethod
    def addButtons(cls):
        pass