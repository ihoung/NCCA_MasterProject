import sys
import maya.api.OpenMaya as OpenMaya


class EditableShading(object):
    def __init__(self):
        pass


#####################################################################
# Plugin Commands
#####################################################################
# class AddEditableShadingShelf(OpenMaya.MPxCommand):
#     CMD_NAME = "AddEditableShadingShelf"

#     def __init__(self):
#         if sys.version_info.major == 3:
#             super().__init__()
#         else:
#             super(AddEditableShadingShelf, self).__init__()

#     @classmethod
#     def doIt(cls, args):
#         """
#         Called when the command is executed in script
#         """
#         EditableShadingShelf.initializeShelf()

#     @classmethod
#     def redoIt(cls, args):
#         EditableShadingShelf.deleteShelf()

#     @classmethod
#     def creator(cls):
#         """
#         Think of this as a factory
#         """
#         return AddEditableShadingShelf()

#     @classmethod
#     def cleanup(cls):
#         # cleanup the UI and call the destructors
#         pass
