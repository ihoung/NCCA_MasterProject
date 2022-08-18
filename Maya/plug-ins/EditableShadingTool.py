from ctypes import util
from imp import reload
import inspect
import os
import sys
from functools import partial

import maya.api.OpenMaya as OpenMaya
import maya.api.OpenMayaRender as OMR
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
from src.locator import *
from src.render import *

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
    # Locator node
    try:
        plugin_fn.registerNode('shadingLocatorNode', ShadingLocatorNode.id,                               \
                                ShadingLocatorNode.creator, ShadingLocatorNode.initialize,                \
                                OpenMaya.MPxNode.kLocatorNode, ShadingLocatorNode.drawDbClassification)
    except:
        OpenMaya.MGlobal.displayError("Failed to register node ShadingLocatorNode")
    try:
        OMR.MDrawRegistry.registerDrawOverrideCreator(ShadingLocatorNode.drawDbClassification, ShadingLocatorNode.drawRegistrantId, ShadingLocatorNodeDrawOverride.creator)
    except:
        OpenMaya.MGlobal.displayError("Failed to register draw override ShadingLocatorNodeDrawOverride for locator")
    # Locator pivot node
    try:
        plugin_fn.registerNode('shadingPivotNode', ShadingPivotNode.id,                               \
                                ShadingPivotNode.creator, ShadingPivotNode.initialize,                \
                                OpenMaya.MPxNode.kLocatorNode, ShadingPivotNode.drawDbClassification)
    except:
        OpenMaya.MGlobal.displayError("Failed to register node ShadingPivotNode")
    try:
        OMR.MDrawRegistry.registerDrawOverrideCreator(ShadingPivotNode.drawDbClassification, ShadingPivotNode.drawRegistrantId, ShadingLocatorNodeDrawOverride.creator)
    except:
        OpenMaya.MGlobal.displayError("Failed to register draw override ShadingLocatorNodeDrawOverride for pivot")
    # Shader node
    try:
        userClassify = "shader/surface:" + EditableToonShader.sDbClassification
        plugin_fn.registerNode('editableToonShader', EditableToonShader.id,                          \
                                EditableToonShader. creator, EditableToonShader.initialize,          \
                                OpenMaya.MPxNode.kDependNode, userClassify)
    except:
        OpenMaya.MGlobal.displayError("Failed to register node EditableToonShader")
    try:
        OMR.MDrawRegistry.registerSurfaceShadingNodeOverrideCreator(EditableToonShader.sDbClassification, EditableToonShader.sRegistrantId, EditableToonShaderOverride.creator)
    except:
        OpenMaya.MGlobal.displayError("Failed to register shading override EditableToonShaderOverride")

def deregisterNodes(plugin_fn):
    # Remove fragments
    fragmentMgr = OMR.MRenderer.getFragmentManager()
    if fragmentMgr:
        fragmentMgr.removeFragment("ETS_ShaderSurface")
        # fragmentMgr.removeFragment("ETS_ShadingMapFragment")
        # fragmentMgr.removeFragment("ETS_ToonFragment")        
    # Locator node
    try: 
        plugin_fn.deregisterNode(ShadingLocatorNode.id)
    except:
        OpenMaya.MGlobal.displayError("Failed to deregister node ShadingLocatorNode")
    try:
        OMR.MDrawRegistry.deregisterDrawOverrideCreator(ShadingLocatorNode.drawDbClassification, ShadingLocatorNode.drawRegistrantId)
    except:
        OpenMaya.MGlobal.displayError("Failed to deregister draw override ShadingLocatorNodeDrawOverride for locator")
    # Locator pivot node
    try: 
        plugin_fn.deregisterNode(ShadingPivotNode.id)
    except:
        OpenMaya.MGlobal.displayError("Failed to deregister node ShadingPivotNode")
    try:
        OMR.MDrawRegistry.deregisterDrawOverrideCreator(ShadingPivotNode.drawDbClassification, ShadingPivotNode.drawRegistrantId)
    except:
        OpenMaya.MGlobal.displayError("Failed to deregister draw override ShadingLocatorNodeDrawOverride for pivot")
    # Shader node
    try:
        plugin_fn.deregisterNode(EditableToonShader.id)
    except:
        OpenMaya.MGlobal.displayError("Failed to deregister node EditableToonShader")
    try:
        OMR.MDrawRegistry.deregisterSurfaceShadingNodeOverrideCreator(EditableToonShader.sDbClassification, EditableToonShader.sRegistrantId)
    except:
        OpenMaya.MGlobal.displayError("Failed to deregister draw override EditableToonShaderOverride")


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
