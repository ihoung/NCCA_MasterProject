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
import fragments


class TestMayaScene(unittest.TestCase):
    def setUp(self):
        print("Set up tests for maya scene.")

    def test_maya_python_version(self):
        self.assertEqual(utils.isPy2Env(), True)

    def test_shader(self):
        shaderMgr = OMR.MRenderer.getShaderManager()
        # dc = OMR.MRenderUtilities.acquireSwatchDrawContext()
        # shaderInstance = shaderMgr.getEffectsFileShader(os.path.join(utils.getShaderDirPath(),"EditableShadingMap.ogsfx"), "")
        # shaderInstance.bind(dc)
        # errorMsg = "EditableShadingMap10" + ":\n" + OMR.MShaderManager.getLastError() + OMR.MShaderManager.getLastErrorSource(TRUE,TRUE,2)
        # OM.MGlobal.displayError(errorMsg)
        # shaderInstance.unbind(dc)

    def test_fragment(self):
        fragmentMgr = OMR.MRenderer.getFragmentManager()
        fragmentMgr.addFragmentPath(utils.getFragmentDirPath())
        # if fragmentMgr.hasFragment("ETS_ShadingMapFragment"):
        #     fragmentMgr.removeFragment("ETS_ShadingMapFragment")
        # if fragmentMgr.hasFragment("ETS_ToonFragment"):
        #     fragmentMgr.removeFragment("ETS_ShadingMapFragment")
        # if fragmentMgr.hasFragment("ETS_ShaderSurface"):
        #     fragmentMgr.removeFragment("ETS_ShaderSurface")
        # fragmentMgr.addShadeFragmentFromFile("ETS_ShadingMapFragment.xml", False)
        # fragmentMgr.addShadeFragmentFromFile("ETS_ToonFragment.xml", False)
        fragmentMgr.addFragmentGraphFromFile("ETS_ShaderSurface.xml") 

    def test_fragmentGenerator(self):
        # frag = fragments.getShaderSurfaceFragment(3)
        # print(frag)
        pass


if __name__ == '__main__':
    maya.standalone.initialize(name='python')
    unittest.main()
    maya.standalone.uninitialize()