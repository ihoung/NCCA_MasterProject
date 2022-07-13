from ctypes import util
from imp import reload
import inspect
import os
import sys
from functools import partial

import maya.api.OpenMaya as OpenMaya
import maya.cmds as cmds
# import maya.OpenMayaUI as omui
# from PySide2 import QtCore, QtWidgets
# from PySide2.QtCore import QFile
# from PySide2.QtGui import QColor, QFont
# from PySide2.QtUiTools import QUiLoader
# from shiboken2 import wrapInstance

maya_useNewAPI = True

test_env = True

# Delete all the package modules before importing, so that all the modules can be reloaded in Python 2
if test_env and sys.version_info.major == 2:
    plugin_paths = [path for path in os.getenv('MAYA_PLUG_IN_PATH').split(os.pathsep) if os.getenv('EDITABLE_SHADING_PLUGIN_ROOT') in path]
    if len(plugin_paths) is not 0:
        src_path = os.path.join(plugin_paths[0], 'src')
        toDelete = []
        for key, module in sys.modules.iteritems():
            try:
                module_file_path = inspect.getfile(module)
                if module_file_path.startswith(src_path):
                    # print('Delete module {0}'.format(module_file_path))
                    toDelete.append(key)
            except:
                pass
        for module in toDelete:
            del(sys.modules[module])


# import src moduls here
from src.toolbar import EditableShadingShelf, EditableShadingMenu
import src.commands as commands
from src.commands import *
from src.nodes import *

# Get all MPxCommand classes
def getCommands():
    cmd_classes = [cls for name, cls in inspect.getmembers(commands, inspect.isclass) if issubclass(cls, OpenMaya.MPxCommand)]
    return cmd_classes

def registerCommands(plugin_fn):
    commands = getCommands()
    for command in commands:
        try:
            plugin_fn.registerCommand(command.CMD_NAME, command.creator)
        except:
            OpenMaya.MGlobal.displayError(
                "Failed to register command: {0}".format(command.CMD_NAME)
            )

def deregisterCommands(plugin_fn):
    commands = getCommands()
    for command in commands:
        try:
            plugin_fn.deregisterCommand(command.CMD_NAME)
        except:
            OpenMaya.MGlobal.displayError(
                "Failed to deregister command: {0}".format(command.CMD_NAME)
            )

def registerNodes(plugin_fn):
    try:
        plugin_fn.registerNode('editableShadingNode', EditableShadingNode.id, EditableShadingNode.creator, EditableShadingNode.initialize, OpenMaya.MPxNode.kLocatorNode)
    except:
        OpenMaya.MGlobal.displayError("Failed to register node EditableShadingNode")

def deregisterNodes(plugin_fn):
    try: 
        plugin_fn.deregisterNode(EditableShadingNode.id)
    except:
        OpenMaya.MGlobal.displayError("Failed to deregister node EditableShadingNode")


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
    registerNodes(plugin_fn)
    registerCommands(plugin_fn)
    EditableShadingMenu.initializeMenu()
    EditableShadingShelf.initializeShelf()


def uninitializePlugin(plugin):
    # cleanup the dialog first
    plugin_fn = OpenMaya.MFnPlugin(plugin)
    EditableShadingShelf.deleteShelf()
    EditableShadingMenu.deleteMenu()
    deregisterCommands(plugin_fn)
    deregisterNodes(plugin_fn)


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
