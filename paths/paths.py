import os

THIS_DIR = os.path.abspath(os.path.dirname(__file__))


def project_root():
    """Return the path to the project root

    This should be the only function that needs to be edited on a per-project
    basis, depending on where this file is placed within your dir structure.
    """
    return os.path.abspath(os.path.join(THIS_DIR, "..", ".."))


def env():
    """Return the path to a programs environment, similar to a CWD"""
    return os.path.join(project_root(), ".env")


def settings_path():
    """Return path to a JSONSettings file, if using that library"""
    return os.path.join(env(), "settings.json")


def webif_static():
    return os.path.join(project_root(), "src", "webif", "static")


def project_tmp():
    return os.path.join(env(), "tmp")


def init_dirs(path):
    """Helper function to make the directories in `path` if they don't exist

    Path should only consist of directories, to avoid making a directory with
    a filename extension, but we will put in place checks against this.
    """
    if not os.path.exists(path):  # path doesn't exist, safe to proceed

        # make sure the path doesn't look file-like
        if ("." in os.path.split(path)[-1]) and (not path.startswith(".")):
            dirs, filename = os.path.split(path)
            if not os.path.exists(dirs):
                os.makedirs(dirs)
        else:
            os.makedirs(path)
