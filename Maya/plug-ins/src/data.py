import maya.cmds as cmds
import locator
import utils

class ShadingLocatorPair(object):
    def __init__(self, parent):
        self.locator = cmds.createNode('shadingLocatorNode', name='shadingEdit')
        self.pivot = cmds.createNode('shadingLocatorNode', name='shadingPivot')

        viewPos = utils.viewPos(0.5, 0.5)
        cmds.move(viewPos[0], viewPos[1], viewPos[2], self.locator, a=1)
        centrePos = cmds.objectCenter(parent, gl=1)
        cmds.move(centrePos[0], centrePos[1], centrePos[2], self.pivot, a=1)


class EditManager(object):
    editData = dict()

    @classmethod
    def createEdit(cls, parent):
        locatorPair = ShadingLocatorPair(parent)
        if parent in cls.editData:
            cls.editData[parent].append(locatorPair)
        else:
            cls.editData.pop(parent, [locatorPair])
        