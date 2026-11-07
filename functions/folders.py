import os
import shutil
from functools import wraps
import sys


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("File not Found!")
        except FileExistsError:
            print("File already exists!")
        except NotADirectoryError:
            print("This is not a directory!")
        except OSError as error:
            print(f"Operation failed: {error}")

        return False

    return wrapper


@handle_exceptions
def create_folder(name="New Folder"):
    os.mkdir(name)
    return True


@handle_exceptions
def del_folder(name=""):
    os.rmdir(name)
    return True

@handle_exceptions
def ren_folder(old_name="", new_name="Recently-Renamed Folder"):
    os.rename(old_name, new_name)
    return True

@handle_exceptions
def move(old_path="", new_path=""):
    shutil.move(old_path, new_path)
    return True

@handle_exceptions
def copy(old_path="", new_path=""):
    shutil.copy(old_path, new_path)
    return True

@handle_exceptions
def list_contents(folder=""):
    return os.listdir(folder)

if __name__ == "__main__":
    continue_confirm = input("You have entered debugging for functions. Would you like to continue?")

    match continue_confirm.lower():
        case "y":
            # Moving and Copying
            create_folder("Second Folder")
            print("Created Second Folder!")

            # Copy the folder into the renamed folder
            copy(
                "Second Folder",
                "Recently-Renamed Folder/Second Folder"
            )
            print("Copied folder!")

            # Move the original folder into the renamed folder
            move(
                "Second Folder",
                "Recently-Renamed Folder/Second Folder-Moved"
            )
            print("Moved folder!")

            print(list_contents("Second Folder"))
            print("Successfully listed contents!")

            # Deleting Folder
            del_folder(
                "Recently-Renamed Folder/Second Folder"
            )
            del_folder(
                "Recently-Renamed Folder/Second Folder-Moved"
            )
            del_folder("Recently-Renamed Folder")
            print("Cleanup complete!")
        case "n":
            print("Bye!")
            sys.exit()
