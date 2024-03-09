# DeathTrap Dungeon for Windows update program v1.0.0 - by Reuben Parfrey 2024
# This script is responsible for downloading and installing the latest DTD updates for the Windows version of DTD.

# Import the necessary libraries.
import os, platform, shutil, sys, itertools, time, threading, getpass
from urllib.request import urlretrieve

# Determine the user's operating system.
user_platform = platform.system()


# This class is used to display a visual indicator whilst the update is downloading, so the user knows that the
# program hasn't frozen. This code came from StackOverflow a long time ago, so I will update this and add the
# credits if I come across it again.
class Spinner:
    def __init__(self, message, delay=0.1):
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.delay = delay
        self.busy = False
        self.spinner_visible = False
        sys.stdout.write(message)

    def write_next(self):
        with self._screen_lock:
            if not self.spinner_visible:
                sys.stdout.write(next(self.spinner))
                self.spinner_visible = True
                sys.stdout.flush()

    def remove_spinner(self, cleanup=False):
        with self._screen_lock:
            if self.spinner_visible:
                sys.stdout.write('\b')
                self.spinner_visible = False
                if cleanup:
                    sys.stdout.write(' ')  # overwrite spinner with blank
                    sys.stdout.write('\r')  # move to next line
                sys.stdout.flush()

    def spinner_task(self):
        while self.busy:
            self.write_next()
            time.sleep(self.delay)
            self.remove_spinner()

    def __enter__(self):
        if sys.stdout.isatty():
            self._screen_lock = threading.Lock()
            self.busy = True
            self.thread = threading.Thread(target=self.spinner_task)
            self.thread.start()

    def __exit__(self, exception, value, tb):
        if sys.stdout.isatty():
            self.busy = False
            self.remove_spinner(cleanup=True)
        else:
            sys.stdout.write('\r')


def handle_error(message):  # A simple function to display error output, and to close the program gracefully.
    print("\nSorry for the inconvenience, but an error has occurred:\nERROR INFO: "+str(message))
    handle = input("\nIf you believe this to be a bug, please report it using the 'Report a Bug' feature in the 'Settings'\nmenu of the game.\n\nPress [ENTER] to close the program ")
    raise message


def download_update(download_path, url):
    with Spinner('Downloading update, please wait...'):
        try:
            download = urlretrieve(url, download_path)  # Download the latest executable file and save it alongside the previous version.
            user = getpass.getuser()
            print("Successfully downloaded update data!\nInstalling update...")
            shutil.copyfile(download_path, f'C:\\Users\\{user}\\AppData\\Local\\Programs\\DTDGame\\DTD.exe')    # Overwrite the previous version of the game with the newly downloaded one.
            print("\nThe update has successfully been downloaded and installed!")
            print("\nCleaning temporary files...")
            os.remove(download_path)    # Perform cleanup - delete the downloaded executable as it's not needed anymore.
            time.sleep(3)
            os.startfile(f'C:\\Users\\{user}\\AppData\\Local\\Programs\\DTDGame\\DTD.exe')  # Start the new copy of the game.
            sys.exit(0)
        except Exception as e:
            handle_error(e)


if __name__ == "__main__":
    print("\n== DeathTrap Dungeon for Windows update program v1.0.0 by Reuben Parfrey ==\n")
    time.sleep(1)
    if user_platform == "Windows":  # Perform a check to ensure that the updater is only running on Windows.
        user = getpass.getuser()    # Get the username.
        download_path = f'C:\\Users\\{user}\\AppData\\Local\\Programs\\DTDGame\\DTD_latest.exe'     # Path that the latest DTD executable will be saved to.
        url = 'https://github.com/mlaude545/DeathTrap-Dungeon/raw/main/OTA%20Resources/DTD.exe'     # URL to the latest DTD executable.
        download_update(download_path, url)
    else:
        error_message = f"This program is only intended for Windows hosts, but you are using {str(user_platform)}."
        handle_error(error_message)
