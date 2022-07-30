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

def viewPos(screenX, screenY):
    vx, vy, vw, vh = omui.M3dView().active3dView().viewport()
    viewPosX = int(vx + vw * screenX)
    viewPosY = int(vy + vh * screenY)
    pos = om.MPoint()
    dir = om.MVector()
    omui.M3dView().active3dView().viewToWorld(viewPosX, viewPosY, pos, dir)
    return pos