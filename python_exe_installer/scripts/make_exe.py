from python_exe_installer import create_exe
import sys, getopt


def main(argv):
    console = True
    venv = None
    folder = None
    file_name = None
    project_name = None

    try:
        opts, args = getopt.getopt(argv, "cwf:v:n:", ['console', 'window', 'folder=', 'venv=', 'project_name='])
    except getopt.GetoptError:
        print('error')
        sys.exit(2)

    if len(args) is 0:
        print('enter file name')
        sys.exit(2)

    file_name = args[0]
    print(opts)

    for opt, data in opts:
        if opt in ['-c', '--console']:
            console = True
        elif opt in ['-w', '--window']:
            console = False
        elif opt in ['-f', '--folder']:
            folder = data
        elif opt in ['-v', '--venv']:
            venv = data
        elif opt in ['-n', '--project_name']:
            project_name = data

    print(console)
    print(venv)
    print(folder)
    print(file_name)
    create_exe(file_name, project_name, folder, venv, not console)


if __name__ == "__main__":
    main(sys.argv[1:])
