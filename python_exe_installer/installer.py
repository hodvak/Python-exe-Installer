import time

import PyInstaller.__main__
import os
from zipfile import ZipFile


def create_exe(
        main_file_path: str,
        project_name: str,
        all_files_needed_path: str = None,
        venv_path: str = None,
        windowed: bool = False
):
    if not os.path.isdir(os.getcwd() + '\\py_exe_install'):
        os.mkdir(os.getcwd() + '\\py_exe_install')
    if os.path.isdir(os.getcwd() + '\\py_exe_install\\' + project_name):
        print('this folder exist :(' + os.path.abspath(os.getcwd() + '\\py_exe_install\\' + project_name))
        exit(-1)
    project_dir = os.getcwd() + '\\py_exe_install\\' + project_name

    __create_main_exe(
        project_name,
        main_file_path,
        project_dir,
        all_files_needed_path,
        venv_path,
        windowed
    )
    __zip_file(project_dir + '\\' + project_name, project_name, project_dir)
    __create_installer_file(project_dir, project_name)


def __zip_file(file_dir: str, new_file_name: str, new_file_dir: str):
    """
    zip the folder to zip file
    :param file_dir: where the folder needed to zip is.
    :param new_file_name:new name for the zip file
    :param new_file_dir: were to put the zip file
    :return: None
    """
    print(new_file_dir + '\\' + new_file_name + '.zip')
    with ZipFile(new_file_dir + '\\' + new_file_name + '.zip', 'w') as zip:
        for folder_name, sub_folders, filenames in os.walk(file_dir):

            for filename in filenames:
                # create complete file path of file in directory
                file_path = os.path.join(folder_name, filename)
                # Add file to zip
                zip.write(file_path, file_dir.split('\\')[-1] + '\\' + '\\'.join(file_path.split(file_dir + '\\')[1:]))
    zip.close()


def __create_main_exe(project_name: str,
                      main_file_path: str,
                      output_path: str,
                      all_files_needed_path: str = None,
                      venv_path: str = None,
                      windowed: bool = False) -> None:
    """
    create folder with exe for python project
    :param project_name: project name
    :param main_file_path: main file for exe file to run
    :param output_path: were to put this file
    :param all_files_needed_path: add all file in this dir to the project
    :param venv_path: the venv path
    :param windowed: is the program need console
    :return: None
    """

    main_file_path = os.path.abspath(main_file_path)

    if all_files_needed_path is None:
        all_files_needed_path = os.path.dirname(main_file_path)

    if venv_path is None:
        venv_path = os.path.dirname(main_file_path)
        while not os.path.exists(venv_path + '\\venv') and venv_path != '':
            venv_path = os.path.dirname(venv_path)
        if not os.path.exists(venv_path + '\\venv'):
            print('need venv path')
            exit(-1)
        venv_path = venv_path + '\\venv'

    pyinstaller_data = ['--name=' + project_name]

    if windowed:
        pyinstaller_data.append('-w')

    pyinstaller_data.append('--distpath=' + output_path)

    for filename in os.listdir(all_files_needed_path):
        file_path = os.path.join(all_files_needed_path, filename)
        if os.path.isdir(file_path):
            # not included some folders
            if not filename.startswith('.') and \
                    filename != 'venv' and \
                    filename != '__pycache__' and \
                    filename != 'build' and \
                    filename != 'dist':
                pyinstaller_data.append('--add-data=' + file_path + ';' + str(file_path.split("\\")[-1]) + '/')
                pass
        else:
            # not included some files (as main file and .spec files)
            if filename != main_file_path and not filename.endswith(".spec"):
                pyinstaller_data.append('--add-data=' + file_path + ';.')
                pass

    pyinstaller_data.append('--paths=' + venv_path + '\\Lib\\site-packages')
    pyinstaller_data.append('--add-data=' + venv_path + '\\Lib\\site-packages;./')
    pyinstaller_data.append(main_file_path)
    PyInstaller.__main__.run(pyinstaller_data)


def __create_installer_file(path, project_name):
    with open(path + '\\' + project_name + '.py', 'w+') as new_file:
        with open(os.path.dirname(os.path.abspath(__file__)) + '\\src\\install.py', 'r+') as old_file:
            for line in old_file:
                if line == '        dirname = \'new project\'\n':
                    line = '        dirname = \'' + project_name + '\'\n'
                new_file.write(line)
