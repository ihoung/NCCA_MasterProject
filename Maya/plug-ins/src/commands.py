import sys
import maya.api.OpenMaya as OpenMaya

from toolbar import EditableShadingShelf


class EditableShading(OpenMaya.MPxCommand):
    CMD_NAME = "EditableShading"
    ui = None

    def __init__(self):
        if sys.version_info.major == 3:
            super().__init__()
        else:
            super(EditableShading, self).__init__()
        ui = None

    @classmethod
    def doIt(cls, args):
        """
        Called when the command is executed in script
        """
        pass

    @classmethod
    def creator(cls):
        """
        Think of this as a factory
        """
        return EditableShading()

    @classmethod
    def cleanup(cls):
        # cleanup the UI and call the destructors
        pass

    @classmethod
    def addShelf(cls):
        EditableShadingShelf.initializeShelf()

    @classmethod
    def deleteShelf(cls):
        EditableShadingShelf.deleteShelf()
