from zipfile import ZipFile
import ctypes
import sys
import os
from win32com.client import Dispatch


def main():
    try:
        path = os.path.dirname(__file__)
        if getattr(sys, 'frozen', False):
            path = sys._MEIPASS
        dirname = 'new project'
        path = os.environ.get("PROGRAMFILES") + '\\' + dirname
        if os.path.exists(path):
            print('this dir already exist')
            input()
            exit(-1)
        os.makedirs(path)
        with ZipFile(path + '\\' + dirname + '.zip', 'r') as zipObj:
            zipObj.extractall(os.environ.get("PROGRAMFILES"))
        create_shortcut(dirname, path)

    except Exception as e:
        print(e)
    input()


def create_shortcut(name, path):
    new_path = os.environ['USERPROFILE'] + "\\Desktop\\" + name + ".lnk"
    print(new_path)
    target = path + "\\" + name + ".exe"
    wDir = path
    icon = path + "\\" + name + ".exe"
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(new_path)
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.IconLocation = icon
    shortcut.save()


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    if is_admin():
        print("admin")
        main()
    else:
        print("no admin")
        ctypes.windll.shell32.ShellExecuteW(
            None,
            "runas",
            sys.executable,
            ' '.join('"' + arg + '"' for arg in sys.argv),
            None,
            1
        )
