from pickle import TRUE
import maya.standalone
import unittest
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as OM
import maya.api.OpenMayaRender as OMR
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import utils


class TestMayaScene(unittest.TestCase):
    def setUp(self):
        print("Set up tests for maya scene.")

    def test_maya_python_version(self):
        self.assertEqual(utils.isPy2Env(), True)

    def test_shader(self):
        shaderMgr = OMR.MRenderer.getShaderManager()
        dc = OMR.MRenderUtilities.acquireSwatchDrawContext()
        shaderInstance = shaderMgr.getEffectsFileShader(os.path.join(utils.getShaderDirPath(),"EditableShadingMap.ogsfx"), "")
        # shaderInstance.bind(dc)
        # errorMsg = "EditableShadingMap10" + ":\n" + OMR.MShaderManager.getLastError() + OMR.MShaderManager.getLastErrorSource(TRUE,TRUE,2)
        # OM.MGlobal.displayError(errorMsg)
        # shaderInstance.unbind(dc)
    

if __name__ == '__main__':
    maya.standalone.initialize(name='python')
    unittest.main()
    maya.standalone.uninitialize()