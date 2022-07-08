import sys
import os


def getImgPath(imgName):
    icon_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons')
    return os.path.join(icon_dir, imgName+'.png')