import sys
import os


def isPy2Env():
    py_version = sys.version_info.major
    return py_version == 2

def getImgPath(imgName):
    icon_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons')
    return os.path.join(icon_dir, imgName+'.png')