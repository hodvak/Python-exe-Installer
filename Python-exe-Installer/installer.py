import PyInstaller.__main__
import os


def create_exe(main_path, project_name=None, files_path=None, project_path=None,new_files_folder=None , window=False):
    """
    create exe folder with PyInstaller
    :param main_path: main file path
    :param project_name: name of the project and the exe file
    :param files_path: all files to include in the exe path
    :param project_path: path to the project path(where 'venv' folder is)
    :param new_files_folder: where the new files will be
    :param windows: hide console mode
    :return: None
    """
    # add files_path if not exists
    if files_path is None:
        if '\\' in main_path:
            files_path = '\\'.join(main_path.split('\\')[:-1])
        else:
            files_path = os.getcwd()
            main = files_path + '\\' + main_path

    # add project_path if not exists
    if project_path is None:
        project_path = files_path
        print(project_path)

        while not os.path.exists(project_path + '\\venv') and project_path is not '':
            project_path = "\\".join(project_path.split('\\')[:-1])

        if project_path is '':
            print('no project directory was founded')
            exit(-1)
    # add project_name if not exists
    if project_name is None:
        project_name = main_path.split('\\')[-1].split('.')[0]

    # pyinstaller parameters, first one is the project name
    pyinstaller_data = ['--name=' + project_name]

    # add window parameter if needed
    if window:
        pyinstaller_data.append('-w')

    # add all files from files_path
    for filename in os.listdir(files_path):
        file_path = os.path.join(files_path, filename)
        if os.path.isdir(file_path):
            # not included some folders
            if not filename.startswith('.') and \
                    filename != 'venv' and \
                    filename != '__pycache__' and \
                    filename != 'build' and \
                    filename != 'dist':
                pyinstaller_data.append('--add-data=' + file_path + ';' + file_path.split("\\")[-1] + '/')
                pass
        else:
            # not included some files
            if main_path != filename and not filename.endswith(".spec"):
                pyinstaller_data.append('--add-data=' + file_path + ';.')
                pass
    # add all packages from the venv folder
    pyinstaller_data.append('--paths=' + project_path + '\\venv\\Lib\\site-packages')
    pyinstaller_data.append('--add-data=' + project_path + '\\venv\\Lib\\site-packages;./')

    # set the folder of the new files to the new_files_folder
    if new_files_folder is not None:
        pyinstaller_data.append('--distpath='+new_files_folder)

    # add the file that will run
    pyinstaller_data.append(main_path)

    # create the exe folder with pyinstaller
    PyInstaller.__main__.run(pyinstaller_data)
