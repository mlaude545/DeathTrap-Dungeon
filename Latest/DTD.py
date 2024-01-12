#!/usr/bin/python3

import random
import pickle
import os.path
import subprocess
import webbrowser
from concurrent.futures import thread
from urllib.request import urlretrieve
import getpass
import platform
import io
from datetime import datetime
import threading
import itertools
import sys
import time
import multiprocessing
import socket
from pathlib import Path
import os
import logging


currentVer=b"2.9.5" # Version of this release of DTD. Modify this, along with HTML, for every new release

savePoint = 0
savePointCopy=0
gotstring = 0
debug = 0
gotRope = 0
area = 0
quitToTitle=0
guardDamage=3
playerHealth=20
playerMaxHealth=20
gotShield=0
item=0
muteAudio=False
mute=0
damage=5
gotKey = False
foundDoor = False
createProfile = False
noModuleSound=False
noPyGame=False
saveWarning=False
musicLoop=False
musicStop=False
playBattleTheme=False
died=False
noPyGameModule=False
smokescreen=False
importSimpleaudio=False
usedSmoke=False
healingPotion=False
searchedChest2=False
usedHealing=False
highRank=False
hyperPotion=False
discoveredPadlock=False
compatibility=False
devProfile=False
continueLoad=False
errorImporting=False
noPsutil=False
audioMuted=False
developerProfile=False
defeatedGuardOutsideConfinement=False
customResSet=False
originalGuardHealth=0
usedHyperPotion=0
originalDamage=0
originalHealth=0
skipUpdateCheck=False
firstSaveRequest=True
originalSavePoint=0
save3Corrupt=False
save2Corrupt=False
save1Corrupt=False
createSlot1=False
createSlot2=False
createSlot3=False
convertSlotOne=False
convertSlotTwo=False
convertSlotThree=False
activateDebug=False
loadDevmenu=False
searchedChest5=False
smokescreenQuantity=0
hyperpotionQuantity=0
healingpotionQuantity=0
giveSmokescreen=False
testHP=False
smallerDisplay=False
courtyardGuardKilled=False
courtyardKey=False
foundCourtyardDoor=False
leverPulled=False
leftDialCorrect=False
rightDialCorrect=False
dialogCount=0
puzzleComplete=False
lockout=False
leftDialPos=str("down, towards you.")
rightDialPos=str("upwards, towards the door.")
e=""
installationFuckedUp=False
currentOS=""
discoveredChapterSevenDoor=False
defeatedChapterSevenGuard=False
pickedUpKey=False
searchedChest7=False
searchedChest7mk2=False
searchedChest8=False
juniperDamage=0
juniperHealth=0
engagedJuniperFight=False
creditsRolled=False
gameBeat=False
sfxMissing=False
disableLogging=False
checkForUpdatesThroughOptions=False
loadMenu=False

try:os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
except Exception:
    pass

currentOS=platform.platform()

