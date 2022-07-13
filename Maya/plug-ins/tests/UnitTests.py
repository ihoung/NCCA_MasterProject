import maya.standalone
import unittest
import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as OM
import os
import sys

sys.path.append(os.path.dirname(__file__) + r'/../src')
import utils


class TestMayaScene(unittest.TestCase):
    def setUp(self):
        print("Set up tests for maya scene.")

    def test_maya_python_version(self):
        self.assertEqual(utils.isPy2Env(), True)
    

if __name__ == '__main__':
    maya.standalone.initialize(name='python')
    unittest.main()
    maya.standalone.uninitialize()