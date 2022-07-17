import sys
import os


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