logging.basicConfig(filename='crash.log', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s')

try:
    with open('logsettings.dat', 'rb') as f:
        disableLogging=pickle.load(f)
except FileNotFoundError:
    disableLogging=False
    pass
except EOFError:
    disableLogging=False
    pass
except Exception:
    disableLogging=False
    pass
#print(disableLogging)
if disableLogging == [True]:
    disableLogging=True
elif disableLogging == [False]:
    disableLogging=False
#print(disableLogging)

os.system('mode con: cols=180 lines=65')

try:
    with open('displaysettings.dat', 'rb') as f:
        smallerDisplay=pickle.load(f)
except FileNotFoundError:
    smallerDisplay=False
    pass
except EOFError:
    smallerDisplay=False
    pass
except Exception:
    smallerDisplay=False
    pass

if smallerDisplay == True:
    os.system('mode con: cols=145 lines=50')
    print("\n== The game is running in a lowered resolution in order to better fit smaller displays. ==\n")
elif smallerDisplay == [True]:
    os.system('mode con: cols=145 lines=50')
    print("\n== The game is running in a lowered resolution in order to better fit smaller displays. ==\n")

try:
    import ssl
except Exception:
    skipUpdateCheck=True
    pass

try:
    import urllib.request
except Exception:
    skipUpdateCheck=True
    pass


try:import pygame
except ImportError:
    noPyGameModule=True
    errorImporting=True


class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False



def installationFailure():
    choice=0
    global e, muteAudio, noPyGameModule, noModuleSound, noPyGame, installationFuckedUp, disableLogging
    if not disableLogging:
        logging.exception("Exception occurred")
    print("\nAn error occurred and installation cannot continue. Choose an option from the list below:")
    try:choice=int(input("1] Retry\n2] Get help online/report a bug\n3] See detailed error info (Advanced)\n4] Cancel\n-->"))
    except Exception:
        installationFailure()
    if choice==1:
        install('pygame')
    elif choice==2:
        webbrowser.open("https://reubenparfrey.wixsite.com/deathtrapdungeon/tutorials")
        installationFailure()
    elif choice==3:
        print(e)
        installationFailure()
    elif choice==4:
        muteAudio=True
        noPyGameModule=True
        noModuleSound=True
        noPyGame=True
        time.sleep(0.7)
        try:choice=int(input("\nAre you sure? Any features that utilise this module will be disabled.\n1] Yes\n2] No\n--> "))
        except ValueError:
            installationFailure()
        if choice==1:
            print("\n== Audio has been muted ==")
            installationFuckedUp=True
            install('pygame')
        elif choice==2:
            installationFailure()
        else:
            print("\nMISSING MODULE(S):\n-Pygame:")
            print("This module handles the game's audio. Without it, audio will be permanently muted.\n")
            time.sleep(0.8)
            installationFailure()

def install(pygame):
    selection=0
    global importSimpleaudio, e, installationFuckedUp, noPyGameModule, muteAudio
    if installationFuckedUp==False:
        print("\nPreparing to install...")
        time.sleep(1.2)
        try:subprocess.check_call([sys.executable, "-m", "pip", "install", pygame])
        except Exception as e:
            installationFailure()
        if importSimpleaudio==True and installationFuckedUp==False:
            importSimpleaudio=False
            print("\nSuccessfully installed missing module 1 of 2 (Pygame)\n")
            time.sleep(2.2)
            print("Attempting to install missing module 2 of 2 (simpleaudio)...")
            install('simpleaudio')
        else:
            if installationFuckedUp==False:
                print("\nSuccessfully installed missing module(s)! The game must be restarted for these changes to take effect. Choose an option to continue:")
                try:selection=int(input("1] Close the game now\n2] Continue with module dependant features disabled\n--> "))
                except ValueError:
                    print("\n= Audio has been muted =")
                    time.sleep(0.8)
                    installationFuckedUp = True
                    muteAudio = True
                    noPyGameModule = True
                    install('pygame')
                if selection==1:
                    sys.exit(0)
                else:
                    print("\n== Audio has been muted ==")
                    time.sleep(0.8)
                    installationFuckedUp=True
                    muteAudio=True
                    noPyGameModule=True
                    install('pygame')
            else:
                pass
    elif installationFuckedUp==True:
        pass


def importChoice(): #This is only called when the user selects 'more info' below.
    global noModuleSound, noPyGameModule, muteAudio, noPyGame
    choice=0
    try:choice=int(input("\nChoose an option to continue:\n1] Continue without installing modules\n2] Install missing modules\n3] More info\n--> "))
    except ValueError:
        importChoice()
    if choice==2 and noModuleSound == True and noPyGameModule==True:
        #importSimpleaudio=True
        install('pygame')
    elif choice==1 and noPyGameModule==True:
        noPyGame=True
        noModuleSound=True
        muteAudio=True
        print("\n== Audio has been muted ==")
    elif choice==2 and noPyGameModule==True:
        install('pygame')
    elif choice==3:
        print("\nCurrently missing modules:\n-Pygame: This module handles the game's audio. Without it, all audio will be permanently muted.\n")
        time.sleep(0.3)
        importChoice()

if errorImporting==True:
    choice=0
    print("\n== UNABLE TO IMPORT MODULE(S) ==")
    print("The following module(s) could not be imported:")
    if noPyGameModule==True:
        print("-Pygame")
    if noPsutil==True:
        print("-Psutil")
    print("\nThis usually happens when the specified modules haven't been installed on your computer. The game will still work without these modules, \nhowever it's recommended you install them as features that utilise these modules will be disabled without them.\n")
    time.sleep(0.36)
    try:
        choice=int(input("You can either continue without installing the missing modules, or install the modules now (this process should only take a moment depending \non your internet speed.) For detailed info about which features will be disabled if the module(s) aren't installed, select 'More info'.\n\nChoose an option to continue:\n1] Continue without installing modules\n2] Install missing modules\n3] More info\n--> "))
    except ValueError:
        importChoice()
    if choice==2 and noModuleSound == True and noPyGameModule==True:
        install('pygame')
    elif choice==1 and noPyGameModule==True:
        noPyGame=True
        noModuleSound=True
        muteAudio=True
        print("\n== Audio has been muted ==")
    elif choice==2 and noPyGameModule==True:
        install('pygame')
    elif choice==3:
        print("\nCurrently missing modules:\n-Pygame: This module handles the game's audio. Without it, all audio will be permanently muted.\n")
        time.sleep(0.3)
        importChoice()
    else:
        importChoice()



try:
    with open('updateprefs.dat', 'rb') as f:
        skipUpdateCheck=pickle.load(f)
except Exception:
    skipUpdateCheck=False
    with open ('updateprefs.dat', 'wb') as f:
        pickle.dump([skipUpdateCheck],f,protocol=2)


def releaseNoteFailure():
    choice=0
    time.sleep(0.7)
    print("\nAn error occurred, and the data could not be downloaded. Choose an option to continue:\n1] Retry\n2] View release notes online\n3] See detailed error info (advanced)\n4] Get help online/report a bug\n5] Cancel")
    try: choice=int(input("--> "))
    except ValueError:
        releaseNoteFailure()
    if choice==1:
        downloadReleaseNotes()
    elif choice==2:
        webbrowser.open("https://sourceforge.net/projects/deathtrapdungeon/files/Latest/readme.txt/download")
        releaseNoteFailure()
    elif choice==3:
        print(e)
        releaseNoteFailure()
    elif choice==4:
        webbrowser.open("https://reubenparfrey.wixsite.com/deathtrapdungeon/tutorials/")
        releaseNoteFailure()
    else:
        menu()

def downloadFailure():
    choice=0
    time.sleep(0.7)
    print("\nAn error occurred, and the update data could not be downloaded. Choose an option to continue:\n1] Retry\n2] Download the new version manually\n3] See detailed error info (advanced)\n4] Get help online/report a bug\n5] Cancel")
    try: choice=int(input("--> "))
    except ValueError:
        downloadFailure()
    if choice==1:
        downloadUpdate()
    elif choice==2:
        webbrowser.open("https://reubenparfrey.wixsite.com/deathtrapdungeon/downloads/")
        downloadFailure()
    elif choice==3:
        print(e)
        downloadFailure()
    elif choice==4:
        webbrowser.open("https://reubenparfrey.wixsite.com/deathtrapdungeon/tutorials/")
        downloadFailure()
    else:
        menu()

def downloadReleaseNotes():
    global currentOS, e, debug, checkForUpdatesThroughOptions
    url='https://sourceforge.net/projects/deathtrapdungeon/files/Latest/readme.txt/download'
    filename="readme.txt"
    print("Working...")
    currentOS=platform.system()
    if currentOS=="Windows":
        usrname = getpass.getuser()
        destination = f'C:\\Users\\{usrname}\\Downloads\\changelog.txt'
        try:download = urlretrieve(url, destination)
        except Exception as e:
            releaseNoteFailure()
        try:f = open(destination, "r", encoding="utf8")
        except Exception as e:
            releaseNoteFailure()
        try:print(f.read())
        except Exception as e:
            releaseNoteFailure()
        if checkForUpdatesThroughOptions is True:
            checkForUpdatesThroughOptions=False
            newVerAvailableOptions()
        else:
            newVerAvailable()
    else:
        downloads_path = str(Path.home() / "Downloads/readme.txt")
        try:download = urlretrieve(url, downloads_path)
        except Exception as e:
            releaseNoteFailure()
        textfile_path=str(Path.home() / "Downloads/readme.txt")
        if debug!=0:
            print(textfile_path)
        try:f = open(textfile_path, "r", encoding="utf8")
        except Exception:
            releaseNoteFailure()
        try:print(f.read())
        except Exception as e:
            releaseNoteFailure()
        newVerAvailable()

def downloadUpdate():
    global currentOS, e, debug
    currentOS = platform.system()
    if currentOS == "Windows":
        if debug!=0:
            print("\nDetected OS: Windows")
        originalurl = "https://sourceforge.net/projects/deathtrapdungeon/files/Latest/DTDSetup.exe/download"
        url="https://downloads.sourceforge.net/project/deathtrapdungeon/Latest/DTDSetup.exe?ts=gAAAAABh50KlBwxpcpnFuAtCOGLY_hBpFH6FmAK4CDLxt30skBPn5GAtxzKktFNjgM7WkZBEAr-hLbKCKNRyfIQ_Av8lCf2rGw%3D%3D&amp;use_mirror=master&amp;r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fdeathtrapdungeon%2Ffiles%2FLatest%2F"
        print("Downloading data, please wait... (This could take up to 5 minutes depending on your internet connection/hardware.)")
        filename = "DTDSetup.exe"
        usrname = getpass.getuser()
        destination = f'C:\\Users\\{usrname}\\Downloads\\DTDSetup.exe'
        with Spinner():
            try:download = urlretrieve(url, destination)
            except Exception as e:
                downloadFailure()
            with urllib.request.urlopen(url) as Response:
                Length = Response.getheader('content-length')
                BlockSize = 1000000  # default value

                if Length:
                    Length = int(Length)
                    BlockSize = max(4096, Length // 20)
            if debug!=0:
                print("UrlLib len, blocksize: ", Length, BlockSize)
                print("\nSuccess! Downloading data...\n")

            BufferAll = io.BytesIO()
            Size = 0
            while True:
                BufferNow = Response.read(BlockSize)
                if not BufferNow:
                    break
                BufferAll.write(BufferNow)
                Size += len(BufferNow)
                if Length:
                    Percent = int((Size / Length) * 100)
                    print(f"Download progress: {Percent}%")
        if debug!=0:
            print("Buffer All len:", len(BufferAll.getvalue()))
        print("\nSuccessfully downloaded update data! The game cannot be updated whilst it is running, so it will close shortly.\n")
        time.sleep(2)
        try:
            os.startfile(destination)
        except Exception as e:
            downloadFailure()
        time.sleep(4)
        sys.exit(0)
    else:
        if debug!=0:
            print("\nDetected OS: Linux/MacOS")
        url="https://sourceforge.net/projects/deathtrapdungeon/files/Latest/Source%20Code/DTD.py/download"
        print("Receiving data, please wait... (This could take up to 5 minutes depending on your internet connection/hardware.)")
        filename = "DTD.py"
        downloads_path = str(Path.home() / "Downloads/DTD.py")
        try:download = urlretrieve(url, downloads_path)
        except Exception as e:
            updateFailure()
        with urllib.request.urlopen(url) as Response:
            Length = Response.getheader('content-length')
            BlockSize = 1000000  # default value

            if Length:
                Length = int(Length)
                BlockSize = max(4096, Length // 20)

            if debug!=0:
                print("UrlLib len, blocksize: ", Length, BlockSize)
            print("Downloading data...\n")

            BufferAll = io.BytesIO()
            Size = 0
            while True:
                BufferNow = Response.read(BlockSize)
                if not BufferNow:
                    break
                BufferAll.write(BufferNow)
                Size += len(BufferNow)
                if Length:
                    Percent = int((Size / Length) * 100)
                    print(f"Download progress: {Percent}%")

        if debug !=0:
            print("Buffer All len:", len(BufferAll.getvalue()))
        print("\nThe latest release of DeathTrap Dungeon has been saved to: "+downloads_path+"\n")
        time.sleep(0.6)
        menu()

def newVerAvailable():
    global loadMenu
    choice=0
    print("\nA new version of DeathTrap Dungeon is available! Please choose from one of the following options:\n1] Download the new version\n2] View the release notes\n3] Cancel\n4] Don't ask again")
    try:choice=int(input("--> "))
    except ValueError:
        newVerAvailable()
    if choice==1:
        downloadUpdate()
    elif choice==2:
        downloadReleaseNotes()
    elif choice==3:
        loadMenu=True
        pass
    elif choice==4:
        print("\nGot it, you'll no longer see this message upon starting the game. You can check for new versions manually, or re-enable automatic updates, by\nselecting 'Options' on the main menu, then selecting 'Update settings'.")
        skipUpdateCheck=True
        with open('updateprefs.dat', 'wb') as f:
            pickle.dump([skipUpdateCheck], f, protocol=2)
        pass

def checkForUpdates():
    global currentVer
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "http://www.dtdlatestversion.xp3.biz"
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    # print(response.read())
    contents = response.read()
    if debug!=0:
        print(contents)
    shortCont = contents.split(b'<p>')[1].lstrip().split(b'</p>')[0]
    if debug!=0:
        print(shortCont)
    if shortCont == currentVer:
        pass
    elif shortCont > currentVer:
        newVerAvailable()
    else:
        pass

def internet_on():
    global skipUpdateCheck
    try:
        socket.setdefaulttimeout(5)
        host = socket.gethostbyname("www.google.com")
        s = socket.create_connection((host, 80), 2)
        s.close()
        checkForUpdates()

    except Exception as e:
        #skipUpdateCheck=True
        pass

if skipUpdateCheck==True or skipUpdateCheck==[True]:
    pass
elif skipUpdateCheck==False or skipUpdateCheck==[False]:
    internet_on()

if muteAudio is True:
    muteAudio=True


if noPyGameModule != True:
    pygame.mixer.init()


#The following code checks to see if the 'sfx' folder exists. If not, an error message is displayed.
def sfxError():
    global muteAudio
    choice=0
    try:choice=int(input("\n== UNABLE TO ACCESS AUDIO DATA ==\nAn error occurred, and audio data could not be accessed. Choose an option to continue:\n1] Continue without loading audio data (Audio will be muted)\n2] More info\n3] Get help online/report a bug\n--> "))
    except ValueError:
        sfxError()
    if choice==1:
        print("\n== Audio has been muted ==")
        muteAudio = True
    elif choice==2:
        print("""
You are seeing this message due to the game not being able to successfully load audio data. This can happen for multiple reasons, but can
usually be fixed fairly easily. Here are some things you can try:

== SOURCE CODE VERSION ==
    -Extract all contents of the downloaded zip folder before running the game
    -Ensure the folder named 'sfx' is saved to the same directory as the game
    -Ensure permissions haven't been modified on the 'sfx' folder

== WINDOWS VERSION ==
    -Uninstall and then reinstall the game
    -Restart your computer
        
If none of the above steps worked for you, select "Get help online/report a bug".""")
        sfxError()
    elif choice==3:
        webbrowser.open('https://reubenparfrey.wixsite.com/deathtrapdungeon/tutorials')
        sfxError()
    else:
        sfxError()

if os.path.isdir('sfx'):
    pass
else:
    sfxMissing=True
    sfxError()

understand = 0

class Player:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 20
        self.health = self.maxhealth
        self.attack = damage
        self.location = savePoint

    def display(self, name):
        print("Name:", self.name, "\nHealth:", self.health, "/", self.maxhealth, "\nAttack Damage:", self.attack,
              "\nLocation:", self.location)

try:
    with open('startup.dat', 'rb') as f:
         activateDebug, loadDevmenu , giveSmokescreen=pickle.load(f)
except FileNotFoundError:
    pass
except EOFError or pickle.unPicklingError:
    print("\n== ERROR LOADING STARTUP DATA FILE ==\nThe file containing startup commands is corrupt. Any commands that were set to run at startup have not been executed, and will have to be registered again.")
    choice=int(input("\nChoose an option to continue:\n1] Load Developer Options menu\n2] Exit to main menu\n--> "))
    if choice==1:
        loadDevmenu=True
        os.remove('startup.dat')
        pass
    else:
        os.remove('startup.dat')
        pass
except ValueError:
    print("\n== ERROR LOADING STARTUP DATA FILE ==\nThe file containing startup commands is corrupt. Any commands that were set to run at startup have not been executed, and will have to be registered again.")
    choice=int(input("\nChoose an option to continue:\n1] Load Developer Options menu\n2] Exit to main menu\n--> "))
    if choice==1:
        loadDevmenu=True
        os.remove('startup.dat')
        pass
    else:
        os.remove('startup.dat')
        pass

if activateDebug == True or activateDebug == [True]:
    #debug=1
    print("\nTHE FOLLOWING COMMAND WAS SUCCESSFULLY EXECUTED: 'enabledebug=true'\n")
if loadDevmenu == True or activateDebug == [True]:
    print("\nTHE FOLLOWING COMMAND WAS SUCCESSFULLY EXECUTED: 'devoptions'\n")
if giveSmokescreen == True or giveSmokescreen == [True]:
    print("\nTHE FOLLOWING COMMAND WAS SUCCESSFULLY EXECUTED: 'grant smokescreen x2'\n")
    smokescreen=True
    smokescreenQuantity=2

print(" ")

def sendErrorReport():
    pass

def createErrorReport():
    global disableLogging
    print("Creating error report...")
    time.sleep(1.2)
    if disableLogging is True:
        print("Unable to create error report; error logging has been disabled.")
        menu()
    currentOS=platform.platform()
    logging.info("\nCurrentVer="+str(currentVer)+"\nsysInfo="+str(currentOS))
    sendErrorReport()

def errorReportNoInternet():
    print("You are not connected to the internet. Choose an option to continue:\n1] Retry\n2] Get help online/report a bug\n3] Cancel")

def errorReportInternetCheck():
    print("\nChecking your internet connection...")
    time.sleep(0.9)
    try:
        socket.setdefaulttimeout(5)
        host = socket.gethostbyname("www.google.com")
        s = socket.create_connection((host, 80), 2)
        s.close()
        createErrorReport()

    except Exception as e:
        errorReportNoInternet()

def recoveryFailure():
    choice=0
    confirm=0
    global save1Corrupt, save2Corrupt, save3Corrupt,e
    try:choice=int(input("\nAn error occurred, and the recovery process cannot continue. Please choose an option from the list below:\n1] Retry\n2] Get help online\n3] See detailed error info (Advanced)\n4] Cancel (Unrecoverable data will be erased)\n--> "))
    except ValueError:
        recoveryFailure()
    if choice==1:
        recoverBackup()
    elif choice==2:
        webbrowser.open('https://www.reubenparfrey.wixsite.com/deathtrapdungeon/tutorials/')
        recoveryFailure()
    elif choice==3:
        print(e)
        recoveryFailure()
    elif choice==4:
        try:confirm=int(input("\nThe corrupt save file will be erased. Proceed?\n1] Yes\n2] No\n--> "))
        except ValueError:
            recoveryFailure()
        if confirm==1 and save1Corrupt is True:
            os.remove('savedata.dat')
            print("\nSuccessfully erased corrupt data.\n")
            menu()
        elif confirm==1 and save2Corrupt is True:
            os.remove('savedata2.dat')
            print("\nSuccessfully erased corrupt data.\n")
            menu()
        elif confirm==1 and save3Corrupt is True:
            os.remove('savedata3.dat')
            print("\nSuccessfully erased corrupt data.\n")
            menu()
        else:
            recoveryFailure()


def overwriteSuccess():
    choice=0
    global savePoint, playerName, playerHealth, playerMaxHealth, gameBeat, smokescreen, hyperPotion, healingPotion
    time.sleep(0.5)
    savePoint = 0
    playerName = ""
    damage = 5
    playerHealth = 20
    playerMaxHealth = 20
    gameBeat = False
    smokescreen = False
    hyperPotion = False
    healingPotion = False
    try:choice=int(input("Save data has successfully been recovered!\n1] Load recovered data \n2] Return to menu\n--> "))
    except ValueError:
        overwriteSuccess()
    if choice==1:
        load()
    elif choice==2:
        print("\nReturning to menu...\n")
        time.sleep(1)
        menu()

def recoverBackup():
    global playerName, savePoint, damage, playerMaxHealth, playerHealth, healingPotion, smokescreen, area, devProfile, save3Corrupt, save2Corrupt, save1Corrupt, gameBeat, e
    sdbackupExists=False
    sdbackup2Exists = False
    sdbackup3Exists = False
    if os.path.exists('sdbackup,dat'):
        sdbackupExists=True
    if os.path.exists('sdbackup2.dat'):
        sdbackup2Exists=True
    if os.path.exists('sdbackup3.dat'):
        sdbackup3Exists=True

    print("Corrupted data could not be accessed. Loading backup data...")
    time.sleep(1.1)
    if save1Corrupt is True:
        try:
            with open('sdbackup.dat', 'rb') as f:
                playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat = pickle.load(
                    f)
        except Exception as e:
            recoveryFailure()
        print("\nBackup data loaded successfully!\n")
        time.sleep(0.4)
        print("Overwriting corrupted save data...\n")
        with open('savedata.dat', 'wb') as f:
            pickle.dump([playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat], f,
                        protocol=2)
        overwriteSuccess()
    elif save2Corrupt is True:
        try:
            with open('sdbackup2.dat', 'rb') as f:
                playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat = pickle.load(
                    f)
        except Exception as e:
            recoveryFailure()
        print("\nBackup data loaded successfully!\n")
        time.sleep(0.4)
        print("Overwriting corrupted save data...\n")
        with open('savedata2.dat', 'wb') as f:
            pickle.dump([playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat], f,
                        protocol=2)
        overwriteSuccess()
    elif save3Corrupt is True:
        try:
            with open('sdbackup3.dat', 'rb') as f:
                playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat = pickle.load(
                    f)
        except Exception as e:
            recoveryFailure()
        print("\nBackup data loaded successfully!\n")
        time.sleep(0.4)
        print("Overwriting corrupted save data...\n")
        with open('savedata3.dat', 'wb') as f:
            pickle.dump([playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat], f,
                        protocol=2)
        overwriteSuccess()

def recover():
    global playerName, savePoint, damage, playerMaxHealth, playerHealth, healingPotion, smokescreen, area, devProfile, save3Corrupt, save2Corrupt, save1Corrupt
    time.sleep(3)
    print("Accessing save data...\n")
    time.sleep(0.9)
    if save1Corrupt is True:
        try:
            with open('savedata.dat', 'rb') as f:
                playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat= pickle.load(f)
        except FileNotFoundError:
            print("Save data could not be accessed. Attempting to load backup...")
            recoverBackup()
        except EOFError and Exception:
            print("Failed to access data! Retrying...\n")
            time.sleep(0.8)
            recoverBackup()
    elif save2Corrupt is True:
        try:
            with open('savedata2.dat', 'rb') as f:
                playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat= pickle.load(f)
        except FileNotFoundError:
            print("Save data could not be accessed. Loading backup data...")
            recoverBackup()
        except EOFError and Exception:
            print("Failed to access data! Retrying...\n")
            time.sleep(0.8)
            recoverBackup()
    elif save3Corrupt is True:
        try:
            with open('savedata3.dat', 'rb') as f:
                playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat= pickle.load(f)
        except FileNotFoundError:
            print("Save data could not be accessed. Loading backup data...")
            recoverBackup()
        except EOFError and Exception:
            print("Failed to access data! Retrying...\n")
            time.sleep(0.8)
            recoverBackup()


def saveRecovery():
    time.sleep(0.7)
    print("""                                                                                                                                             ______________
        SAVE DATA RECOVERY UTILITY by REUBEN PARFREY ©2020                                                                                  |[]            |                  
        V1.5                                                                                                                                |  __________  |
                                                                                                                                            |  | Save   |  |
        All code by Reuben Parfrey. Do not attempt to distribute without explicit consent from the creator. Thanks to everyone testing      |  |  Data  |  |
        the game during it's alpha stages, none of this would be possible without your support!                                             |  |________|  |
                                                                                                                                            |   ________   |
        Stuck? Found a bug? Maybe you just want to chat? Reach out! Email reubenparfrey@gmail.com for any queries or concerns.              |   [ [ ]  ]   |
                                                                                                                                            \___[_[_]__]___|""")
    time.sleep(0.5)
    print("\nPreparing to recover data...\n")
    recover()


def convertingSave():
    global playerName
    global savePoint
    global damage
    global playerMaxHealth
    global playerHealth
    global smokescreen
    global hyperPotion
    global healingPotion
    global compatibility
    global area
    global devProfile
    global error, convertSlotTwo, convertSlotThree, convertSlotOne, gameBeat
    playerHealth = 20
    smokescreen = False
    healingPotion = False
    hyperPotion = False
    gameBeat = False
    time.sleep(0.6)
    print("\nSuccessfully converted! Now saving...")
    if convertSlotOne is True:
        with open('savedata.dat', 'wb') as f:
            pickle.dump([playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat], f,
                        protocol=2)
    elif convertSlotTwo is True:
        with open('savedata2.dat', 'wb') as f:
            pickle.dump([playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat], f,
                        protocol=2)
    elif convertSlotThree is True:
        with open('savedata3.dat', 'wb') as f:
            pickle.dump([playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat], f,
                        protocol=2)
    time.sleep(0.3)
    try:choice2 = int(input("\nSave data has been converted to work on this version of DeathTrap Dungeon!\n1] Return to menu\n2] Load converted save data\n--> "))
    except ValueError:
        menu()
    if choice2 == 1:
        menu()
    else:
        load()
    time.sleep(5)
    compatibility = False
    error = 0
    load()

def conversionFailure():
    ass = int(input("\nSave data could not be converted due to an invalid save format in use. Press [1] for more info, [2] to return to menu: "))
    if ass == 1:
        print("\nYou are seeing this message due to an unrecognisable save format being used. Save Data Conversion Utility is still in it's infantcy, and as such, is still incomplete. Keep\nan eye on new releases as new formats are being added frequently!")
        time.sleep(1)
        menu()
    else:
        menu()

def conversionThree():
    global playerName
    global savePoint
    global damage
    global playerMaxHealth
    global playerHealth
    global smokescreen
    global hyperPotion
    global healingPotion
    global compatibility
    global error, convertSlotOne, convertSlotTwo, convertSlotThree
    time.sleep(0.9)
    print("\nApplying new parameters and attempting to load data...\n")
    time.sleep(0.4)
    if convertSlotOne is True:
        try:
            with open('savedata.dat', 'rb') as f:
                playerName, savePoint = pickle.load(f)
        except FileNotFoundError:
            print("\nAn error occurred whilst accessing save data and the conversion process cannot continue. Ensure the 'savedata.dat' file hasn't been renamed and file permissions haven't been changed.\n")
            time.sleep(0.4)
            print("\nExiting compatibility mode and returning to menu...\n")
            time.sleep(0.1)
            menu()
        except ValueError:
            conversionFailure()
    elif convertSlotTwo is True:
        try:
            with open('savedata.dat', 'rb') as f:
                playerName, savePoint = pickle.load(f)
        except FileNotFoundError:
            print("\nAn error occurred whilst accessing save data and the conversion process cannot continue. Ensure the 'savedata.dat' file hasn't been renamed and file permissions haven't been changed.\n")
            time.sleep(0.4)
            print("\nExiting compatibility mode and returning to menu...\n")
            time.sleep(0.1)
            menu()
        except ValueError:
            conversionFailure()
    elif convertSlotThree is True:
        try:
            with open('savedata.dat', 'rb') as f:
                playerName, savePoint = pickle.load(f)
        except FileNotFoundError:
            print("\nAn error occurred whilst accessing save data and the conversion process cannot continue. Ensure the 'savedata.dat' file hasn't been renamed and file permissions haven't been changed.\n")
            time.sleep(0.4)
            print("\nExiting compatibility mode and returning to menu...\n")
            time.sleep(0.1)
            menu()
        except ValueError:
            conversionFailure()

    print("Loaded successfully! Attepting to convert data...")
    convertingSave()

def conversionTwo():
    global playerName
    global savePoint
    global damage
    global playerMaxHealth
    global playerHealth
    global smokescreen
    global hyperPotion
    global healingPotion
    global compatibility, convertSlotOne, convertSlotTwo, convertSlotThree
    global error
    time.sleep(0.2)
    print("\nApplying new parameters and attempting to load data...\n")
    time.sleep(0.6)
    if convertSlotOne is True:
        try:
            with open('savedata.dat', 'rb') as f:
                playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity = pickle.load(f)
        except FileNotFoundError:
            print("\nAn error occurred whilst accessing save data and the conversion process cannot continue. Ensure the 'savedata.dat' file hasn't been renamed and file permissions haven't been changed.\n")
            time.sleep(0.2)
            print("\nExiting compatibility mode and returning to menu...\n")
            time.sleep(0.3)
            menu()
        except ValueError:
            print("Unable to load data with newly applied parameters. Attempting to load under different parameters...")
            time.sleep(0.2)
            conversionThree()
    elif convertSlotTwo is True:
        try:
            with open('savedata2.dat', 'rb') as f:
                playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity = pickle.load(f)
        except FileNotFoundError:
            print("\nAn error occurred whilst accessing save data and the conversion process cannot continue. Ensure the 'savedata2.dat' file hasn't been renamed and file permissions haven't been changed.\n")
            time.sleep(0.2)
            print("\nExiting compatibility mode and returning to menu...\n")
            time.sleep(0.3)
            menu()
        except ValueError:
            print("Unable to load data with newly applied parameters. Attempting to load under different parameters...")
            time.sleep(0.2)
            conversionThree()
    elif convertSlotThree is True:
        try:
            with open('savedata3.dat', 'rb') as f:
                playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity = pickle.load(f)
        except FileNotFoundError:
            print("\nAn error occurred whilst accessing save data and the conversion process cannot continue. Ensure the 'savedata3.dat' file hasn't been renamed and file permissions haven't been changed.\n")
            time.sleep(0.2)
            print("\nExiting compatibility mode and returning to menu...\n")
            time.sleep(0.3)
            menu()
        except ValueError:
            print("Unable to load data with newly applied parameters. Attempting to load under different parameters...")
            time.sleep(0.2)
            conversionThree()

    print("Loaded successfully! Attepting to convert data...")
    convertingSave()

def conversion():
    global playerName
    global savePoint
    global damage
    global playerMaxHealth
    global playerHealth
    global smokescreen
    global hyperPotion
    global healingPotion
    global compatibility, convertSlotOne, convertSlotTwo, convertSlotThree
    global error, gameBeat
    error=1
    time.sleep(0.9)
    gameBeat=False
    print(r"""                                                                                                                                                 ______________
            SAVE DATA CONVERSION UTILITY by REUBEN PARFREY ©2020                                                                                |[]            |                  
            V1.7                                                                                                                                |  __________  |
                                                                                                                                                |  | Save   |  |
            All code by Reuben Parfrey. Do not attempt to distribute without explicit consent from the creator. Thanks to everyone testing      |  |  Data  |  |
            the game during it's alpha stages, none of this would be possible without your support!                                             |  |________|  |
                                                                                                                                                |   ________   |
            Stuck? Found a bug? Maybe you just want to chat? Reach out! Email reubenparfrey@gmail.com for any queries or concerns.              |   [ [ ]  ]   |
                                                                                                                                                \___[_[_]__]___|                        """)
    time.sleep(1.3)
    print("\nYour save will be converted to work on newer versions of DTD. Please stand by...")
    time.sleep(0.7)
    print("\nLoading data under compatibility mode...\n")
    time.sleep(0.8)
    if convertSlotOne is True:
        try:
            with open('savedata.dat', 'rb') as f:
                playerName, savePoint, damage, playerMaxHealth, playerHealth, healingPotion, smokescreen, devProfile, area = pickle.load(f)
        except FileNotFoundError:
            print("\nAn error occurred whilst loading save data and the conversion process cannot continue; the data file could not be found.\n")
            time.sleep(0.3)
            menu()
        except ValueError:
            print("Unable to load data with legacy parameters. Attempting to load under different parameters...")
            time.sleep(0.3)
            conversionTwo()
    elif convertSlotTwo is True:
        try:
            with open('savedata2.dat', 'rb') as f:
                playerName, savePoint, damage, playerMaxHealth, playerHealth, healingPotion, smokescreen, devProfile, area = pickle.load(f)
        except FileNotFoundError:
            print("\nAn error occurred whilst loading save data and the conversion process cannot continue; the data file could not be found.\n")
            time.sleep(0.3)
            menu()
        except ValueError:
            print("Unable to load data with legacy parameters. Attempting to load under different parameters...")
            time.sleep(0.3)
            conversionTwo()
    elif convertSlotThree is True:
        try:
            with open('savedata3.dat', 'rb') as f:
                playerName, savePoint, damage, playerMaxHealth, playerHealth, healingPotion, smokescreen, devProfile, area = pickle.load(f)
        except FileNotFoundError:
            print("\nAn error occurred whilst loading save data and the conversion process cannot continue; the data file could not be found.\n")
            time.sleep(0.3)
            menu()
        except ValueError:
            print("Unable to load data with legacy parameters. Attempting to load under different parameters...")
            time.sleep(0.3)
            conversionTwo()
    print("Loaded successfully! Converting data...")
    convertingSave()

def chapterReplay():
    global playerHealth, playerMaxHealth, damage
    try:choice=int(input("\nSelect a chapter to play:\n===============================\n1] Enter the Dungeon\n2] Solitary Confinement\n3] The Great Escape!\n4] What Doesn't Kill You Makes You Stronger\n5] A Breath of Fresh Air\n6] A Puzzle in Darkness\n7] With Great Power\n8] Finale\n===============================\n9] Cancel\n--> "))
    except ValueError:
        chapterReplay()
    if choice==1:
        area1()
    elif choice==2:
        choice4()
    elif choice==3:
        escape()
    elif choice==4:
        backInside()
    elif choice==5:
        chapterFive()
    elif choice==6:
        chapterSix()
    elif choice==7:
        chapterSeven()
    elif choice==8:
        chapterEight()
    else:
        gameBeatWarp()

def gameBeatWarp():
    global savePoint, gameBeat, noPyGame, sfxMissing, playerHealth, playerMaxHealth, damage
    try:choice=int(input("\n== EXTRAS ==\nPlease select an option from the list below:\n1] Music Player\n2] Chapter Replay\n3] Cancel (Continue load)\n4] Quit (Return to menu)\n--> "))
    except ValueError:
        gameBeatWarp()
    if choice==1 and noModuleSound is False and sfxMissing is False:
        print("\n== MUSIC PLAYER ==\nListen to DeathTrap Dungeon's soundtrack! All the songs that play in-game can be heard here, as well as some never-before-heard beta tracks!\n")
        audioPlayer()
    elif choice==1 and noModuleSound is True:
        try:denied=int(input("\nMusic Player can't be accessed because the required module 'Pygame' is not installed. Choose an option to continue:\n1] Install the module\n2] Cancel\n--> "))
        except ValueError:
            gameBeatWarp()
        if denied==1:
            install('pygame')
        else:
            gameBeatWarp()
    elif choice==1 and sfxMissing is True:
        print("\nMusic Player can't be accessed because the audio data could not be loaded. See the error message displayed upon starting the game for more details.")
        gameBeatWarp()
    elif choice==2:
        gameBeat=True
        chapterReplay()
    elif choice==4:
        menu()
    else:
        if debug!=0:
            print(savePoint)
        if savePoint == 0:
            area1()
        elif savePoint == 2:
            choice4()
        elif savePoint == 2:
            escape()
        elif savePoint == 3:
            backInside()
        elif savePoint == 4:
            chapterFive()
        elif savePoint == 5:
            chapterSix()
        elif savePoint == 6:
            chapterSeven()
        elif savePoint == 7 and gameBeat is False:
            chapterEight()
        elif savePoint == 7 and gameBeat is True:
            area1()

def loadSlot3():
    global playerName
    global damage
    global savePoint
    global debug
    global playerMaxHealth
    global playerHealth
    global healingPotion
    global smokescreen
    global continueLoad
    global devProfile
    global noModuleSound
    global muteAudio, save3Corrupt, convertSlotThree, smokescreenQuantity, hyperpotionQuantity, healingpotionQuantity, savePointCopy
    error = 0
    print("Loading data...")
    time.sleep(0.5)
    try:
        with open('savedata3.dat', 'rb') as f:
            playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat = pickle.load(
                f)
    except FileNotFoundError:
        print("\nThere is no save data stored in Slot 3.\n")
        error = 1
        load()
    except ValueError:
        convert=int(input("\nSave data cannot be loaded because it is incompatible with this version of DeathTrap Dungeon. Would you like to convert it so it can be loaded on \nnewer versions of the game?\n1] Yes\n2] No\n--> "))
        if convert == 1:
            convertSlotThree=True
            conversion()
        elif convert==2:
            load()
        else:
            loadSlot3()
    except pickle.UnpicklingError and EOFError and Exception:
        pandeco = int(input(
            "\nSave data is corrupt and cannot be loaded. Would you like to recover the corrupted data?\n1] Yes\n2] No\n--> "))
        if pandeco == 1:
            save3Corrupt=True
            saveRecovery()
        else:
            menu()
    try:
        if playerName == "Null" and damage == 0:
            error = 1
            print("There is no save data stored in Slot 3.\n")
            menu()
    except Exception:
        pass
    if error != 1:
        print("Welcome back, "+str(playerName)+"!")
        if muteAudio == True:
            print("\n== Audio is muted ==")
        savePointCopy=savePoint
        if debug!=0:
            print(savePoint, savePointCopy)
        if muteAudio!=True:
            s = pygame.mixer.Sound("sfx/load.wav")
            empty_channel = pygame.mixer.find_channel()
            empty_channel.play(s)
        if debug != 0:
            print(playerMaxHealth, "\n", savePoint)
            print("devProfile=", devProfile)
    if debug != 0:
        print("attack", damage)
    if debug != 0:
        print(damage)
    if savePoint == 1 and gameBeat is False:
        choice4()
    elif savePoint == 2 and gameBeat is False:
        escape()
    elif savePoint == 3 and gameBeat is False:
        backInside()
    elif savePoint == 4 and gameBeat is False:
        chapterFive()
    elif savePoint==5 and gameBeat is False:
        chapterSix()
    elif savePoint == 6 and gameBeat is False:
        chapterSeven()
    elif savePoint == 7 and gameBeat is False:
        chapterEight()
    elif gameBeat is True:
        gameBeatWarp()
    elif damage == 0:
        print("Unable to load; there is no save data stored in Slot 3.\n")
        menu()
    else:
        print("\nSave data could not be loaded. A player profile was detected, but no progress has been made.\n")
        menu()

def loadSlot2():
    global playerName
    global damage
    global savePoint
    global debug
    global playerMaxHealth
    global playerHealth
    global healingPotion
    global smokescreen
    global continueLoad
    global devProfile
    global noModuleSound
    global muteAudio, save2Corrupt, convertSlotTwo, smokescreenQuantity, hyperpotionQuantity, healingpotionQuantity, savePointCopy
    error = 0
    print("Loading data...")
    time.sleep(0.5)
    try:
        with open('savedata2.dat', 'rb') as f:
            playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat = pickle.load(
                f)
    except FileNotFoundError:
        print("\nThere is no save data stored in Slot 2.\n")
        error = 1
        load()
    except ValueError:
        convert=int(input("\nSave data cannot be loaded because it is incompatible with this version of DeathTrap Dungeon. Would you like to convert it so it can be loaded on \nnewer versions of the game?\n1] Yes\n2] No\n--> "))
        if convert == 1:
            convertSlotTwo=True
            conversion()
        elif convert==2:
            load()
        else:
            loadSlot2()
    except pickle.UnpicklingError and EOFError and Exception:
        pandeco = int(input(
            "\nSave data is corrupt and cannot be loaded. Would you like to recover the corrupted data?\n1] Yes\n2] No\n--> "))
        if pandeco == 1:
            save2Corrupt=True
            saveRecovery()
        else:
            menu()
    try:
        if playerName == "Null" and damage == 0:
            error = 1
            print("There is no save data stored in Slot 2.\n")
            menu()
    except Exception:
        pass
    if error != 1:
        print("Welcome back, "+str(playerName)+"!")
        if muteAudio == True:
            print("\n== Audio is muted ==")
        savePointCopy = savePoint
        if debug != 0:
            print(savePoint, savePointCopy)
        if muteAudio!=True:
            s = pygame.mixer.Sound("sfx/load.wav")
            empty_channel = pygame.mixer.find_channel()
            empty_channel.play(s)
        if debug != 0:
            print(playerMaxHealth, "\n", savePoint)
            print("devProfile=", devProfile)
    if debug != 0:
        print("attack", damage)
    # attack==damage
    if debug != 0:
        print(damage)
    if savePoint == 1 and gameBeat is False:
        choice4()
    elif savePoint == 2 and gameBeat is False:
        escape()
    elif savePoint == 3 and gameBeat is False:
        backInside()
    elif savePoint == 4 and gameBeat is False:
        chapterFive()
    elif savePoint==5 and gameBeat is False:
        chapterSix()
    elif savePoint == 6 and gameBeat is False:
        chapterSeven()
    elif savePoint == 7 and gameBeat is False:
        chapterEight()
    elif gameBeat is True:
        gameBeatWarp()
    elif damage == 0:
        print("Unable to load; there is no save data stored in Slot 2.\n")
        menu()
    else:
        print("\nSave data could not be loaded. A player profile was detected, but no progress has been made.\n")
        menu()

def loadSlot1():
    global playerName
    global damage
    global savePoint
    global debug
    global playerMaxHealth
    global playerHealth
    global healingPotion
    global smokescreen
    global continueLoad
    global devProfile
    global noModuleSound
    global muteAudio
    global save1Corrupt, convertSlotOne, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, savePointCopy
    error=0
    print("Loading data...")
    time.sleep(0.5)
    try:
        with open('savedata.dat', 'rb') as f:
            playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat= pickle.load(f)
    except FileNotFoundError:
        print("\nThere is no save data stored in Slot 1.\n")
        error=1
        load()
    except ValueError:
        try:convert=int(input("\nSave data cannot be loaded because it is incompatible with this version of DeathTrap Dungeon. Would you like to convert it so it can be loaded on \nnewer versions of the game?\n1] Yes\n2] No\n--> "))
        except ValueError:
            print("\nBad input. Only integers can be entered here!\n")
            loadSlot1()
        if convert == 1:
            convertSlotOne=True
            conversion()
        elif convert==2:
            load()
        else:
            loadSlot1()
    except pickle.UnpicklingError and EOFError and Exception:
        pandeco=int(input("\nSave data is corrupt and cannot be loaded. Would you like to recover the corrupted data?\n1] Yes\n2] No\n--> "))
        save1Corrupt=True
        if pandeco==1:
            saveRecovery()
        else:
            load()
    try:
        if playerName=="[EMPTY]" and damage==0:
            error=1
            print("Unable to load; there is no save data stored in Slot 1.\n")
            menu()
    except Exception:
        pass
    if error != 1:
        print("Welcome back, "+str(playerName)+"!")
        if muteAudio == True:
            print("\n== Audio is muted ==")
        savePointCopy = savePoint
        if debug != 0:
            print(savePoint, savePointCopy)
        if muteAudio!=True:
            s = pygame.mixer.Sound("sfx/load.wav")
            empty_channel = pygame.mixer.find_channel()
            empty_channel.play(s)
        if debug != 0:
            print(playerMaxHealth,"\n",savePoint)
            print("devProfile=",devProfile)
    if debug !=0:
        print("attack",damage)
    if savePoint == 1 and gameBeat is False:
        choice4()
    elif savePoint==2 and gameBeat is False:
        escape()
    elif savePoint==3 and gameBeat is False:
        backInside()
    elif savePoint==4 and gameBeat is False:
        chapterFive()
    elif savePoint==5 and gameBeat is False:
        chapterSix()
    elif savePoint == 6 and gameBeat is False:
        chapterSeven()
    elif savePoint == 7 and gameBeat is False:
        chapterEight()
    elif gameBeat is True:
        gameBeatWarp()
    elif damage == 0:
        print("Unable to load; there is no save data stored in Slot 1.\n")
        menu()
    else:
        print("\nSave data could not be loaded. A player profile was detected, but no progress has been made.\n")
        load()

def load():
    global playerName
    global damage
    global savePoint
    global debug
    global playerMaxHealth
    global playerHealth
    global healingPotion
    global hyperPotion
    global smokescreen
    global continueLoad
    global devProfile
    global noModuleSound
    global muteAudio, sfxMissing, gameBeat
    gameBeat=False
    error=0
    if noModuleSound == True:
        muteAudio = True
    if sfxMissing is True:
        muteAudio = True
    print("Select a save file to load:")
    print("===============================")
    slot1Used=True
    slot2Used=True
    slot3Used=True
    try:
        with open('savedata.dat', 'rb') as f:
            playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat= pickle.load(f)
    except FileNotFoundError:
        print("1] SLOT 1 - [EMPTY]")
        slot1Used=False
    except EOFError:
        print("1] SLOT 1 - [CORRUPT]")
        slot1Used=False
    except KeyError:
        print("1] SLOT 1 - [CORRUPT]")
        slot1Used=False
    except ValueError:
        print("1] SLOT 1 - [INCOMPATIBLE]")
        slot1Used=False
    if slot1Used==True and gameBeat is False:
        try:print("1] SLOT 1 -",playerName)
        except Exception:
            pass
    elif slot1Used==True and gameBeat is True:
        try:print("1] SLOT 1 -",playerName," *")
        except Exception:
            pass
    else:
        pass
    try:
        with open('savedata2.dat', 'rb') as f:
            playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat=pickle.load(f)
    except FileNotFoundError:
        print("2] SLOT 2 - [EMPTY]")
        slot2Used=False
    except EOFError or KeyError:
        print("2] SLOT 2 - [CORRUPT]")
        slot2Used=False
    except ValueError:
        print("2] SLOT 2 - [INCOMPATIBLE]")
        slot2Used=False
    if slot2Used==True and gameBeat is False:
        print("2] SLOT 2 -",playerName)
    elif slot2Used==True and gameBeat is True:
        print("2] SLOT 2 -",playerName," *")
    else:
        pass
    try:
        with open('savedata3.dat', 'rb') as f:
            playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat= pickle.load(f)
    except FileNotFoundError:
        print("3] SLOT 3 - [EMPTY]")
        slot3Used=False
    except EOFError or KeyError:
        print("3] SLOT 3 - [CORRUPT]")
        slot3Used=False
    except ValueError:
        print("3] SLOT 3 - [INCOMPATIBLE]")
        slot3Used=False
    if slot3Used==True and gameBeat is False:
        print("3] SLOT 3 -",playerName)
    elif slot3Used==True and gameBeat is True:
        print("3] SLOT 3 -",playerName," *")
    else:
        pass
    print("===============================")
    print("4] Cancel")
    try:choice=int(input("--> "))
    except ValueError:
        print("\nBad input. Only integers can be entered here!")
        load()
    if choice==1:
        loadSlot1()
    elif choice==2:
        loadSlot2()
    elif choice==3:
        loadSlot3()
    elif choice==4:
        print(' ')
        savePoint=0
        playerName=""
        damage=5
        playerHealth=20
        playerMaxHealth=20
        gameBeat = False
        smokescreen = False
        hyperPotion = False
        healingPotion = False
        menu()
    else:
        print("\nThat doesn't compute! Please select a valid option.")
        load()

def saveSuccess():
    global savePoint, gameBeat, playerMaxHealth, playerHealth, smokescreen, healingPotion, hyperPotion, area, damage, creditsRolled
    try:continue2 = int(input("\nGame saved successfully! Continue playing? \n1]Yes\n2]No  \n--> "))
    except ValueError:
        print("Bad input; an integer must be entered.")
        saveSuccess()
    savePoint = originalSavePoint
    if continue2 == 1:
        print(" ")
        if savePoint == 1:
            choice4()
        elif savePoint == 2:
            escape()
        elif savePoint == 3:
            backInside()
        elif savePoint == 4:
            chapterFive()
        elif savePoint == 5:
            chapterSix()
        elif savePoint == 6:
            chapterSeven()
        elif savePoint == 7 and gameBeat is False:
            chapterEight()
        elif gameBeat is True and creditsRolled is True:
            print("Saved!")
            postCredits()
        else:
            return
    elif continue2 == 2:
        print("Returning to menu...\n")
        savePoint=0
        area=0
        gameBeat=False
        playerHealth=20
        playerMaxHealth=20
        smokescreen=False
        healingPotion=False
        hyperPotion=False
        damage=5
        menu()
    else:
        saveSuccess()

def saveToSlotOne():
    global originalSavePoint, savePoint, gameBeat, creditsRolled
    print("Now saving...")
    time.sleep(0.8)
    with open('savedata.dat', 'wb') as f:
        pickle.dump([playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat], f, protocol=2)
    with open('sdbackup.dat', 'wb') as f:
        pickle.dump([playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat], f, protocol=2)
    if muteAudio != True:
        pygame.mixer.music.load("sfx/incident_jingle.wav")
        pygame.mixer.music.play(1)
    if creditsRolled is False:
        saveSuccess()
    elif creditsRolled is True and gameBeat is True:
        print("Saved!")
        postCredits()

def saveToSlotTwo():
    global originalSavePoint, savePoint, gameBeat, creditsRolled
    print("Now saving...")
    time.sleep(0.8)
    with open('savedata2.dat', 'wb') as f:
        pickle.dump([playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat], f, protocol=2)
    with open('sdbackup2.dat', 'wb') as f:
        pickle.dump([playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat], f, protocol=2)
    if muteAudio != True:
        pygame.mixer.music.load("sfx/incident_jingle.wav")
        pygame.mixer.music.play(1)
    if creditsRolled is False:
        saveSuccess()
    elif creditsRolled is True and gameBeat is True:
        print("Saved!")
        postCredits()


def saveToSlotThree():
    global originalSavePoint, savePoint, creditsRolled
    print("Now saving...")
    time.sleep(0.8)
    with open('savedata3.dat', 'wb') as f:
        pickle.dump([playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat], f, protocol=2)
    with open('sdbackup3.dat', 'wb') as f:
        pickle.dump([playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area,
                     smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat], f, protocol=2)
    if muteAudio != True:
        pygame.mixer.music.load("sfx/incident_jingle.wav")
        pygame.mixer.music.play(1)
    if creditsRolled is False:
        saveSuccess()
    elif creditsRolled is True and gameBeat is True:
        print("Saved!")
        postCredits()

#playerName, savePoint, damage, playerMaxHealth, playerHealth, healingPotion, smokescreen, devProfile, area - OLD SAVE FORMAT

def saveSlot():
    global debug
    slot1Used=True
    slot2Used=True
    slot3Used=True
    overwrite=0
    print("\nSave to which slot?\n===============================")
    try:
        with open('savedata.dat', 'rb') as f:
            playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat= pickle.load(f)
    except FileNotFoundError:
        print("1] SLOT 1 - [EMPTY]")
        slot1Used=False
    except EOFError:
        print("1] SLOT 1 - [CORRUPT]")
        slot1Used=False
    except ValueError:
        print("1] SLOT 1 - [INCOMPATIBLE]")
        slot1Used=False
    if slot1Used == True and gameBeat is False:
        try:
            print("1] SLOT 1 -", playerName)
        except Exception:
            pass
    elif slot1Used == True and gameBeat is True:
        try:
            print("1] SLOT 1 -", playerName, " *")
        except Exception:
            pass
    else:
        pass
    try:
        with open('savedata2.dat', 'rb') as f:
            playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat=pickle.load(f)
    except FileNotFoundError:
        print("2] SLOT 2 - [EMPTY]")
        slot2Used=False
    except EOFError:
        print("2] SLOT 2 - [CORRUPT]")
        slot2Used=False
    except ValueError:
        print("2] SLOT 2 - [INCOMPATIBLE]")
        slot2Used=False
    if slot2Used == True and gameBeat is False:
        try:
            print("2] SLOT 2 -", playerName)
        except Exception:
            pass
    elif slot2Used == True and gameBeat is True:
        try:
            print("2] SLOT 2 -", playerName, " *")
        except Exception:
            pass
    try:
        with open('savedata3.dat', 'rb') as f:
            playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat= pickle.load(f)
    except FileNotFoundError:
        print("3] SLOT 3 - [EMPTY]")
        slot3Used=False
    except EOFError:
        print("3] SLOT 3 - [CORRUPT]")
        slot3Used=False
    except ValueError:
        print("3] SLOT 3 - [INCOMPATIBLE]")
        slot3Used=False
    if slot3Used == True and gameBeat is False:
        try:
            print("3] SLOT 3 -", playerName)
        except Exception:
            pass
    elif slot3Used == True and gameBeat is True:
        try:
            print("3] SLOT 3 -", playerName, " *")
        except Exception:
            pass
    print("===============================\n4] Cancel")
    try:choice=int(input("--> "))
    except ValueError:
        print("\nBad input. Only integers can be entered here!")
        saveSlot()
    if choice==1:
        if slot1Used==True:
            try:overwrite=int(input("There is already save data stored in Slot 1. Overwrite it?\n1] Yes\n2] No\n--> "))
            except ValueError:
                saveSlot()
            if overwrite==1:
                saveToSlotOne()
            else:
                saveSlot()
        else:
            saveToSlotOne()
    elif choice==2:
        if slot2Used==True:
            try:overwrite=int(input("There is already save data stored in Slot 2. Overwrite it?\n1] Yes\n2] No\n--> "))
            except ValueError:
                saveSlot()
            if overwrite==1:
                saveToSlotTwo()
            else:
                saveSlot()
        else:
            saveToSlotTwo()
    elif choice==3:
        if slot3Used==True:
            try:overwrite=int(input("There is already save data stored in Slot 3. Overwrite it?\n1] Yes\n2] No\n--> "))
            except ValueError:
                saveSlot()
            if overwrite==1:
                saveToSlotThree()
            else:
                saveSlot()
        else:
            saveToSlotThree()
    elif choice==4:
        askSave()
    else:
        print("\nThat doesn't compute! Please choose a valid option.")
        saveSlot()

def askSave():
    global PlayerIG, firstSaveRequest
    global playerMaxHealth
    global muteAudio
    global playerHealth
    global smokescreen
    global healingPotion
    global savePoint
    global playerName
    global damage
    global area
    global debug
    global saveWarning
    global devProfile
    global originalSavePoint, creditsRolled, gameBeat
    if debug > 0:
        print(savePoint, gameBeat)
    originalSavePoint=savePoint
    if debug!=0:
        print("originalSavePoint=",originalSavePoint,"\ndevProfile=",devProfile,"\n")
    global quitToTitle
    print(" ")
    if not creditsRolled:
        try:ask = int(input("Checkpoint reached! Would you like to save your progress?\n1] Yes\n2] No\n--> "))
        except ValueError:
            askSave()
    elif creditsRolled is True:
        try:ask = int(input("Would you like to save?\n1] Yes\n2] No\n--> "))
        except ValueError:
            askSave()
    if ask ==1:
        saveSlot()
    elif ask==2:
        if not creditsRolled:
            print("Okay, maybe next time.")
        else:
            try:choice=int(input("Are you sure? Some features unlocked after beating the game will be unavailable if you don't save.\n1] Yes\n2] No\n--> "))
            except ValueError:
                askSave()
            if choice==1:
                pass
            else:
                askSave()
        if savePoint == 1:
            choice4()
        elif savePoint == 2:
            escape()
        elif savePoint == 3:
            backInside()
        elif savePoint == 4:
            chapterFive()
        elif savePoint == 5:
            chapterSix()
        elif savePoint == 6:
            chapterSeven()
        elif savePoint == 7 and gameBeat is False:
            chapterEight()
        elif creditsRolled is True:
            postCredits()
        else:
            return
    else:
        print("That doesn't compute! Please select a valid option.")
        askSave()

def multiChoiceExit():
    choice=0
    print("\nAre you sure you'd like to quit? The data you just entered will be lost and you'll be returned to the main menu.\n1] Yes\n2] No")
    try:choice=int(input("--> "))
    except ValueError:
        multiChoiceExit()
    if choice==1:
        menu()
    else:
        userMultiChoice()

def userMultiChoice():
    global playerName, damage
    print("\nYou're nearly ready to begin, "+str(playerName)+"! Take a moment to finalize your Player Profile, or select 'Begin' to start:")
    try:choice=int(input("1] Begin!\n2] Change name\n3] View stats\n4] Quit\n--> "))
    except ValueError:
        print("\nBad input; only integers can be entered here!")
        userMultiChoice()
    if choice==1:
        damage=5
        if debug != 0:
            print("DAMAGE=",str(damage))
        area1()
    elif choice==2:
        newNameInput()
    elif choice==3:
        stats()
    elif choice==4:
        multiChoiceExit()

def stats():
    global PlayerIG
    global damage
    global area
    global savePoint
    global playerHealth
    global playerMaxHealth
    global gotShield
    print("\nName: %s" % playerName)
    print("Attack Damage: %d" % damage)
    print("Health: %i/%i" % (playerHealth, playerMaxHealth))
    time.sleep(1)
    if savePoint==0 and area==0:
        userMultiChoice()
    elif savePoint==0 and area==1:
        choice2Alternate()
    elif savePoint==1:
        choice4()
    elif savePoint==2:
        outsideConfinement()
    elif area==1:
        choice2Alternate()
    elif area==2:
        outsideConfinement()
    elif area==4:
        defeatedHighRank()
    elif area==6:
        courtyardGuardDefeated()
    elif area==7:
        chapterSevenSplit()


def statInputAsk():
    global damage
    try:check_input = input("\nWould you like to see your stats?\n1] Yes\n2] No\n--> " )
    except ValueError:
        statInputAsk()
    if check_input == "y" or check_input == "Y" or check_input == "yes" or check_input == "Yes" or check_input == "1":
        damage=5
        stats()
    elif check_input == "n" or check_input == "N" or check_input == "no" or check_input == "No" or check_input == "2":
        print("Okay, then. Don't forget you can always check your stats later! Select 'View Player Profile' on the main menu.")
        userMultiChoice()
    else:
        print("That doesn't compute! Please try again.")
        statInputAsk()

def newNameInput():
    global playerName, PlayerIG
    option = input("\nEnter your new name:\n--> ")
    PlayerIG = Player(option)
    print("So you'd rather be called %s? Got it." % PlayerIG.name)
    playerName = PlayerIG.name
    time.sleep(0.5)
    userMultiChoice()

def saveProfile():
    global playerName, muteAudio
    global playerHealth
    global playerMaxHealth
    global damage
    global savePoint
    global healingPotion
    global hyperPotion
    global smokescreen
    global createdProfile, area, devProfile, createSlot1,createSlot2,createSlot3
    devProfile=False
    print("Finished creating player profile! Now saving... ")
    savePoint=0
    damage=5
    time.sleep(2.2)
    if createSlot1 is True:
        with open('savedata.dat', 'wb') as f:
            pickle.dump([playerName, savePoint, damage, playerMaxHealth, smokescreen, healingPotion, hyperPotion, devProfile, area], f, protocol=2)
        print("\nNew player profile was saved to slot 1!")
    elif createSlot2 is True:
        with open('savedata2.dat', 'wb') as f:
            pickle.dump([playerName, savePoint, damage, playerMaxHealth, smokescreen, healingPotion, hyperPotion, devProfile, area], f, protocol=2)
        print("\nNew player profile was saved to slot 2!")
    elif createSlot3 is True:
        with open('savedata3.dat', 'wb') as f:
            pickle.dump([playerName, savePoint, damage, playerMaxHealth, smokescreen, healingPotion, hyperPotion, devProfile, area], f, protocol=2)
        print("\nNew player profile was saved to slot 3!")
    if muteAudio != True:
        pygame.mixer.music.load("sfx/incident_jingle.wav")
        pygame.mixer.music.play()
    createdProfile = True
    time.sleep(0.5)
    profile()

def nameChangeAsk():
    global createProfile
    global playerName
    name_input = input("Would you like to change your name?\n1] Yes\n2] No\n--> ")
    if name_input == "y" or name_input == "Y" or name_input == "yes" or name_input == "Yes" or name_input == "1" or name_input == "YES":
        option = input("What would you like to be called instead?\n--> ")
        global PlayerIG
        PlayerIG = Player(option)
        print("So you'd rather be called %s? Got it." % PlayerIG.name)
        time.sleep(1)
        playerName=PlayerIG.name
        if debug != 0:
            print(playerName)
        if createProfile == True:
            saveProfile()
        else:
            statInputAsk()
    # User answered "no"
    elif name_input == "n" or name_input == "N" or name_input == "no" or name_input == "No" or name_input == "2" or name_input == "NO":
        print("Okay. Make sure you're happy with your name; once you've started a game you can't change it.")
        if createProfile is True:
            saveProfile()
        else:
            statInputAsk()
    else:
        print("Sorry, that does not compute. Please try again.")
        nameChangeAsk()

def nameInputAsk():
    global playerName
    print("Welcome to DeathTrap Dungeon! What's your name? ")
    option = input("--> ")
    global PlayerIG
    PlayerIG = Player(option)
    if PlayerIG.name == "" or PlayerIG.name == " ":
        print("Please enter a valid name.\n")
        nameInputAsk()
    elif len(option) >= 150:
        message=random.randint(1,6)
        if message == 1:
            print("FILENAME TOO LONG: SA IS NOT DEFINED\n")
        elif message == 2:
            print("FILENAME TOO LONG: WIPE OUT ALL 1.2 BILLION OF THE RED COMMUNISTS\n")
        elif message == 3:
            print("FILENAME TOO LONG: MI HANNO RUBATO LA MIA VERGINITÀ!\n")
        elif message == 4:
            print("FILENAME TOO LONG: WOULD YOU LIKE TO SWITCH ORGS?\n")
        elif message == 5:
            print("FILENAME TOO LONG: ALTER GRAVITATIONAL PATTERNS\n")
        elif message==6:
            print("FILENAME TOO LONG: DICK ONE OF THE THREE OPTIONS\n")
        nameChangeAsk()
    else:
        print("Oh nice! That's a cool name %s!" % PlayerIG.name)
        playerName = PlayerIG.name
        time.sleep(1)
        print(" ")
        nameChangeAsk()

def highGuardAttack():
    global guardDamage
    global damage
    global playerHealth
    global died
    global musicStop
    global highRank
    guardDamage = 7
    if debug != 0:
        print(guardDamage)
    print("The high ranking guard attacks, dealing",guardDamage," damage!\n ")
    time.sleep(1)
    playerHealth = playerHealth - 7
    if playerHealth < 0:
        playerHealth=0
    if debug == 1:
        print(playerHealth)
    print("You have", playerHealth, "health remaining.\n")
    time.sleep(1)
    if playerHealth <= 0:
        print("The high ranking guard is victorious! You fall to the ground in defeat...")
        died = True
        musicStop = True
    else:
        fightGuard()

def guardAttack():
    global guardDamage
    global damage
    global playerHealth
    global playerMaxHealth
    global died
    global musicStop
    global highRank
    time.sleep(1)
    print("The guard attacks, dealing 5 damage!\n ")
    time.sleep(1)
    playerHealth = playerHealth - 5
    if playerHealth < 0:
        playerHealth=0
    if debug==1:
        print(playerHealth)
    print("You have",playerHealth,"health remaining.\n")
    time.sleep(1)
    if playerHealth <=0:
        print("The guard is victorious! You fall to the ground in defeat...")
        if playerMaxHealth==20:
            playerHealth=20
        else:
            playerHealth=22
        if debug != 0:
            print("playerHealth =",playerHealth)
        died=True
        musicStop=True
    else:
        fightGuard()

def afterMathStats():
    global savePoint, area, gameBeat
    if gameBeat is True:
        if savePoint == 0 and area == 0:
            userMultiChoice()
        elif savePoint == 0 and area == 1:
            choice2Alternate()
        elif savePoint == 1:
            choice4()
        elif savePoint == 2:
            outsideConfinement()
        elif area == 1:
            choice2Alternate()
        elif area == 2:
            outsideConfinement()
        elif area == 4:
            defeatedHighRank()
        elif area == 6:
            courtyardGuardDefeated()
        elif area == 7:
            chapterSevenSplit()
    else:
        try:choice2 = int(input("Would you like to see your stats? \n1] Yes \n2] No\n--> "))
        except ValueError:
            afterMathStats()
        if choice2 == 1:
            stats()
        else:
            if savePoint == 0 and area == 0:
                userMultiChoice()
            elif savePoint == 0 and area == 1:
                choice2Alternate()
            elif savePoint == 1:
                choice4()
            elif savePoint == 2:
                outsideConfinement()
            elif area == 1:
                choice2Alternate()
            elif area == 2:
                outsideConfinement()
            elif area == 4:
                defeatedHighRank()
            elif area == 6:
                courtyardGuardDefeated()
            elif area == 7:
                chapterSevenSplit()

def battleAfterMath():
    global playerMaxHealth
    global playerHealth
    global choice
    global weapon
    global area
    global damage
    global attack
    global musicLoop
    global playBattleTheme
    global defeatedGuardOutsideConfinement
    global hyperPotion
    global musicStop, hyperpotionQuantity, defeatedChapterSevenGuard, pickedUpKey, healingpotionQuantity, healingPotion, gameBeat
    if area == 1:
        try:weapon = int(input("\nThe guard drops a wooden spear. Pick it up?\n1] Yes\n2] No\n--> "))
        except ValueError:
            print("\nOnly integers can be entered here!")
            weapon=1
        if weapon == 1:
            print("\nYou obtained a Wooden Spear! \n")
            try:print(r"""                                                                    ▓▓▓▓▓▓▓▓
                                                                  ██▒▒░░░░██
                                                                ██▒▒░░░░░░██
                                                              ██▒▒░░░░░░  ██
                                                            ██▒▒░░░░░░  ██░░
                                                          ▓▓▒▒░░░░░░  ▓▓    
                                                ██████████▒▒░░░░░░  ██      
                                              ██▒▒░░░░    ██░░░░  ██        
                                                ████████    ██  ██          
                                                    ██▒▒██    ██            
                                                  ▓▓▒▒▒▒▒▒▓▓  ██            
                                                ██▒▒▒▒▒▒████░░██            
                                              ██▒▒▒▒▒▒██  ██░░██            
                                            ██▒▒▒▒▒▒██    ██▒▒██            
                                          ▒▒▒▒▒▒▒▒██░░    ░░██              
                                        ██▒▒▒▒▒▒██                          
                                      ▓▓▒▒▒▒▒▒██                            
                                    ██▒▒▒▒▒▒██                              
                                  ██▒▒▒▒▒▒██                                
                                ▒▒▒▒▒▒▒▒▓▓░░                                
                              ██▒▒▒▒▒▒██                                    
                            ▓▓▒▒▒▒▒▒██                                      
                          ██▒▒▒▒▒▒██                                        
                        ██▒▒▒▒▒▒██                                          
                      ▒▒▒▒▒▒▒▒▓▓░░                                          
                    ██▒▒▒▒▒▒██░░                                            
                  ▓▓▒▒▒▒▒▒██                                                
                ██▒▒▒▒▒▒██                                                  
              ██▒▒▒▒▒▒██                                                    
            ▒▒▓▓▒▒▒▒██░░                                                    
          ██▒▒▒▒▒▒██░░                                                      
        ▓▓▒▒▒▒▒▒██                                                          
      ██▒▒▒▒▒▒██                                                            
    ██▒▒▒▒▒▒██                                                              
  ▒▒▓▓▒▒▒▒▓▓░░                                                              
    ██▒▒██░░                                                                
      ██                                                                    
""")
            except Exception:
                print("========[>")
            print("\nA basic wooden spear. It's nothing special, but it's a lot more effective than using the shard of glass.")
            if gameBeat is False:
                print("\n       Attack +2\n         Defence +0\n")
                damage = damage + 2
                time.sleep(1)
                afterMathStats()
            else:
                afterMathStats()
    elif area == 2:
        defeatedGuardOutsideConfinement=True
        try:weapon = int(input("\nThe guard drops a wooden shield. Pick it up?\n1] Yes\n2] No\n-->  "))
        except ValueError:
            print("\nOnly integers can be entered here!")
            weapon=1
        if weapon == 1:
            print("You obtained a Wooden Shield! \n")
            try:print(r"""                ██████                
              ██▒▒▒▒▒▒██              
          ████  ▒▒▒▒▒▒  ████          
      ████      ▒▒▒▒▒▒      ████      
  ████          ▒▒▒▒▒▒          ████  
██              ▒▒▒▒▒▒              ██
██              ▒▒▒▒▒▒              ██
██              ▒▒▒▒▒▒              ██
██              ▒▒▒▒▒▒              ██
██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
  ██            ▒▒▒▒▒▒            ██  
  ██            ▒▒▒▒▒▒            ██  
  ██            ▒▒▒▒▒▒            ██  
  ██            ▒▒▒▒▒▒            ██  
    ██          ▒▒▒▒▒▒          ██    
    ██          ▒▒▒▒▒▒          ██    
      ██        ▒▒▒▒▒▒        ██      
        ██      ▒▒▒▒▒▒      ██        
          ██    ▒▒▒▒▒▒    ██          
            ██  ▒▒▒▒▒▒  ██            
              ████▒▒████              
                  ██                  
""")
            except Exception:
                print("""      |`-._/\_.-`|
      |    ||    |
      |___o()o___|
      |__((<>))__|
      \   o\/o   /
       \   ||   /
        \  ||  /
         '.||.'
           ``""")
            if gameBeat is False:
                print("\nA basic wooden shield. Chips and cracks adorn the surface, but it should still offer some protection in a pinch.")
                print("\n       Attack +0\n         Defence +2\n")
                afterMathStats()
            else:
                afterMathStats()
        elif weapon == 2:
            print("\nYou did not pick up the shield.")
            outsideConfinement()
    elif area == 3:
        try:weapon=int(input("\nThe guard drops a loaf of bread. Pick it up?\n1] Yes \n2] No\n--> "))
        except ValueError:
            print("\nOnly integers can be entered here!")
            weapon=1
        if weapon == 1:
            print("\nYou pick up the load of bread! In desperate need of nourishment, you gulp it down.\n")
            try:print(r"""                                                                                        
                                                                                        
                                                                                        
                                                                                        
                                                                                        
            ░░                                                                    ░░    
                                ██████████                                              
                            ██████████████████                                          
                          ██████████████████████                                        
                          ██████████████░░░░████████                                    
                          ████████████░░░░██████░░▒▒██                                  
                          ██████████░░░░██████░░░░▒▒██                                  
                          ██████████░░██████░░░░░░▒▒██                                  
                          ██████████░░████░░░░░░░░▒▒██                                  
                          ██████████░░████░░░░░░░░▒▒██                                  
                            ████████░░████░░░░░░▒▒░░░░████                              
                              ██████░░██░░░░░░▒▒░░░░░░░░░░████                          
                                  ██░░██░░▒▒▒▒░░░░░░░░░░░░░░░░██                        
                                      ██▒▒▒▒░░░░░░░░░░░░░░░░████                        
                                        ██████░░░░░░░░░░░░██████                        
                                          ████████░░░░░░██████                          
                                              ██████████████                            
                                                ░░████████                              
                                                                                        
                                                                                        
                                                                                        
                                                                                        
                                                                                        
                                                                                        
""")
            except Exception:
                print("""    _______
   /       )
  /_____   | 
 (  '   ) /   
  |.  '| /      
  |____|/""")
            time.sleep(1)
            print("\nHealth has been fully restored!\n")
            playerHealth=playerMaxHealth
            time.sleep(1)
            fightSecond()
        else:
            print("\nYou did not pick up the loaf of bread.\n")
            time.sleep(1)
            fightSecond()
    elif area == 4:
        try:weapon = int(input("\nThe guard drops a rusty sword. Pick it up?\n1] Yes \n2] No\n--> "))
        except ValueError:
            print("\nOnly integers can be entered here!")
            weapon=1
        if weapon == 1:
            print("\nYou obtained a rusty sword! \n")
            try:print(r"""                          ██████
                        ██░░░░██
                      ██░░░░░░██
                    ██░░░░░░██  
                  ██░░░░░░██    
                ██░░░░░░██      
    ██        ██░░░░░░██        
  ██░░██    ██░░░░░░██          
  ██░░░░████░░░░░░██            
    ██░░░░██░░░░██              
      ████▒▒████                
    ██▒▒▒▒██░░██                
  ██░░██▒▒██░░░░██              
██░░░░░░██  ██░░░░██            
██░░░░██      ████              
██████                          
""")
            except Exception:
                print(r""" _          /~~>________________________________________
/ \////////|   \..................................~~~~~---_
\_/\\\\\\\\|   /__________________________________-----~~~
            \__>     
            """)
            time.sleep(2)
            if gameBeat is False:
                print("\nA well used sword. It's a little rusty, but should still offer some decent attack power.")
                print("\n       Attack +3\n         Defence +0\n")
                damage=damage+3
                time.sleep(1)
                afterMathStats()
            else:
                afterMathStats()
        else:
            print("\nYou did not pick up the sword.\n")
            defeatedHighRank()
    elif area == 5:
        try:weapon=int(input("\nThe guard drops a Hyper Potion. Pick it up?\n1] Yes\n2] No\n--> "))
        except ValueError:
            print("\nOnly integers can be entered here!")
            weapon=0
        if weapon==1:
            print("\nYou obtained the Hyper Potion!\n")
            try:print(r"""                                                                                        
                                                                                        
                                                                                        
                                                                                        
                                                                                        
                                                                                        
                                             ░░                                  
                                         ░░                              
                                               ░░                                  
                                        ██████████                            
                                          ██  ██                              
                                          ██░░██                              
                                          ██  ██                              
                                          ██  ██                              
                                        ██░░    ██                            
                                        ██    ░░██                            
                                      ██  ░░      ██                          
                                      ██░░░░░░░░░░██                          
                                    ██░░░░░░░░░░░░░░██                        
                                    ██░░░░░░░░░░░░░░██                        
                                  ██░░░░░░░░░░░░░░░░░░██                      
                                  ██░░░░░░░░░░░░░░░░░░██                      
                                    ██████████████████                        
                                                                                        
                                                                                        
                                                                                        
                                                                                        
                                                                                        
                                                                                        
""")
            except Exception:
                print("""      .  .          
      o .  .        
      . O o .     
     O  .  .         
       o O.           
        o o .         
      aaaaaaaa        
      "8. o 8"       
       8 O .8        
       8 o .8        
       8. O 8        
       8 o. 8        
    ,adP O .Yba,     
   dP". O  o  "Yb    
  dP' O . o .O `Yb   
  8^^^^^^^^^^^^^^8   
  8              8  
  Yb,          ,dP 
   "Ya,______,rP'""")
            time.sleep(2)
            print("\nA rare item that can only be used in battles. Temporarily boosts attack power to 25, regardless of previous stats.")
            hyperPotion=True
            if hyperpotionQuantity==0:
                hyperpotionQuantity=1
            defeatedSecondGuard()
        else:
            print("\nYou didn't pick up the potion.\n")
            defeatedSecondGuard()
    elif area == 6:
        try:weapon=int(input("\nThe guard drops a rusty chestplate. Pick it up?\n1] Yes\n2] No\n--> "))
        except ValueError:
            battleAfterMath()
        if weapon==1:
            print("\nYou obtained the rusty chestplate!\n")
            print(r"""
          .=='\   /`==.
        .'\ # (`:')  #/`.
      _/_ |_.-' : `-._|__\_
     <___>'\ ## :   / `<___>
           >=======<
          /  ,-:-. #\
         |__/v^v^v\__|""")
            time.sleep(2)
            if gameBeat is False:
                print("\nA well-worn chestplate. It's clearly seen many battles and has lost some protection as a result, but it's still got some life left in it.")
                print("\n       Attack +0\n         Defence +3\n")
                time.sleep(1)
                playerMaxHealth = playerMaxHealth+3
                afterMathStats()
            else:
                afterMathStats()
        else:
            print("\nYou did not pick up the chestplate.\n")
            courtyardGuardDefeated()
    elif area==7:
        try:weapon=int(input("\nThe guard drops a Potion of Healing. Pick it up?\n1] Yes\n2] No\n--> "))
        except ValueError:
            battleAfterMath()
        if weapon==1:
            print("\nYou obtained the Potion of Healing!\n")
            time.sleep(1)
            try:
                print(r"""                                                                                                                                                              
                                              ░░                                                  
                                          ░░                                                      

                                        ██████████                                      
                                          ██  ██                                      
                                          ██  ██                                          
                                          ██  ██                                            
                                          ██  ██                                             
                                          ██  ██                                         
                                        ██  ░░  ██                                       
                                      ██          ██                                 
                                    ██        ░░    ██                            
                                    ██  ░░          ██                          
                                    ██░░░░░░░░░░░░░░██                           
                                    ██░░░░░░░░░░░░░░██                    
                                      ██░░░░░░░░░░██                       
                                        ██████████                              

            """)
            except Exception:
                print("""      _____
                 `.___,'
                  (___)
                  <   >
                   ) (
                  /`-.\  
                 /     \ 
                / _    _\ 
               :,' `-.' `:
               |         |
               :         ;
                \       /
                 `.___.'""")
            time.sleep(2)
            print("\nAn item that can only be used during battles. One sip of this, and health will be fully restored instantly!\n")
            defeatedChapterSevenGuard=True
            healingPotion=True
            healingpotionQuantity=healingpotionQuantity+1
            time.sleep(1.5)
            print("You return to the previous area where the paths split.")
            chapterSevenSplit()
        else:
            print("\nYou did not pick up the potion.")
            time.sleep(1.5)
            print("\nYou return to the area where the paths split, in order to evaluate your other options.")
            defeatedChapterSevenGuard=True
            time.sleep(1.5)
            chapterSevenSplit()



def musicBattle():
    global musicStop
    global muteAudio
    global noPyGame
    global musicLoop
    global usedSmoke
    global highRank
    global died, area
    if musicLoop != True and muteAudio != True and noPyGame != True:
        try:pygame.mixer.music.load('sfx/battle.mp3')
        except pygame.error:
            pass
        try:pygame.mixer.music.play(999)
        except pygame.error:
            if muteAudio != True:
                pass
        musicLoop=True
        fightGuard()
    elif noPyGame == True:
        if muteAudio != True:
            pass
    if musicStop is True:
        if not muteAudio:
            pygame.mixer.music.fadeout(30)
        musicStop = False
        musicLoop = False
        if died == True:
            died=False
            gameOver()
        elif usedSmoke is True:
            usedSmoke=False
            if area == 1:
                choice2Alternate()
            elif area == 2:
                outsideConfinement()
            elif area == 3:
                print("\nYou rush back to your previous hiding spot.")
                hidingChoice()
            elif area == 4:
                print("\nYou scurry back to the closet you were previously in.")
                closet()
            elif area == 5:
                print("\nYou rush back to your previous hiding spot.")
                hidingChoice()
            elif area == 6:
                print("\nYou scurry back up the path you came down, back towards the fountain.")
                courtyard()
            elif area == 7:
                chapterSevenSplit()
        else:
            battleAfterMath()
        #Don't even ask how I got this to work, I don't have a clue. Frankly I'm scared to even look at it in case I
        #mess it up somehow.


def fightGuard():
    global playerMaxHealth, playerHealth, originalGuardHealth
    global choice
    global weapon
    global area
    global damage
    global attack
    global musicLoop
    global playBattleTheme
    global highRank
    global musicStop
    global usedHyperPotion, originalDamage, originalHealth, testHP, guardDamage, usedSmoke
    guardHeldItem="null"
    if usedHyperPotion >= 1:
        usedHyperPotion=usedHyperPotion+1
    if debug !=0:
        print("usedHP=",usedHyperPotion)
    if usedHyperPotion==5:
        time.sleep(0.5)
        print("\nThe effects of the Hyper Potion have worn off! Attack and defense levels have been reverted back to their original values.\n")
        time.sleep(1)
        if originalDamage==7:
            damage=7
        else:
            damage=5
        if playerMaxHealth==22:
            playerHealth=22
        else:
            playerHealth=20
    if debug !=0:
        print(area)
        print("damage",damage)
        print("playermaxhealth",playerMaxHealth)
        print(musicStop)
    musicBattle()
    if area==2 and savePoint==0:
        area=area-1
    global guardHealth
    try:choice=int(input("What will you do? \n1] Attack \n2] Examine \n3] Use item\n4] Run\n--> "))
    except ValueError:
        print(" \nOnly integers are allowed!\n ")
        fightGuard()
    if choice==1:
        guardHealth-damage
        print(" \nYou attack the guard and deal",damage,"damage!\n")
        time.sleep(1)
        guardHealth=guardHealth-damage
        if guardHealth < 0:
            guardHealth=0
        print("The guard has",guardHealth,"health remaining.\n ")
        if guardHealth <=0:
            print("You are victorious!")
            musicStop=True
            time.sleep(1)
            musicLoop=False
            if testHP is True:
                ass=int(input("\n==testHP==\nStart a new battle?\n1] Yes\n2] No\n--> "))
                if ass == 1:
                    encounterGuard()
                else:
                    print("\n==testHP==\nTest completed successfully!\n")
                    menu()
            musicBattle()
        else:
            if highRank == True:
                highGuardAttack()
            else:
                guardAttack()
    elif choice==4:
        escapeChance=random.randint(1,10)
        if debug != 0:
            print(escapeChance)
        if escapeChance==1 or escapeChance==2 or debug !=0:
            print("\nYou manage to escape!")
            usedSmoke=True
            musicStop=True
            musicBattle()
            if area ==1:
                choice2Alternate()
            elif area == 2:
                outsideConfinement()
            elif area == 3:
                print("\nYou rush back to your previous hiding spot.")
                hidingChoice()
            elif area == 4:
                print("\nYou scurry back to the closet you were previously in.")
                closet()
            elif area == 5:
                print("\nYou rush back to your previous hiding spot.")
                hidingChoice()
            elif area == 6:
                print("\nYou scurry back up the path you came down, back towards the fountain.")
                courtyard()
            elif area == 7:
                chapterSevenSplit()
        else:
            print("\nThe guard blocks your path!")
            time.sleep(1)
            if highRank is True:
                highGuardAttack()
            else:
                guardAttack()
    elif choice==3:
        print("\n== INVENTORY ==")
        inventory()
    elif choice==2:
        if highRank is True:
            print("\nHIGH RANKING GUARD:\nAttack: 7\nDefence: "+str(guardHealth)+"/"+str(originalGuardHealth)+"\nHolding: ???\n\nThe High Ranking Guard towers above you.\n")
            time.sleep(0.6)
            fightGuard()
        else:
            print("\nGUARD:\nAttack: "+str(guardDamage)+"\nDefence: "+str(guardHealth)+"/"+str(originalGuardHealth)+"")
            if area==1:
                guardHeldItem="Wooden spear"
            elif area==2:
                guardHeldItem="Wooden shield"
            elif area==3:
                guardHeldItem="Loaf of bread"
            elif area==4:
                guardHeldItem="Rusty sword"
            elif area==5:
                guardHeldItem="Hyper Potion"
            elif area==6:
                guardHeldItem="Rusty chestplate"
            elif area==7:
                guardHeldItem="Potion of Healing"
            print("Holding:",guardHeldItem)
            time.sleep(0.2)
            print("\nThe Guard stares you down menacingly.\n")
            time.sleep(0.6)
            fightGuard()
    else:
        print("I don't understand")
        fightGuard()

def encounterGuard():
    global muteAudio, damage, guardDamage, originalGuardHealth
    if muteAudio != True:
        s=pygame.mixer.Sound("sfx/encounter.wav")
        empty_channel = pygame.mixer.find_channel()
        empty_channel.play(s)
    global damage
    global guardHealth
    guardHealth=20
    if damage==7:
        guardHealth=guardHealth+3
    if damage == 7:
        guardDamage = 6
    elif highRank==True:
        guardDamage=7
    else:
        guardDamage=5
    if debug != 0:
        print(guardDamage)
    originalGuardHealth=guardHealth
    print(" ")
    print("""=======
*FIGHT!*
=======""")
    time.sleep(1.1)
    print(" \nYou've encountered a guard!\n ")
    time.sleep(1)
    print(r"""  ,^.
  |||
  |||       _T_
  |||   .-.[:|:].-.
  ===_ /\|  "'"  |/
   E]_|\/ \--|-|''''|
   O  `'  '=[:]| R  |
          /''''|  P |
         /'''''`.__.'
        []"/'''\"[]
        | \     / |
        | |     | |
      <\\\)     (///>""")
    time.sleep(1.45)
    fightGuard()

def encounterHighRank():
    global damage
    global highRank
    global guardHealth
    if muteAudio != True:
        s = pygame.mixer.Sound("sfx/encounter.wav")
        empty_channel = pygame.mixer.find_channel()
        empty_channel.play(s)
    guardHealth = 20
    if damage == 7:
        guardHealth = guardHealth + 3
    print(" ")
    originalGuardHealth=guardHealth
    print("""=======
*FIGHT!*
=======""")
    time.sleep(1)
    print(" \nYou've encountered a high ranking guard!\n ")
    time.sleep(1)
    print(r"""                                  __*       
                                  \/        
                                  P3        
                                  ||        
                   @@@@      _T_  /\;        
                  @||||@ .-.[:|:]^\/         
                    \||/ /\|  "'" \/          
                      E]_|\/ \--|--/           
                    "  `'  '=[:]='           
                           /'''''\           
                          /''''''''\          
                        []''/''''\'[]         
                         | \     / |         
                         | |     | |         
         ~~~~~~~~~~~~~~<\\\)~~~~~(///>~~~~~~~~~~~~~ rp""")
    highRank=True
    time.sleep(1.45)
    fightGuard()

def inventory():
    global item
    global musicStop
    global playerHealth
    global playerMaxHealth
    global damage
    global gotRope
    global gotstring
    global smokescreen
    global area
    global usedSmoke
    global healingPotion
    global usedHyperPotion, hyperPotion
    global originalDamage, originalHealth, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, engagedJuniperFight
    print("Use what item?")
    print("===============================")
    if smokescreen == True and smokescreenQuantity > 0:
        print("1] Smokescreen  x"+str(smokescreenQuantity))
    else:
        print("1] ????")
    if healingPotion==True and healingpotionQuantity > 0:
        print("2] Potion of Healing  x"+str(healingpotionQuantity))
    else:
        print("2] ????")
    if hyperPotion==True and hyperpotionQuantity > 0:
        print("3] Hyper Potion  x"+str(hyperpotionQuantity))
    else:
        print("3] ????")
    print("===============================")
    print("4] Close inventory")
    try:inv=int(input("--> "))
    except ValueError:
        print("\nOnly integers can be entered here!\n")
        inventory()
    if inv==1 and smokescreen == False:
        print("There is no held item in inventory slot 1!\n")
        inventory()
    elif inv == 1 and smokescreen == True and engagedJuniperFight == False:
        print("You used the smokescreen!")
        time.sleep(1)
        print("\nThe battlefield is engulfed in a thick cloud of smoke!\n")
        time.sleep(0.4)
        print("""                _                                  
              (`  ).                   _           
             (     ).              .:(`  )`.       
)           _(       '`.          :(   .    )      
        .=(`(      .   )     .--  `.  (    ) )      
       ((    (..__.:'-'   .+(   )   ` _`  ) )                 
`.     `(       ) )       (   .  )     (   )  ._   
  )      ` __.:'   )     (   (   ))     `-'.-(`  ) 
)  )  ( )       --'       `- __.'         :(      )) 
.-'  (_.'          .')                    `(    )  ))
                  (_  )                     ` __.:'      """)
        time.sleep(2)
        print("\nYou use this to your advantage and slip away unnoticed, escaping completely unharmed!\n")
        time.sleep(1)
        musicStop=True
        usedSmoke=True
        smokescreenQuantity=smokescreenQuantity-1
        if smokescreenQuantity < 0:
            smokescreenQuantity=0
        if smokescreenQuantity <= 0:
            smokescreen=False
        musicBattle()
    elif inv == 1 and smokescreen == True and engagedJuniperFight == True:
        print("That item can't be used here!\n")
        inventory()
    elif inv==2 and healingPotion == False:
        print("There is no held item in inventory slot 2!\n")
        inventory()
    elif inv==2 and healingPotion==True:
        print("\nYou take a sip of the Potion of Healing, instantly revitalizing you and restoring your health!\n")
        #healingPotion=False
        time.sleep(1)
        #if playerMaxHealth==20:
        #    playerHealth=20
        #elif playerMaxHealth==22:
        #    playerHealth=22
        playerHealth=playerMaxHealth
        healingpotionQuantity=healingpotionQuantity-1
        if healingpotionQuantity < 0:
            healingpotionQuantity=0
        if healingpotionQuantity <= 0:
            healingPotion=False
        if highRank is True:
            highGuardAttack()
        elif engagedJuniperFight is True:
            juniperAttack()
    elif inv==3 and hyperPotion==False:
        print("There is no held item in inventory slot 3!\n")
        inventory()
    elif inv==3 and hyperPotion==True and engagedJuniperFight == False:
        print("\nYou take a sip of the Hyper Potion! You can immediately feel it's power coursing through you. Attack and defence levels have temporarily been raised to 25!\n")
        time.sleep(2)
        originalDamage=damage
        originalHealth=playerHealth
        print(originalDamage, originalHealth)
        damage=25
        playerHealth=25
        usedHyperPotion=1
        #hyperPotion=False
        hyperpotionQuantity=hyperpotionQuantity-1
        if hyperpotionQuantity < 0:
            hyperpotionQuantity=0
        if hyperpotionQuantity <= 0:
            hyperPotion=False
        if highRank is True:
            highGuardAttack()
        else:
            guardAttack()
    elif inv == 3 and hyperPotion == True and engagedJuniperFight == True:
        print("That item can't be used here!\n")
        inventory()
    else:
        print(" ")
        if engagedJuniperFight is False:
            fightGuard()
        else:
            fightJuniper()

def restartGameOver():
    global savePoint, engagedJuniperFight
    global muteAudio
    if debug > 0:
        print(savePoint)
    try:restart = int(input("Continue from last checkpoint? \n1] Yes\n2] No\n--> "))
    except ValueError:
        print("\nBad input. Only integers can be entered here!\n")
        restartGameOver()
    if restart == 1:
        if muteAudio!=True:
            pygame.mixer.music.stop()
        if savePoint == 1:
            choice4()
        elif savePoint == 2:
            escape()
        elif savePoint == 3:
            backInside()
        elif savePoint == 4:
            chapterFive()
        elif savePoint == 5:
            chapterSix()
        elif savePoint == 6:
            chapterSeven()
        elif savePoint == 7:
            chapterEight()
        elif engagedJuniperFight is True:
            chapterEight()
        else:
            area1()
    elif restart == 2:
        pygame.mixer.music.stop()
        savePoint == 0
        menu()
    else:
        print("Sorry, that doesn't compute! Try again.")
        print(" ")
        restartGameOver()

def gameOver():
    global mute, playerHealth, playerMaxHealth
    playerHealth=playerMaxHealth
    if not muteAudio:
        pygame.mixer.music.load("sfx/gameover.wav")
        pygame.mixer.music.play(1)
    time.sleep(1)
    print(" ")
    print("Your mission is failed! As you lay dying on the ground, you think of all of the innocent people that you didn't manage to save...")
    time.sleep(2.55)
    print(" ")
    try:print(r""" ▄▀▀▀▀▄    ▄▀▀█▄   ▄▀▀▄ ▄▀▄  ▄▀▀█▄▄▄▄                   
█         ▐ ▄▀ ▀▄ █  █ ▀  █ ▐  ▄▀   ▐                   
█    ▀▄▄    █▄▄▄█ ▐  █    █   █▄▄▄▄▄                    
█     █ █  ▄▀   █   █    █    █    ▌                    
▐▀▄▄▄▄▀ ▐ █   ▄▀  ▄▀   ▄▀    ▄▀▄▄▄▄                     
▐         ▐   ▐   █    █     █    ▐                     
                  ▐    ▐     ▐                          
                 ▄▀▀▀▀▄   ▄▀▀▄ ▄▀▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄ 
                █      █ █   █    █ ▐  ▄▀   ▐ █   █   █ 
                █      █ ▐  █    █    █▄▄▄▄▄  ▐  █▀▀█▀  
                ▀▄    ▄▀    █   ▄▀    █    ▌   ▄▀    █  
                  ▀▀▀▀       ▀▄▀     ▄▀▄▄▄▄   █     █   
                                     █    ▐   ▐     ▐  """)
    except Exception:
        pass
    restartGameOver()

def chapter5Chest():
    global smokescreen, searchedChest5, smokescreenQuantity
    try:choice = int(input("After a short period of walking, you come to a chest. Search it? ([1] Yes, [2] No) "))
    except ValueError:
        chapter5Chest()
    if choice == 1:
        try:choice2 = int(input("\nYou search the chest. Inside you find a smokescreen. Take it? \n1] Yes\n2] No\n--> "))
        except ValueError:
            chapter5Chest()
        if choice2 == 1:
            if searchedChest5 != True:
                print("\nYou obtained the smokescreen!\n")
                print("""                       .')             _
                          (_  )        .+(`  ) ) --:--
                _                     :(    ) )
            .:(`  )  ) --        .--  `.  (    ) )  - --
           :(      )           .(   )   ` __.:'
    `.     `(       ) )       (      )
      )      ` __.:'   ))--- (       )) ----      _
    )  ) --         --'  _    `- __.'         .=(`  )
    .-'                (`  ).                :(      )
                     (       '`. .  --       `(       ) ) ) ----
                     (         ) ) ---         ` __.:'
                      ` __.:'-'""")
                time.sleep(2)
                print(
                    "\n\nAn item that can only be used in battles. Cloaks the battlefield in a veil of smoke, allowing you to swiftly exit! Grants a 100% chance of escaping unharmed.")
                time.sleep(1)
                smokescreen = True
                smokescreenQuantity=smokescreenQuantity+1
                searchedChest5 = True
                print("\nConfident there is nothing of value in the chest, you head back along the corridor.")
                time.sleep(2)
                chapter5Corridor()
            else:
                print(
                    "\nThis chest has already been searched, and there is nothing of value contained within. Disappointed, you head back along the corridor.")
                time.sleep(1)
                chapter5Corridor()
        else:
            print("You did not take the smokescreen. You return to the previous area empty-handed.")
            chapter5Corridor()

def chest8():
    global healingPotion, healingpotionQuantity, searchedChest8
    try: choice=int(input("\nYou rummage around the chest. Inside, you find a Potion of Healing. Take it?\n1] Yes\n2] No\n--> "))
    except ValueError:
        chest8()
    if choice==1:
        print("\nYou obtained the Potion of Healing!\n")
        time.sleep(1)
        try:
            print(r"""                                                                                                                                                              
                                          ░░                                                  
                                      ░░                                                      

                                    ██████████                                      
                                      ██  ██                                      
                                      ██  ██                                          
                                      ██  ██                                            
                                      ██  ██                                             
                                      ██  ██                                         
                                    ██  ░░  ██                                       
                                  ██          ██                                 
                                ██        ░░    ██                            
                                ██  ░░          ██                          
                                ██░░░░░░░░░░░░░░██                           
                                ██░░░░░░░░░░░░░░██                    
                                  ██░░░░░░░░░░██                       
                                    ██████████                              

        """)
        except Exception:
            print("""      _____
             `.___,'
              (___)
              <   >
               ) (
              /`-.\  
             /     \ 
            / _    _\ 
           :,' `-.' `:
           |         |
           :         ;
            \       /
             `.___.'""")
        time.sleep(2)
        print(
            "\nAn item that can only be used during battles. One sip of this, and health will be fully restored instantly!\n")
        healingPotion = True
        searchedChest8 = True
        healingpotionQuantity = healingpotionQuantity + 1
        time.sleep(1)
        print("\nYou return to your previous position, in front of the door.")
        time.sleep(1.5)
        chapterEightChoice()
    else:
        print("\nYou did not take the Potion of Healing. You wander back over to your previous position before the door.")
        time.sleep(1.5)
        chapterEightChoice()

def postCredits():
    if not muteAudio:
        pygame.mixer.music.load("sfx/curtain_call.mp3")
        pygame.mixer.music.play(0)
    print("\n== CONGRATULATIONS! ==")
    print("Well done for overcoming the challenge and beating the game! The future of Medway may be uncertain, but it's sure to be prosperous with\nEmperor Juniper gone. I hope you enjoyed playing the game as much as I enjoyed making it!")
    time.sleep(2)
    print("\nOh, one last thing - as a reward for beating the game, you've now unlocked some cool extras! Check it out:")
    time.sleep(1)
    print("\nUNLOCKED: Music Player mode - listen to the game's soundtrack, in addition to some never-before-heard beta tracks!")
    time.sleep(0.5)
    print("UNLOCKED: Chapter Replay - You can now warp to specific chapters whenever you want! See how many secrets you can discover!")
    time.sleep(0.5)
    print("\nTo take advantage of these new features, simply load this save from the main menu. (Saves that you beat the game under are marked\nwith a '*' symbol!)")
    time.sleep(0.7)
    print("\nHey, thanks for playing the game! When I started to program this, I honestly had no idea it'd ever get this big. None of this would be\npossible without the continued support of the amazing people in the credits!\n")
    time.sleep(0.5)
    choice=input("\nPress [Enter] to continue... ")
    if choice=="":
        time.sleep(0.5)
        if not muteAudio:
            pygame.mixer.music.fadeout(200)
        print(" ")
        menu()
    else:
        time.sleep(0.5)
        if not muteAudio:
            pygame.mixer.music.fadeout(200)
        print(" ")
        menu()


def DTDCredits():
    global muteAudio, creditsRolled, gameBeat, playerHealth, playerMaxHealth
    if not muteAudio:
        if not gameBeat:
            try:
                pygame.mixer.music.load("sfx/ambient.wav")
                pygame.mixer.music.play(1)
            except Exception:
                pass
        elif gameBeat is True:
            try:
                pygame.mixer.music.load("sfx/ambient_percussion.wav")
                pygame.mixer.music.play(1)
            except Exception:
                pass
    print("\n\n\n== DEATHTRAP DUNGEON ==")
    time.sleep(4.5)
    print("\nLead game design: Reuben Parfrey")
    time.sleep(2.5)
    print("\nSoundtrack director: Charly Sly")
    time.sleep(2.5)
    print("\nPlay tester: Joe Parfrey")
    time.sleep(2.5)
    print("\nLogo design/imagery: Charly Sly")
    time.sleep(2.5)
    print("\nStory: Reuben Parfrey")
    time.sleep(2.5)
    print("\nCode: Reuben Parfrey")
    print("      Stephen Chapple")
    time.sleep(2.5)
    print("\nSpecial thanks to: The stars over at Stack Overflow")
    print("                   Textart.sh for providing some of the game's graphics")
    print("                   My family and friends for the encouragement (and the many, many cups of tea)")
    print("                   Georgia Wales, for the kind words (and for generally being amazing)")
    time.sleep(2.5)
    print("\nDedicated to Mr. Chapple; so much of this game was inspired by you. Rest in peace.")
    time.sleep(5)
    creditsRolled=True
    choice=input("\n\nPress [Enter] to continue... ")
    if choice==" ":
        if not muteAudio:
            pygame.mixer.music.fadeout(1000)
        gameBeat=True
        playerHealth=playerMaxHealth
        time.sleep(1)
        askSave()
    else:
        if not muteAudio:
            pygame.mixer.music.fadeout(1000)
        gameBeat=True
        playerHealth=playerMaxHealth
        time.sleep(1)
        askSave()

def juniperAfterMath():
    #code after beating juniper goes here!
    print("\nYou stand dazed, confused, wounded, shaken... but alive.")
    time.sleep(3)
    print("\nEmperor Juniper lies on the floor, mortally wounded. He coughs and splutters, then begins to talk...")
    time.sleep(3)
    print("\n'...The power... I wanted it...'")
    time.sleep(3)
    print("\n'...I saw other leaders being overthrown... being... used.'")
    time.sleep(3)
    print("\n'I... I couldn't lose my... power.'")
    time.sleep(3)
    print("\n'So... so I exerted the ultimate control... to secure my power... my legacy...'")
    time.sleep(3)
    print("\n'...But... what use is any of that... in the grand scheme of things...?'")
    time.sleep(3)
    print("\n'...One day... everyone will forget your name...'")
    time.sleep(3)
    print("\nThe Emperor's eyes roll back into his head; he smiles one last time, then grows still. ")
    time.sleep(3)
    print("\nYou stand there, in total shock. Everything is silent.")
    time.sleep(3)
    print("\nYou snap back to reality. You glance back and forth between your own bloodied hands and the Emperor. He's still motionless.")
    time.sleep(3)
    print("\nSomberly, you trudge back from the way you came. To release the other inmates, and then, whatever follows.")
    time.sleep(3)
    print("\nYou're shaken and wounded, the future of Medway is uncertain. But you're alive.")
    time.sleep(4)
    DTDCredits()

def juniperMusic():
    global musicStop
    global muteAudio
    global noPyGame
    global musicLoop
    global usedSmoke
    global highRank
    global died, debug
    if musicLoop != True and muteAudio != True and noPyGame != True:
        try:pygame.mixer.music.load('sfx/puppets.mp3')
        except pygame.error as e:
            if debug != 0:
                print(e)
        if debug!=0:
            print("= music playing =")
        try:pygame.mixer.music.play(999)
        except pygame.error:
            if muteAudio != True:
                pass
        musicLoop=True
        fightJuniper()
    elif noPyGame == True:
        if muteAudio != True:
            pass
    if musicStop == True:
        pygame.mixer.music.fadeout(30)
        musicStop = False
        musicLoop = False
        if died == True:
            died=False
            gameOver()
        else:
            juniperAfterMath()

def juniperAttack():
    global guardDamage
    global damage
    global playerHealth
    global playerMaxHealth
    global died
    global musicStop
    global highRank
    print("Emperor Juniper attacks, dealing 8 damage!\n ")
    time.sleep(1)
    playerHealth = playerHealth - 8
    if debug == 1:
        print(playerHealth)
    if playerHealth < 0:
        playerHealth=0
    print("You have", playerHealth, "health remaining.\n")
    time.sleep(1)
    if playerHealth <= 0:
        print("Emperor Juniper is victorious! You fall to the ground in defeat...")
        if playerMaxHealth == 20:
            playerHealth = 20
        else:
            playerHealth = 22
        if debug != 0:
            print("playerHealth =", playerHealth)
        died = True
        musicStop = True
    else:
        fightJuniper()

def fightJuniper():
    global playerMaxHealth, playerHealth
    global weapon
    global area
    global damage
    global attack
    global guardHealth
    global usedHyperPotion, originalDamage, originalHealth, juniperHealth, juniperDamage, musicStop, playBattleTheme, musicLoop, healingpotionQuantity, healingPotion
    if usedHyperPotion >= 1:
        usedHyperPotion = usedHyperPotion + 1
    if debug != 0:
        print("fightJuniper")
    if usedHyperPotion != 0:
        time.sleep(0.5)
        print("\nThe effects of the Hyper Potion have worn off! Attack and defense levels have been reverted back to their original values.\n")
        time.sleep(2)
        if originalDamage == 7:
            damage = 7
        else:
            damage = 5
        if playerMaxHealth == 22:
            playerHealth = 22
        else:
            playerHealth = 20
    juniperMusic()
    try:
        choice = int(input("What will you do? \n1] Attack \n2] Examine \n3] Use item\n4] Run\n--> "))
    except ValueError:
        fightJuniper()
    if choice == 1:
        print(" \nYou attack Emperor Juniper and deal", damage, "damage!\n")
        time.sleep(1)
        juniperHealth = juniperHealth - damage
        if juniperHealth < 0:
            juniperHealth=0
        print("Emperor Juniper has", juniperHealth, "health remaining.\n ")
        time.sleep(1)
        if juniperHealth <= 0:
            print("You are victorious!")
            musicStop = True
            time.sleep(1)
            musicLoop = False
            juniperMusic()
        else:
            juniperAttack()
    elif choice == 4:
        print("\nThere's no running from this battle!\n")
        fightJuniper()
    elif choice == 3:
        print("\n== INVENTORY ==")
        inventory()
    elif choice == 2:
        print("\nEMPEROR JUNIPER:\nAttack: "+str(juniperDamage)+"\nDefence: "+str(juniperHealth)+"/"+str(originalGuardHealth)+"\nHolding: Samurai sword\n\nEmperor Juniper grins maniacally.\n")
        time.sleep(0.75)
        fightJuniper()
    else:
        fightJuniper()

def encounterJuniper():
    global muteAudio, damage, juniperDamage, juniperHealth, engagedJuniperFight, healingpotionQuantity, healingPotion, originalGuardHealth
    engagedJuniperFight = True
    if not muteAudio:
        s = pygame.mixer.Sound("sfx/encounter.wav")
        empty_channel = pygame.mixer.find_channel()
        empty_channel.play(s)
    print("""\n=======
*FIGHT!*
=======""")
    time.sleep(1.1)
    print(" \nEmperor Juniper draws his sword!\n ")
    time.sleep(1)
    print(r"""                                                                                   
                                                          ▓▓                                                                                    
                                                          ▒▒██                ▒▒██                                                              
                                                          ▒▒██▓▓          ▓▓████  ▒▒░░    ░░                                                    
                                                          ▒▒▓▓▓▓░░██████▒▒▓▓██░░▒▒▒▒████▓▓██▓▓▒▒                                                
                                                          ▒▒▓▓▒▒▓▓▒▒▒▒████▒▒████▒▒▒▒▓▓▓▓▒▒▓▓████▒▒                                              
                                                            ██▓▓██████░░▒▒██░░                ░░▓▓                                              
                                                            ▒▒████████░░██▒▒▓▓░░▓▓▓▓          ████                                              
                                                          ████▓▓██████  ▒▒██▓▓▓▓████▓▓██      ▒▒▓▓                                              
                                                        ██▒▒▓▓████▒▒▓▓▓▓▓▓▒▒████▓▓▒▒████▒▒      ██▒▒██████                                      
                                                      ░░▓▓▒▒▒▒██▓▓▓▓██▓▓██▒▒▒▒██▓▓▒▒▓▓██▒▒▓▓░░    ▒▒████▓▓                                      
                                                    ▒▒▓▓▒▒██  ▒▒▒▒▒▒░░▒▒▒▒██▓▓▒▒░░████▒▒████▓▓░░          ░░                                    
                                                  ░░██▓▓▓▓▒▒  ▒▒    ▒▒▒▒  ▓▓▓▓░░████▓▓▓▓▓▓██████                                                
                                                ▓▓██▒▒██▓▓██        ░░    ░░██▒▒██▓▓██████████▒▒░░▓▓░░                                          
                                              ░░▓▓██▒▒████▓▓▒▒▓▓▒▒░░▓▓  ░░▒▒░░▒▒░░██▓▓██▓▓████▓▓▒▒░░▒▒▒▒                                        
                                            ░░▒▒▓▓████▒▒████▓▓██░░▒▒▓▓░░  ░░░░██▒▒▓▓████████▒▒  ▓▓░░▓▓░░                                        
                                          ▒▒▒▒▒▒▓▓██████▒▒████▓▓░░░░▓▓░░▓▓▒▒██▓▓░░██▓▓▓▓▓▓▒▒  ██  ██░░██                                        
                                        ▒▒▒▒  ▓▓░░██████▓▓▒▒▒▒▓▓  ░░▒▒▒▒░░██▒▒▒▒██░░▒▒▒▒▒▒░░██  ██  ██▒▒                                        
                                      ░░▒▒  ▓▓░░▒▒██▓▓▓▓████▒▒▒▒░░░░░░▒▒████▓▓██▒▒██▒▒  ▒▒▓▓  ██  ████                                          
                                      ░░  ▓▓░░  ▓▓░░██████░░██▒▒▓▓▓▓░░██▓▓▓▓▓▓██▓▓▓▓▒▒██░░  ██░░▓▓▒▒▓▓                                          
                                        ▓▓▒▒  ▓▓  ██░░██▓▓▓▓██▓▓██████████████▒▒████░░▒▒▒▒▓▓  ▓▓░░▓▓▓▓▓▓                                        
                                        ▒▒░░██░░▓▓░░▒▒░░▓▓████████████████▓▓▓▓██▓▓░░▓▓▓▓░░░░▓▓▒▒██▓▓████                                        
                                        ░░▓▓  ▓▓░░░░▓▓▓▓▒▒░░▓▓████████████▓▓▒▒  ░░████▓▓██  ██████▓▓██▓▓▒▒██                                    
                                        ▓▓▒▒▓▓░░░░▓▓░░████▓▓▒▒░░░░░░░░      ▒▒██▓▓██████  ████████▓▓████░░                                      
                                        ██▓▓░░▒▒▓▓░░▒▒██████▓▓██▓▓██████████▓▓████████  ████▓▓▓▓▓▓▓▓▓▓▒▒                                        
                                        ████▓▓▓▓▓▓████▒▒▒▒▓▓██████▓▓██████▓▓██▓▓██▓▓░░██▓▓▓▓██████▒▒▓▓░░                                        
                                      ░░████████▓▓▓▓██████▒▒▒▒████▓▓██████▓▓▓▓██▒▒▓▓▓▓████▓▓██▓▓░░██▒▒▒▒                                        
                                    ▒▒██▓▓██▓▓████▓▓██▓▓██████▓▓▒▒▓▓████████▓▓░░██▓▓▓▓████▓▓░░▓▓██▒▒▒▒▒▒                                        
                                            ▒▒██████████▓▓▓▓████████▓▓▒▒▓▓      ████████░░▓▓▓▓▓▓████░░  ▒▒                                      
                                                ░░▒▒▓▓██▓▓████▓▓████      ░░    ▒▒██░░▓▓████▓▓▓▓██  ▓▓▒▒  ▒▒                                    
                                              ▒▒░░▓▓  ▓▓░░░░▒▒▓▓▒▒██▓▓░░    ░░  ▒▒▒▒██▓▓▓▓▓▓██▓▓░░██  ░░  ▒▒                                    
                                            ▓▓░░██  ▓▓▒▒████░░▒▒██▓▓████░░  ░░  ██▒▒████████▒▒▒▒▓▓  ██▒▒                                        
                                        ▓▓██▒▒▒▒▒▒▓▓░░██▓▓▓▓██▒▒  ▒▒████░░  ██████░░████▓▓░░▓▓▓▓  ██░░▒▒██                                      
                                    ░░████▓▓▓▓▓▓▒▒▒▒░░██▓▓▒▒    ▒▒██▓▓▓▓██████▓▓██▒▒░░░░▒▒▓▓▓▓  ██░░░░████▒▒                                    
                                      ██▒▒████▒▒▓▓░░▓▓░░  ░░▓▓░░▒▒██▓▓████████████░░░░░░██▒▒  ▓▓▓▓░░██▒▒▒▒██                                    
                                      ▒▒▓▓████▓▓░░  ░░▒▒▓▓░░░░  ▒▒▒▒██▓▓▓▓▓▓▓▓▓▓▓▓░░▓▓▓▓▒▒  ▓▓▒▒▒▒██▓▓▓▓▓▓██                                    
                                  ░░██▒▒░░    ░░▓▓▓▓▒▒▓▓██▓▓██    ▒▒██▒▒░░▒▒████░░▒▒██░░░░██░░████▓▓▒▒████                                      
          ▓▓▒▒░░░░░░░░░░░░▒▒░░░░      ▒▒▓▓▓▓██▒▒░░██▓▓▒▒▓▓████  ░░▒▒████░░░░██▓▓  ░░██▓▓░░██████▓▓▓▓████                                        
                ░░▒▒░░░░░░░░▒▒▒▒░░▒▒████████████▒▒▒▒▓▓██▒▒░░░░▒▒▒▒▒▒██████▓▓██████░░████░░██▒▒▒▒██▓▓▓▓                                          
                                  ▒▒██████▓▓▓▓▒▒░░██▓▓██▒▒██████████▓▓▓▓▓▓▒▒▓▓▓▓▓▓░░▓▓██▓▓██▓▓██▓▓░░                                            
                                  ▒▒██████▓▓██████▓▓████▒▒▒▒▒▒▓▓████▒▒▓▓▓▓▓▓▒▒▓▓██░░▓▓██▓▓▒▒██░░▓▓▓▓▒▒                                          
                                    ██▓▓████▓▓▓▓██████▓▓▓▓██▓▓▓▓████▒▒▓▓████▒▒▒▒▓▓░░▓▓██▓▓▓▓████▓▓██                                            
                                    ░░▒▒▒▒████▓▓████████▒▒░░░░▒▒▒▒▓▓▓▓▓▓▓▓██████▓▓▒▒████▓▓████████                                              
                                        ██▒▒▓▓██████████▓▓██              ▓▓████████▓▓██▓▓▓▓████▓▓                                              
                                        ████▓▓▒▒██▓▓████▓▓▓▓                ▒▒██▓▓▓▓▓▓██▓▓██▓▓                                                  
                                        ██████░░▒▒▒▒▓▓▓▓░░                        ██████▒▒▓▓██                                                  
                                        ██▓▓██▒▒██▓▓                              ▒▒██▓▓▓▓▓▓██▒▒                                                
                                        ██████▒▒▓▓▒▒                                ████▓▓▓▓▓▓██                                                
                                        ██▓▓██▒▒▓▓                                  ░░██▓▓▓▓▒▒██▒▒                                              
                                        ██▓▓██▒▒██                                    ▓▓▓▓██████▓▓                                              
                                        ██████▒▒██                                      ██▓▓▓▓░░██▓▓                                            
                                        ▒▒▓▓▒▒░░▒▒                                      ░░▓▓██▒▒██▓▓                                            
                                      ▒▒██████▒▒██                                      ▒▒████▒▒▓▓██▒▒                                          
                                      ██▓▓██▒▒████                                      ████░░██████░░                                          
                                    ██▓▓▒▒▓▓▓▓▓▓▓▓░░                                    ▓▓████████                                              
                                  ████████████▓▓▒▒                                    ▓▓▓▓██████                                                
                                  ██████▓▓▒▒                                          ████████▒▒                                                
                                                                                        ░░                                                      
                                                                                                                                        """)
    time.sleep(1.5)
    juniperDamage=8
    #this section of code determines Juniper's health stats; the more experienced the player, the harder he is to beat.
    if healingPotion is True:
        if healingpotionQuantity==1:
            if damage==5:
                juniperHealth=20
            else:
                juniperHealth=27
        elif healingpotionQuantity==2:
            if damage==5:
                juniperHealth=25
            else:
                juniperHealth=30
        else:
            if damage==5:
                juniperHealth=27
            else:
                juniperHealth=32
    else:
        if damage==5:
            juniperHealth=15
        else:
            juniperHealth=20
    if debug!=0:
        print(engagedJuniperFight, juniperHealth)
    originalGuardHealth=juniperHealth
    fightJuniper()


def preShowdown():
    print("\nYou push on the door, and it creaks open. The loud squeal of the hinges makes you jump.")
    time.sleep(1.5)
    try:choice=int(input("\nProceed through the door? [1] Yes [2] No "))
    except ValueError:
        preShowdown()
    if choice==1:
        print("\nMustering up the courage, you fight the trembles and press on forward through the door, into the unknown...")
        time.sleep(1.5)
        print("\nYou find yourself in a huge room. Stony walls stretch upwards to a mossy ceiling. Torches cast an eerie flickering glow around the room.")
        time.sleep(1.5)
        print("\nHuge stone pillars line the interior of this room, and ivy creeps up all of them.")
        time.sleep(1.5)
        print("\nSuddenly, you freeze. In the center of this room is a raised section with a throne sitting proudly on top. On this throne, sits Emperor Juniper.")
        time.sleep(2)
        print("\nHe's unlike anything you've seen up until this point. His hair is unkempt and wild. His beard is a mess and is full of knots.")
        time.sleep(2)
        print("\nIn his hand he holds a samurai sword. His eyes dart around the room, dancing manically. He looks nothing like he used to; a shell of his former self.")
        time.sleep(2)
        print("\nA sickly grin adorns his face. You stand, mouth ajar, unsure what to think.")
        time.sleep(2)
        print("\nSuddenly, his eyes lock onto you. His expression changes; what used to be a maniacal grin is now a foreboding frown.")
        time.sleep(2)
        print("\nHe lets out a startling yell and points at you. You feel nauseous and your legs feel weak.")
        time.sleep(2)
        print("\nSwiftly, he leaps to his feet and charges at you. This is it.")
        time.sleep(2)
        encounterJuniper()
    else:
        print("\nNot quite ready to press on just yet, you evaluate your other options.")
        time.sleep(1.5)
        chapterEightChoice()

def chapterEightChoice():
    global searchedChest8
    try:choice=int(input("\nWhat will you do? [1] to examine the door, [2] to search the chest."))
    except ValueError:
        chapterEightChoice()
    if choice==1:
        print("\nYou wander over to the door. Your heart sinks. You have a feeling that whatever lies behind this door is serious.")
        time.sleep(1.5)
        preShowdown()
    elif choice==2 and searchedChest8 is True:
        print("\nThis chest has already been searched, and there is no loot remaining.")
        time.sleep(1.5)
        chapterEightChoice()
    else:
        print("\nYou wander over to the chest.")
        time.sleep(1.5)
        chest8()

def chapterEight():
    time.sleep(0.5)
    print("\n\n== Chapter 8: Finale ==\n")
    if muteAudio != True:
        pygame.mixer.music.load("sfx/thud.wav")
        pygame.mixer.music.play(1)
    time.sleep(3)
    print("\nAfter what feels like an age of walking, you freeze.")
    time.sleep(1.5)
    print("\nA huge wooden door looms above you. Torches either side cast an eerie flickering glow over the area around you.")
    time.sleep(1.5)
    print("\nYou peer around, taking in this new morbid environment. You notice a chest to the left side of the door.")
    time.sleep(1.5)
    chapterEightChoice()

def postChest7():
    global savePoint
    print("\nYou gaze down the long, dark corridor that lays ahead of you. A familiar feeling of terror hangs over you.")
    time.sleep(1.5)
    try:choice=int(input("\nAre you ready to proceed? You can't return to this area later.\n1] Yes\n2] No\n--> "))
    except ValueError:
        postChest7()
    if choice==1:
        print("\nYou proceed onwards, into the unknown...")
        time.sleep(1)
        savePoint=7
        askSave()
    else:
        print("\nNot quite finished here just yet, you backtrack to the area where the paths originally split.")
        chapterSevenSplit()


def chest7():
    global healingPotion,searchedChest7mk2, healingpotionQuantity
    try:
        choice = int(input("\nYou refocus your attention to the chest in the corner. Search it?\n1] Yes\n2] No\n--> "))
    except ValueError:
        chest7()
    if choice == 1 and searchedChest7mk2 != True:
        try:
            choice2 = int(input("\nYou decide to search the chest! Inside you find a Potion of Healing. Take it?\n1] Yes\n2] No\n--> "))
        except ValueError:
            print("\nOnly integers can be entered here!")
            chest7()
        if choice2 == 1 and searchedChest7mk2 == False:
            print("\nYou obtained the Potion of Healing!\n")
            time.sleep(1)
            try:
                print(r"""                                                                                                                                                              
                                  ░░                                                  
                              ░░                                                      

                            ██████████                                      
                              ██  ██                                      
                              ██  ██                                          
                              ██  ██                                            
                              ██  ██                                             
                              ██  ██                                         
                            ██  ░░  ██                                       
                          ██          ██                                 
                        ██        ░░    ██                            
                        ██  ░░          ██                          
                        ██░░░░░░░░░░░░░░██                           
                        ██░░░░░░░░░░░░░░██                    
                          ██░░░░░░░░░░██                       
                            ██████████                              

""")
            except Exception:
                print("""      _____
     `.___,'
      (___)
      <   >
       ) (
      /`-.\  
     /     \ 
    / _    _\ 
   :,' `-.' `:
   |         |
   :         ;
    \       /
     `.___.'""")
            time.sleep(2)
            print("\nAn item that can only be used during battles. One sip of this, and health will be fully restored instantly!\n")
            healingPotion = True
            searchedChest7mk2 = True
            healingpotionQuantity = healingpotionQuantity + 1
            time.sleep(1)
            print("\nYou return to the previous area where the paths split.")
            time.sleep(1.5)
            chapterSevenSplit()
        elif choice2 == 2:
            print("\nYou decide not to take the Potion of Healing, and return to the previous area where the paths split.")
            chapterSevenSplit()
    elif choice == 1 and searchedChest7mk2 == True:
        print("\nThis chest has already been searched, and there is no loot remaining. You return to the previous area where the paths split.")
        chapterSevenSplit()
    else:
        print("\nYou elect not to search the chest.")
        chapterSevenSplit()

def chapterSevenChest():
    global healingPotion,searchedChest7, healingpotionQuantity, pickedUpKey
    try:
        choice = int(input("\nBefore pressing on, you decide glance to the chest once more. Search it?\n1] Yes\n2] No\n--> "))
    except ValueError:
        chapterSevenChest()
    if choice == 1 and searchedChest7 != True:
        try:
            choice2 = int(input("\nYou decide to search the chest! Inside you find a key. Take it?\n1] Yes\n2] No\n--> "))
        except ValueError:
            print("\nOnly integers can be entered here!")
            chapterSevenChest()
        if choice2 == 1 and searchedChest7 == False:
            print("\nYou obtained the key!\n")
            try:
                print(r"""                                                                    ██████          
                                                                ████░░░░░░████      
                                                              ██░░░░░░░░░░    ██    
                                                            ██░░░░██████████░░  ██  
                                                            ██░░░░██      ██░░  ██  
            ████████████████████████████████████████████████░░░░██          ██░░░░██
            ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██          ██░░░░██
              ██░░░░██░░░░██░░░░████████████████████████████░░░░██          ██░░░░██
                ████  ████  ████                            ██░░░░██      ██░░░░██  
                                                            ██░░░░██████████░░░░██  
                                                              ██░░░░░░░░░░░░░░██    
                                                                ████░░░░░░████      
                                                                    ██████          """)
            except Exception:
                pass
            print("\nA simple-looking key. Maybe it could be used to open a nearby door?")
            time.sleep(1)
            pickedUpKey = True
            searchedChest7 = True
            time.sleep(1)
            postChest7()
        elif choice2 == 2:
            print("\nYou decide not to take the key.")
            postChest7()
    elif choice == 1 and searchedChest7 == True:
        print("\nThis chest has already been searched, and there is no loot remaining.")
        postChest7()
    else:
        print("\nYou elect not to search the chest.")
        postChest7()

def chapterSevenSplit():
    global discoveredChapterSevenDoor, defeatedChapterSevenGuard, area, pickedUpKey, playerHealth, playerMaxHealth
    try:choice=int(input("\nEventually, you come to a split; you can either go left [1] or right [2] "))
    except ValueError:
        chapterSevenSplit()
    if choice==1 and defeatedChapterSevenGuard is not True:
        print("\nYou head left! As you trudge down the blinding corridor, you begin to see a faint figure in the distance... It's a guard!")
        time.sleep(1.5)
        print("\nYou turn to run, but it's too late! The pounding of heavy boots reverberates around you, and you feel a hand on your shoulder...")
        time.sleep(0.8)
        area=7
        encounterGuard()
    elif choice==1 and defeatedChapterSevenGuard is True:
        print("\nYou go left once again. The guard still lays defeated on the floor. You step over him.")
        time.sleep(1.5)
        print("\nYou proceed down the corridor, and eventually come to a door. You push it, and it effortlessly glides open.")
        time.sleep(1.5)
        print("\nBehind this door is a chest, along with a corridor that leads off into the distance.")
        time.sleep(1.5)
        print("\nThis corridor is a complete departure from the area you're in now; the walls are stony once again, and water drips from the ceiling.")
        time.sleep(1.5)
        print("\nThere is also no light at all. You shudder. This corridor gives off an extremely unnerving vibe.")
        chapterSevenChest()
    elif choice==2 and pickedUpKey is True:
        print("\nYou head right! As you round a corner, you come to a thick-looking metal door.")
        time.sleep(1.5)
        print("\nYou push on it, but as expected, it doesnt budge.")
        time.sleep(1.5)
        print("\nSuddenly, you remember the key you found in the chest! You raise the key to the door and turn it...")
        time.sleep(1.5)
        print("\n... And... Success! The door unlocks.")
        time.sleep(1.5)
        print("\nBehind the door, you find a small room with a chest in one corner. A loaf of bread also sits on the floor. It's a little mouldy, but\nit's food. You eat it.")
        time.sleep(1.5)
        print("\nHealth has been fully restored!")
        if playerMaxHealth == 20:
            playerHealth = 20
        elif playerMaxHealth == 22:
            playerHealth = 22
        elif playerMaxHealth == 23:
            playerHealth = 23
        elif playerMaxHealth == 25:
            playerHealth = 25
        chest7()
    else:
        print("\nYou head right! As you round a corner, you come to a thick-looking metal door.")
        time.sleep(1.5)
        print("\nYou push on it, but as expected, it doesnt budge at all. Could the key be nearby?")
        time.sleep(1.5)
        print("\nOut of ideas for now, you return to the previous area where the paths split.")
        time.sleep(1.5)
        discoveredChapterSevenDoor=True
        chapterSevenSplit()

def chapterSeven():
    if debug != 0:
        print("\n=Loaded chapter 7=")
    time.sleep(1)
    print("\n\n== Chapter 7: With Great Power ==\n")
    if muteAudio != True:
        pygame.mixer.music.load("sfx/thud.wav")
        pygame.mixer.music.play(1)
    time.sleep(3)
    print("\nThe environment around you begins to fade into existence as your pupils contract. You're in a long corridor. The walls are smooth and painted white.")
    time.sleep(1.5)
    print("\nThis place is unlike any you have been in a long time. You actually have to do a double take to ensure you haven't just imagined it.")
    time.sleep(1.5)
    print("\nCautiously, you trudge down the sterile white corridor, your footsteps echoing off of the plain walls.")
    time.sleep(1.5)
    chapterSevenSplit()

def puzzleSuccess():
    global puzzleComplete, lockout
    if debug!=0:
        print("=puzzleSuccess function called successfully=")
    time.sleep(1)
    print("*THUNK!*")
    time.sleep(1.5)
    print("\nThe sound makes you jump. It seemed to come from the door at the end of the room.")
    time.sleep(1.5)
    puzzleComplete=True
    lockout=True
    chapterSixChoice()


def rightDial():
    global rightDialPos, rightDialCorrect
    print("\nThe right dial is currently pointing "+rightDialPos+" Which direction shall you turn it?\n1] Left\n2] Right\n3] Up\n4] Down\n5] Cancel")
    try:choice=int(input("--> "))
    except ValueError:
        leftDial()
    if choice==1:
        print("The dial is now facing left!")
        rightDialPos=str("left.")
        dialChoice()
    elif choice==2:
        print("The dial is now facing right!")
        rightDialPos=str("right.")
        rightDialCorrect=True
        dialChoice()
    elif choice==3:
        print("The dial is now facing up, towards the door!")
        rightDialPos=str("up, towards the door.")
        dialChoice()
    elif choice==4:
        print("The dial is now facing down, towards you!")
        rightDialPos=str("down, towards you.")
        dialChoice()
    else:
        dialChoice()

def leftDial():
    global leftDialPos, leftDialCorrect
    print("\nThe left dial is currently pointing "+leftDialPos+" Which direction shall you turn it?\n1] Left\n2] Right\n3] Up\n4] Down\n5] Cancel")
    try:choice=int(input("--> "))
    except ValueError:
        leftDial()
    if choice==1:
        print("The dial is now facing left!")
        leftDialPos=str("left.")
        leftDialCorrect=True
        dialChoice()
    elif choice==2:
        print("The dial is now facing right!")
        leftDialPos=str("right.")
        dialChoice()
    elif choice==3:
        print("The dial is now facing up, towards the door!")
        leftDialPos=str("up, towards the door.")
        dialChoice()
    elif choice==4:
        print("The dial is now facing down, towards you!")
        leftDialPos=str("down, towards you.")
        dialChoice()
    else:
        dialChoice()

def dialChoice():
    if leftDialCorrect is True and rightDialCorrect is True and leverPulled is True and lockout is False:
        puzzleSuccess()
    try:choice=int(input("Interact with the left dial [1] or the right dial [2], or leave them where they are [3]? "))
    except ValueError:
        dialChoice()
    if choice==1:
        leftDial()
    elif choice==2:
        rightDial()
    else:
        chapterSixChoice()

def inspectDials():
    global dialogCount
    if dialogCount==0:
        print("\nYou examine the contraption that stands before you! Both dials have an arrow engraved into them, and appear to be able to rotate.")
        time.sleep(1.5)
        print("\nYou wonder if this is some sort of combination lock. If you could just figure out the right combination...")
        time.sleep(2)
        print("\nSuddenly, you think back to the cryptic message engraved into the base of the fountain:\n'Only when the light and the darkness is revealed will the path forward present itself.'")
        time.sleep(2)
        print("\nDoes this have anything to do with the task at hand?")
        dialogCount=1
        inspectDials()
    else:
        time.sleep(1)
        try:choice=int(input("\nWill you interact with the dials? ([1] = yes, [2] = no) "))
        except ValueError:
            inspectDials()
        if choice==1:
            dialChoice()
        else:
            print("\nYou do not interact with the dials.")
            time.sleep(0.3)
            chapterSixChoice()


def noticedLever():
    global leverPulled
    time.sleep(2)
    if leverPulled is False:
        try:choice=int(input("\nYou pace over to the lever and trace your hands over the cold metal rod. It's currently pointing upwards. Pull it down? ([1] = yes, [2] = no) "))
        except ValueError:
            noticedLever()
        if choice==1:
            print("\nYou pull the lever down! You hear a hushed thud, then... nothing.")
            time.sleep(1.5)
            print("\nJust as you begin to evaluate other options, you notice a flickering light from the other side of the room. The torches that line the left wall are slowly\nflickering to life!")
            time.sleep(2)
            print("\nYou wander back over to the center of the room.")
            leverPulled=True
            chapterSixChoice()
        else:
            print("\nYou decide against pulling the lever, and wander back to the center of the room")
            time.sleep(1)
            chapterSixChoice()
    else:
        print("\nYou stand and ponder. When you pulled the lever, the torches to your left activated. Does this have something to do with the mechanism in the center\nof the room?")
        time.sleep(2)
        chapterSixChoice()

def chapterSixChoice():
    global leverPulled, leftDialCorrect, rightDialCorrect, puzzleComplete, savePoint
    if leftDialCorrect is True and rightDialCorrect is True and leverPulled is True and lockout is False:
        puzzleSuccess()
    try:choice=int(input("\nIt's your call! Will you inspect the room further [1], examine the door [2], or examine the contraption [3]? "))
    except ValueError:
        chapterSixChoice()
    if choice==1:
        print("\nYou glance around the room, looking for anything that may aid you.")
        time.sleep(1.5)
        print("\nTorches line the walls either side of you, however none of these are lit; the chandelier is the only source of light.")
        time.sleep(1.5)
        print("\nYou notice a handle on the wall, with a long rope extending up to the chandelier- this must control it's height.")
        time.sleep(1.5)
        print("\nYou also notice an unmarked lever on the wall to your right.")
        noticedLever()
    elif choice==2 and puzzleComplete is False:
        print("\nYou wander over to the door! From a distance it looked sturdy, but up close it only looks even more impenetrable.")
        time.sleep(1.5)
        print("\nYou extend your arm and brush your hand over the cold metal door. You push it out of curiosity, but unsurprisingly, it's locked.")
        time.sleep(1.5)
        print("\nYou realize that the only way through here is by figuring out how to unlock the door. There's no keyhole, so there has to be some sort of\nmechanism keeping it closed.")
        time.sleep(1.5)
        print("\nOut of ideas for now, you head back over to the center of the room.")
        chapterSixChoice()
    elif choice==2 and puzzleComplete is True:
        print("\nYou wander back over to the door! Tentatively, you extend your arm and once again push on the door...")
        time.sleep(2)
        print("\nAnd... success! The door pushes open. Breathing a sigh of relief, you swing the door fully open.")
        time.sleep(1.5)
        print("\nThe corridor that lays ahead is totally different to the room you were just in, as it's super bright.")
        time.sleep(1.5)
        print("\nA blinding light pours out from the newly revealed path. Squinting, you wait for your eyes to re-adjust.")
        time.sleep(1.5)
        print("\nShielding your eyes, you step forward, into the light...")
        time.sleep(1.5)
        savePoint=6
        askSave()
    elif choice==3:
        inspectDials()

def chapterSix():
    global playerMaxHealth, playerHealth
    time.sleep(1)
    print("\n\n== Chapter 6: A Puzzle In Darkness ==\n")
    if muteAudio != True:
        pygame.mixer.music.load("sfx/thud.wav")
        pygame.mixer.music.play(1)
    time.sleep(3)
    print("\nTrudging along the desolate hallway, you feel an odd sense of mundanity coming on. ")
    time.sleep(1.5)
    print("\nThis place used to terrify you, and whilst it very much still does, you begin to feel a huge increase in your determination.")
    time.sleep(1.5)
    print("\nAfter some more walking, you come to a door. Apprehensively, you push it open. What could possibly lie on the other side?")
    time.sleep(2)
    print("\n...")
    time.sleep(2)
    print("\n     ...")
    time.sleep(1.5)
    print("\nThe answer? A loaf of bread.")
    time.sleep(1.5)
    print("\nYou didn't really know what to expect, but it wasn't that.")
    time.sleep(1)
    print("\nRegardless, you gulp it down. It's a little stale, but it provides you with some well-needed nourishment.")
    time.sleep(1)
    print("\nHealth has been fully restored!")
    if playerMaxHealth==20:
        playerHealth=20
    elif playerMaxHealth==22:
        playerHealth=22
    elif playerMaxHealth==23:
        playerHealth=23
    elif playerMaxHealth==25:
        playerHealth=25
    time.sleep(2.5)
    print("\nHaving revitalised yourself, you peer around, examining this new area.")
    time.sleep(1.5)
    print("\nThe surrounding area is extremely dark. You squint, waiting for your eyes to adjust.")
    time.sleep(1.5)
    print("\nThis room is massive; stone pillars stretch upwards towards an intricate arched ceiling. A large chandeleir hangs, but is not lit.")
    time.sleep(1.5)
    print("\nOn the other side of the room lies a door, however it's unlike anything you've seen so far. It's also huge, but is made entirely of metal.")
    time.sleep(1.5)
    print("\nThe room is barren, save for a short pillar situated in the middle. A torn red carpet lines the floor.")
    time.sleep(3)
    print("\nYou make your way over to the pedestal in the middle of the room. It's some sort of contraption; two dials occupy the top.")
    time.sleep(1.5)
    #print("\nBoth dials have an arrow engraved into them, and can be oriented in four directions.")
    chapterSixChoice()


def courtyardGuardDefeated():
    global courtyardGuardKilled
    print("\nThe guard lays defeated on the floor. Figuring he may have had another guard with him, you scurry back up the path you came from.")
    courtyardGuardKilled=True
    courtyard()

def turnBackToCourtyard():
    global courtyardGuardKilled
    try:
        choice=int(input("\nThere must be a way forward! Will you turn around and explore the garden some more [1], or try to force the door open [2]? "))
    except ValueError:
        turnBackToCourtyard()
    if choice==1:
        #courtyardGuardKilled=True
        courtyard()
    else:
        print("\nYou decide to force the door open! Gathering up your little remaining strength, you take a few paces back...")
        time.sleep(1)
        print("\nYou dart towards the door!")
        time.sleep(1.5)
        print("\n*THUD!*")
        time.sleep(1)
        print("\nYou lie dazed on the floor. The door is still firmly shut. You curse and get back to your feet.")
        time.sleep(1)
        print("\nOut of ideas for now, you decide to head back to the main area to explore further.")
        courtyardGuardKilled=True
        courtyard()

def backInsideFromCourtyard():
    global courtyardKey, foundCourtyardDoor, savePoint, courtyardGuardKilled
    choice=int(input("\nAfter some walking, you reach a door which appears to lead back inside the dungeon. Enter [1], or continue to explore the courtyard [2]? "))
    if choice==1:
        print("\nYou head on over to the door! It's made of solid metal; grey paint flakes off with age. It looks oddly out of place.")
        time.sleep(1.5)
        print("\nYou push firmly... but it won't budge! There is a large keyhole halfway down the door.")
        time.sleep(1.5)
        if courtyardKey is True:
            print("\nSuddenly you remember; the key you found in the fountain! Hastily, you draw the key from your pocket and insert it into the keyhole...")
            time.sleep(1.5)
            print("\nAnd it turns! With a dull click, the door is unlocked.")
            time.sleep(1.5)
            print("\nA strong, musty smell eminates from the newly revealed passageway. The pathway ahead is pitch black.")
            time.sleep(1.5)
            print("\nBreathing a sigh of relief, you nervously press on forward, into the depths of the unknown...")
            time.sleep(3)
            savePoint = 5
            askSave()
        elif courtyardKey is False:
            turnBackToCourtyard()
    else:
        print("\nYou turn around, heading back towards the fountain.")
        time.sleep(1)
        courtyard()

def courtyard():
    global area, courtyardGuardKilled, courtyardKey, foundCourtyardDoor
    if courtyardGuardKilled is False:
        try:
            choice=int(input("\nYou step towards the fountain. You can either follow the path left [1] or right [2]. Which way will you go?"))
        except ValueError:
            courtyard()
    else:
        try:
            choice=int(input("\nYou return to the fountain where the paths split. Do you head down the other path [1] or examine your surroundings [2]? "))
        except ValueError:
            courtyard()
    if choice==1 and courtyardGuardKilled is False:
        print("\nYou head left! Uncertain, you follow the winding path through the thick overgrown bushes.")
        time.sleep(1.8)
        print("\nAs you progress, you begin to hear a faint sound. It sounds like... whistling?")
        time.sleep(1.8)
        print("\nYou carry on, eagerly listening out. The sound only grows louder as you head down the path.")
        time.sleep(1.8)
        print("\nAt first you thought your ears were deceiving you, but now you're certain; this isn't the sound of a bird, but rather of a person.")
        time.sleep(1.8)
        print("\nAbruptly, the path ends. You observe your surroundings and freeze. A stone bench lays a few metres ahead. Here, a guard is sat with his back turned to you.")
        time.sleep(1.8)
        print("\nYou begin to back away. If you can just make it out of the guard's general whereabouts you might be able to slip away...")
        time.sleep(1.8)
        print("\nYour heart sinks as the guard turns his head... and makes eye contact with you. With a startled yell, he picks up his weapon and approaches...")
        courtyardGuardKilled=False
        time.sleep(3)
        area=6
        encounterGuard()
    elif choice==2 and courtyardGuardKilled is False:
        print("\nYou go right! Hesitantly, you stick to the path through the overgrown gardens.")
        time.sleep(0.9)
        backInsideFromCourtyard()
    elif choice==1 and courtyardGuardKilled is True:
        print("\nYou head down the other path! ")
        time.sleep(0.9)
        backInsideFromCourtyard()
    elif choice==2 and courtyardKey is False and courtyardGuardKilled is True:
        print("\nYou peer around, wondering when this place was last used. ")
        time.sleep(0.9)
        print("\nBut wait! Out of the corner of your eye, at the base of the fountain, you think you see something gleaming.")
        time.sleep(0.9)
        print("\nYou inch closer, and begin to rummage through the thick undergrowth...")
        time.sleep(1.2)
        print("\n...And you unearth a key! You pocket it, certain it'll come in handy later.")
        courtyardKey=True
        time.sleep(1.5)
        print("\nYou also notice something engraved into the stone of the fountain. It's a little hard to read, but it says: 'Only when \nthe light and the darkness is revealed will the path forward present itself.'")
        time.sleep(1)
        print("\n...")
        time.sleep(1)
        print("\nWhat could that possibly mean?")
        courtyard()
    elif choice==2 and courtyardKey is True and courtyardGuardKilled is True:
        print("\nYou once again observe your surroundings... certain nothing is left to be dicovered, you focus your attention back to your next move.")
        courtyard()



def chapter5Corridor():
    choice=int(input("Do you head left [1], or venture right instead [2]? Both passages look the same. "))
    if choice==1:
        print("\nYou decide to go left!")
        time.sleep(0.7)
        chapter5Chest()
    elif choice==2:
        print("\nYou head right! As you head down the stony corridor, you begin to hear something...")
        time.sleep(0.7)
        print("\nThe rustling of leaves... birds chirping... but that means...")
        time.sleep(0.7)
        print("\n...You must be heading outside! Excitedly, you feel your spirits lift and you pick up the pace. Could this be your ticket out of here?\n")
        time.sleep(0.7)
        print("Nearing the end of the corridor, you can see daylight creeping around a corner, and you feel a soft breeze against your face.\n")
        time.sleep(0.7)
        print("Cautiously, you near the end of the corridor and take a peek around the corner...")
        time.sleep(1.3)
        print(
            "\nYou are greeted by an overgrown courtyard! Huge trees tower above you, with ivy creeping up the trunks. Cracked stone tiles line the floors with weeds")
        time.sleep(0.2)
        print(
            "snaking up from between the cracks. In the middle of the garden, a crumbling fountain stands covered in ivy and moss. Two paths branch around the fountain, heading")
        time.sleep(0.2)
        print("deeper into the garden in each direction. A large, crumbling stone wall lines the perimeter of the area.")
        time.sleep(2.5)
        print(
            "\nConfident that there are no guards lurking, you take a step out into the abandoned garden. You take a gulp of breath air; which only seems to re-invigorate\nyou further.")

        courtyard()

def chapterFive():
    time.sleep(3)
    print("\n\n== Chapter 5: A Breath Of Fresh Air ==\n")
    if muteAudio != True:
        pygame.mixer.music.load("sfx/thud.wav")
        pygame.mixer.music.play(1)
    time.sleep(3)
    print("Clambering down the steep spiral steps, you can feel that familiar sense of dread coming on once again.\n")
    time.sleep(2)
    print("After what feels like an eternity of descending the depressing stairwell, you finally reach a small archway at the bottom.\n")
    time.sleep(1.3)
    print("Hesitantly, you peer around the mossy doorway and deduce that nobody is on the other side.")
    time.sleep(1.4)
    print("\nYou silently slip through the opening, and observe your surroundings; you're stood in a long corridor, with two branching paths to your left and right.\n")
    chapter5Corridor()

def findTheExit():
    global savePoint
    global findExit
    findExit=True
    choice=int(input("\nYou must find a way forwards! [1] To continue up the corridor, [2] to return back to the closet."))
    if choice==1:
        leftChest()
    elif choice==2:
        print("\nYou backtrack towards the closet at the end of the corridor! ")
        time.sleep(1.2)
        print("\nAs you approach the entrance to the closet, you step inside in order to get a better view of things.")
        time.sleep(1.2)
        print("\nUpon stepping into the closet, you immediately notice something you hadn't before; a thick, wooden trapdoor protruding slightly above a pile of debris on the floor!")
        time.sleep(2)
        print("\nTensely, you kick aside the rubble on the floor...")
        time.sleep(1.2)
        print("\nOnly to discover a heavy iron padlock keeping the trapdoor strongly wedged shut. You groan, only to remember the key you previously aqcuired!")
        time.sleep(1.3)
        print("\nNervously, you crouch down and insert the key into the padlock. You begin to turn the key...")
        time.sleep(2)
        print("\n*CLUNK!*")
        time.sleep(2)
        print("\nPhew! You take a deep breath as the lock releases it's grip on the trapdoor")
        time.sleep(1.2)
        print("\nAs soon as you begin to lift the rotten trapdoor, the first thing you notice is a strong, musty odour eminating from the pit in the stony floor")
        time.sleep(2)
        print("\nFighting the odour, you push the trapdoor open, revealing a narrow, spiral staircase leading down. With no other options, you begin to descend...")
        savePoint=4
        askSave()


def defeatedHighRank():
    global discoveredPadlock, highRank
    global savePoint
    global debug
    if highRank is True:
        highRank=False
    time.sleep(2)
    print("\nYou have overcome the challenge and defeated the High Ranking guard!")
    time.sleep(1.3)
    print("\nAs you gaze upon his body on the floor, you think you see something glimmer beside him")
    time.sleep(1.2)
    print("\nCautiously, you glance down to where you think you saw the shimmer, only to discover a large, silver key laying beside the guard! He must have dropped it when he fell!")
    time.sleep(1.2)
    if discoveredPadlock is True:
        print("\nWith shaking hands, you pick up the key dropped by the guard. Could this be the key needed to unlock the tapdoor and forge yet another path onward?")
        time.sleep(1.2)
        print("\nYou scurry back along the corridor, and return to the room with the trapdoor.")
        time.sleep(2)
        print("\nNervously, you crouch down and insert the key into the padlock. You begin to turn the key...")
        time.sleep(2)
        print("\n*CLUNK!*")
        time.sleep(2)
        print("\nPhew! You take a deep breath as the lock releases it's grip on the trapdoor")
        time.sleep(1.2)
        print(
            "\nAs soon as you begin to lift the rotten trapdoor, the first thing you notice is a strong, musty odour eminating from the pit in the stony floor")
        time.sleep(2)
        print(
            "\nFighting the odour, you push the trapdoor open, revealing a narrow, spiral staircase leading down. With no other options, you begin to descend...")
        savePoint = 4
        if debug != 0:
            print(savePoint)
        askSave()
    else:
        print("\nWith shaking hands, you pick up the key and pocket it. It may end up coming in handy...")
        findTheExit()


def chest2():
    global healingPotion
    global searchedChest2, healingpotionQuantity
    try:choice=int(input("\nAll hope is not lost, however. In the corner of the room, you spot a decrepit wooden chest. Search it? ([1] Yes, [2] No) "))
    except ValueError:
        chest2()
    if choice==1 and searchedChest2 != True:
        try:choice2=int(input("\nYou decide to search the chest! Inside you find a Potion of Healing. Take it?\n1] Yes\n2] No\n--> "))
        except ValueError:
            print("\nOnly integers can be entered here!")
            chest2()
        if choice2==1 and searchedChest2==False:
            print("\nYou obtained the Potion of Healing!\n")
            time.sleep(1)
            try:print(r"""                                                                                                                                                              
                                  ░░                                                  
                              ░░                                                      
                                                                                      
                            ██████████                                      
                              ██  ██                                      
                              ██  ██                                          
                              ██  ██                                            
                              ██  ██                                             
                              ██  ██                                         
                            ██  ░░  ██                                       
                          ██          ██                                 
                        ██        ░░    ██                            
                        ██  ░░          ██                          
                        ██░░░░░░░░░░░░░░██                           
                        ██░░░░░░░░░░░░░░██                    
                          ██░░░░░░░░░░██                       
                            ██████████                              
                                                                                                                                                                          
""")
            except Exception:
                print("""      _____
     `.___,'
      (___)
      <   >
       ) (
      /`-.\  
     /     \ 
    / _    _\ 
   :,' `-.' `:
   |         |
   :         ;
    \       /
     `.___.'""")
            time.sleep(2)
            print("\nAn item that can only be used during battles. One sip of this, and health will be fully restored instantly!\n")
            healingPotion=True
            searchedChest2=True
            healingpotionQuantity=healingpotionQuantity+1
            time.sleep(1)
            closet()
        elif choice2==2:
            print("\nYou decide not to take the Potion of Healing, and return to the previous area.")
            closet()
        else:
            chest2()
    elif choice==1 and searchedChest2==True:
        print("\nThis chest has already been searched, and there is no loot remaining.")
        closet()
    else:
        print("\nYou chose not to search the chest.")
        closet()

def beforeHighRank():
    global area
    time.sleep(1)
    try:choice=int(input("\nDo you attempt to take on the guard [1]? Or return to the previous area in the hopes you'll find something to aid you in the battle [2]? "))
    except ValueError:
        print("\nOnly integers can be entered here!")
        beforeHighRank()
    if choice==1:
        print("\nYou approach the menacing-looking guard, ready for combat...")
        area=4
        encounterHighRank()
    elif choice==2:
        print("\nQuietly, you steal back up the corridor you just came down, in the hopes of finding something useful...")
        closet()

def closet():
    global discoveredPadlock
    try:choice=int(input("\nDo you inspect the empty room further [1], or backtrack and try to find a different path forward [2]? "))
    except ValueError:
        print("\nBad input. Only an integer can be entered here!")
        closet()
    if choice==1:
       print("\nYou decide to inspect the room further, stepping inside to get a better view. You scan every surface of the room, and find nothing.")
       time.sleep(1)
       print("\nJust as you're about to give up hope, you notice a rotting wooden trapdoor beneath a pile of rubble on the floor. Tentatively, you kick the rubble away in order to get a closer look...\n")
       time.sleep(1)
       print("...Only to discover it's being held firmly shut with a rusty iron padlock. You curse, then scramble to your feet. There must be another path forward!")
       time.sleep(1)
       discoveredPadlock=True
       chest2()
    elif choice == 2:
        print("\nYou decide to backtrack, in order to find another path forward. As you begin to retrace your steps around the corner of the narrow corridor, you hear footsteps.")
        time.sleep(1)
        print("\nYou stand in terror, as the horrifying reality dawn on you; you're not alone down here.")
        time.sleep(1)
        print("\nYou decide to peer your head around the corner in order to see who you might be up against. You spot a guard, pacing around menacingly.")
        time.sleep(1.3)
        print("\nBut, wait... something seems different about this guard. He almost seems... stronger... more menacing...")
        beforeHighRank()

def rightDoor():
    global gotKey
    global foundDoor
    global damage
    print("After a few minutes of advancing down the dim corridor, you reach what appears to be a blockade; a thick, rusty iron door looms above you.")
    time.sleep(1)
    print("\nThis door looks too strong to be able to force open, besides, any loud noise could alert any nearby guards to your presence!")
    time.sleep(1)
    if gotKey == False and foundDoor == False:
        print("\nA tiny keyhole situated in the middle of the huge door is the only point light from the other side seeps through. Perhaps if \nyou could find the key, you'd be able to slip through unnoticed...")
        foundDoor = True
        time.sleep(1.2)
        print("\nOut of ideas for now, you head back up the corridor, back to the previous area.\n")
        backInsideChoice()
    elif gotKey == False and foundDoor == True:
        print("\nThat keyhole must be the path forward! Maybe if you carried on searching, maybe you'd find something...")
        time.sleep(1)
        print("\nOut of ideas, you head back up the corridor, back to the previous area.\n")
        backInsideChoice()
    elif gotKey == True:
        print("\nSuddenly, you remember; the key from the chest you've just looted! Hand shaking in anticipation, you raise they key to the lock and turn...")
        time.sleep(1.5)
        print("\n*CLICK!*")
        time.sleep(1)
        print("\nPhew! You gasp a sigh of relief as you hear the thud of the lock releasing it's grasp. Tentatively, you begin to shove the door open. \nA feeling of dread comes over you. What could possibly lurk on the other side...")
        time.sleep(2)
        print("\nUpon pushing open the door, your heart sinks. There's nothing but an empty closet on the other side!")
        time.sleep(1)
        print("\nYou cry out in frustration. There must be another way!")
        time.sleep(2)
        closet()

def leftChest():
    global gotKey
    search=0
    global playerHealth, playerMaxHealth
    if debug != 0:
        print(gotKey)
    try:search=int(input("\nEventually, you reach the end of the corridor. A lone wooden chest lays forlorn and forgotten in a corner. Search it? [1] = yes, [2] = no "))
    except ValueError:
        print("\nBad input; only integers can be entered!\n")
        leftChest()
    if search == 1 and gotKey == False:
        print("\nYou rummage around inside of the chest! You dig for any useful items...")
        time.sleep(1.5)
        print("\n..And you uncover a rusty key!")
        time.sleep(1.5)
        gotKey = True
        print("\nYou also reveal a stale loaf of bread. Starving, you gulp it down without a second thought.")
        time.sleep(0.6)
        print("\nHealth has been fully restored!")
        playerHealth=playerMaxHealth
        time.sleep(1.5)
        print("\nSatisfied you've collected all of the items that may become useful, you close the chest and return to the previous area at the bottom of the stairs.\n")
        backInsideChoice()
    elif search == 2:
        print("\nYou did not search the chest. You swiftly head back up the corridor you just came down. \n")
        backInsideChoice()
    elif search == 1 and gotKey == True:
        print("\nThis chest has already been searched, and there is no loot remaining. Disappointed, you  return back to the previous area. \n")
        backInsideChoice()
    else:
        leftChest()

def backInsideChoice():
    time.sleep(1.2)
    choice=0
    try:
        choice = int(input("You reach the bottom of the stairs, and are met with two paths forward. You can either go left [1], or right [2]. Both \npassages look the same. "))
    except ValueError:
        print("\nBad input; only integers can be entered!")
        backInsideChoice()
    if choice == 1:
        print("\nYou turn left! You hesitantly walk down the ominous corridor, a few flickering torches on the wall your only source of light.")
        time.sleep(1.3)
        leftChest()
    elif choice == 2:
        print("\nYou head right! Heart racing, you tread cautiously down the dingy corridor.\n")
        time.sleep(1.3)
        rightDoor()
    else:
        backInsideChoice()

def backInside():
    global savePoint, muteAudio
    print(" ")
    print("== Chapter 4: What Doesn't Kill You Makes You Stronger ==")
    if muteAudio != True:
        pygame.mixer.music.load("sfx/thud.wav")
        pygame.mixer.music.play(1)
    print(" ")
    print(" ")
    time.sleep(3)
    print(" ")
    print("Upon re-entering, you are hit with an immense feeling of dread. Why are you doing this? Are you really willing to risk \nyour life for a load of strangers?")
    print(" ")
    time.sleep(2)
    print("Slowly regaining courage, you look around. You are met with a stony staircase leading down, to what you presume to be back into the dungeon. ")
    time.sleep(1.2)
    print("\nYou begin to descend the staircase, your footsteps reverberating off of the mossy stone walls.\n")
    time.sleep(1.2)
    backInsideChoice()

def balcony():
    global gotRope
    global savePoint
    print("You get to the door, and without thinking, fling yourself outside...")
    time.sleep(3)
    print(" ")
    print("You find yourself on a precarious balcony! The floor is made of rotting wood, and there's a sheer drop below. Looking around gives you a clear view of all \nthe guards circling the perimeter of the building.")
    print(" ")
    time.sleep(3)
    print("You notice another balcony below you, which looks equally dangerous.")
    print(" ")
    time.sleep(1)
    if gotRope != 0:
        print("Thinking fast, you remember the rope you picked up earlier. Maybe you could use this to get to the lower balcony?")
        print(" ")
        time.sleep(3)
        print("Hurriedly, you tie the rope around the balcony's railing, and inhale deeply. This has been your first time outdoors in ages. And it could well be your last...")
        print(" ")
        time.sleep(3)
        print("Figuring you'd rather die this way than to the hands of those guards, you grab hold of the rope, and begin to clamber over the railing.")
        print(" ")
        time.sleep(3)
        print("Your arms ache as you begin to scale down the rope. Having not eaten for days, there's essentially no muscle left on your frail body.")
        print(" ")
        time.sleep(3)
        print("As the wind ruffles through your unkempt hair, you try your hardest not to look down at the drop that would lead to certain death below...")
        print(" ")
        time.sleep(3)
        print("Suddenly, you feel a jolt through the rope. You look up and see a guard attempting to cut through the rope with a switchblade! Panicking, you begin to climb down the rope faster...")
        print(" ")
        time.sleep(3)
        print("Suddenly, you hear a triumphant yell from above as you begin to plummet. That guard managed to cut through the rope! This is it. The end... you shut your eyes and brace for impact.")
        print(" ")
        time.sleep(3)
        print("*THUD!*")
        time.sleep(3)
        print("...")
        time.sleep(3)
        print("   ...")
        time.sleep(3)
        print("      ...")
        time.sleep(3)
        print("You slowly come to. Your head aches, and your bones all feel shattered. But you're alive.")
        print(" ")
        time.sleep(3)
        print("Did you survive an almost 7 storey plunge? Surely not...")
        print(" ")
        time.sleep(3)
        print("You slowly regain composure, and sit up to observe your surroundings. It's night time. How long had you been lying here? Come to think of it, where were you?")
        print(" ")
        time.sleep(3)
        print("Suddenly, you realize where you are. On the lower balcony. The rope lies severed next to you, a cruel reminder of the guard's brutality.")
        time.sleep(3)
        print(" ")
        print("Fighting the pain, you get up and look around. A door leads back into the dungeon. Thinking of all the innocent lives at stake, you head back inside...")
        print(" ")
        time.sleep(3)
        savePoint=3
        if debug > 0:
            print(savePoint)
        askSave()
    else:
        print("Thinking of your next move, you suddenly remember: The rope from the dark room you hid in! That's your only ticket to escape!")
        print(" ")
        time.sleep(2)
        print("As the foolish mistake you have made dawns on you, two burly guards burst through the door. They each grab your arms, and before you can so much as scream, they toss you off the balcony...")
        gameOver()


def defeatedSecondGuard():
    time.sleep(2)
    print("\nYou have overcome the two guards, winning against all odds! Your reward should make up for any sustained injuries.")
    time.sleep(1.5)
    print("\nSuddenly, you hear the crash of a door being flung open behind you. You spin around, only to be met with 3 more guards charging towards you!")
    time.sleep(1.5)
    print("\nYou race towards the door at the end of the corridor! Who knows what lies beyond...\n")
    time.sleep(1.5)
    balcony()

def fightSecond():
    global musicStop
    global musicLoop
    global area
    time.sleep(1)
    print("You have defeated the first guard! As he falls to the ground having been defeated in battle, his comrade takes a defensive stance and lunges towards you!")
    time.sleep(2)
    print("\nYou ready yourself for yet another battle! The payoff better be worth the risk...")
    time.sleep(2)
    musicStop=False
    musicLoop=False
    area=5
    encounterGuard()

def hidingChoice():
    run=0
    global area
    try:run = int(input("""Silently, you slip out from behind the boxes. Peering your head around the door reveals the guards waiting for you at one end of the hallway. You 
can either make a dash for the door with natural light pouring through [1], or attempt to take on the guards [2] """))
    except ValueError:
        hidingChoice()
    if run == 1:
        print(" ")
        print("You make a beeline for the door at the opposite end of the hall! The guards notice this, and begin to give chase once again!")
        print(" ")
        balcony()
    else:
        area = 3
        print("\nYou decide to take on the guards! Swiftly, you approach the first guard and prepare to battle...")
        time.sleep(2)
        encounterGuard()

def hiding():
    global area
    print("You peer out from behind the boxes. Sure enough, you can hear the guards storming towards the room, calling your name mockingly.")
    print(" ")
    time.sleep(1.7)
    print("You can just barely make out a silhouette enter the pitch black room, followed by two other menacing figures. They seem to head straight for the table. Thank god you didn't hide there!")
    print(" ")
    time.sleep(2)
    print("After some searching, the guards appear to give up, cursing under their breath as they exit the room. Now's your chance!")
    print(" ")
    time.sleep(1.3)
    hidingChoice()

def ropeChoice():
    global gotRope
    getRope=0
    print(" ")
    try:
        getRope = int(input("You dive behind the boxes! You can feel rats scurrying about around your legs. Feeling around the floor, you can feel a coil of rope. Pick it up? [1] for yes, [2] for no. "))
    except ValueError:
        print(" ")
        print("Bad input. Only integers can be entered!")
        ropeChoice()
    if getRope == 1:
        print(" ")
        print("You've got the rope! You never know when it might prove useful...")
        print(" ")
        gotRope = 1
        if debug > 0:
            print(gotRope)
        hiding()
    else:
        print(" ")
        print("You don't pick up the rope. You never know, it may have come in handy at some point...\n")
        hiding()

def chaseChoice():
    hide=0
    try:hide = int(input("You quickly scan the dark room, and settle on two hiding spots; behind a stack of boxes [1], and under a table [2]. Choose one! "))
    except ValueError:
        chaseChoice()
    if hide == 1:
        ropeChoice()
    else:
        print(" ")
        print("You dive under the table! Sure enough, you hear the guards approaching the room. They sound angry!!")
        print(" ")
        time.sleep(1.5)
        print("The guards enter the room. They seem to know you're in there, as they're calling your name mockingly...")
        print(" ")
        time.sleep(1.8)
        print("The room is pitch black, so they shouldn't be able to spot you easily. You place a hand over your mouth to muffle you're erratic breathing.")
        time.sleep(2)
        print(" ")
        print("*CLANG!*")
        print(" ")
        time.sleep(1.2)
        print("You freeze. You've just accidentally knocked over a metal bucket! The guards snap their heads in your direction. They begin approaching the table, guns loaded...")
        time.sleep(2)
        gameOver()

def chase():
    global gotRope
    door=0
    #gotRope=0
    try:door=float(input("Which door do you go through? [1] for the door at the end of the corridor, [2] for the door you've just noticed. Act fast! "))
    except ValueError:
        print(" ")
        chase()
    if door==1:
        print(" ")
        print("You continue to run for the door at the end of the corridor! Oddly enough, the guards appear to stop just short of the end of the corridor. \nHave they given up? Surely not...")
        print(" ")
        time.sleep(2)
        print("Without a second thought, you fling open the door and race out...")
        print(" ")
        time.sleep(2)
        print("Only to find yourself standing on a precarious balcony above a sheer drop. The floor is made of rotting wood, and looks like it could \nbreak with the slightest movement.")
        print(" ")
        time.sleep(2)
        print("You stand there, clueless about your next move. You notice an equally rotten balcony below you. If only you had some sort of rope, \nthen you could reach it...")
        print(" ")
        time.sleep(2)
        print("Suddenly, two strong looking guards appear in the doorway. They each grab one of your arms, and without a second thought, toss you \noff the balcony! The last thing you hear is them laughing before your world turns black...")
        time.sleep(2)
        gameOver()
    elif door == 2:
        print(" ")
        print("You dive for the door on your left! This seems to throw the guards off, as they run right past the entrance!")
        print(" ")
        time.sleep(2)
        print("Time is of the essence! Those guards will no doubt come in here looking for you! You must hide!")
        print(" ")
        time.sleep(1)
        chaseChoice()
    else:
        chase()

def chest():
    global smokescreen, smokescreenQuantity
    try:choice=int(input("You come to a chest. Search it? ([1] Yes, [2] No) "))
    except ValueError:
        chest()
    if choice == 1:
        choice2=int(input("\nYou search the chest. Inside you find a smokescreen. Take it? \n1] Yes\n2] No\n--> "))
        if choice2==1:
            if smokescreen != True:
                print("\nYou obtained the smokescreen!\n")
                print("""                       .')             _
                      (_  )        .+(`  ) ) --:--
            _                     :(    ) )
        .:(`  )  ) --        .--  `.  (    ) )  - --
       :(      )           .(   )   ` __.:'
`.     `(       ) )       (      )
  )      ` __.:'   ))--- (       )) ----      _
)  ) --         --'  _    `- __.'         .=(`  )
.-'                (`  ).                :(      )
                 (       '`. .  --       `(       ) ) ) ----
                 (         ) ) ---         ` __.:'
                  ` __.:'-'""")
                time.sleep(2)
                print("\n\nAn item that can only be used in battles. Cloaks the battlefield in a veil of smoke, allowing you to swiftly exit! Grants a 100% chance of escaping unharmed.")
                time.sleep(1)
                smokescreen=True
                smokescreenQuantity=smokescreenQuantity+1
                print("\nConfident there is nothing of value in the chest, you head back up the stairs.")
                time.sleep(2)
                outsideConfinement()
            else:
                print("\nThis chest has already been searched, and there is nothing of value contained within. Disappointed, you head back up the stairs.")
                time.sleep(1)
                outsideConfinement()
        else:
            print("You did not take the smokescreen. You return to the previous area empty-handed.")
            outsideConfinement()
    elif choice == 2:
        print("\nYou decide not to search the chest, and instead return to the previous area.")
        outsideConfinement()

def outsideConfinement():
    global area
    area=2
    if debug !=0:
        print(area)
    global playerMaxHealth
    global gotShield
    global defeatedGuardOutsideConfinement
    try:wayToGo=float(input("You are faced with three paths forward: A door to your right [1], A door to your left [2], and a small hatch in the floor [3]. Choose wisely... "))
    except ValueError:
        print(" ")
        print("Bad input. Only integers can be entered!")
        outsideConfinement()
    if wayToGo==1 and defeatedGuardOutsideConfinement is False:
        print(" ")
        print("You decide to exit through the door on the right! As you near the door, you think you can hear rapidly approaching footsteps on the other side...")
        print(" ")
        time.sleep(2)
        print("As you stand there contemplating whether this was a good choice, suddenly the door is flung open by a familiar looking \nface; it's the guard who stormed off earlier!")
        print(" ")
        time.sleep(2)
        area=2
        encounterGuard()
    elif wayToGo==1 and defeatedGuardOutsideConfinement is True:
        print("\nThe guard's body lays in the doorway. You mustn't try to get through in case more guards are on the way!\n")
        outsideConfinement()
    elif wayToGo==2:
        print(" ")
        print("You decide on exiting through the door on the left! As you approach the heavy wooden door, your heart begins to race. What could\npossibly lurk behind this door?")
        time.sleep(2)
        print(" ")
        print("Having gained enough courage, you press your palm against the door and push it open... ")
        time.sleep(2)
        print(" ")
        print("As you peer around the door, you are met with a stone-walled corridor that seems to stretch on forever. A red carpet, covered\nin ominous stains, trails along the rotting wooden floor.")
        time.sleep(2)
        print(" ")
        print("Upon closer inspection, you notice a door at the end of the corridor. Natural light pours in though the small gaps around the \ndoor, making this the only light source. Could this door be your ticket to freedom?")
        print(" ")
        time.sleep(2)
        print("As you're pondering over your next move, you hear the sudden crash of a door being flung open behind you, as well as manic \nyelling and rapid footsteps. That guard from earlier must have returned with backup!")
        print(" ")
        time.sleep(2)
        print("The chase is on! You begin to dash for the door at the end of the corridor, the guards hot on your trail!")
        print(" ")
        time.sleep(2)
        print("As you near the end of the corridor, you spot a door that you hadn't previously noticed. This door looks rotten, and there's no light on the other side")
        time.sleep(2)
        print(" ")
        chase()
    else:
        print(" ")
        print("You decide to check out the hatch in the floor! You slowly lift the hatch, being careful not to make too much noise.")
        print(" ")
        time.sleep(2)
        try:stairs=int(input("Under the hatch, you find a staircase leading down. [1] to head down the stairs, [2] to evaluate the other options: "))
        except ValueError:
            outsideConfinement()
        if stairs==1:
            print("\nYou descend the stairs carefully, your footsteps echoing off of the cold stone walls...")
            time.sleep(1)
            print(" ")
            chest()
        elif stairs == 2:
            print(" ")
            outsideConfinement()

def escape():
    global savePoint, muteAudio
    time.sleep(2)
    print("\n\n== Chapter 3: The Great Escape! ==\n")
    if muteAudio != True:
        pygame.mixer.music.load("sfx/thud.wav")
        pygame.mixer.music.play(1)
    time.sleep(3)
    savePoint=2
    if debug>0:
        print("savePoint=",savePoint)
        print(damage)
    time.sleep(1)
    print(" ")
    print("Hurriedly, you pull the keys towards you, being careful not to make a sound. Remember, the guard could return at any moment!")
    time.sleep(2)
    print(" ")
    print("You slowly pull the keys through the small metallic hatch, and insert the key into the keyhole. Your hands tremble in anticipation as you begin to turn the key...")
    time.sleep(2)
    print(" ")
    print("*CLICK!*")
    time.sleep(1.4)
    print(" ")
    print("Success! You breathe a sigh of relief as you hear the dull click of the lock. Maybe all hope isn't lost?")
    time.sleep(2)
    print(" ")
    print("You slowly push the door open, being careful to minimize the shrill shrieks of the worn out hinges.")
    time.sleep(2)
    print(" ")
    print(
        "As you peer your head around the door, you are met with a small room with two doors on each side. A musty odour fills your nostrils.")
    time.sleep(2)
    print(" ")
    outsideConfinement()

def getKeys():
    global savePoint
    global gotKeys
    print(" ")
    time.sleep(1)
    print("You flick the string towards the keys...")
    print(" ")
    time.sleep(2)
    gotKeys = random.randint(1, 5)
    if debug > 0:
        print("gotKeys =", gotKeys)
    if gotKeys <= 2:
        try:tossAgain = float(input("Damn it! Missed by just a bit! Press [1] to toss the sting again..."))
        except ValueError:
            print(" ")
            print("Bad input. Only integers can be entered!")
            getKeys()
        if tossAgain == 1:
            getKeys()
        else:
            print("""You decide to not try and toss the string again for some reason! As you stand there doing nothing, the guard storms back in, gun raised... next 
time, don't try and be smart and press an option that's not there!!""")
            gameOver()
    elif gotKeys >= 3:
        print("Aha! Looks like the keys have been entangled in the string! You breathe a sigh of relief as you drag them towards you.")
        print(" ")
        time.sleep(2)
        savePoint=2
        if debug > 0:
            print("savePoint=", savePoint)
        askSave()

def chooseObjectSearch():
    global gotstring
    getobject=0
    try:
        getobject = int(input("You search the room. You find an empty plate [1], a cup [2], and a piece of string [3]. Which one do you use?"))
    except ValueError:
        chooseObjectSearch()
    if getobject == 3:
        print(" ")
        print("Good choice. You've got the string!")
        gotstring = 1
        print("You turn back around to face the door, and to your surprise, the guard has left! Even more surprising; it looks like he dropped his keys too!")
        print(" ")
        time.sleep(0.75)
        print("Hurriedly, you scurry over to the hatch, string in hand. You tie a knot in the string, hoping to entangle the keys and drag them over to you...")
        time.sleep(0.5)
        getKeys()
    else:
        print("That's no use! Time is of the essence. Choose wisely before the guard notices!")
        try:
            getobject = int(input("You've found an empty plate [1], a cup [2], and a piece of string [3]. Which one do you use?"))
        except ValueError:
            chooseObjectSearch()
        if getobject == 3:
            print(" ")
            print("Good choice. You've got the string!")
            print(" ")
            gotstring = 1
            getKeys()
        else:
            print(" ")
            print("That's no use! It's too late! You see the guard approaching, gun in hand...")
            time.sleep(0.75)
            gameOver()

def continueYelling():
    try:stop = int(input("\nDo you continue to yell [1], or stop? [2]"))
    except ValueError:
        continueYelling()
    if stop == 1:
        time.sleep(0.25)
        print("\nYou carry on yelling! The guard finally snaps, storming out of the room. As luck would have it, he drops his keys on the way out!")
        if gotstring == 0:
            print("\nIf only you could find some way of grabbing the keys...")
            time.sleep(1)
            print("\nYou glance around, looking for anything that could aid you.\n")
            chooseObjectSearch()
    else:
        print("""\nYou stop the manic yelling! The guard, seemingly regaining his composure, calmly walks over to the hatch and slides it shut. Your heart sinks
as you hear the metallic click of the lock. You are trapped with no escape...""")
        gameOver()

def choice6():
    global gotstring
    distract2=0
    try:distract2 = int(input("\nDo you distract the guard in the hopes he'll open the door [1], or continue to explore the room? [2] "))
    except ValueError:
        choice6()
    if distract2 == 1:
        print("\nYou begin to yell uncontrollably! The guard gazes in your direction. He looks angry...")
        time.sleep(1)
        continueYelling()
    else:
        chooseObjectSearch()


def choice5():
    print(" ")
    print("You hastily walk over to the hatch! out of curiosity, you decide to touch the hatch, and to your surprise it easily slides open! That guard must've forgotten to lock it!!")
    print(" ")
    time.sleep(2)
    print("Perhaps if you distract the guard he'll open the door...")
    time.sleep(1.1)
    choice6()


def choice4():
    global savePoint
    global playerHealth
    global playerMaxHealth
    print("\n\n== Chapter 2: Solitary Confinement ==\n")
    if muteAudio != True:
        pygame.mixer.music.load("sfx/thud.wav")
        pygame.mixer.music.play(1)
    time.sleep(3)
    savePoint=1
    if debug > 0:
        print("SavePoint =", savePoint)
    print("You are now in solitary confinement. The walls are made of solid grey stone, with a few areas tinted an ominous shade of red. If the stains \nare what you think they are, you're in trouble...")
    try:stay = float(input("\nThere is a single window. You peer out, estimating the fall to be around 6 storeys. Maybe a fall from here won't kill you? (1 to jump, 2 to remain)"))
    except ValueError:
        print(" ")
        print("Bad input. Only integers can be entered!")
        choice4()
    if stay == 1:
        print(" ")
        print("You jump from the window! As the ground hurtles towards you, you begin to regret your decision. The last thing you remember is a loud crack as you hit the ground...")
        print(" ")
        time.sleep(2.75)
        gameOver()
    else:
        print(" ")
        print(
            """You decide to remain in the tower! Jumping out the window is a stupid idea anyway! Just as you are thinking about how desperate you'd have to be 
to jump out the window, you hear the rattling of keys as a small metal shutter slides open on the door, revealing the face of your captor...""")
        print(" ")
        time.sleep(1.5)
        print(
            """All that's visible is the eyes of the guard through the small horizontal opening in the metallic door. He tosses a small package of what appears to be food through 
the opening and promptly slams the hatch back shut.""")
        print(" ")
        time.sleep(1.5)
        try:checkDoor = float(input(
            "What do you do now? (1 to check out the package of food, 2 to check out the small hatch in the door)"))
        except ValueError:
            print(" ")
            print("Bad input. Only integers can be entered!")
            choice4()
        if checkDoor == 1:
            print("")
            print(
                "The package contains what looks like crackers. Without a second thought, you gulp them down, having not eaten for days. They taste like cardboard, but food is food!")
            print("\nHealth has been fully restored!\n")
            if playerMaxHealth==20:
                playerHealth=20

            print("You decide to make your way over to the hatch. It could be your only means of escape!")
            time.sleep(1)
            choice5()
        elif checkDoor == 2:
            choice5()
        else:
            print("I don't understand.")
            print(" ")
            checkDoor = int(input(
                "What do you do now? (1 to check out the package of food, 2 to check out the small hatch in the door)"))
            if checkDoor == 1:
                print(" ")
                print(
                    "The package contains what looks like crackers. Without a second thought, you gulp them down, having not eaten for days. They taste like cardboard, but food is food!")
                yn = int(input("Do you check out the hatch now?(1 for yes, 2 for no"))
                hunger = 1
                if yn == 1:
                    choice5()
                elif yn == 2:
                    print(" ")
                    print("You decide to check out the hatch anyway, what's there to lose?")
                    print(" ")
                    time.sleep(1)
                    choice5()
                else:
                    print("I don't understand.")


import time

def debugWarp():
    global damage, save3Corrupt, save2Corrupt, save1Corrupt, hyperPotion, hyperpotionQuantity, testHP, playerHealth, healingPotion, healingpotionQuantity, playerName
    funcWarp = input("Type the name of the function you wish to warp to, or type 'end' to quit: ")
    if funcWarp == "1":
        area1()
    elif funcWarp == "2":
        choice2()
    elif funcWarp == "3":
        choice3()
    elif funcWarp == "4":
        choice4()
    elif funcWarp == "hiding":
        damage=5
        hiding()
    elif funcWarp == "inventory":
        inventory()
    elif funcWarp == "keys":
        getKeys()
    elif funcWarp == "gameover":
        gameOver()
    elif funcWarp == "menu" or funcWarp== "end":
        menu()
    elif funcWarp == "guard":
        damage=7
        encounterGuard()
    elif funcWarp == "save":
        askSave()
    elif funcWarp=="highRank":
        damage=7
        encounterHighRank()
    elif funcWarp=="hiding":
        hiding()
    elif funcWarp=="smallDisplay":
        smallDisplay()
    elif funcWarp=="defeatedHighRank":
        defeatedHighRank()
    elif funcWarp=="convert":
        conversion()
    elif funcWarp=="recover":
        saveRecovery()
    elif funcWarp=="testHP" or funcWarp=="testHyperPotion" or funcWarp=="HPtest":
        print("\n'Hyper Potion x1' has been granted.\n")
        hyperPotion=True
        hyperpotionQuantity=1
        testHP=True
        damage=5
        playerHealth=100
        encounterGuard()
    elif funcWarp=="saveSlot" or funcWarp=="saveslot":
        saveSlot()
    elif funcWarp=="corrupt":
        corruptSave()
    elif funcWarp=="update" or funcWarp=="checkForUpdates":
        checkForUpdates()
    elif funcWarp=="audioPlayer" or funcWarp=="audioPlayer":
        audioPlayer()
    elif funcWarp=="downloadUpdate":
        downloadUpdate()
    elif funcWarp=="newVer" or funcWarp=="newver":
        newVerAvailable()
    elif funcWarp=="printLn" or funcWarp=="println":
        print("\n\n= printLn OK =")
        debugWarp()
    elif funcWarp=="chest7":
        chapterSevenChest()
    elif funcWarp=="report":
        errorReportInternetCheck()
    else:
        print("'"+funcWarp + "' is not a recognised function or warp location. Check spelling and try again.\n")
        debugWarp()

def audioPlayerError():
    global e
    try:choice=int(input("\nAn error occurred, and the selected track could not be played. Choose an option to continue:\n1] Retry\n2] See detailed error info (Advanced)\n3] Get help online/report a bug\n4] Cancel\n--> "))
    except ValueError:
        audioPlayerError()
    if choice==1:
        audioPlayerError()
    elif choice==2:
        print(e)
        audioPlayerError()
    elif choice==3:
        webbrowser.open("https://www.reubenparfrey.wixsite.com/deathtrapdungeon/tutorials/")
        audioPlayerError()
    else:
        audioPlayer()

def audioPlayer():
    global noModuleSound, e
    print("Choose a track to listen to:\n===============================")
    print("""1] Theme of DTD
2] Theme of DTD (Beta)
3] Exploration
4] Encounter!
5] Encounter! (Beta)
6] Battle!
7] Battle with Emperor Juniper!
8] Groov
9] Move
10] Incident Jingle
11] Elevator
12] Elevator (Alt. version)
13] Game Over
14] Background
15] Credits
16] Credits (Alt. version)
17] Curtain Call
===============================
18] Quit""")
    try:choice=int(input("--> "))
    except ValueError:
        audioPlayer()
    if choice==1:
        try:pygame.mixer.music.load('sfx/dtd_main.wav')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Theme of DTD\n")
        audioPlayer()
    elif choice==2:
        try:pygame.mixer.music.load('sfx/dtd_main_beta.wav')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Theme of DTD (Beta)\n")
        audioPlayer()
    elif choice==3:
        try:pygame.mixer.music.load('sfx/exploration.wav')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Exploration\n")
        audioPlayer()
    elif choice==4:
        try:pygame.mixer.music.load('sfx/encounter.wav')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Encounter!\n")
        audioPlayer()
    elif choice==5:
        try:pygame.mixer.music.load('sfx/encounter_full.wav')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Encounter! (Full version)\n")
        audioPlayer()
    elif choice==6:
        try:pygame.mixer.music.load('sfx/battle.mp3')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Battle!\n")
        audioPlayer()
    elif choice==7:
        try:pygame.mixer.music.load('sfx/puppets.mp3')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Battle with Emperor Juniper!\n")
        audioPlayer()
    elif choice==8:
        try:pygame.mixer.music.load('sfx/groov.wav')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Groov\n")
        audioPlayer()
    elif choice==9:
        try:pygame.mixer.music.load('sfx/move.mp3')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Move\n")
        audioPlayer()
    elif choice==10:
        try:pygame.mixer.music.load('sfx/incident_jingle.wav')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Incident Jingle\n")
        audioPlayer()
    elif choice==11:
        try:pygame.mixer.music.load('sfx/elevator.mp3')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Elevator\n")
        audioPlayer()
    elif choice==12:
        try:pygame.mixer.music.load('sfx/load.wav')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Elevator (Alt. version)\n")
        audioPlayer()
    elif choice==13:
        try:pygame.mixer.music.load('sfx/gameover.wav')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Game Over\n")
        audioPlayer()
    elif choice==14:
        try:pygame.mixer.music.load('sfx/basckground.mp3')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Background\n")
        audioPlayer()
    elif choice==15:
        try:pygame.mixer.music.load('sfx/ambient.wav')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Credits\n")
        audioPlayer()
    elif choice==16:
        try:pygame.mixer.music.load('sfx/ambient_percussion.wav')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Credits (Alt. version)\n")
        audioPlayer()
    elif choice==17:
        try:pygame.mixer.music.load('sfx/curtain_call.mp3')
        except Exception as e:
            audioPlayerError()
        pygame.mixer.music.play(0)
        print("\nNOW PLAYING: Curtain Call\n")
        audioPlayer()
    else:
        pygame.mixer.music.stop()
        gameBeatWarp()

def testSound():
    global noModuleSound, sfxMissing
    choice=0
    denied=0
    if noModuleSound is True:
        print("SoundTest cannot be accessed because the required module 'pygame' is not installed.")
        audioOptions()
    elif sfxMissing is True:
        print("SoundTest cannot be accessed because audio data could not be loaded.")
        audioOptions()
    print("\n== SOUND TEST ==")
    time.sleep(0.5)
    try:
        pygame.mixer.music.load("sfx/groov.wav")
    except Exception as e:
        print("\nAn error occurred, and the test audio could not be loaded.")
        audioOptions()
    pygame.mixer.music.play(15)
    print("Can you hear a tune playing? If so, sound should be working!\n1] I hear a tune\n2] I can't hear anything")
    try:choice=int(input("--> "))
    except ValueError:
        pygame.mixer.music.stop()
        audioOptions()
    if choice == 1:
        print("Great, sound is configured and working properly!")
        time.sleep(0.2)
        pygame.mixer.music.stop()
        audioOptions()
    elif choice==2:
        pygame.mixer.music.stop()
        print("\nHere are some things you can try:\n-Ensure volume is turned up on your device\n-Restart the program\n-Reinstall pygame (Source code users only)\n-Ensure audio isn't muted in the game\n-Ensure the game's audio files have been downloaded and saved in the same folder as the Python script\n-Uninstall and reinstall the program (Windows users only)\n\nIf none of the above steps work for you, reach out! Use the 'Report a bug' feature in the 'Options' menu in order to report a bug.")
        try:choice2=int(input("\nRepeat sound test or return to the previous menu?\n1] Repeat the test\n2] Return to previous menu\n--> "))
        except ValueError:
            audioOptions()
        if choice2==1:
            testSound()
        elif choice2==2:
            print(" ")
            audioOptions()
        else:
            pass
    else:
        pygame.mixer.music.stop()
        testSound()


def audioOptions():
    global muteAudio
    global noModuleSound
    global audioMuted
    global customResHorizontal, customResVertical, customResSet, sfxMissing
    if debug !=0:
        print(muteAudio)
    if noModuleSound is True:
        muteAudio=True
    print("\n== AUDIO SETTINGS ==")
    if muteAudio is True:
        print("1] Unmute audio")
    else:
        print("1] Mute audio")
    try:choice=int(input("""2] Test audio
3] Cancel\n-->"""))
    except ValueError:
        print("\nBad input. Only an integer can be entered here!")
        audioOptions()
    if choice==1 and muteAudio is not True:
        if muteAudio != True:
            muteAudio=True
            audioMuted=True
            print("Saving changes...")
            time.sleep(0.2)
            with open('savedprefs.dat', 'wb') as f:
                pickle.dump([muteAudio], f, protocol=2)
            print("Audio has been muted.")
            audioOptions()
    elif choice==1 and muteAudio is True:
        if noModuleSound == True:
            print("Audio cannot be unmuted because the required module 'pygame' is not installed.")
            audioOptions()
        elif sfxMissing is True:
            print("Audio cannot be unmuted because audio data could not be loaded.")
            audioOptions()
        else:
            print("Saving changes...")
            time.sleep(0.2)
            muteAudio=False
            if debug!=0:
                print(muteAudio)
            audioMuted=False
            with open('savedprefs.dat', 'wb') as f:
                pickle.dump([muteAudio], f, protocol=2)
            if debug!=0:
                print(muteAudio)
            print("Audio has been unmuted.")
            audioOptions()
    elif choice==2:
        time.sleep(0.4)
        testSound()
    elif choice==3:
        print(" ")
        options()
    else:
        audioOptions()

def corruptSave():
    file=input("\nEnter the name of the data file you'd like to corrupt, or type 'end' to quit: ")
    if os.path.exists(file+'.dat'):
        confirm = int(input("\nAll data will be corrupted, and may be unrecoverable depending on the selected file. Proceed?\n1] Yes\n2] No\n--> "))
        if file=='end':
            menu()
        if confirm == 1:
            if os.path.exists(file+'.dat'):
                try:
                    with open(file+'.dat', 'wb') as f:
                        pickle.dump([thisFilesFuckedNow], f, protocol=2)
                except Exception:
                    print("\nFile has been corrupted.\n")
                    menu()
        else:
            menu()
    else:
        print("\n'"+file+"' is not a recognised data file, or the file could not be found. Check spelling and try again.")
        corruptSave()

def forceIncompatibility():
    global playerName, savePoint, damage, playerMaxHealth
    playerName="null"
    damage=5
    playerMaxHealth=7
    choice=int(input("\nForce incompatibility for which save file? "))
    if choice==1:
        with open('savedata.dat', 'wb') as f:
            pickle.dump([playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion,
                     area, devProfile], f, protocol=2)
    elif choice==2:
        with open('savedata2.dat', 'wb') as f:
            pickle.dump([playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion,
                     area, devProfile], f, protocol=2)
    elif choice==3:
        with open('savedata3.dat', 'wb') as f:
            pickle.dump([playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion,
                     area, devProfile], f, protocol=2)
    else:
        forceIncompatibility()
    time.sleep(1.3)
    print("\nThe selected save file has been made incompatible. (Format=DTD V2.6-2.8)")
    time.sleep(0.5)
    cmd()

def cmdExe():
    print("Command executed successfully.")
    cmd()

def cmd():
    global debug, noModuleSound, smokescreen, smokescreenQuantity
    command=str(input("\nEnter a command: "))
    command=command.lower()
    if command=="enabledebug=true":
        debug=True
        cmdExe()
    elif command=="enabledebug=false":
        debug=False
        cmdExe()
    elif command=="warp":
        debugWarp()
    elif command=="nomodulesound=true" or command == "nopygame=true":
        noModuleSound=True
        cmdExe()
    elif command=="menu" or command == "end":
        menu()
    elif command=="devoptions" or command=="dev":
        devOptions()
        #fi
    elif command=="forceincompatibility":
        forceIncompatibility()
    elif command=="grant smokescreen x2":
        smokescreen=True
        smokescreenQuantity=2
        print("\n'smokescreen x2' has been granted.\n")
        cmd()
    else:
        print("'"+command+"' is not a reognised command. Check spelling/syntax and try again.")
        cmd()

def removeStartup():
    global activateDebug, loadDevmenu, giveSmokescreen
    choice=input("\nType the name of the command you wish to remove from the startup list. Alternatively, type 'list' to see commands that are executed\nat startup, type 'all' to stop all startup commands from running, or type 'quit' to exit this menu: ")
    if choice=="list":
        executedCommands()
    elif choice=="all":
        if os.path.exists('startup.dat'):
            ass=int(input("\nDelete all startup commands?\n1] Yes\n2] No\n--> "))
            if ass==1:
                os.remove('startup.dat')
                time.sleep(0.6)
                print("All startup commands have been erased.")
                startupCommandOptions()
            else:
                removeStartup()
        else:
            print("Unable to remove; the 'startup' data file cannot be located.")
            removeStartup()
    elif choice=='enabledebug=true':
        activateDebug=False
        with open('startup.dat', 'wb') as f:
            pickle.dump([activateDebug, loadDevmenu, giveSmokescreen], f, protocol=2)
        print("The command 'enabledebug=true' will no longer be executed at startup.")
        startupCommandOptions()
    elif choice=='dev' or choice=='devoptions':
        loadDevmenu=False
        with open('startup.dat', 'wb') as f:
            pickle.dump([activateDebug, loadDevmenu, giveSmokescreen], f, protocol=2)
        print("The command 'devoptions' will no longer be executed at startup.")
        startupCommandOptions()
    elif choice=='grant smokescreen x2':
        giveSmokescreen=False
        with open('startup.dat', 'wb') as f:
            pickle.dump([activateDebug, loadDevmenu, giveSmokescreen], f, protocol=2)
        print("The command 'grant smokescreen x2' will no longer be executed at startup.")
        startupCommandOptions()

def executedCommands():
    global activateDebug, loadDevmenu
    commandSet=False
    try:
        with open('startup.dat', 'rb') as f:
            activateDebug, loadDevmenu, giveSmokescreen= pickle.load(f)
    except Exception:
        print("\nAn error occurred, and the startup data file cannot be opened.")
        startupCommand()
    print("\nCommands that currently run at startup:")
    if activateDebug==True or activateDebug==[True]:
        print("- enabledebug=true")
        commandSet=True
    if loadDevmenu==True or loadDevmenu==[True]:
        print("- devoptions")
        commandSet=True
    if giveSmokescreen==True or giveSmokescreen==[True]:
        print("-grant smokescreen x2")
    if commandSet != True:
        print("= No commands are currently set to run at startup =")
    time.sleep(0.7)
    startupCommandOptions()

def startupSuccess():
    print("\nThis command will now execute the next time DTD is started. Please choose an action to continue:")
    choice=int(input("1] Set another command\n2] Remove a command from startup list\n3] View commands executed upon startup\n4] Quit\n--> "))
    if choice==1:
        startupCommand()
    elif choice==2:
        removeStartup()
    elif choice==3:
        executedCommands()
    else:
        devOptions()

def startupCommand():
    global activateDebug, loadDevmenu, giveSmokescreen
    choice=input("\nEnter a command, and it will be executed every time DTD starts: ")
    if choice=="enabledebug=true":
        activateDebug=True
        with open('startup.dat', 'wb') as f:
            pickle.dump([activateDebug, loadDevmenu, giveSmokescreen], f, protocol=2)
        print("Success! This command will now be executed the next time DTD is started.")
        time.sleep(0.3)
        startupCommandOptions()
    elif choice=="dev" or choice=="devoptions":
        loadDevmenu=True
        with open('startup.dat', 'wb') as f:
            pickle.dump([activateDebug, loadDevmenu, giveSmokescreen], f, protocol=2)
        print("Success! This command will now be executed the next time DTD is started.")
        time.sleep(0.3)
        startupCommandOptions()
    elif choice=="grant smokescreen x2":
        giveSmokescreen=True
        with open('startup.dat', 'wb') as f:
            pickle.dump([activateDebug, loadDevmenu, giveSmokescreen], f, protocol=2)
        print("Success! This command will now be executed the next time DTD is started.")
        time.sleep(0.3)
        startupCommandOptions()

    else:
        print("'"+choice+"' is not a recognised command. Check spelling/syntax and try again.")
        startupCommand()

def startupCommandOptions():
    choice=int(input("\nChoose an option to continue:\n1] Set a command to run at startup\n2] Remove a command from startup list\n3] View commands executed at startup\n4] Cancel\n--> "))
    if choice==1:
        startupCommand()
    elif choice==2:
        removeStartup()
    elif choice==3:
        executedCommands()
    else:
        devOptions()

def devOptions():
    global debug,savePoint,noModuleSound,muteAudio, damage, loadDevmenu
    global playerName
    global playerHealth
    global playerMaxHealth
    global healingPotion, gotRope
    global smokescreen, hyperPotion
    global devProfile
    global area, loadDevmenu
    if loadDevmenu is True or loadDevmenu is [True]:
        loadDevmenu=False
    choice=int(input("\n== DEVELOPER OPTIONS ==\n1] Error logging\n2] Startup commands\n3] Execute a command\n4] Erase data files\n5] Modify 'savePoint' value\n6] Return to main menu\n--> "))
    if choice==1:
        errorReporting()
    elif choice==2:
        startupCommandOptions()
    elif choice==3:
        print("\n== COMMAND LINE ==\n© Reuben Parfrey 2021")
        cmd()
    elif choice==6:
        if loadDevmenu is True or loadDevmenu is [True]:
            loadDevmenu=False
        menu()
    elif choice==4:
        sdbackup=input("\nEnter the name of the data file you'd like to erase, or type 'end' to return to the previous menu: ")
        if sdbackup=="end":
            devOptions()
        confirm=int(input("Are you sure you'd like to erase this data file? This action cannot be undone\n1] Yes\n2] No\n--> "))
        if confirm==1:
            print("Erasing "+sdbackup+".dat...")
            time.sleep(0.6)
            try:os.remove(sdbackup+'.dat')
            except FileNotFoundError:
                print(sdbackup,"could not be deleted; the file wasn't found.")
                devOptions()
            print(sdbackup,"has successfully been erased.")
            devOptions()
        elif confirm==2:
            devOptions()
    elif choice==5:
        print("\nSavePoint value can't be modified in this version of the game. Revert to an older version and try again.")
        devOptions()

def updateFailure():
    time.sleep(0.7)
    print("\nAn error occurred, and the data could not be downloaded. Choose an option to continue:\n1] Retry\n2] Download updates manually\n3] See detailed error info (advanced)\n4] Get help online/Report a bug\n5] Cancel")
    try: choice=int(input("--> "))
    except ValueError:
        updateFailure()
    if choice==1:
        downloadUpdate()
    elif choice==2:
        webbrowser.open("https://reubenparfrey.wixsite.com/deathtrapdungeon/downloads/")
    elif choice==3:
        print(e)
        updateFailure()
    elif choice==4:
        webbrowser.open("https://reubenparfrey.wixsite.com/deathtrapdungeon/tutorials/")
        updateFailure()
    else:
        menu()



def newVerAvailableOptions():
    global checkForUpdatesThroughOptions
    choice=0
    print("\nA new version of DeathTrap Dungeon is available!\n1] Download the new version\n2] View the release notes\n3] Cancel")
    try:choice=int(input("--> "))
    except ValueError:
        newVerAvailableOptions()
    if choice==1:
        downloadUpdate()
    elif choice==2:
        checkForUpdatesThroughOptions=True
        downloadReleaseNotes()
    else:
        updOptions()

def checkForUpdatesError():
    choice=0
    try:choice=int(input("\nAn error occurred, and the server could not be reached. Choose an option to continue:\n1] Retry\n2] Get help online/report a bug\n3] Check for new versions online\n4] Cancel\n--> "))
    except ValueError:
        checkForUpdatesError()
    if choice==1:
        internet_on_options()
    elif choice==2:
        webbrowser.open('https://www.reubenparfrey.wixsite.com/deathtrapdungeon/tutorials/')
        checkForUpdatesError()
    elif choice==3:
        webbrowser.open('https://www.reubenparfrey.wixsite.com/deathtrapdungeon/downloads/')
        checkForUpdatesError()
    else:
        updOptions()

def optionsCheckForUpdatesOld(): #The old update system; only here for backwards compatibility.
    global currentVer
    print("Checking for updates...")
    time.sleep(0.5)
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "https://dtdlatestver.000webhostapp.com"
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    if debug != 0:
        print(response.read())
    contents = response.read()
    if debug != 0:
        print(contents)
    shortCont = contents.split(b'<p>')[1].lstrip().split(b'</p>')[0]
    if debug != 0:
        print(shortCont)
    if shortCont == currentVer:
        print("\nYou're up to date! There are no new versions of DeathTrap Dungeon available at this time.")
        updOptions()
    elif shortCont > currentVer:
        newVerAvailableOptions()
    else:
        checkForUpdatesError()

def optionsCheckForUpdates():
    global currentVer, debug
    print("Checking for updates...")
    time.sleep(0.3)
    ssl._create_default_https_context = ssl._create_unverified_context
    url = "http://www.dtdlatestversion.xp3.biz"
    hdr = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
    req = urllib.request.Request(url, headers=hdr)
    response = urllib.request.urlopen(req)
    contents = response.read()
    shortCont = contents.split(b'<p>')[1].lstrip().split(b'</p>')[0]
    if debug != 0:
        print(response.read)
        print(contents)
        print(shortCont)
    if shortCont == currentVer:
        print("\nYou're up to date! There are no new versions of DeathTrap Dungeon available at this time.")
        updOptions()
    elif shortCont > currentVer:
        newVerAvailableOptions()
    else:
        checkForUpdatesError()

def internet_on_options():
    global skipUpdateCheck, debug
    try:
        print("Connecting to the internet...")
        time.sleep(1.1)
        socket.setdefaulttimeout(5)
        host = socket.gethostbyname("www.google.com")
        s = socket.create_connection((host, 80), 2)
        s.close()
        if debug != 0:
            print("Connected!")
            print(host)
        optionsCheckForUpdates()
    except Exception as e:
        print("\nYou are not connected to the internet. Connect to a network and try again.")
        if debug!=0:
            print(e)
        updOptions()

def eraseSave():
    print("\n== DELETE SAVE DATA ==\nSelect a save file to erase:")
    slot1Used = True
    slot2Used = True
    slot3Used = True
    print("===============================")
    try:
        with open('savedata.dat', 'rb') as f:
            playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat = pickle.load(
                f)
    except FileNotFoundError:
        print("1] SLOT 1 - [EMPTY]")
        slot1Used = False
    except EOFError or pickle.UnpicklingError:
        print("1] SLOT 1 - [CORRUPT]")
        slot1Used = False
    except ValueError:
        print("1] SLOT 1 - [INCOMPATIBLE]")
        slot1Used = False
    if slot1Used == True and gameBeat is False:
        try:
            print("1] SLOT 1 -", playerName)
        except Exception:
            pass
    elif slot1Used == True and gameBeat is True:
        try:
            print("1] SLOT 1 -", playerName, " *")
        except Exception:
            pass
    try:
        with open('savedata2.dat', 'rb') as f:
            playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat = pickle.load(
                f)
    except FileNotFoundError:
        print("2] SLOT 2 - [EMPTY]")
        slot2Used = False
    except EOFError or pickle.UnpicklingError:
        print("2] SLOT 2 [CORRUPT]")
        slot2Used=False
    except ValueError:
        print("2] SLOT 2 - [INCOMPATIBLE]")
        slot2Used = False
    if slot2Used == True and gameBeat is False:
        try:
            print("2] SLOT 2 -", playerName)
        except Exception:
            pass
    elif slot2Used == True and gameBeat is True:
        try:
            print("2] SLOT 2 -", playerName, " *")
        except Exception:
            pass
    try:
        with open('savedata3.dat', 'rb') as f:
            playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat = pickle.load(
                f)
    except FileNotFoundError:
        print("3] SLOT 3 - [EMPTY]")
        slot3Used = False
    except EOFError or pickle.UnpicklingError:
        print("3] SLOT 3 - [CORRUPT]")
        slot3Used=False
    except ValueError:
        print("3] SLOT 3 - [INCOMPATIBLE]")
        slot3Used = False
    if slot3Used == True and gameBeat is False:
        try:
            print("3] SLOT 3 -", playerName)
        except Exception:
            pass
    elif slot3Used == True and gameBeat is True:
        try:
            print("3] SLOT 3 -", playerName, " *")
        except Exception:
            pass
    print("===============================")
    print("4] Cancel")
    try:choice = int(input("--> "))
    except ValueError:
        print("\nBad input. Only integers can be entered here!")
        eraseSave()
    if choice==4:
        print(" ")
        savePoint=0
        playerName=""
        damage=5
        playerHealth=20
        playerMaxHealth=20
        gameBeat = False
        smokescreen = False
        hyperPotion = False
        healingPotion = False
        options()
    #elif choice==1 and slot1Used==False:
    #    print("\nThere is no save data stored in save slot 1.")
    #    eraseSave()
    #elif choice==2 and slot2Used==False:
    #    print("\nThere is no save data stored in save slot 2.")
    #    eraseSave()
    #elif choice==3 and slot3Used==False:
    #    print("\nThere is no save data stored in save slot 3.")
    #    eraseSave()
    elif choice==1:
        print("Are you sure? This will delete all saved progress, as well as any items or upgrades that may have been obtained. Once data has been erased, it cannot be recovered.")
        time.sleep(1.7)
        try:
            delete = int(input("1] Erase Save Data \n2] Cancel\n-->"))
        except ValueError:
            print("\nBad input. Only integers can be entered here!")
            eraseSave()
        if delete == 1:
            print("Deleting data...")
            time.sleep(0.3)
            if os.path.exists('savedata.dat'):
                os.remove('savedata.dat')
            else:
                print("The selected slot contains no save data.")
                eraseSave()
            if os.path.exists('sdbackup.dat'):
                print("Deleting backup data...")
                time.sleep(0.2)
                os.remove('sdbackup.dat')
            else:
                pass
            print("Save data has been erased.")
            time.sleep(1.7)
            eraseSave()
        elif delete == 2:
            eraseSave()
        else:
            print("I don't understand.")
            eraseSave()
    elif choice==2:
        print("Are you sure? This will delete all saved progress, as well as any items or upgrades that may have been obtained. Once data has been erased, it cannot be recovered.")
        time.sleep(2)
        try:
            delete = int(input("1] Erase Save Data \n2] Cancel\n-->"))
        except ValueError:
            print("\nBad input. Only integers can be entered here!")
            eraseSave()
        if delete == 1:
            print("Deleting data...")
            time.sleep(0.2)
            if os.path.exists('savedata2.dat'):
                os.remove('savedata2.dat')
            else:
                print("The selected slot contains no save data.")
                eraseSave()
            if os.path.exists('sdbackup2.dat'):
                print("Deleting backup data...")
                time.sleep(0.3)
                os.remove('sdbackup2.dat')
            else:
                pass
            print("Save data has been erased.")
            time.sleep(1)
            eraseSave()
        elif delete == 2:
            eraseSave()
        else:
            print("I don't understand.")
            eraseSave()
    elif choice==3:
        print("Are you sure? This will delete all saved progress, as well as any items or upgrades that may have been obtained. Once data has been erased, it cannot be recovered.")
        time.sleep(1.7)
        try:
            delete = int(input("1] Erase Save Data \n2] Cancel\n-->"))
        except ValueError:
            print("\nBad input. Only integers can be entered here!")
            eraseSave()
        if delete == 1:
            print("Deleting data...")
            time.sleep(0.4)
            if os.path.exists('savedata3.dat'):
                os.remove('savedata3.dat')
            else:
                print("The selected slot contains no save data.")
                eraseSave()
            if os.path.exists('sdbackup3.dat'):
                print("Deleting backup data...")
                time.sleep(0.3)
                os.remove('sdbackup3.dat')
            else:
                pass
            print("Save data has been erased.")
            time.sleep(1.7)
            eraseSave()
        elif delete == 2:
            eraseSave()
        else:
            eraseSave()

def updOptions():
    global skipUpdateCheck
    print("\n== UPDATE SETTINGS ==")
    try:choice=int(input("1] Check for updates\n2] Automatic updates\n3] Cancel\n--> "))
    except ValueError:
        updOptions()
    if choice==1:
        internet_on_options()
    elif choice==3:
        print(" ")
        options()
    elif choice==2:
        if skipUpdateCheck==False or skipUpdateCheck==[False]:
            print("\nAutomatic updates are enabled. Disabling this means you may miss out on newer versions of the game when they become available. Continue?")
            try:updChoice=int(input("1] Yes\n2] No\n--> "))
            except ValueError:
                updOptions()
            if updChoice==1:
                print("Saving changes...")
                time.sleep(0.5)
                skipUpdateCheck = True
                with open('updateprefs.dat', 'wb') as f:
                    pickle.dump([skipUpdateCheck], f, protocol=2)
                print("Automatic updates have been disabled.")
                updOptions()
            elif updChoice==2:
                updOptions()
        elif skipUpdateCheck==True or [True]:
            print("\nAutomatic updates are currently disabled. Enable them?")
            try:updChoice=int(input("1] Yes\n2] No\n--> "))
            except ValueError:
                updOptions()
            if updChoice==1:
                print("Saving changes...")
                time.sleep(0.5)
                skipUpdateCheck = False
                with open('updateprefs.dat', 'wb') as f:
                    pickle.dump([skipUpdateCheck], f, protocol=2)
                print("Automatic updates have been enabled.")
                updOptions()
            elif updChoice==2:
                updOptions()
    else:
        updOptions()

def smallDisplayDisabled():
    global smallerDisplay
    print("Saving changes...")
    smallerDisplay = False
    time.sleep(0.7)
    with open('displaysettings.dat', 'wb') as f:
        pickle.dump([smallerDisplay], f, protocol=2)
    print("Resolution settings have been reverted back to default.")
    videoSettings()

def smallDisplayEnabled():
    global smallerDisplay
    print("Resolution has been adjusted to fit smaller displays. Choose an option to continue:")
    try:choice=int(input("1] Keep these settings\n2] Cancel\n--> "))
    except ValueError:
        smallDisplayEnabled()
    if choice==1:
        print("Saving changes...")
        time.sleep(0.8)
        smallerDisplay=True
        with open('displaysettings.dat', 'wb') as f:
            pickle.dump([smallerDisplay], f, protocol=2)
        print("Success! These settings will take effect every time the game is started.")
        videoSettings()
    else:
        print("Reverting settings...")
        time.sleep(1.2)
        os.system('mode con: cols=180 lines=65')
        print("Resolution settings have been reverted back to default.")
        videoSettings()

def smallDisplay():
    global smallerDisplay
    if debug==1:
        print(smallerDisplay)
    if smallerDisplay==[True]:
        smallerDisplay=True
    elif smallerDisplay==[False]:
        smallerDisplay=False
    if debug!=0:
        print(smallerDisplay)
    if smallerDisplay == False:
        try:choice=int(input("\nOptimise DeathTrap Dungeon for use on smaller displays? This will reduce the resolution, however this may affect how certain graphics \nlook. It's recommended that you only adjust this setting if you're having issues with how the game is displayed. Continue?\n1] Yes\n2] No\n--> "))
        except ValueError:
            smallDisplay()
        if choice==1:
            print("Applying new resolution settings...")
            time.sleep(1.3)
            os.system('mode con: cols=145 lines=50')
            smallDisplayEnabled()
        else:
            print("The resolution has not been changed.\n")
            videoSettings()

    else:
        try:choice = int(input("\nThe game is currently running in a lowered resolution. Revert back to default resolution settings?\n1] Yes\n2] No\n--> "))
        except ValueError:
            smallDisplay()
        if choice == 1:
            print("Applying new resolution settings...")
            time.sleep(1.1)
            os.system('mode con: cols=180 lines=65')
            smallDisplayDisabled()

def videoSettings():
    global smallerDisplay
    if smallerDisplay==[True]:
        smallerDisplay=True
    if smallerDisplay==[False]:
        smallerDisplay=False
    print("\n== DISPLAY SETTINGS ==")
    if debug!=0:
        print(smallerDisplay)
    if smallerDisplay is True:
        print("1] Run in default resolution\n2] Cancel")
    elif smallerDisplay is False:
        print("1] Optimise for smaller display\n2] Cancel")
    try:choice=int(input("--> "))
    except ValueError:
        videoSettings()
    if choice==1:
        smallDisplay()
    elif choice==2:
        print(" ")
        options()
    else:
        print("I don't understand.")
        videoSettings()

def errorReporting():
    global disableLogging
    if disableLogging == [True]:
        disableLogging=True
    if disableLogging == [False]:
        disableLogging=False
    print("\n== ERROR LOGGING ==")
    if disableLogging is False:
        print("1] Disable error logging")
    else:
        print("1] Enable error logging")
    print("2] Erase logged data\n3] Cancel")
    try:choice=int(input("--> "))
    except ValueError:
        errorReporting()
    if choice==1 and disableLogging is False:
        try:choice2=int(input("\nError logging is enabled. Disabling this means errors may be harder to troubleshoot. Continue?\n1] Yes\n2] No\n--> "))
        except ValueError:
            errorReporting()
        if choice2==1:
            disableLogging=True
            print("Saving changes...")
            time.sleep(0.5)
            with open('logsettings.dat', 'wb') as f:
                pickle.dump([disableLogging], f, protocol=2)
            print("Error logging has been disabled.\n")
            errorReporting()
        else:
            print(" ")
            errorReporting()
    elif choice==1 and disableLogging is True:
        try:choice2=int(input("\nError logging is disabled. Enable it?\n1] Yes\n2] No\n--> "))
        except ValueError:
            errorReporting()
        if choice2==1:
            disableLogging=False
            print("Saving changes...")
            time.sleep(0.4)
            with open('logsettings.dat', 'wb') as f:
                pickle.dump([disableLogging], f, protocol=2)
            print("Error logging has been enabled.\n")
            errorReporting()
        else:
            print(" ")
            errorReporting()
    elif choice==2:
        choice2=int(input("\nErase logged data?\n1] Yes\n2] No\n--> "))
        if choice2==1:
            print("Erasing data...")
            time.sleep(0.2)
            with open('crash.log', 'w'):
                pass
            print("Logged data has been erased.\n")
            errorReporting()
    else:
        devOptions()

def bugReport():
    print("Found a bug? Use this feature to report it! Please note that this feature requires you to be connected to the internet.")
    try:choice=int(input("1] Report a bug online\n2] Cancel\n--> "))
    except ValueError:
        bugReport()
    if choice==1:
        time.sleep(0.8)
        webbrowser.open("https://reubenparfrey.wixsite.com/deathtrapdungeon/report-a-bug/")
        print(" ")
        options()
    else:
        print(" ")
        options()

def options():
    global playerName
    global playerHealth
    global optionsChoice
    global playerMaxHealth
    global healingPotion
    global hyperPotion
    global smokescreen
    global devProfile
    global savePoint
    global skipUpdateCheck
    print("Select an option:\n===============================")
    print("""1] Audio settings
2] Display settings
3] Update settings
4] Delete save data
5] Report a bug
===============================
6] Cancel""")
    if debug != 0:
        print("7] Developer options")
    try:optionsChoice=int(input("--> "))
    except ValueError:
        print("\nBad input. Only integers can be entered here!")
        options()
    if optionsChoice == 1:
        audioOptions()
    elif optionsChoice == 2:
        videoSettings()
    elif optionsChoice == 4:
        eraseSave()
    elif optionsChoice == 3:
        updOptions()
    elif optionsChoice==7 and debug != 0:
        print(
            "\nDISCLAIMER:\nEverything within this menu is experimental, and should only be modified if you know what you're doing. Settings being incorrectly \nconfigured may result in the game becoming highly unstable, or even completely unplayable. Proceed with caution!")
        print("\n++DTD v2.9 rev A++")
        devOptions()
    elif optionsChoice==5:
        print("\n== REPORT A BUG ==")
        bugReport()
    elif optionsChoice == 6:
        print(" ")
        menu()
    else:
        print("\nI don't understand. Try again!")
        options()




def soundtest():
    global noModuleSound
    stopAudio=False
    if noModuleSound==1:
        print("Sound test can't be accessed because the required module 'pygame' couldn't be found. Returning to menu...")
        menu()
    choice=input("\nEnter the filename of the sound you want to hear. Alternatively, type 'stop' to halt playback of the \ncurrently playing track, or 'end' to return to menu:")
    if choice=="end":
        print(" ")
        menu()
    elif choice=="stop":
        pygame.mixer.music.stop()
        print("\nPlayback has been halted via user input.")
        soundtest()
    else:
        try:pygame.mixer.music.load('sfx/'+choice+'.wav')
        except Exception:
            print("\nUnable to play sound; audio file doesn't exist.")
            soundtest()
        pygame.mixer.music.play(1)
        print("\nSuccessfully played '"+choice+"'")
        soundtest()

def incompatiblePlayerProfile():
    try:choice = int(input("\nSave data cannot be loaded because it is incompatible with this version of DeathTrap Dungeon. Would you like to convert it so it can be loaded on \nnewer versions of the game?\n1] Yes\n2] No\n--> "))
    except ValueError:
        incompatiblePlayerProfile()
    if choice==1:
        conversion()
    else:
        profile()

def corruptPlayerProfile():
    try:choice=int(input("\nSave data is corrupt and cannot be loaded. Choose an option to continue:\n1] Launch Save Data Recovery Utility\n2] Cancel\n--> "))
    except ValueError:
        corruptPlayerProfile()
    if choice==1:
        saveRecovery()
    else:
        profile()

def profile():
    global savePoint
    global playerMaxHealth
    global playerName
    global createProfile
    global smokescreen
    global healingPotion
    global hyperPotion
    global devProfile, save1Corrupt, save2Corrupt, save3Corrupt, convertSlotOne, convertSlotTwo, convertSlotThree, gameBeat
    gameBeat=False
    savefileCorrupt=False
    smokescreen=False
    hyperPotion=False
    healingPotion=False
    print("Select a Player Profile to view:")
    print("===============================")
    slot1Used = True
    slot2Used = True
    slot3Used = True
    try:
        with open('savedata.dat', 'rb') as f:
            playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat = pickle.load(
                f)
    except FileNotFoundError:
        print("1] SLOT 1 - [EMPTY]")
        slot1Used = False
    except EOFError:
        print("1] SLOT 1 - [CORRUPT]")
        slot1Used = False
        save1Corrupt=True
    except ValueError:
        print("1] SLOT 1 - [INCOMPATIBLE]")
        slot1Used = False
        convertSlotOne=True
    if slot1Used == True and gameBeat is False:
        try:
            print("1] SLOT 1 -", playerName)
        except Exception:
            pass
    elif slot1Used == True and gameBeat is True:
        try:
            print("1] SLOT 1 -", playerName, " *")
        except Exception:
            pass
    else:
        pass
    try:
        with open('savedata2.dat', 'rb') as f:
            playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat = pickle.load(
                f)
    except FileNotFoundError:
        print("2] SLOT 2 - [EMPTY]")
        slot2Used = False
    except EOFError:
        print("2] SLOT 2 - [CORRUPT]")
        slot2Used = False
        save2Corrupt = False
    except ValueError:
        print("2] SLOT 2 - [INCOMPATIBLE]")
        slot2Used = False
        convertSlotTwo = True
    if slot2Used==True and gameBeat is False:
        try:print("2] SLOT 2 -",playerName)
        except Exception:
            pass
    elif slot2Used==True and gameBeat is True:
        try:print("2] SLOT 2 -",playerName," *")
        except Exception:
            pass
    else:
        pass
    try:
        with open('savedata3.dat', 'rb') as f:
            playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat = pickle.load(
                f)
    except FileNotFoundError:
        print("3] SLOT 3 - [EMPTY]")
        slot3Used = False
    except EOFError:
        print("3] SLOT 3 - [CORRUPT]")
        slot3Used = False
        save3Corrupt = True
    except ValueError:
        print("3] SLOT 3 - [INCOMPATIBLE]")
        slot3Used = False
        convertSlotThree = True
    if slot3Used==True and gameBeat is False:
        try:print("3] SLOT 3 -",playerName)
        except Exception:
            pass
    elif slot3Used==True and gameBeat is True:
        try:print("3] SLOT 3 -",playerName," *")
        except Exception:
            pass
    else:
        pass
    print("===============================")
    print("4] Cancel")
    try:choice = int(input("--> "))
    except ValueError:
        profile()
    if choice==4:
        print(" ")
        gameBeat = False
        savefileCorrupt = False
        smokescreen = False
        hyperPotion = False
        healingPotion = False
        playerMaxHealth = 20
        menu()
    elif choice==1:
        print("Loading data...")
        time.sleep(0.4)
        try:
            with open('savedata.dat', 'rb') as f:
                playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat= pickle.load(f)
        except FileNotFoundError:
            print("\nThe selected slot contains no save data.\n")
            profile()
        except pickle.UnpicklingError and EOFError:
            save1Corrupt=True
            corruptPlayerProfile()
        except ValueError:
            incompatiblePlayerProfile()
    elif choice==2:
        print("Loading data...")
        time.sleep(0.4)
        try:
            with open('savedata2.dat', 'rb') as f:
                playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat= pickle.load(f)
        except FileNotFoundError:
            print("\nThe selected slot contains no save data.\n")
            profile()
        except pickle.UnpicklingError and EOFError:
            save2Corrupt=True
            corruptPlayerProfile()
        except ValueError:
            incompatiblePlayerProfile()
    elif choice==3:
        #print(" ")
        print("Loading data...")
        time.sleep(0.3)
        try:
            with open('savedata3.dat', 'rb') as f:
                playerName, savePoint, damage, playerMaxHealth, playerHealth, smokescreen, healingPotion, area, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, gameBeat= pickle.load(f)
        except FileNotFoundError:
            print("\nThe selected slot contains no save data.\n")
            profile()
        except pickle.UnpicklingError and EOFError:
            save3Corrupt=True
            corruptPlayerProfile()
        except ValueError:
            incompatiblePlayerProfile()
    #elif choice==1 and slot1Used is False or choice==2 and slot2Used is False or choice==3 and slot3Used is False:
    #    print("\nThe selected slot contains no save data.\n")
    #    profile()

    print("\n===============================")
    print("Name: %s" % playerName)
    print("Attack Damage: %d" % damage)
    print("Health: %i/%i" % (playerHealth, playerMaxHealth))
    print("")
    print("HELD ITEMS:")
    if hyperPotion is True:
        print("- Hyper Potion  x"+str(hyperpotionQuantity))
    if smokescreen is True:
        print("- Smokescreen  x"+str(smokescreenQuantity))
    if healingPotion is True:
        print("- Potion of Healing  x"+str(healingpotionQuantity))
    #if healingPotion and smokescreen and hyperPotion is False:
    if hyperPotion is not True and smokescreen is not True and healingPotion is not True:
        print("= No held items =")
    print(" ")
    print("PROGRESS:")
    if savePoint==0:
        print("Chapter 1: Enter The Dungeon")
    elif savePoint==1:
        print("Chapter 2: Solitary Confinement")
    elif savePoint==2:
        print("Chapter 3: The Great Escape")
    elif savePoint==3:
        print("Chapter 4: What Doesn't Kill You Makes You Stronger")
    elif savePoint==4:
        print("Chapter 5: A Breath Of Fresh Air")
    elif savePoint==5:
        print("Chapter 6: A Puzzle In Darkness")
    elif savePoint==6:
        print("Chapter 7: With Great Power")
    elif savePoint==7:
        print("Chapter 8: Finale")
    else:
        print("No progress has been saved.")
    if not gameBeat:
        pass
    else:
        print("\nThe game has been beaten.")
    print("===============================\n")
    time.sleep(0.8)
    gameBeat=False
    savefileCorrupt=False
    smokescreen=False
    hyperPotion=False
    healingPotion=False
    playerMaxHealth=20
    profile()

def story():
    print(
        "\nThe land of Medway was a quiet and soothing place. Day in and day out, people went about the mundanities of life with little more than a care in")
    time.sleep(1.5)
    print("the world. The ruler of this land, Emperor Juniper, was a kind and gentle man... until one day, something changed. He isolated himself")
    time.sleep(1.5)
    print("from everyone, and threw anyone who questioned his dangerous antics into the darkest, most desolate dungeon in the land. You were one of")
    time.sleep(1.5)
    print("the many poor souls left to rot, and you, like many others, can't survive much longer on the scraps the guards feed all the inmates. What caused")
    time.sleep(1.5)
    print("the downfall of Medway? Can you escape, put an end to Emperor Juniper's reign of terror, and return Medway to it's former glory? Only time will tell...")
    time.sleep(5)
    print("""

    """)
    nameInputAsk()

def chapterTwo():
    global savePoint, debug
    savePoint=1
    if debug > 0:
        print("SavePoint =", savePoint)
    print(" ")
    time.sleep(3)
    askSave()

def chapterOneEscape():
    try:
        left1 = int(input("As you round the corner, you come to a fork in the passage. You must decide which way to go! Left or right? (1 for left, 2 for right):"))
    except ValueError:
        print(" ")
        print("Bad input. Only integers can be entered!")
        chapterOneEscape()
    if left1 == 1:
        print("You decide to go left! As you round another corner, your heart sinks; you can see a heavy iron door blocking your path! You try to pull it \nopen but to no avail. It's jammed!")
        time.sleep(1.75)
        print(" ")
        print(
            "You can hear the echoing footsteps getting closer now, reverberating off the stone walls. You drop to the ground as the guard rounds the \ncorner. He cocks his gun...")
        time.sleep(1.75)
        gameOver()
    elif left1 == 2:
        print(" ")
        print(
            "You go right!! As you race down the grimy stone corridor, your heart drops; you can see a congestion of guards gathered at the bottom, their guns \ntrained on you.")
        print(" ")
        time.sleep(1.75)
        print("You sink to the ground in dismay and despair. There's no escape...")
        gameOver()
    else:
        print("The guard catches up because that's not a valid choice! He shoots and doesn't miss...")
        gameOver()

def choice3():
    global savePoint
    global muteAudio
    print(" ")
    try:runForIt = int(input("Do you let the guard take you to solitary confinement? [1] Or do you make a break for it? [2]"))
    except ValueError:
        print(" ")
        print("Bad input. Only integers can be entered!")
        choice3()
    if runForIt == 1:
        time.sleep(0.75)
        print("\nYou are dragged to solitary confinement, and the heavy iron door is slammed shut behind you.")
        time.sleep(1)
        chapterTwo()
    elif runForIt == 2:
        print("You make a break for it! As you run down the grimy corridor, you can hear the rapid slams of footsteps behind you; the guard is hot on your tail.")
        time.sleep(1)
        print(" ")
        chapterOneEscape()
    else:
        choice3()


def choice2Alternate():
    global savePoint
    print("\nA nearby guard spots the commotion and comes running over with backup. There are too many guards to take on alone!")
    time.sleep(1)
    print("\nThe guards roughly grasp you, yelling something about solitary confinement. Looks like that's where you're headed next...")
    time.sleep(2)
    savePoint=1
    if debug > 0:
        print("SavePoint =", savePoint)
    time.sleep(3)
    askSave()

def choice2():
    global item
    global area, debug
    area=1
    time.sleep(1.5)
    try:dropSaw = int(input("\nYou eye up the shard of glass. You can either threaten the guard [1], or wave the shard around and scream like a maniac [2]."))
    except ValueError:
        print(" ")
        print("Bad input. Only integers can be entered!")
        choice2()
    if dropSaw == 1:
        print("\nYou begin to shout at the guard, he turns.")
        time.sleep(1.25)
        print("\nYou raise the shard, and he raises his weapon...")
        time.sleep(1.5)
        if debug!=0:
            print("area=",area)
        encounterGuard()
    elif dropSaw == 2:
        time.sleep(0.75)
        print("\nYou decide to scream and wave the glass shard around. The nearby guard turns and makes his way over to your cell, muttering something about putting you into\nsolitary confinement.")
        time.sleep(1.5)
        choice3()
    elif dropSaw == 9 and debug != 0:
        inventory()
    else:
        choice2()

def chapterOneChoice():
    try:choice = int(input("\nWhat will you do? [1] to examine your surroundings further, [2] to try rattling the cell door. "))
    except ValueError:
        print(" ")
        print("Bad input. Only integers can be entered!")
        chapterOneChoice()
    if choice == 1:
        print("\nYou glance around, looking for anything that could aid you. You notice a shard of glass laying in one corner.")
        time.sleep(1.5)
        print("\nYou pocket it, sure it'll come in handy.")
        choice2()
    elif choice == 2:
        print("\nYou rattle the cell door! But it's no use. The guard on the other side of the door doesn't even look at you.")
        chapterOneChoice()
    else:
        chapterOneChoice()

def area1():
    global debug
    global area
    area=1
    print("\n== Chapter 1: Enter The Dungeon ==\n")
    if muteAudio != True:
        pygame.mixer.music.load("sfx/thud.wav")
        pygame.mixer.music.play(1)
    time.sleep(3)
    print("\nYou slowly come to. You are lying on a hard, cold wireframe bed, in the corner of your dark cell.")
    time.sleep(1.5)
    print("\nHow long had you been here for? A week? A month? Certainly long enough to lose track of time.")
    time.sleep(1.5)
    print("\nYou groan, and slowly stand up. You are malnourished and weak; you know that you won't survive here much longer.")
    time.sleep(1.5)
    print("\nYou glance around at this all-too-familiar environment. A single iron barred door is the only point natural light enters.")
    time.sleep(1.5)
    print("\nThe floor is made entirely of concrete, and the walls are constructed of damp, mossy stone.")
    time.sleep(1.5)
    print("\nA guard stands on the other side of the door, his back turned towards you.")
    time.sleep(1.5)
    chapterOneChoice()


def menu():
    global debug
    global damage
    global playStory
    global newgame
    global compatibility
    global devprofile
    global muteAudio
    global creditsRolled, area
    creditsRolled=False
    global noModuleSound, activateDebug, currentVer, sfxMissing, gameBeat, savePoint, playerMaxHealth, playerHealth, smokescreen, healingPotion, hyperPotion
    playStory = False
    savePoint = 0
    area = 0
    gameBeat = False
    playerHealth = 20
    playerMaxHealth = 20
    smokescreen = False
    healingPotion = False
    hyperPotion = False
    damage = 5
    newgame=0
    if activateDebug == True or activateDebug == [True]:
        debug=1
        activateDebug = False
    if loadDevmenu == True or loadDevmenu == [True]:
        devOptions()
    if sfxMissing is False:
        try:
            with open('savedprefs.dat', 'rb') as f:
                muteAudio=pickle.load(f)
        except FileNotFoundError:
            pass
        except pickle.UnpicklingError or ValueError:
            print("\n== ERROR LOADING SAVED PREFERENCES ==")
            print("The file containing saved preferences is corrupt. The game will continue to work as normal, however all settings have been reset to default.\n")
            muteAudio=False
            with open('savedprefs.dat', 'wb') as f:
                pickle.dump([muteAudio], f, protocol=2)
            time.sleep(0.7)
        except EOFError:
            print("\n== ERROR LOADING SAVED PREFERENCES ==")
            print("The file containing saved preferences is corrupt. The game will continue to work as normal, however all settings have been reset to default.\n")
            muteAudio=False
            with open('savedprefs.dat', 'wb') as f:
                pickle.dump([muteAudio], f, protocol=2)
            time.sleep(0.7)
    if muteAudio == [True]:
        muteAudio=True
    elif sfxMissing is True:
        muteAudio = True
    else:
        muteAudio=False

    print("""+------------------------------+
|      DEATHTRAP DUNGEON       |
+------------------------------+
| [1] New game                 |
| [2] Load saved game          |
| [3] View Player Profile      |
| [4] Options                  |
| [5] About DeathTrap Dungeon  |
| [6] Quit                     | 
+------------------------------+""")
    try:newgame = int(input("          ---> "))
    except ValueError:
        print(" ")
        print("Bad input. Only integers can be entered!")
        print(" ")
        menu()
    if debug > 0:
        print("= Debug mode is enabled= ")

    if newgame == 1:
        if noModuleSound or noPyGameModule == True:
            muteAudio=True
        if muteAudio == True:
            print("\n== Audio is muted ==")
        print(" ")
        print("Welcome to...")
        if debug!=0:
            print("gamebeat=",gameBeat)
        time.sleep(1.25)
        print(" ")
        try:print("""█████▄ ▓█████ ▄▄▄     ▄▄▄█████▓ ██░ ██ ▄▄▄█████▓ ██▀███   ▄▄▄       ██▓███      
▒██▀ ██▌▓█   ▀▒████▄   ▓  ██▒ ▓▒▓██░ ██▒▓  ██▒ ▓▒▓██ ▒ ██▒▒████▄    ▓██░  ██▒    
░██   █▌▒███  ▒██  ▀█▄ ▒ ▓██░ ▒░▒██▀▀██░▒ ▓██░ ▒░▓██ ░▄█ ▒▒██  ▀█▄  ▓██░ ██▓▒    
░▓█▄   ▌▒▓█  ▄░██▄▄▄▄██░ ▓██▓ ░ ░▓█ ░██ ░ ▓██▓ ░ ▒██▀▀█▄  ░██▄▄▄▄██ ▒██▄█▓▒ ▒    
░▒████▓ ░▒████▒▓█   ▓██▒ ▒██▒ ░ ░▓█▒░██▓  ▒██▒ ░ ░██▓ ▒██▒ ▓█   ▓██▒▒██▒ ░  ░    
 ▒▒▓  ▒ ░░ ▒░ ░▒▒   ▓▒█░ ▒ ░░    ▒ ░░▒░▒  ▒ ░░   ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░▒▓▒░ ░  ░    
 ░ ▒  ▒  ░ ░  ░ ▒   ▒▒ ░   ░     ▒ ░▒░ ░    ░      ░▒ ░ ▒░  ▒   ▒▒ ░░▒ ░         
 ░ ░  ░    ░    ░   ▒    ░       ░  ░░ ░  ░        ░░   ░   ░   ▒   ░░           
   ░       ░  ░     ░  ░         ░  ░  ░            ░           ░  ░             
 ░                                                                               
                  ▓█████▄  █    ██  ███▄    █   ▄████ ▓█████  ▒█████   ███▄    █ 
                  ▒██▀ ██▌ ██  ▓██▒ ██ ▀█   █  ██▒ ▀█▒▓█   ▀ ▒██▒  ██▒ ██ ▀█   █ 
                  ░██   █▌▓██  ▒██░▓██  ▀█ ██▒▒██░▄▄▄░▒███   ▒██░  ██▒▓██  ▀█ ██▒
                  ░▓█▄   ▌▓▓█  ░██░▓██▒  ▐▌██▒░▓█  ██▓▒▓█  ▄ ▒██   ██░▓██▒  ▐▌██▒
                  ░▒████▓ ▒▒█████▓ ▒██░   ▓██░░▒▓███▀▒░▒████▒░ ████▓▒░▒██░   ▓██░
                   ▒▒▓  ▒ ░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒  ░▒   ▒ ░░ ▒░ ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒ 
                   ░ ▒  ▒ ░░▒░ ░ ░ ░ ░░   ░ ▒░  ░   ░  ░ ░  ░  ░ ▒ ▒░ ░ ░░   ░ ▒░
                   ░ ░  ░  ░░░ ░ ░    ░   ░ ░ ░ ░   ░    ░   ░ ░ ░ ▒     ░   ░ ░ 
                     ░       ░              ░       ░    ░  ░    ░ ░           ░""")
        except Exception:
            print(r"""    ____             __  __  ______                             
   / __ \___  ____ _/ /_/ /_/_  __/________ _____               
  / / / / _ \/ __ `/ __/ __ \/ / / ___/ __ `/ __ \              
 / /_/ /  __/ /_/ / /_/ / / / / / /  / /_/ / /_/ /              
/_____/\___/\__,_/\__/_/ /_/_/ /_/   \__,_/ .___/               
                        / __ \__  ______ /_/__ ____  ____  ____ 
                       / / / / / / / __ \/ __ `/ _ \/ __ \/ __ \
                      / /_/ / /_/ / / / / /_/ /  __/ /_/ / / / /
                     /_____/\__,_/_/ /_/\__, /\___/\____/_/ /_/ 
                                       /____/                   \n""")
        if muteAudio != True:
            try:
                pygame.mixer.music.load('sfx/dtd_main.wav')
            except Exception:
                pass
            try: pygame.mixer.music.play(1)
            except Exception:
                pass
        if debug == 0:
            damage=5
            time.sleep(3)
            story()
        else:
            if noModuleSound == False:
                pygame.mixer.music.stop()
            print("\n= Intro sequence skipped via debug mode =\n")
            nameInputAsk()
    elif newgame == 2 and compatibility != True:
        load()
    elif newgame == 6:
        quitChoice = str(input("Are you sure you want to quit? The game will close. (Y/N) \n--> "))
        quitChoice.lower()
        if quitChoice == "y":
            sys.exit(0)
        elif quitChoice=="warp":
            print("\n== WARP ==")
            debugWarp()
        elif quitChoice=="sndtest":
            print("\n== SOUND TEST ==")
            soundtest()
        elif quitChoice=="cmd" or quitChoice=="command":
            print("\n== COMMAND LINE ==\n© Reuben Parfrey 2021")
            cmd()
        else:
            print(" ")
            print("Returning to main menu...")
            print(" ")
            time.sleep(0.25)
            menu()
    elif newgame == 5:
        print(r"""

        DEATHTRAP DUNGEON by REUBEN PARFREY   2019
        V2.9.5

        All code and story events by Reuben Parfrey. Props to Charly Sly and Joe Parfrey for helping me 
        find and fix some major bugs. And, of course, thanks to you; the player. Enjoy the game!                         ____  
                                                                                                                        |    \ 
        All music and sound effects by Charly Sly. Thanks a tonne for doing all the musical stuff! ©2020                |  |  | 
                                                                                                                        |____/ 
        Dedicated to Mr. Chapple; the best damn teacher in the college and the man that convinced me to                         _____
        study computer science in the first place. One of the most genuine and down to earth people I've                       |_   _|
        ever met. Words can't even begin to describe how much you influenced me and I miss you more and more                     | | 
        every day. This game wouldn't even exist without you; rest easy.                                                         |_|
                                                                                                                                       ____
        Stay in the loop! Follow my social media for further updates to this game, or any upcoming projects:                          |    \
        @_reuben._.parfrey_ on Instagram                                                                                              |  |  |
        u/mlaude545 on Reddit                                                                                                         |____/
        @R3d_da on Twitter                                                                                                            
                                                                                                                                      
        Or follow @deathtrap_dungeon_official on Instagram; the official DTD Instagram page and your one-stop                         
        shop for all things DTD-related!                                                                                             
                                                                                                                                      
        Found a bug? Please be sure to report it using the 'Report a bug' feature in the 'Options' menu.
        
        """)
        if debug!=0:
            print("        == DEBUG INFORMATION: ==")
            latestVer=currentVer.decode('utf-8')
            print("        currentVer = "+latestVer)
            if noPyGameModule != True:
                pygameVer=pygame.version.ver
                print("        PyGame Version = "+pygameVer)
            else:
                print("        = Pygame info is unavailable =")
            currentOS=platform.platform()
            print("        currentOS: "+currentOS)
        menu()
    elif newgame==1739 and debug == 0:
        print("\n=Debug mode has been enabled=\n")
        debug=1
        menu()
    elif newgame==1739 and debug > 0:
        print("\n=Debug mode has been disabled=\n")
        debug=0
        print
        menu()
    elif newgame == 4:
        options()
    elif newgame == 3:
        profile()

    elif debug > 0:
        print(debug)

    else:
        print(" ")
        print("Bad input. Enter one of the options specified!")
        print(" ")
        menu()


if debug == 0:
    menu()
    time.sleep(3.5)
else:
    print(" ")
    print("= Debug mode is enabled =")
    time.sleep(0.2)




