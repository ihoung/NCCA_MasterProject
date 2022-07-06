from imp import reload
import os
import sys
from functools import partial
import shutil

import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaUI as OpenMayaUI
import maya.cmds as cmds
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaUI as omui
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QFile
from PySide2.QtGui import QColor, QFont
from PySide2.QtUiTools import QUiLoader
from shiboken2 import wrapInstance

maya_useNewAPI = True


def get_main_window():
    window = omui.MQtUtil.mainWindow()
    return wrapInstance(int(window), QtWidgets.QWidget)


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


def initializePlugin(plugin):
    vendor = "YiyangHuang"
    version = "1.0.0"
    if os.environ.get("EDITABLE_SHADING_PLUGIN_ROOT") is None:
        OpenMaya.MGlobal.displayError(
            "Module Environment not set ensure EDITABLE_SHADING_PLUGIN_ROOT is set in module file"
        )
        # throw exception and let maya deal with it
        raise

    plugin_fn = OpenMaya.MFnPlugin(plugin, vendor, version)
    try:
        plugin_fn.registerCommand(EditableShading.CMD_NAME, EditableShading.creator)
        # cmds.evalDeferred("cmds.M2UExport()")
        # cmds.evalDeferred("cmds.menu('M2UExportSetting', label='Unreal Export Tool', parent='MayaWindow', pmc=cmds.M2UExport)")
    except:
        OpenMaya.MGlobal.displayError(
            "Failed to register command: {0}".format(EditableShading.CMD_NAME)
        )


def uninitializePlugin(plugin):
    # cleanup the dialog first
    EditableShading.cleanup()
    plugin_fn = OpenMaya.MFnPlugin(plugin)
    try:
        cmds.evalDeferred("cmds.deleteUI('M2UExportSetting')")
        plugin_fn.deregisterCommand(EditableShading.CMD_NAME)
    except:
        OpenMaya.MGlobal.displayError(
            "Failed to deregister command: {0}".format(EditableShading.CMD_NAME)
        )


if __name__ == '__main__':
    plugin_name = "EditableShadingTool"

    cmds.evalDeferred(
        'if cmds.pluginInfo("{0}", q=True, loaded=True): cmds.unloadPlugin("{0}")'.format(
            plugin_name
        )
    )
    cmds.evalDeferred(
        'if not cmds.pluginInfo("{0}", q=True, loaded=True): cmds.loadPlugin("{0}")'.format(
            plugin_name
        )
    )
