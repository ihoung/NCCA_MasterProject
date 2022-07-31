import maya.cmds as cmds
import locator
import utils

class ShadingLocatorPair(object):
    def __init__(self, parent):
        self.locator = cmds.createNode('shadingLocatorNode')
        self.pivot = cmds.createNode('shadingLocatorNode')

        centrePos = cmds.objectCenter(parent, gl=1)
        cmds.move(centrePos[0], centrePos[1], centrePos[2], self.pivot, a=1)
        pivotTrans = cmds.listRelatives(self.pivot, p=1, f=1, typ='transform')[0]
        self.pivotTrans = cmds.rename(pivotTrans, 'shadingPivot#')
        cmds.parentConstraint(parent, self.pivotTrans, mo=1)

        viewPos = utils.getMeshNearbyPosInView(parent, 0.5, 0.5)
        cmds.move(viewPos[0], viewPos[1], viewPos[2], self.locator, a=1)
        locTrans = cmds.listRelatives(self.locator, p=1, f=1, typ='transform')[0]
        self.locTrans = cmds.rename(locTrans, 'shadingEdit#')
        cmds.parentConstraint(parent, self.locTrans, mo=1)


class EditManager(object):
    editData = dict()

    @classmethod
    def createEdit(cls, parent):
        locatorPair = ShadingLocatorPair(parent)
        if parent in cls.editData:
            cls.editData[parent].append(locatorPair)
        else:
            cls.editData[parent] = [locatorPair]
        return locatorPair

    @classmethod
    def getEditPivot(cls, editLocator):
        pMesh = cmds.parentConstraint(editLocator, q=1, tl=1)[0]
        for pair in cls.editData[pMesh]:
            if pair.locTrans == editLocator:
                return pair.pivotTrans
        