from zipfile import ZipFile
import ctypes
import sys
import os
from win32com.client import Dispatch
from os.path import expanduser
from progress.bar import Bar


def main():
    try:
        home = expanduser("~").split('\\')[0] + '\\python programs'
        bar = Bar('Installing', max=20)

        path = os.path.dirname(__file__)
        bar.next(4)
        if getattr(sys, 'frozen', False):
            path = sys._MEIPASS
        dirname = 'new project'
        new_path = home + '\\' + dirname
        bar.next(5)
        if os.path.exists(new_path):
            print(f'this dir already exist({new_path})')
            exit(-1)
        os.makedirs(new_path)
        with ZipFile(path + '\\' + dirname + '.zip', 'r') as zipObj:
            zipObj.extractall(home)
        bar.next(10)
        create_shortcut(dirname, new_path)

    except Exception as e:
        print(e)
        exit()


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
    if is_admin() or True:
        # print("admin")
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
