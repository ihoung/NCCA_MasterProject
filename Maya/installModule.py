#!/usr/bin/env python
import os
import pathlib
import platform
import sys
from pathlib import Path
import argparse

'''
The following codes are original from the class of Pipeline&TD, with some corrections and improvements.
'''

maya_locations = {
    "Linux": "/maya",
    "Darwin": "/Library/Preferences/Autodesk/maya",
    "Windows": "\\Documents\\maya",
}


def install_module(location):
    print(f"installing to {location}")
    # first write the module file
    modules_dir = location + "modules/"
    Path(modules_dir).mkdir(parents=True, exist_ok=True)
    current_dir = Path(__file__).resolve().parent
    if not Path(modules_dir + "EditableShadingTool.mod").is_file():
        print("writing module file")
        with open(location + "modules/EditableShadingTool.mod", "w") as file:
            file.write(f"+ EditableShadingTool 1.0 {current_dir}\n")
            file.write(f"MAYA_PLUG_IN_PATH +:= plug-ins\n")
            file.write(f"EDITABLE_SHADING_PLUGIN_ROOT={current_dir}\n\n")
    # if we are using Maya 2022 and above this will be ok
    # however if using 2020 and below we need to set Maya.env
    folders = os.listdir(location)
    for folder in folders:
        if folder.startswith("20") and int(folder) < 2022:
            with open(f"{location}/{folder}/Maya.env", "a+") as env_file:
                env_file.seek(0)
                if 'EDITABLE_SHADING_PLUGIN_ROOT' not in env_file.read():
                    env_file.write(f"EDITABLE_SHADING_PLUGIN_ROOT={current_dir}\n\n")


def check_maya_installed(dir_path):
    if dir_path:
        mloc = str(dir_path) + '/'
    else:
        op_sys = platform.system()
        mloc = f"{Path.home()}{maya_locations.get(op_sys)}/"
    
    if not os.path.isdir(mloc):
        raise OSError(f"<{mloc}> Path doesn't exist!")
    return mloc


if __name__ == "__main__":
    parse = argparse.ArgumentParser(description='Modify the parameters of the module installation.')
    parse.add_argument('--dirpath', '-d', nargs='?', type=Path, help='specific directory path of Maya')
    args = parse.parse_args()

    try:
        m_loc = check_maya_installed(args.dirpath)
    except OSError as e:
        print("Error can't find maya install")
        print("error = ", e)
        sys.exit(0)

    install_module(m_loc)
