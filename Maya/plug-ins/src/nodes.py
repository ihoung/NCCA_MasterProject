import maya.api.OpenMaya as OM
import maya.api.OpenMayaUI as OMUI

import utils

class EditableShadingNode(OMUI.MPxLocatorNode):
    id = OM.MTypeId(0x00070001)

    @staticmethod
    def creator():
        return EditableShadingNode()

    @staticmethod
    def initialize():
        pass
    
    def __init__(self):
        OMUI.MPxLocatorNode.__init__(self)

    def compute(self, plug, data):
        OMUI.MPxLocatorNode.compute(self, plug, data)

    def draw(self, view, path, style, status):
        import maya.OpenMayaRender as v1omr      
        glRenderer = v1omr.MHardwareRenderer.theRenderer()
        glFT = glRenderer.glFunctionTable()
        view.beginGL()
        
        glFT.glBegin(v1omr.MGL_LINES)
        glFT.glVertex3f(0.0, -0.5, 0.0)
        glFT.glVertex3f(0.0, 0.5, 0.0)
        glFT.glEnd()
 
        view.endGL()