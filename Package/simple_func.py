import os

def __remove_folder(dir = ""):
    try:
        files = os.listdir(dir)
        for f in files:
            fPath = os.path.join(dir, f)
            if os.path.isfile(fPath):
                os.remove(fPath)
            if os.path.isdir(fPath):
                __remove_folder(fPath)
        os.rmdir(dir)
    except OSError as ose:
        print(f"Error occured at functions.py at line {e}")
    except Exception as e:
        print(f"Error occured at functions.py at line {e}")

def create_folder(dir = ""):
    __remove_folder(dir)
    os.mkdir(dir)