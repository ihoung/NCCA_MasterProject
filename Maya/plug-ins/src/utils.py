import sys
import os
import maya.api.OpenMaya as om
import maya.api.OpenMayaUI as omui
import maya.cmds as cmds


def isPy2Env():
    py_version = sys.version_info.major
    return py_version == 2

def getRootPath():
    return os.path.dirname(os.path.abspath(__file__))

def getImgPath(imgName):
    icon_dir = os.path.join(getRootPath(), 'icons')
    return os.path.join(icon_dir, imgName+'.png')

def getFragmentDirPath():
    return os.path.join(getRootPath(), 'fragments')

def getShaderDirPath():
    return os.path.join(getRootPath(), 'shaders')

def getMeshNearbyPosInView(mesh, screenX, screenY):
    vx, vy, vw, vh = omui.M3dView().active3dView().viewport()
    viewPosX = int(vx + vw * screenX)
    viewPosY = int(vy + vh * screenY)
    pos = om.MPoint()
    dir = om.MVector()
    omui.M3dView().active3dView().viewToWorld(viewPosX, viewPosY, pos, dir)
    selectionList = om.MSelectionList()
    selectionList.add(mesh)
    nodeDagPath = selectionList.getDagPath(0)
    mfnMesh = om.MFnMesh(nodeDagPath)
    closestP, fId = mfnMesh.getClosestPoint(pos, om.MSpace.kWorld)
    res = closestP + (pos - closestP) * 0.1
    return res