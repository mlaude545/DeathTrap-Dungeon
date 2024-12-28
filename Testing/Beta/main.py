#!/usr/bin/python3


# DEATHTRAP DUNGEON by Reuben Parfrey 2019 - 2024

# This game is open source software and is released under the MIT Licence. As such, you can freely modify and
# redistribute the source code. This software comes with NO WARRANTY. A full copy of the MIT Licence can be
# found in the 'copying' file provided with this game.

# Thanks to everybody who helped me during the development of this game; I genuinely never thought it would
# receive the support that is has, and I am eternally grateful. If you have any suggestions for improvements to
# this game, or want to report a bug, please use the 'Report a Bug' option in-game in the Settings menu.


# Import the needed libraries
import random, pickle, os, webbrowser, platform, sys, time, socket
import shutil
from urllib.request import urlretrieve
from pathlib import Path
from datetime import datetime

# Initialise global variables
current_version = "3.0.0"  # Version of this release of DTD, used when checking for updates.
internal_identifier = "DTD v3.0.0 BETA Build 171124"   # A more human-readable version identifier, which is shown to the user.
checked_for_update = False  # This changes to True after the game has completed an auto update check.
is_beta = True   # Set this to True if this is a beta copy of DTD, otherwise it should be False.
refreshed_latest_release_ver = False    # This is used when the user initiates an update check. It ensures that the game refreshes to have the latest version number available from the online repo.
active_theme = "flow"   # The active menu theme. Defaults to Flow.

enemies_defeated = [0]   # This array contains the enemy_ID values associated with defeated enemies - allows the game to keep a log of which enemies have been defeated during gameplay, so you can't keep fighting them infinitely.
single_use_items = []   # Similar idea as above, although this array contains single use items found throughout the game.

# More various global variables. Please note that many of these have been depreciated or aren't used anymore, so the aim is to
# phase many of these out gradually across future releases.
debug = 0
enemy_ID = 0
gotShield = 0
mute_audio = False
gotKey = False
sound_module_error = False
died = False
smokescreen = False
healingPotion = False
searchedChest2 = False
originalGuardHealth = 0
usedHyperPotion = 0
originalDamage = 0
originalHealth = 0
auto_updates_disabled = False
firstSaveRequest = True
save_location_cache = 0
searchedChest5 = False
searchedChest = False
leverPulled = False
leftDialCorrect = False
rightDialCorrect = False
dialogCount = 0
puzzleComplete = False
lockout = False
leftDialPos = str("down, towards you.")
rightDialPos = str("upwards, towards the door.")
discoveredChapterSevenDoor = False
defeatedChapterSevenGuard = False
pickedUpKey = False
searchedChest7 = False
searchedChest7mk2 = False
searchedChest8 = False
juniperDamage = 0
juniperHealth = 0
engagedJuniperFight = False
have_credits_rolled = False
gameBeat = False
sound_directory_error = False
checkForUpdatesThroughOptions = False
loadMenu = False
basic_graphics_enabled = False
dependenciesChecked = False
auto_applied_basic_graphics = False
classic_theme_enabled = False
skip_overwrite_confirmation = False
disableOverwrite = False
disable_critical = False
player_only_critical = False
enemy_only_critical = False
juniperCanHeal = False
juniperPhase = 0
diedToJuniper = False
expert_mode_enabled = False
selectedSlot = 0
originalHealingPotion = False
originalHealingPotionQuantity = 0
originalSmokescreen = False
originalHyperPotion = False
originalSmokescreenQuantity = 0
originalHyperPotionQuantity = 0
beatExpertMode = False
searchedSink = False
searchedBed = False
searchedCupboard = False
checkedHyperPotion = False
postGameSave = 0
no_pygame = False

# Hide the 'Welcome to Pygame' message on startup
if not no_pygame:
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Identify the host operating system
if platform.system() == "Windows":
    try:
        os.system('mode con: cols=155 lines=50')    # Resize the game window on Windows-based computers
    except Exception:
        pass

# Load graphics settings, and then apply them.
# The current implementation for loading config files is pretty messy - I want to implement a function that
# opens all the configs in one go, but this works and will do for now.
try:
    with open('config/graphics_configuration.dat', 'rb') as f:
        active_theme, basic_graphics_enabled = pickle.load(f)
except Exception:
    active_theme = 'flow'   # Use the default theme if the graphics config file can't be loaded.

if active_theme == 'classic' and not basic_graphics_enabled:    # Show a message if a different theme is active.
    print("\n== Classic Theme is enabled ==")
    active_theme = "classic"
elif active_theme == 'basic' and not basic_graphics_enabled:
    print("\n== Basic Theme is enabled ==")

if basic_graphics_enabled:  # Show a message if basic graphics mode is enabled.
    print("\n== Basic Graphics mode is enabled - graphics will not be drawn in full quality ==\n")
    active_theme = "basic"    # Enable Basic theme as a fallback to ensure menus cannot be loaded with the Flow style under any circumstances.

# Check if the host supports Unicode graphics. If not, enable Basic Graphics mode to avoid crashes.
try:
    sys.stdout.write("█")   # Write out a Unicode character.
    sys.stdout.write("\b")  # Move back one space.
    sys.stdout.write(" ")   # Delete the character.
except Exception:   # If an error occurs when trying to print a Unicode character, show a warning and enable Basic Graphics mode.
    basic_graphics_enabled = True
    active_theme = "basic"
    auto_applied_basic_graphics = True  # This variable tells the game that Basic Graphics was applied automatically, and means that the user can't disable it.
    print("\n== INFORMATION ==\nYour system does not appear to support unicode characters, so Basic Graphics mode has\nbeen enabled. This means that menus and in-game graphics will be rendered in a \nless detailed way. For more info, go to Settings > Graphics > Basic Graphics Mode.\n")

if basic_graphics_enabled == [True]:
    basic_graphics_enabled = True
if basic_graphics_enabled == [False]:
    basic_graphics_enabled = False


def generate_unformatted_title(title, mode):    # This function generates a header title bar used in the Flow and Basic graphics styles.
    if mode == 'flow':
        return '\n█ ' + str(title) + ': ░▒▒███████████████████████████████████████'  # Create a header more than 34 characters long.
    elif mode == 'basic':
        return '\n= ' + str(title) + ': =========================================='  # Same, but for Basic Theme.


def generate_header(title):  # This function is used throughout the game to render headings for menus in the correct style.
    global active_theme
    if active_theme == 'flow' or active_theme == 'basic':
        unformatted_title = generate_unformatted_title(title, active_theme)
        unformatted_length = len(unformatted_title)     # Get the length of the returned header
        difference = unformatted_length - 35    # Menus in the Flow style are 34 characters wide, so work out the difference between the length of the generated header and where we want it to be.
        header = unformatted_title[:-difference]    # Removes the excess end characters
    else:
        header = '\n== '+str(title)+' =='   # Generate headers that mimic older releases of DTD for the Classic Theme style. These are much simpler to generate than headers for the other two themes.
    return header   # Return the generated header.


def generate_seperator():       # A basic function that generates separators used in UIs.
    global active_theme
    menu_bar = r'██████████████████████████████████'    # Separator in the Flow style.
    if active_theme == 'basic':
        menu_bar = r'=================================='    # Separator in the Basic style.
    elif active_theme == 'classic':
        menu_bar = None     # Classic theme doesn't use separators, so set the value to None.
    return menu_bar


# Try to import the Pygame library; this handles audio.
try:
    import pygame
    pygame.mixer.init()
except Exception:   # If Pygame can't be imported, show a warning and mute audio to avoid crashes.
    no_pygame = True    # Raise the no_pygame flag, so the game knows not to let the player unmute audio.
    mute_audio = True   # Set mute_audio to True to (you guessed it) mute the game's audio.
    print(generate_header("MISSING DEPENDENCY"))
    print("The 'Pygame' module is not installed, so the game will run without sound.\nFor more help, visit: "
          "https://reubenparfrey.wixsite.com/deathtrapdungeon/help/")

# Try to import the necessary libraries for checking for updates.
try:
    import ssl
    import urllib.request
except Exception:
    auto_updates_disabled = True

# Open the file containing gameplay settings, and apply them.
try:
    with open('config/gameplay_settings.dat', 'rb') as f:
        disable_critical, player_only_critical, enemy_only_critical, disableOverwrite, skip_overwrite_confirmation = pickle.load(
            f)
except Exception:
    pass
if disable_critical == [True]:
    disable_critical = True
if player_only_critical == [True]:
    player_only_critical = True
if enemy_only_critical == [True]:
    enemy_only_critical = True
if disableOverwrite == [True]:
    disableOverwrite = True
if skip_overwrite_confirmation == [True]:
    skip_overwrite_confirmation = True


class Enemy:
    def __init__(self, guard_type, guard_damage, guard_maxhealth, guard_health, held_item):
        self.guard_type = guard_type            # Denotes the type of guard, for example regular or High Ranking.
        self.guard_damage = guard_damage        # The damage that the guard will inflict.
        self.guard_maxhealth = guard_maxhealth  # The guard's maximum health.
        self.guard_health = guard_health        # The guard's current health.
        self.held_item = held_item              # The item that the guard is holding.

    def get_stats(self):
        info = str("\nATTACK: "+str(self.guard_damage)+"\nDEFENCE: "+str(self.guard_health)+"/"+str(self.guard_maxhealth)+"\nHOLDING: "+str(self.held_item))
        return info

    def attack_player(self, player_health):
        player_health -= self.guard_damage
        return self.guard_damage

    def land_critical_hit(self):
        self.guard_damage += 2  # Temporarily raise attack damage by 2
        critical_value = self.guard_damage
        self.guard_damage -= 2  # Reset attack damage to normal value.
        return critical_value

    def get_health(self):
        return self.guard_health    # Returns remaining health.

    def get_attack(self):
        return self.guard_damage    # Returns attack damage.

    def sustain_damage(self, damage_dealt):
        self.guard_health -= damage_dealt
        return

    def get_held_item(self):
        return self.held_item   # Returns the enemy's held item.


class Juniper:
    def __init__(self, attack_damage, max_health, health, phase):
        self.attack_damage = attack_damage  # The amount of damage that Juniper will inflict.
        self.max_health = max_health        # Maximum health.
        self.health = health                # Current health.
        self.phase = phase                  # Denotes which phase of the fight is underway - there are three in total.

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health

    def get_stats(self):
        info = str("\nATTACK: "+str(self.attack_damage)+"\nDEFENCE: "+str(self.health)+"/"+str(self.get_max_health())+"\nHOLDING: Samurai Sword")
        return info

    def set_health(self, health):
        self.health = health
        return

    def set_attack(self, attack):
        self.attack_damage = attack
        return

    def get_attack(self):
        return self.attack_damage

    def get_phase(self):
        return self.phase

    def increment_phase(self):
        self.phase += 1
        return

    def reset_phase(self):
        self.phase = 0

    def restore_stats(self):
        self.health = self.max_health

    def sustain_damage(self, damage_dealt):
        self.health -= damage_dealt
        if self.health < 0:
            self.health = 0
        return
    def attack_player(self, player_health):
        player_health -= self.attack_damage
        return self.attack_damage

    def land_critical_hit(self):
        self.attack_damage += 2
        critical_value = self.attack_damage
        self.attack_damage -= 2
        return critical_value


class Player:
    def __init__(self, attack_damage, health, max_health, entered_name, inventory, defensive_items, has_beaten_game, has_completed_expert_mode, save_location):
        self.attack = attack_damage     # The damage dealt to enemies.
        self.health = health            # The player's health value.
        self.max_health = max_health    # The maximum amount of health that can be restored.
        self.name = entered_name        # Player name.
        self.inventory = inventory      # A list containing items that can be used in battle, along with their respective quantities.
        self.has_beaten_game = has_beaten_game  # Boolean - set to True if the main story has been completed.
        self.has_completed_expert_mode = has_completed_expert_mode  # Boolean - set to True if Expert Mode is complete.
        self.save_location = save_location  # Integer - corresponds to the location in the game. Mainly used when saving progress and when restarting from checkpoints.
        self.defensive_items = defensive_items  # An array made up of defensive items (IE - weapons.)
        self.hyper_potion_use_count = 0 # Keep track of how many turns the player has had the Hyper Potion active for.
        self.original_attack = 0        # Keep a backup of the player's original attack damage stat when using Hyper Potion.
        self.original_defence = 0       # Same as above, but for the defence stat.

    def get_name(self):
        return self.name

    def set_name(self, entered_name):
        self.name = entered_name
        return self.name

    def default_stats(self):
        self.attack = 5
        self.health = 20
        self.max_health = 20
        return

    def restore_health(self):
        self.health = self.max_health
        return "Health has been fully restored!"

    def sustain_damage(self, damage_dealt):
        self.health -= damage_dealt
        return

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health

    def get_attack(self):
        return self.attack

    def get_stats(self):
        return self.name, self.health, self.max_health, self.attack

    def attack_guard(self, guard_health):
        guard_health -= self.attack
        return self.attack

    def land_critical_hit(self, guard_health):
        self.attack += 2
        critical_value = self.attack
        guard_health -= self.attack
        self.attack -= 2
        return critical_value

    def get_inventory_items(self):
        return self.inventory

    def has_item(self, item_name):  # Checks if the player is holding an item, and returns the quantity of that item.
        quantity = self.inventory.get(item_name, 0)
        return quantity

    def get_hyper_use_count(self):
        return self.hyper_potion_use_count

    def set_hyper_use_count(self, value):
        self.hyper_potion_use_count = value
        return self.hyper_potion_use_count

    def reduce_hyper_potion_use(self):
        self.hyper_potion_use_count -= 1
        return

    def use_hyper_potion(self, original_defence, original_attack):
        self.original_defence = original_defence    # The player's defence and attack levels are stored in these two
        self.original_attack = original_attack      # variables, so they can be restored later.
        self.inventory['Hyper Potion'] -= 1     # Reduce inventory item quantity.
        self.attack = 25
        self.health = 25
        self.max_health = 25
        self.hyper_potion_use_count = 3
        return

    def hyper_potion_end(self):
        self.attack = self.original_attack
        self.max_health = self.original_defence
        self.health = self.max_health
        return

    def gain_defence(self, defence_value):  # This is used to increase the player's max health when they get an upgrade.
        self.max_health += defence_value
        return

    def gain_attack(self, attack_value):
        self.attack += attack_value
        return

    def use_healing_potion(self):
        self.health = self.max_health   # Restore health
        self.inventory['Healing Potion'] -= 1   # Reduce healing potion quantity by one.
        return self.health

    def use_smokescreen(self, enemy_ID):
        self.inventory['Smokescreen'] -= 1
        if enemy_ID == 1:
            second_choice_alternate()
        elif enemy_ID == 2:
            chapter_3_choose_direction()
        elif enemy_ID == 3:
            print("\nYou rush back to your previous hiding spot.")
            chapter_3_hiding_choice()
        elif enemy_ID == 4:
            print("\nYou scurry back to the closet you were previously in.")
            closet()
        elif enemy_ID == 5:
            print("\nYou rush back to your previous hiding spot.")
            chapter_3_hiding_choice()
        elif enemy_ID == 6:
            print("\nYou scurry back up the path you came down, towards the fountain.")
            courtyard()
        elif enemy_ID == 7:
            chapter_7_split()
        elif enemy_ID == 8:
            ChapterTwoGuardEscape()
        
    def get_save_location(self):
        return self.save_location

    def set_save_location(self, new_save_value):
        self.save_location = new_save_value
        return

    def is_game_beaten(self):
        return self.has_beaten_game

    def game_beaten(self):  # Set has_beaten_game to True if the main story is complete.
        self.has_beaten_game = True
        return

    def is_expert_mode_complete(self):  # Returns the status of Expert Mode completion.
        return self.has_completed_expert_mode

    def completed_expert_mode(self):    # Sets has_completed_expert_mode to True if Expert Mode has been beaten.
        self.has_completed_expert_mode = True
        return

    def grant_default_inventory(self):  # Reset the inventory back to it's default state.
        self.inventory = {'Healing Potion': 0, 'Hyper Potion': 0, 'Smokescreen': 0}
        return

    def update_inventory(self, item_name, quantity=1):  # Add an item to the player's inventory.
        item_name = item_name.title()   # Capitalise the item name - if this method receives the item name in lowercase, it doesn't get recognised as a valid item.
        if item_name in self.inventory:
            self.inventory[item_name] += quantity
        else:
            print(f"Invalid item: {item_name}")

    def get_defensive_items(self):  # Return the player's held defensive items.
        return self.defensive_items

    def update_defensive_items(self, item_name):
        if item_name not in self.defensive_items:   # Only add to the defensive items list if the player doesn't already have that item.
            self.defensive_items.append(str(item_name))
        if self.defensive_items[0] == '* No Defensive Items *' and len(self.defensive_items) > 1:
            self.defensive_items.pop(0)   # Remove the 'no defensive items' warning when the player gains an item (if the first element of the array is the warning and there is more than one element in the array.)
        return


try:    # Open the file that contains the user's update settings.
    with open('config/update_configuration.dat', 'rb') as f:
        auto_updates_disabled = pickle.load(f)
except Exception:
    auto_updates_disabled = False   # If the file can't be accessed, enable auto updates as a fallback.


class BattleLogic:  # This class contains the various logic functions used within battles.
    def __init__(self, enemy_type, music_track):
        self.enemy_type = enemy_type
        self.music_track = music_track

    def play_music(self):               # This method plays the appropriate
        global no_pygame, mute_audio     # track for the battle.
        if not no_pygame and not mute_audio:
            try:
                pygame.mixer.music.load(self.music_track)
                pygame.mixer.music.play(999)   # Loop the track.
            except pygame.error:
                pass
        return

    def stop_music(self):   # This method stops playback of a track, for example when the player dies.
        pygame.mixer.music.stop()
        return

    def critical_hit(self, expert_mode_enabled, type):
        max_boundary = 10   # Max boundary is the chance that a critical hit will be landed. So if its 10 for example, then there's a 1 in 10 chance of a critical hit.
        if type == 'enemy' and expert_mode_enabled:
            max_boundary = 7
        elif type == 'enemy' and not expert_mode_enabled:
            max_boundary = 25
        elif type == 'player' and expert_mode_enabled:
            max_boundary = 15
        elif type == 'player' and not expert_mode_enabled:
            max_boundary = 10
        crit = random.randint(0, int(max_boundary))
        if crit == 1:
            return True
        else:
            return False

    def has_hyper_potion_worn_off(self, hyper_potion_use_count):  # This method is used when the Hyper Potion is active
        hyper_potion_use_count -= 1                               # during battle. It returns True if the potion has
        if hyper_potion_use_count <= 0:                           # worn off, or False if not.
            return True
        else:
            return False

    def is_dead(self, health):  # This method is used in battles to check if the enemy or player is dead. If health
        if health <= 0:         # is below or equal to zero, it returns True, which is handled accordingly.
            return True
        else:
            return False

    def handle_player_death(self):  # Does what it says on the tin; handles the player's death.
        self.stop_music()
        game_over()


class Items:
    def __init__(self, item_name):
        self.item_name = item_name
        self.item_sprite = ""
        self.basic_sprite = ""
        self.item_description = ""
        self.attack_value = 0
        self.defense_value = 0
        if self.item_name == "Smokescreen":
            self.item_description = "\nA fairly uncommon item that can be used during battles. When deployed, the battlefield is shrouded in thick\nsmoke, granting a 100% chance of escaping form battle unharmed!\n"
            self.item_sprite = r"""                       .')             _
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
                      ` __.:'-'"""
            self.basic_sprite = self.item_sprite
        if self.item_name == "Wooden Spear":
            self.attack_value = 2
            self.item_description = "\nA basic wooden spear. It's nothing special, but it's a lot more effective than using the shard of glass.\n\n       Attack +2\n         Defence +0\n"
            self.item_sprite = r"""                                                                    ▓▓▓▓▓▓▓▓
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
"""
            self.basic_sprite = r"========[>"
        if self.item_name == "Wooden Shield":
            self.defense_value = 2
            self.item_description = "\nA basic wooden shield. Chips and cracks adorn the surface, but it should \nstill offer some protection in a pinch.\n\n       Attack +0\n         Defence +2\n"
            self.item_sprite = r"""                ██████                
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
"""
            self.basic_sprite = r"""      |`-._/\_.-`|
      |    ||    |
      |___o()o___|
      |__((<>))__|
      \   o\/o   /
       \   ||   /
        \  ||  /
         '.||.'
           ``"""
        if self.item_name == "Loaf of Bread":
            self.item_description = "\nYou pick up the load of bread! In desperate need of nourishment, you gulp it down."
            self.item_sprite = r"""                                                                                        
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
                                                               """
            self.basic_sprite = r"""    _______
   /       )
  /_____   | 
 (  '   ) /   
  |.  '| /      
  |____|/"""
        if self.item_name == "Rusty Sword":
            self.attack_value = 3
            self.item_description = "\nA well-used sword. It's a little rusty, but should still offer some decent attack power.\n\n       Attack +3\n         Defence +0\n"
            self.item_sprite = r"""                          ██████
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
"""
            self.basic_sprite = r""" _          /~~>________________________________________
            / \////////|   \..................................~~~~~---_
            \_/\\\\\\\\|   /__________________________________-----~~~
                         \__>     """
        if self.item_name == "Hyper Potion":
            self.item_description = "\nA rare item that can be used in battles. Temporarily boosts attack power and defence levels to 25, regardless of previous stats."
            self.item_sprite = r"""                                        
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
                                    ██████████████████  """
            self.basic_sprite = r"""      .  .          
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
   "Ya,______,rP'"""
        if self.item_name == "Rusty Chestplate":
            self.defense_value = 3
            self.item_description = "\nA well-worn chestplate. It's clearly seen many battles and has lost some \nprotection as a result, but it's still got some life left in it.\n\n       Attack +0\n         Defence +3\n"
            self.item_sprite = r"""
          .=='\   /`==.
        .'\ # (`:')  #/`.
      _/_ |_.-' : `-._|__\_
     <___>'\ ## :   / `<___>
            >=======<
           /  ,-:-. #\
          |__/v^v^v\__|"""
            self.basic_sprite = self.item_sprite
        if self.item_name == "Healing Potion":
            self.item_description = "\nAn item that can be used during battles. One sip of this, and health will be fully restored instantly!"
            self.item_sprite = r"""                                                                                                                                                              
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
                                        ██████████    """
            self.basic_sprite = r"""      _____
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
                 `.___.'"""
        if self.item_name == "key":
            self.item_description = "A rusty key! Maybe it can be used to open a nearby door..."
            self.item_sprite = r"""                                                                    ██████          
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
                                                                    ██████          """
            self.basic_sprite = r""""""

    def get_item_name(self):
        return self.item_name

    def get_item_sprite(self):
        return self.item_sprite

    def get_basic_sprite(self):
        return self.basic_sprite

    def get_item_description(self):
        return self.item_description

    def get_attack_increment(self):
        return self.attack_value

    def get_defense_increment(self):
        return self.defense_value


def reset_temp_variables():                     # Reset the two arrays used for temporary data storage through the game to avoid holding on
    global enemies_defeated, single_use_items   # to temporary data for longer than it is needed.
    enemies_defeated = []
    single_use_items = []


def invalid_selection_message():
    print("\nPlease select a valid option.")    # Show a message when the user selects an invalid menu option or choice.


def get_diagnostics():  # This function gathers diagnostic data. This data is shown to the user, and can be included in bug reports.
    global current_version, basic_graphics_enabled, auto_updates_disabled, internal_identifier, sound_module_error, sound_directory_error, active_theme
    friendly_active_theme = active_theme.title()
    if not sound_module_error and not no_pygame:
        pygame_ver = pygame.version.ver
    else:
        pygame_ver = "(Pygame version data not available - probably not installed.)"
    current_platform = sys.platform
    general_data = [internal_identifier, current_version]
    auto_updates_status = 'Enabled'
    if auto_updates_disabled:
        auto_updates_status = 'Disabled'
    diagnostic_data = [current_platform, pygame_ver, basic_graphics_enabled, friendly_active_theme, auto_updates_status]
    return f"GENERAL:\nDTD Version: {general_data[0]}\nInternal Identifier: {general_data[1]}\n\nDIAGNOSTIC:\nPlatform: {diagnostic_data[0]}\nPygame Version: {diagnostic_data[1]}\nBasic Graphics: {diagnostic_data[2]}\nActive Theme: {diagnostic_data[3]}\nAuto Updates: {diagnostic_data[4]}"


def handle_error(description, e):  # This function displays error messages, taking basic and advanced error info as parameters to display to the user.
    print(generate_header("SORRY"))
    print("An error has occurred. You can see details of the error below:\n\nDETAILS: "+str(description)+"\nTECHNICAL: "+str(e))
    print("\nNeed some help? Choose an option below. If this issue seems to be a bug, please report it.")
    try:
        choice = int(input("1] Get Help Online\n2] Report a Bug\n3] Cancel\n--> "))
        if choice == 1:
            webbrowser.open('https://reubenparfrey.wixsite.com/deathtrapdungeon/help/')
        elif choice == 2:
            launch_bug_report(get_diagnostics(), description, e)
        elif choice == 3:
            pass    # We can just do nothing for the cancel option, as the function that originally called this function links to something after it as a fallback.
        else:
            print("That's an invalid choice, try again.")
            handle_error(description, e)
    except ValueError:
        handle_error(description, e)


def generate_defensive_item_list(player_max_health, damage):
    defensive_items = ['* No defensive items *']         # This function is used when converting save files from
    if player_max_health == 20 and damage == 5:        # older formats. In this version of the game, the player's
        defensive_items = ['shard of glass']           # defensive items (dropped by enemies) are simply saved as an
    elif player_max_health == 20 and damage == 7:      # array. However, older versions of the game didn't do this. This
        defensive_items = ['wooden spear']             # of course leads to a compatibility issue - the player would
    elif player_max_health == 22 and damage == 5:      # obviously want to keep their items when they convert a save
        defensive_items = ['wooden shield', 'shard of glass']   # file, but this version of the game saves it in a
    elif player_max_health == 22 and damage == 7:      # different way.
        defensive_items = ['wooden shield', 'wooden spear']
    elif player_max_health == 20 and damage == 8:       # That's where this function comes in - it takes the player's
        defensive_items = ['rusty sword']               # max health and attack values as parameters, and uses this info
    elif player_max_health == 22 and damage == 8:       # to identify the correct item / items that the player must
        defensive_items = ['wooden shield', 'rusty sword']  # be holding based off of their stats. It then formats this
    elif player_max_health == 23 and damage == 5:       # data into an array, which can be processed by the conversion
        defensive_items = ['rusty chestplate', 'shard of glass']    # algorithm and then saved in the new format.
    elif player_max_health == 23 and damage == 7:
        defensive_items = ['rusty chestplate', 'wooden spear']  # This solution is very hacky, and this is actually
    elif player_max_health == 23 and damage == 8:               # how this idea was implemented in previous versions
        defensive_items = ['rusty chestplate', 'rusty sword']   # of DTD. My aim is to leave it be for now (whilst the
    elif player_max_health == 25 and damage == 5:               # player base upgrades from older versions to this version
        defensive_items = ['rusty chestplate', 'wooden shield', 'shard of glass']   # of the game), then depreciate it
    elif player_max_health == 25 and damage == 7:               # when the time is right.
        defensive_items = ['rusty chestplate', 'wooden shield', 'wooden spear']
    elif player_max_health == 25 and damage == 8:
        defensive_items = ['rusty chestplate', 'wooden shield', 'rusty sword']
    elif player_max_health == 20 and damage == 10:
        defensive_items = ['wooden spear', 'rusty sword']
    elif player_max_health == 22 and damage == 10:
        defensive_items = ['wooden shield', 'wooden spear', 'rusty sword']
    elif player_max_health == 23 and damage == 10:
        defensive_items = ['rusty chestplate', 'wooden spear', 'rusty sword']
    elif player_max_health == 25 and damage == 10:
        defensive_items = ['rusty chestplate', 'wooden shield', 'wooden spear', 'rusty sword']
    return defensive_items


def data_format_daemon():    # In previous versions of DTD, data and config files were stored in the current working directory, which was
    current_dir = os.getcwd()   # extremely messy. This function copies these files (if they exist) into directories.
    known_config_files = ['update_configuration.dat', 'graphics_configuration.dat', 'gameplay_settings.dat', 'audio_settings.dat']
    known_data_files = ['savedata.dat', 'savedata2.dat', 'savedata3.dat']
    if not os.path.exists(current_dir+'/config'):
        os.mkdir(current_dir+'/config')
    if not os.path.exists(current_dir+'/data'):
        os.mkdir(current_dir+'/data')
    for file in known_data_files:
        if os.path.exists(current_dir+'/'+file):
            shutil.move(current_dir+'/'+file, current_dir+'/data/'+file)
    for file in known_config_files:
        if os.path.exists(current_dir+'/'+file):
            shutil.move(current_dir+'/'+file, current_dir+'/config/'+file)


def download_latest_source(download_path, url):
    print("Working...")
    try:
        download = urlretrieve(url, download_path)
    except Exception as e:
        description = 'General download error; try checking your internet connection.'
        handle_error(description, e)
        menu()
    print("\nThe latest version of DeathTrap Dungeon was downloaded and saved to: " + str(download_path))
    menu()


def choose_custom_directory(download_path, url):
    custom_path = input("\nType the path of the directory you'd like to use instead, or type 'cancel' to go back: ")
    if custom_path == 'cancel' or custom_path == 'Cancel':
        confirm_source_code(download_path, url)
    else:
        if not os.path.isdir(custom_path):
            print("\nThe specified directory could not be found. Check spelling and ensure the path is correct, then try again.")
            choose_custom_directory(download_path, url)
        else:
            download_path = custom_path + "/DTD.py"
            download_latest_source(download_path, url)


def confirm_source_code(download_path, url):
    try:
        choice = int(input("\nThe latest version of DeathTrap Dungeon is going to be downloaded to: " + str(
            download_path) + ".\n1] Continue\n2] Choose a different directory\n--> "))
        if choice == 1:
            download_latest_source(download_path, url)
        elif choice == 2:
            choose_custom_directory(download_path, url)
        else:
            print("\nPlease choose a valid option.")
            confirm_source_code(download_path, url)
    except ValueError:
        print("\nPlease choose a valid option.")
        confirm_source_code(download_path, url)


def view_release_notes(download_path, method_of_access, contents):
    try:
        with open(download_path, 'r') as f:
            lines = f.readlines()
        for line in lines:
            print(line)
            time.sleep(0.1)
    except Exception as e:
        description = "Encountered an issue whilst downloading or accessing the data. Try again, and if the issue persists, paste this link into a browser to\nview what's new manually: https://raw.githubusercontent.com/mlaude545/DeathTrap-Dungeon/refs/heads/main/OTA%20Resources/changelog.txt."
        handle_error(description, e)
        if method_of_access == 'auto':
            menu()
        else:
            software_update_settings()
    time.sleep(2)
    ask_download_update(method_of_access, contents)


def download_release_notes(method_of_access, contents):
    url = 'https://raw.githubusercontent.com/mlaude545/DeathTrap-Dungeon/refs/heads/main/OTA%20Resources/changelog.txt'
    download_path = os.getcwd()+'/temp/release_notes.txt'
    print("Working...\n")
    try:
        urlretrieve(url, download_path)
    except Exception as e:
        description = 'General download error; try checking your internet connection.'
        handle_error(description, e)
        if method_of_access == 'auto':
            menu()
        else:
            software_update_settings()
    view_release_notes(download_path, method_of_access, contents)


def ask_download_update(method_of_access, contents):
    global auto_updates_disabled
    new_version_number = str(contents)
    new_version_number = new_version_number.replace("b", "")
    new_version_number = new_version_number.replace("'", "")
    if method_of_access == 'manual' and generate_seperator():                    # Alter the wording of the options presented to the user slightly, depending
        options = str(f"1] Download update\n2] What's new in the latest version?\n{generate_seperator()}\n3] Skip")  # on how the update check was initiated.
    elif method_of_access == 'manual' and not generate_seperator():
        options = str("1] Download update\n2] What's new in the latest version?\n3] Skip")
    elif method_of_access == 'auto' and generate_seperator():
        options = str(f"1] Download update\n2] What's new in the latest version?\n3] Skip\n{generate_seperator()}\n4] Don't ask again")
    else:
        options = str(f"1] Download update\n2] What's new in the latest version?\n3] Skip\n4] Don't ask again")
    print(f"{generate_header('UPDATE AVAILABLE')}\nA new version of DeathTrap Dungeon (v{new_version_number}) is available! You are currently on v{current_version}.\n{options}")
    try:
        choice = int(input("--> "))
        if choice == 1:
            user_platform = platform.system()
            if user_platform == "Windows":
                os.startfile("updater.exe")
                sys.exit(0)
            else:
                download_path = str(Path.home() / "Downloads/DTD.py")
                url = 'https://raw.githubusercontent.com/mlaude545/DeathTrap-Dungeon/main/Latest/DTD.py'
                confirm_source_code(download_path, url)
        elif choice == 2:
            download_release_notes(method_of_access, contents)
        elif choice == 3 and method_of_access == 'auto':
            menu()
        elif choice == 3 and method_of_access == 'manual':
            software_update_settings()
        elif choice == 4 and method_of_access == 'auto':
            print("\nAutomatic updates have been disabled, so you will no longer see this message. You can always check for updates \nmanually, or re-enable automatic updates, by going to Settings > Software Updates.")
            auto_updates_disabled = True
            save_settings('update_configuration', [auto_updates_disabled])
            menu()
        else:
            invalid_selection_message()
            ask_download_update(method_of_access, contents)
    except ValueError:
        ask_download_update(method_of_access, contents)


# This function pulls the latest version number of DTD from GitHub, and stores it to a file. The game then uses this
# version number when checking for updates: if latest_ver_available > this_game's_ver then a new version is out.
def get_latest_release_ver(filename):
    url = 'https://raw.githubusercontent.com/mlaude545/DeathTrap-Dungeon/main/OTA%20Resources/latest_stable_ver.txt'
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    contents = response.read()  # Store the HTML contents of the site to a variable.
    contents = contents.decode('utf-8')
    with open(filename, 'w') as file:
        file.write(contents)
        file.close()


def check_latest_ver_cached(filename):
    modified_date = os.path.getmtime(filename)  # Get the date and time of when the file was last modified.
    modified_date = datetime.fromtimestamp(
        modified_date)  # Convert it into a human-readable date and time from the timestamp.
    modified_date = datetime.date(
        modified_date)  # Extract just the date from the timestamp, seeing as the time is largely irrelevant.
    current_date = datetime.now()  # Get the current date
    current_date = datetime.date(current_date)  # Again, strip the time from the date, as this is irrelevant.
    delta = current_date - modified_date
    days_elapsed = delta.days  # Get the number of days elapsed from today's date, to when the last stable version check was performed.
    return days_elapsed


def check_for_updates(method_of_access):
    global current_version, refreshed_latest_release_ver
    current_dir = os.getcwd()   # Get the current working directory
    path_to_data = current_dir + '/temp'    # Directory that contains the latest stable version of DTD.
    filename = path_to_data + '/latest_stable_ver.txt'
    if not os.path.exists(path_to_data):    # Check if the 'temp' directory exists - this will contain a file that holds a plaintext version number of the latest stable release of DTD.
        os.mkdir(path_to_data)  # Make that directory if it does not exist.
    if not os.path.isfile(filename) and not refreshed_latest_release_ver:    # Check if a file exists in the temp directory that contains the latest stable version of DTD.
        get_latest_release_ver(filename)  # Get the latest stable version from GitHub if the file doesn't exist.
        refreshed_latest_release_ver = True
        if check_network_connection():  # Check if there is an active internet connection.
            check_for_updates(method_of_access)
    days_elapsed = check_latest_ver_cached(filename)
    if days_elapsed > 3 or method_of_access == "manual" and not refreshed_latest_release_ver:
        get_latest_release_ver(filename)  # Connect to the internet and get the latest stable version of DTD and save it to a file. This happens every few days automatically, or whenever the user manually initiates an update check.
        refreshed_latest_release_ver = True     # Set the refreshed_latest_release_ver flag, to ensure the game doesn't get stuck in an endless loop of refreshing.
        check_for_updates(method_of_access)
    try:
        with open(filename) as f:
            latest_stable_version = f.read()
            latest_stable_version = latest_stable_version.strip()  # Remove newline from end of file
    except Exception as e:
        if method_of_access == 'manual':
            handle_error('Error opening cached content. Try manually checking for new releases at: https://reubenparfrey.wixsite.com/deathtrapdungeon/downloads/', e)
            software_update_settings()
    if latest_stable_version > current_version:
        ask_download_update(method_of_access, latest_stable_version)
    else:
        if method_of_access == 'manual':
            print(f"\nYou're up to date! There are no new versions of DeathTrap Dungeon available at this time.")
            software_update_settings()


def check_network_connection():  # Checks for an internet connection. If none exists, the update check is skipped.
    global auto_updates_disabled
    try:
        socket.setdefaulttimeout(5)
        host = socket.gethostbyname("www.google.com")
        s = socket.create_connection((host, 80), 2)
        s.close()
        return True
    except Exception:
        return False


if auto_updates_disabled == [False]:
    auto_updates_disabled = False

if not os.path.isdir('sfx') and not no_pygame:      # This runs on startup and check to see if the 'sfx' folder that
    sound_directory_error = True                    # contains audio data is present. If it is not, a message is
    mute_audio = True                               # displayed to the user, and audio is muted in-game.
    print(generate_header("UNABLE TO ACCESS AUDIO DATA"))
    print("The directory containing the game's audio files could not be located. In order to keep the game running, audio has been muted.\n\nIf you are running the Source Code version, ensure the game files have been extracted correctly, and ensure that\nthe 'sfx' directory is in the same root directory as the game.\n\nFor more help on fixing this error, visit the help page at: https://reubenparfrey.wixsite.com/deathtrapdungeon/help/")

if sound_directory_error is False and no_pygame is False:
    try:
        with open('config/audio_settings.dat', 'rb') as f:
            mute_audio = pickle.load(f)
    except FileNotFoundError:
        pass
    except pickle.UnpicklingError or ValueError or EOFError:
        os.remove('config/audio_settings.dat')
    if mute_audio == [True]:
        mute_audio = True
    if mute_audio == [False]:
        mute_audio = False


def save_data_conversion_utility(save_file, extra_feature):  # Save Data Conversion Utility is a built-in tool that allows a user
    print("\nConverting save file...")                       # to convert save files created in older versions of DTD. It works by
    expert_mode_beaten = False                               # loading save data using older parameters, then using this data to
    try:                                                     # overwrite the save file in the current format.
        with open(save_file, 'rb') as f:
            player_name, save_location, damage, max_health, health, smokescreen, healingPotion, enemy_ID, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, game_beaten = pickle.load(
                f)
    except FileNotFoundError as e:
        description = "Save data is inaccessible."
        handle_error(description, e)
        load(extra_feature)
    except ValueError:
        try:
            with open(save_file, 'rb') as f:
                 player_name, save_location, damage, max_health, health, smokescreen, healingPotion, enemy_ID, smokescreenQuantity, healingpotionQuantity, hyperpotionQuantity, game_beaten, expert_mode_beaten = pickle.load(
                    f)
        except FileNotFoundError as e:
            description = "Save data is inaccessible."
            handle_error(description, e)
            load(extra_feature)
        except ValueError as e:
            description = "The save file is not supported in this version of Save Data Conversion Utility."
            handle_error(description, e)
            load(extra_feature)
    inventory = {'Healing Potion': int(healingpotionQuantity), 'Hyper Potion': int(hyperpotionQuantity), 'Smokescreen': int(smokescreenQuantity)}   # Populate the inventory as a list using loaded values.
    defensive_items = generate_defensive_item_list(int(max_health), int(damage))    # Generate an array of defensive items to save
    with open(save_file, 'wb') as f:    # Overwrite the incompatible save with a newly generated one.
        pickle.dump([player_name, save_location, damage, max_health, health, game_beaten, expert_mode_beaten, inventory, defensive_items], f,
                    protocol=2)
    print("Save data has been converted to work on this version of DTD! You can now load the save file.")   # Done! This process used to be a lot more 'in-your-face', but now it largely happens in the background with no user input.
    load(extra_feature)


def warp_to_chapter(save_location):     # This function uses the save_location variable to jump to the correct point
    if save_location == 1:              # in the game - this saves me having to repeat this code every time I need this
        choice4()                       # functionality.
    elif save_location == 2:
        chapter_3_start()
    elif save_location == 3:
        chapter_4_start()
    elif save_location == 4:
        chapter_5_start()
    elif save_location == 5:
        chapter_6_start()
    elif save_location == 6:
        chapter_7_start()
    elif save_location == 7:
        start_chapter_8()


def chapter_replay():
    global player, basic_graphics_enabled
    print(generate_header("CHAPTER REPLAY"))
    print("Select a chapter to play:\n1] Enter the Dungeon\n2] Solitary Confinement\n3] The Great Escape\n4] What Doesn't Kill You Makes You Stronger\n5] A Breath of Fresh Air\n6] A Puzzle in Darkness\n7] With Great Power\n8] Finale")
    if generate_seperator():
        print(generate_seperator())
    try:
        choice = int(input("9] Cancel\n--> "))
        if choice == 1:
            player.set_save_location(0)
            start_chapter_1()
        elif choice == 2:
            player.set_save_location(1)
            choice4()
        elif choice == 3:
            player.set_save_location(2)
            chapter_3_start()
        elif choice == 4:
            player.set_save_location(3)
            chapter_4_start()
        elif choice == 5:
            player.set_save_location(4)
            chapter_5_start()
        elif choice == 6:
            player.set_save_location(5)
            chapter_6_start()
        elif choice == 7:
            player.set_save_location(6)
            chapter_7_start()
        elif choice == 8:
            player.set_save_location(7)
            start_chapter_8()
        else:
            game_beat_options()
    except ValueError:
        chapter_replay()


def start_expert_mode():
    global expert_mode_enabled, originalDamage, originalHealth, damage, playerHealth, playerMaxHealth, smokescreen, smokescreenQuantity, originalSmokescreen, originalSmokescreenQuantity
    global hyperPotion, hyperpotionQuantity, originalHyperPotionQuantity, originalHyperPotion
    global healingPotion, healingpotionQuantity, originalHealingPotion, originalHealingPotionQuantity, savePoint, save_location_cache, player_expert_cache, player
    try:
        choice = int(input("\nAre you ready to begin? To learn more about Expert Mode, select 'More Info'.\n1] Yes\n2] No\n3] More Info\n--> "))
        if choice == 1:
            inventory = {'Healing Potion': 0, 'Hyper Potion': 0,
                         'Smokescreen': 0}  # Create an inventory with default values.
            defensive_items = ['* No Defensive Items *']
            expert_mode_enabled = True  # Sets the ExpertModeEnabled flag; this tells the game when expert mode is enabled, and appropriately disables features such as checkpoints.
            savePoint = save_location_cache  # The variable save_location_cache holds the value of the save location before starting Expert Mode, so it can be restored later. This is a little hacky, I keep meaning to redo this.
            player_expert_cache = player  # player_expert_cache creates a new Player object, and initialises it with the save file's original attributes, so they can  be restored.
            player = Player(5, 20, 20, str(player_expert_cache.get_name()), inventory, defensive_items, False, False,
                            0)  # Create a new player object to overwrite the cached original, with basic stats.
            print("Good luck!")  # Displays some motivation.
            time.sleep(0.6)
            start_chapter_1()
        elif choice == 2:
            extras_menu()
        elif choice == 3:
            print("""
        When you play on Expert Mode, here's what is different...
        - You start at the beginning of the game with basic stats and no held items (you get them back, don't worry!)
        - Enemies are more likely to land critical hits, and you are less likely to land them.
        - You can't flee from battles as easily.
        - You can't save your progress, and you can't use checkpoints.
        - Enemies are less likely to drop items upon being defeated.""")
            start_expert_mode()
        else:
            start_expert_mode()
    except ValueError:
        start_expert_mode()


def game_beat_options():
    global savePoint, gameBeat, no_pygame, sound_directory_error, player
    print(generate_header('CONGRATULATIONS'))
    try:
        choice = int(input("You have completed the story with this save file! Choose an option to continue:\n1] Chapter Replay\n2] Extras\n3] Cancel\n--> "))
        if choice == 1:
            chapter_replay()
        elif choice == 2:
            extras_menu()
        elif choice == 3:
            load(extra_feature=None)
        else:
            invalid_selection_message()
            game_beat_options()
    except ValueError:
        game_beat_options()


def save_file_incompatible(filename, extra_feature):   # Allow the player to convert save data.
    try:
        choice = int(input("\nThe save file you selected is incompatible with this version of DTD; it needs to be\nconverted before you can use it. Continue?\n1] Yes\n2] No\n--> "))
        if choice == 1:
            save_data_conversion_utility(filename, extra_feature)
        elif choice == 2:
            load(extra_feature)
        else:
            print("\nPlease select a valid option.")
            save_file_incompatible(filename, extra_feature)
    except ValueError:
        print("\nPlease select a valid option.")
        save_file_incompatible(filename, extra_feature)


def show_save_preview(player):                  # This function generates a clean, compact save file preview that
    global basic_graphics_enabled, classic_theme_enabled   # consolidates all the main info (progress, stats, etc...) into
    display_achievements = "* No achievements have been unlocked *"
    print(generate_header('SAVE FILE INFO'))  # a neat format for the player to read. The preview is shown
    print("PLAYER STATS:")                  # before loading or erasing a save file.
    print("Name: %s" % player.get_name())
    print("Attack Damage: %d" % player.get_attack())
    print("Health: %i/%i" % (player.get_health(), player.get_max_health()))
    defensive_items = player.get_defensive_items()
    print("\nDEFENSIVE ITEMS:")
    if defensive_items is not None:
        for item in defensive_items:
            print("- "+str(item).title())
    print("\nINVENTORY ITEMS:")
    healing_potion_quantity = player.has_item('Healing Potion')
    hyper_potion_quantity = player.has_item('Hyper Potion')
    smokescreen_quantity = player.has_item('Smokescreen')
    if healing_potion_quantity != 0:
        print(f"- Healing Potion x{healing_potion_quantity}")
    if hyper_potion_quantity != 0:
        print(f"- Hyper Potion x{hyper_potion_quantity}")
    if smokescreen_quantity != 0:
        print(f"- Smokescreen x{smokescreen_quantity}")
    if healing_potion_quantity == 0 and hyper_potion_quantity == 0 and smokescreen_quantity == 0:
        print("* No items held in inventory *")
    print("\nPROGRESS:")
    save_location = player.get_save_location()
    if save_location == 0:
        print("Chapter One: Enter The Dungeon")
    elif save_location == 1:
        print("Chapter Two: Solitary Confinement")
    elif save_location == 2:
        print("Chapter Three: The Great Escape")
    elif save_location == 3:
        print("Chapter Four: What Doesn't Kill You Makes You Stronger")
    elif save_location == 4:
        print("Chapter Five: A Breath Of Fresh Air")
    elif save_location == 5:
        print("Chapter Six: A Puzzle In Darkness")
    elif save_location == 6:
        print("Chapter Seven: With Great Power")
    elif save_location == 7:
        print("Chapter Eight: Finale")
    else:
        print("* No progress has been saved. *")
    if player.is_game_beaten():
        display_achievements = "- You have completed the main story."
    if player.is_expert_mode_complete():
        display_achievements += "\n- You have completed Expert Mode."
    print(f"\nACHIEVEMENTS:\n{display_achievements}")
    if generate_seperator():
        print(generate_seperator())


def ask_load_save(filename, extra_feature):
    global mute_audio, player
    try:
        save_data, is_corrupt, is_incompatible = load_save_data(filename)
        if not is_corrupt and save_data is not None:
            player_name, save_location, damage, max_health, health, game_beaten, expert_mode_beaten, inventory, defensive_items = save_data
            player_object = Player(attack_damage=damage, health=health, max_health=max_health, entered_name=player_name, inventory=inventory, defensive_items=defensive_items, has_beaten_game=game_beaten, has_completed_expert_mode=expert_mode_beaten, save_location=save_location)
            show_save_preview(player_object)
            try:
                choice = int(input("\nLoad this save file?\n1] Yes\n2] No\n--> "))
                if choice == 1:
                    player = player_object
                    if not mute_audio:
                        s = pygame.mixer.Sound("sfx/load.ogg")
                        empty_channel = pygame.mixer.find_channel()
                        empty_channel.play(s)
                    if extra_feature is None:   # 'extra_feature' is used when we need to load a save for reasons other than jumping into a game as normal - by default it's set to None, which allows the load process to continue as usual.
                        if save_location == 1 and game_beaten is False:
                            choice4()
                        elif save_location == 2 and game_beaten is False:
                            chapter_3_start()
                        elif save_location == 3 and game_beaten is False:
                            chapter_4_start()
                        elif save_location == 4 and game_beaten is False:
                            chapter_5_start()
                        elif save_location == 5 and game_beaten is False:
                            chapter_6_start()
                        elif save_location == 6 and game_beaten is False:
                            chapter_7_start()
                        elif save_location == 7 and game_beaten is False:
                            start_chapter_8()
                        elif game_beaten is True:
                            game_beat_options()
                    elif extra_feature == 'expert':     # This code runs when the player is starting Expert Mode.
                        if player.has_beaten_game:
                            start_expert_mode()
                        else:
                            print("\nYou can't play Expert Mode with this save file because you have not beaten the game. Select a save\nfile that you have already beaten the game under.")
                            load(extra_feature)
                elif choice == 2:
                    load(extra_feature)
                else:
                    print("\nPlease select a valid option.")
                    ask_load_save(filename, extra_feature)
            except ValueError:
                print("\nPlease select a valid option.")
                ask_load_save(filename, extra_feature)
        elif is_corrupt:
            print("\nThe selected save file is corrupt - it cannot be loaded.")
            load(extra_feature)
        elif is_incompatible:
            save_file_incompatible(filename, extra_feature)
        else:
            print("\nNo save data exists in the specified slot.")
            load(extra_feature)
    except ValueError:
        # Handle Incompatibility
        save_file_incompatible(filename, extra_feature)


def load(extra_feature):
    global basic_graphics_enabled, classic_theme_enabled
    slots = [
        {'number': 1, 'filename': 'data/savedata.dat'},
        {'number': 2, 'filename': 'data/savedata2.dat'},
        {'number': 3, 'filename': 'data/savedata3.dat'}
    ]
    print(generate_header('LOAD GAME'))
    if extra_feature == 'expert':
        print("Please select a save file to play Expert Mode with:")
    for slot_info in slots:                 # Output slot info for each save slot.
        display_save_slot_info(slot_info)
    if generate_seperator():
        print(generate_seperator())
    try:
        choice = int(input("4] Cancel\n--> "))
        if 1 <= choice <= 3:
            slot_info = next((slot for slot in slots if slot['number'] == choice), None)
            ask_load_save(slot_info['filename'], extra_feature)
        if choice == 4:
            menu()
        else:
            print("\nPlease select a valid choice.")
            load(extra_feature)
    except ValueError:
        print("\nBad input. Only integers can be entered here!")
        load(extra_feature)


def save_success():
    global player, have_credits_rolled
    save_location = int(player.get_save_location())
    game_beaten = player.is_game_beaten()
    expert_mode_complete = player.is_expert_mode_complete()
    try:
        continue2 = int(input("\nYour progress has been saved! Continue playing? \n1] Yes\n2] No\n--> "))
        if continue2 == 1:
            print(" ")
            if not have_credits_rolled:
                warp_to_chapter(save_location)
            elif game_beaten and have_credits_rolled:
                print("Saved!")
                if expert_mode_complete:
                    post_credits_expert_mode()
                else:
                    post_credits()
            else:
                return
        elif continue2 == 2:
            print("Returning to menu...\n")
            reset_temp_variables()    # Reset the defeated enemies list.
            menu()
        else:
            invalid_selection_message()
            save_success()
    except ValueError:
        invalid_selection_message()
        save_success()


def load_save_data(slot_filename):
    # This function is responsible for accessing save files stored locally. It accesses the relevant file (determined
    # by the parameter slot_filename), and returns data.
    try:
        with open(str(slot_filename), 'rb') as f:
            player_name, save_location, damage, max_health, health, game_beaten, expert_mode_beaten, inventory, defensive_items = pickle.load(f)
            retrieved_data = player_name, save_location, damage, max_health, health, game_beaten, expert_mode_beaten, inventory, defensive_items
            # Data is returned in this format - retrieved data, is_corrupt, is_incompatible
            return retrieved_data, False, False     # Return the data as a tuple, and don't raise any flags which would indicate an error.
    except FileNotFoundError:
        return None, False, False   # Return 'none', so the game can handle a non-existent save file.
    except EOFError and pickle.UnpicklingError as e:
        return None, True, False    # Returns the 'is_corrupt' flag, indicating a corrupt save.
    except ValueError:
        return None, False, True    # Returns the 'is_incompatible' flag, which tells the game that the selected save data is incompatible.


def display_slot_info(slot_number, player_name, game_beat):
    if game_beat:
        print(f"{slot_number}] SLOT {slot_number} - {player_name} *")
    else:
        print(f"{slot_number}] SLOT {slot_number} - {player_name}")


def save_to_slot(slot_filename, post_game_save):
    global save_location_cache, have_credits_rolled, player, mute_audio
    print("Now saving...")
    # Retrieve all the data that needs to be saved from the Player object, and initialise it to separate variables.
    player_name = str(player.get_name())
    save_location = player.get_save_location()
    damage = player.get_attack()
    max_health = player.get_max_health()
    health = player.get_health()
    game_beaten = player.is_game_beaten()
    expert_mode_beaten = player.is_expert_mode_complete()
    inventory = player.get_inventory_items()
    defensive_items = player.get_defensive_items()
    data_to_save = [player_name, save_location, damage, max_health, health, game_beaten,
                    expert_mode_beaten, inventory, defensive_items]     # Put alllll of those variables above into an array.
    with open(slot_filename, 'wb') as f:    # Save the array to a file
        pickle.dump(data_to_save, f, protocol=2)
    if not mute_audio:
        pygame.mixer.music.load("sfx/incident.ogg")
        pygame.mixer.music.play(1)
    # Logic for loading the correct thing after the player saves progress.
    if not have_credits_rolled:
        save_success()
    elif have_credits_rolled and player.is_game_beaten():
        print("Saved!")
        if not expert_mode_beaten:
            post_credits()
        else:
            post_credits_expert_mode()


def display_save_slot_info(slot_info):
    try:
        save_data, is_corrupt, is_incompatible = load_save_data(slot_info['filename'])
        if not is_corrupt and save_data is not None:
            player_name, save_location, damage, max_health, health, game_beaten, expert_mode_beaten, inventory, defensive_items = save_data
            slot_info.update({'player_name': player_name, 'game_beat': game_beaten})
            display_slot_info(slot_info['number'], player_name, game_beaten)
        elif is_corrupt:
            print(f"{slot_info['number']}] SLOT {slot_info['number']} - [CORRUPT]")
        elif is_incompatible:
            print(f"{slot_info['number']}] SLOT {slot_info['number']} - [INCOMPATIBLE]")
        else:
            print(f"{slot_info['number']}] SLOT {slot_info['number']} - [EMPTY]")
    except ValueError:
        print(f"{slot_info['number']}] SLOT {slot_info['number']} - [INCOMPATIBLE]")


def save_game():
    # The menu that allows a player to save a game to a slot. Note that this function doesn't handle the actual saving
    # process, that's all done by the function save_to_slot.
    global debug, basic_graphics_enabled, disableOverwrite, postGameSave, skip_overwrite_confirmation
    slots = [
        {'number': 1, 'filename': 'data/savedata.dat'},
        {'number': 2, 'filename': 'data/savedata2.dat'},
        {'number': 3, 'filename': 'data/savedata3.dat'}
    ]
    print(generate_header("SAVE GAME"))
    for slot_info in slots:
        display_save_slot_info(slot_info)
    if generate_seperator():
        print(generate_seperator())
    try:
        choice = int(input("4] Cancel\n--> "))
        if 1 <= choice <= 3:
            slot_info = next((slot for slot in slots if slot['number'] == choice), None)

            if 'player_name' in slot_info and 'game_beat' in slot_info and slot_info[
                'player_name'] is not None and not disableOverwrite:
                if skip_overwrite_confirmation is True or skip_overwrite_confirmation is [True]:
                    post_game_save = slot_info['number'] if slot_info['game_beat'] else 0
                    save_to_slot(slot_info['filename'], post_game_save)
                try:
                    overwrite = int(input(
                        f"There is already save data stored in Slot {slot_info['number']}. Is it okay to overwrite it?\n1] Yes\n2] No\n--> "))
                    if overwrite == 1:
                        post_game_save = slot_info['number'] if slot_info['game_beat'] else 0
                        save_to_slot(slot_info['filename'], post_game_save)
                    else:
                        save_game()
                except ValueError:
                    invalid_selection_message()
                    save_game()
            elif 'player_name' in slot_info and 'game_beat' in slot_info and slot_info[
                 'player_name'] is not None and disableOverwrite is True or disableOverwrite is [True]:
                print(
                    f"\nThere is already save data stored in Slot {slot_info['number']}, and it cannot be overwritten. Either select an empty slot to save to, or\ndisable 'Prevent the save file from being overwritten' in the Gameplay menu.")
                save_game()
            else:
                post_game_save = slot_info['number'] if 'game_beat' in slot_info and slot_info['game_beat'] else 0
                save_to_slot(slot_info['filename'], post_game_save)
        elif choice == 4:
            ask_save()
        else:
            print("\nPlease choose a valid option.")
            save_game()
    except ValueError:
        print("\nBad input. Only integers can be entered here!")
        save_game()


def ask_save():
    global mute_audio, player, player_expert_cache
    global enemy_ID
    global have_credits_rolled, expert_mode_enabled
    reset_temp_variables()
    if expert_mode_enabled and have_credits_rolled:   # If expert mode is enabled and the credits have rolled, then expert mode is complete!
        restore_cached_stats()  # Restore player's original stats
    save_location = player.get_save_location()
    has_beaten_game = player.is_game_beaten()
    has_beaten_expert_mode = player.is_expert_mode_complete()
    try:
        if not have_credits_rolled:
            ask = int(input("\nCheckpoint reached! Would you like to save your progress?\n1] Yes\n2] No\n--> "))
        else:
            ask = int(input("\nWould you like to save?\n1] Yes\n2] No\n--> "))
        if ask == 1:
            save_game()
        elif ask == 2:
            if not have_credits_rolled:
                print("Okay, maybe next time.")
            else:
                try:
                    choice = int(input("Are you sure? Bonus features unlocked after beating the game will be unavailable if you don't save.\n1] Yes\n2] No\n--> "))
                    if choice == 1:
                        pass
                    elif choice == 2:
                        ask_save()
                    else:
                        raise ValueError
                except ValueError:
                    invalid_selection_message()
                    ask_save()
        else:
            raise ValueError
    except ValueError:
        invalid_selection_message()
        ask_save()
    # Logic for loading the correct part of the game if the player decides not to save progress.
    if not has_beaten_game and not have_credits_rolled:   # Game hasn't been completed - load the appropriate chapter.
        warp_to_chapter(save_location)
    elif have_credits_rolled and not has_beaten_expert_mode:  # Story has been completed - load the post credits screen.
        post_credits()
    elif have_credits_rolled and has_beaten_expert_mode:  # Story has been completed and expert mode has been beaten - load the post expert mode screen.
        post_credits_expert_mode()
    else:
        return


def post_creditsAutosave(): # I'm gonna be real, I think this is never used but the game seems to have issues whenever
    global postGameSave     # I try to remove it. So, I've decided to do the ultimate programmer move and not touch it for now.
    save_file = 'savedata3.dat'
    if postGameSave == 1:
        save_file = 'savedata.dat'
    elif postGameSave == 2:
        save_file = 'savedata2.dat'
    else:
        ask_save()
    save_to_slot(save_file, post_game_save=0)


def confirm_multichoice_exit():
    choice = 0
    print("\nAre you sure you'd like to quit? The data you just entered will be lost and you'll be returned to the main menu.\n1] Yes\n2] No")
    try:
        choice = int(input("--> "))
        if choice == 1:
            menu()
        elif choice == 2:
            pre_game_multichoice()
        else:
            invalid_selection_message()
            confirm_multichoice_exit()
    except ValueError:
        confirm_multichoice_exit()


def pre_game_multichoice():
    global player
    print("\nYou're nearly ready to begin, " + str(
        player.get_name()) + "! Take a moment to finalize your Player Profile, or select 'Begin' to start:")
    try:
        choice = int(input("1] Begin!\n2] Change Name\n3] Quit\n--> "))
        if choice == 1:
            start_chapter_1()
        elif choice == 2:
            change_name_input()
            pre_game_multichoice()
        elif choice == 3:
            confirm_multichoice_exit()
        else:
            pre_game_multichoice()
    except ValueError:
        print("\nBad input; only integers can be entered here!")
        pre_game_multichoice()


def stats():
    global enemy_ID, player
    print(generate_header('YOUR STATS'))
    print("Name: "+str(player.get_name())+"\nDefence: "+str(player.get_health())+"/"+str(player.get_max_health())+"\nAttack Damage: "+str(player.get_attack()))
    time.sleep(1)
    savePoint = player.get_save_location()
    if savePoint == 0 and enemy_ID == 0:
        pre_game_multichoice()
    if savePoint == 0 and enemy_ID == 1:
        second_choice_alternate()
    elif savePoint == 1:
        choice4()
    elif savePoint == 2:
        chapter_3_choose_direction()
    elif enemy_ID == 1:
        second_choice_alternate()
    elif enemy_ID == 2:
        chapter_3_choose_direction()
    elif enemy_ID == 4:
        chapter_4_high_rank_defeated()
    elif enemy_ID == 6:
        courtyard_guard_defeated()
    elif enemy_ID == 7:
        chapter_7_split()


def stats_input_ask():
    global player
    try:
        check_input = int(input("\nWould you like to see your stats?\n1] Yes\n2] No\n--> "))
        if check_input == 1:
            stats()
        elif check_input == 2:
            print("Okay, then.")
            pre_game_multichoice()
        else:
            invalid_selection_message()
            stats_input_ask()
    except ValueError:
        invalid_selection_message()
        stats_input_ask()


def check_name_validity(entered_name):  # A simple function to check if an entered name is valid.
    try:
        first_character = entered_name[0]   # Invalid names start with a blank character.
    except Exception:
        return False
    if first_character == " ":
        return False    # Return False - prompt the player to choose a different name.
    else:
        return True     # Return True if the name is valid.


def change_name_input():
    global player
    entered_name = input("\nWhat would you like to be called instead?\n--> ")
    if check_name_validity(entered_name):
        print("So you'd rather be called %s? Got it." % str(player.set_name(entered_name)))
    else:
        print("The name you entered is not valid - please choose a different one.")
        change_name_input()


def name_change_ask():
    global player
    try:
        name_input = int(input("\nWould you like to change your name?\n1] Yes\n2] No\n--> "))
        if name_input == 1:
            change_name_input()
            stats_input_ask()
        elif name_input == 2:
            print("Okay. Make sure you're happy with your name; once you've started a game you can't change it.")
            stats_input_ask()
        else:
            invalid_selection_message()
            name_change_ask()
    except ValueError:
        invalid_selection_message()
        name_change_ask()


def player_name_input():
    global basic_graphics_enabled, player
    inventory = {'Healing Potion': 0, 'Hyper Potion': 0,
                 'Smokescreen': 0}  # Creates an inventory with default values, passed to the Player class.
    defensive_items = ['* No Defensive Items *']    # Create an array that will hold defensive items. Seeing as the game hasn't been started yet, set this with a default value of 'No defensive items'.
    player = Player(5, 20, 20, "None set", inventory, defensive_items, False, False, 0) # Create the player object
    print(generate_header("WELCOME"))
    print("Welcome to DeathTrap Dungeon! What's your name? ")
    entered_name = input("--> ")
    if check_name_validity(entered_name):   # Check if the name entered is valid - returns False if invalid (invalid names start with a blank character.)
        print(f"You'd like to be called {str(player.set_name(entered_name))}? No problem!")  # Update the player object with the entered name, and display output.
        name_change_ask()
    else:
        print("The name you entered is not valid - please choose a different one.")
        player_name_input()


def inventory(enemy_type, enemy_object, battle_logic, audio_lockout):
    global player, engagedJuniperFight
    use_item = 0
    print(generate_header("INVENTORY"))
    healing_potion_quantity = player.has_item('Healing Potion')
    hyper_potion_quantity = player.has_item('Hyper Potion')
    smokescreen_quantity = player.has_item('Smokescreen')
    if healing_potion_quantity != 0:
        print(f"1] Healing Potion x{healing_potion_quantity}")
    else:
        print("1] ???")
    if hyper_potion_quantity != 0:
        print(f"2] Hyper Potion x{hyper_potion_quantity}")
    else:
        print("2] ???")
    if smokescreen_quantity != 0:
        print(f"3] Smokescreen x{smokescreen_quantity}")
    else:
        print("3] ???")
    if generate_seperator():
        print(generate_seperator())
    try:
        use_item = int(input("4] Close Inventory\n--> "))
    except ValueError:
        print("\nPlease select a valid option.")
        inventory(enemy_type, enemy_object, battle_logic, audio_lockout)
    if use_item == 1 and healing_potion_quantity != 0:
        max_health = player.use_healing_potion()
        print("\nYou used the Healing Potion! You instantly feel revitalised.")
        time.sleep(1)
        print("\nHealth has been fully restored to "+str(max_health)+"!")
        time.sleep(1)
        if enemy_type == 'juniper' or enemy_type == 'juniper_phase_two' or enemy_type == 'juniper_phase_three':
            print("Emperor Juniper tries to attack, but misses!")   # After healing, Juniper's attacks always miss; this
            time.sleep(1)                                           # is necessary for balancing, otherwise he's almost
            fight_enemy(enemy_type, enemy_object, battle_logic, audio_lockout)  # impossible to beat.
        else:
            enemy_attack_player(enemy_type, enemy_object, battle_logic, audio_lockout)
    elif use_item == 2 and hyper_potion_quantity != 0:
        player.use_hyper_potion(int(player.get_max_health()), int(player.get_attack()))
        print("\nYou have used the Hyper Potion; attack and defence levels have been temporarily boosted to 25.")
        fight_enemy(enemy_type, enemy_object, battle_logic, audio_lockout)
    elif use_item == 3 and smokescreen_quantity != 0:
        if enemy_type != 'juniper' or enemy_type != 'juniper_phase_two' or enemy_type != 'juniper_phase_three':
            print("\nYou have used the Smokescreen! The battlefield is engulfed in a thick cloud of smoke.")
            time.sleep(1)
            print("\nYou use this to your advantage, and slip away unharmed!")
            time.sleep(1)
            battle_logic.stop_music()   # Halt playback of the battle music.
            player.use_smokescreen(enemy_ID)
        else:
            print("\nYou can't use that item here!")
            inventory(enemy_type, enemy_object, battle_logic, audio_lockout)
    elif use_item == 4:
        fight_enemy(enemy_type, enemy_object, battle_logic, audio_lockout)
    else:
        print("\nPlease choose a valid option.")
        inventory(enemy_type, enemy_object, battle_logic, audio_lockout)
    if use_item == 1 and healing_potion_quantity == 0 or use_item == 2 and hyper_potion_quantity == 0 or use_item == 3 and smokescreen_quantity == 0:
        print("\nThere is no item held in inventory slot "+str(use_item)+".")
        inventory(enemy_type, enemy_object, battle_logic, audio_lockout)


def search_chest(chest_contents):   # This function is called every time the player finds a chest in-game. It allows
    global basic_graphics_enabled, player    # them to choose whether to obtain the item, appends their inventory, and displays
    chest_searched = False          # the relevant item artwork and description. It takes the item in the chest as a
    try:                            # parameter, and works the rest out from there.
        choice = int(input("\nYou search the chest. Inside you find a "+str(chest_contents)+". Take it?\n1] Yes\n2] No\n--> "))
        if choice == 1:
            print("\nYou obtained the "+str(chest_contents)+"!")
            item_object = Items(str(chest_contents))    # Create an object using the item name
            time.sleep(1)
            if not basic_graphics_enabled:
                print(item_object.get_item_sprite())
            else:
                print(item_object.get_basic_sprite())
            print(item_object.get_item_description())
            if chest_contents.lower() != 'key' and chest_contents.lower() != 'loaf of bread':    # Don't add single use items to the inventory.
                player.update_inventory(str(chest_contents))    # Append the player's inventory with the found item.
            chest_searched = True   # The function returns True if the player takes the item.
            return chest_searched
        elif choice == 2:
            print("\nYou chose not to loot the chest.")
            return chest_searched
        else:
            print("\nPlease choose a valid option.")
            search_chest(chest_contents)
    except ValueError:
        print("\nPlease choose a valid option.")
        search_chest(chest_contents)


def restart_from_checkpoint():
    global engagedJuniperFight, mute_audio, player
    save_location = int(player.get_save_location())
    try:
        restart = int(input("Continue from last checkpoint? \n1] Yes\n2] No\n--> "))
        if restart == 1:
            player.restore_health()
            warp_to_chapter(
                save_location)  # Pass the save location to the warp_to_chapter function - saves me having to repeat the warp logic every time it is needed.
        elif restart == 2:
            if not mute_audio:
                pygame.mixer.music.stop()
            menu()
        else:
            print("Please choose a valid option.\n")
            restart_from_checkpoint()
    except ValueError:
        print("\nBad input. Only integers can be entered here!\n")
        restart_from_checkpoint()


def expert_checkpoint_restart():
    global player, player_expert_cache, expert_mode_enabled
    try:
        choice = int(input("You have died on Expert Mode! Will you retry or quit? \n1] Retry\n2] Quit\n--> "))
        if choice == 1:
            player.grant_default_inventory()    # Reset inventory items
            player.restore_health()
            print("\nGood luck!")
            start_chapter_1()
        elif choice == 2:
            player = player_expert_cache    # Return the player's original stats.
            expert_mode_enabled = False     # Disable Expert Mode.
            print("\nAll of your stats and items have been returned. Better luck next time!")
            extras_menu()
        else:
            expert_checkpoint_restart()
    except ValueError:
        print("\nBad input. Only integers can be entered here!\n")
        expert_checkpoint_restart()


def game_over():
    global basic_graphics_enabled, expert_mode_enabled, checkedHyperPotion
    reset_temp_variables()  # Reset defeated enemies list, so that previously defeated enemies can be fought again.
    checkedHyperPotion = False
    if not mute_audio:
        pygame.mixer.music.load("sfx/gameover.ogg")
        pygame.mixer.music.play(1)
    time.sleep(1)
    print("\nYour mission is failed. As you lay dying on the ground, you think of all of the innocent people that you didn't manage to save...")
    time.sleep(2.55)
    if not basic_graphics_enabled:
        print(r""" 
▄▀▀▀▀▄    ▄▀▀█▄   ▄▀▀▄ ▄▀▄  ▄▀▀█▄▄▄▄                   
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
                                     █    ▐   ▐     ▐  
""")
    else:
        print("\n== GAME OVER ==\n")
    if not expert_mode_enabled:
        restart_from_checkpoint()
    else:
        expert_checkpoint_restart()


def chapter_5_chest():
    global searchedChest5
    try:
        choice = int(input("After a short period of walking, you come to a chest. Search it? ([1] Yes, [2] No) "))
        if choice == 1:
            if search_chest("Smokescreen"):
                searchedChest5 = True
                print("\nConfident there is nothing of value in the chest, you head back along the corridor.")
                time.sleep(2)
                chapter_5_corridor()
            else:
                searchedChest5 = False
                print("\nYou did not take the smokescreen. You return to the previous enemy_ID empty-handed.")
                chapter_5_corridor()
        elif choice == 2:
            print("You opt not to search the chest.")
            chapter_5_corridor()
        else:
            chapter_5_chest()
    except ValueError:
        print("\nPlease choose a valid option.")
        chapter_5_chest()


def chest8():
    global searchedChest8, basic_graphics_enabled
    if search_chest("Healing Potion"):
        time.sleep(1)
        print("\nYou return to your previous position, in front of the door.")
        time.sleep(1.5)
        chapter_8_choice()
    else:
        print("\nYou did not take the Potion of Healing. You wander back over to your previous position before the door.")
        time.sleep(1.5)
        chapter_8_choice()


def post_credits_expert_mode():
    global mute_audio, expert_mode_enabled
    if not mute_audio:
        pygame.mixer.music.load("sfx/curtain_call.ogg")
        pygame.mixer.music.play(0)
    print(generate_header('CONGRATULATIONS'))
    print(
        "Well done, you've beaten the game on Expert Mode! This is no easy feat; you're truly a DeathTrap Dungeon Master.")
    time.sleep(1)
    print(
        "\nYour save file has been updated to show that you've completed Expert Mode. Feel free to brag to your friends! Your inventory \nitems and stats have also been returned.")
    time.sleep(1)
    print(
        "\nFinally, thank you so much for playing the game. I've been absolutely overwhelmed by the amount of support I've had over the\nyears, and the fact that you've taken the time to not only beat the game, but also complete Expert Mode, genuinely\nmakes me so happy.")
    time.sleep(1)
    input("\nAs soon as you are ready, please press [Enter] to continue... ")
    time.sleep(0.5)
    if not mute_audio:
        pygame.mixer.music.fadeout(200)
    print(" ")
    expert_mode_enabled = False
    menu()


def post_credits():  # The screen showed post-credits.
    global mute_audio, basic_graphics_enabled
    if not mute_audio:
        pygame.mixer.music.load("sfx/curtain_call.ogg")
        pygame.mixer.music.play(0)
    print(generate_header("CONGRATULATIONS"))
    print(
        "Well done for overcoming the challenge and beating the game! The future of Medway may be uncertain, but it's sure to be prosperous with\nEmperor Juniper gone. I hope you enjoyed playing the game as much as I enjoyed making it!")
    time.sleep(2)
    print(
        "\nOh, one last thing - as a reward for beating the game, you've now unlocked some cool extras! Check it out:")
    time.sleep(1)
    print(
        "\nUNLOCKED: Music Player - listen to the game's soundtrack, in addition to some never-before-heard beta tracks!")
    time.sleep(0.5)
    print(
        "UNLOCKED: Chapter Replay - You can now warp to specific chapters whenever you want! See how many secrets you can discover!")
    time.sleep(0.5)
    print(
        "UNLOCKED: Expert Mode - Up for a challenge? Put your skills to the ultimate test in the most challenging DeathTrap Dungeon game mode yet.")
    time.sleep(0.5)
    print(
        "\nTo take advantage of these new features, select 'Extras' on the main menu, or load this save from the main menu. (Saves \nthat you beat the game under are marked with a '*' symbol!)")
    time.sleep(0.7)
    print(
        "\nHey, thanks for playing the game! When I started to program this, I honestly had no idea it'd ever get this big. None of \nthis would be possible without the continued support of the amazing people in the credits!\n")
    time.sleep(0.5)
    input("\nPress [Enter] to continue... ")
    time.sleep(0.5)
    if not mute_audio:
        pygame.mixer.music.fadeout(200)
    print(" ")
    menu()


def restore_cached_stats():  # This function kicks in after you beat Expert Mode. It restores your original stats and items.
    global player, player_expert_cache
    player = player_expert_cache    # Reset the player object with the cached player object.
    player.completed_expert_mode()
    print(player.is_expert_mode_complete())


def game_credits():
    global mute_audio, have_credits_rolled, basic_graphics_enabled, expert_mode_enabled, player
    if not mute_audio:
        if not player.is_game_beaten():
            try:
                pygame.mixer.music.load("sfx/ambient.ogg")
                pygame.mixer.music.play(1)
            except Exception:
                pass
        else:
            try:
                pygame.mixer.music.load("sfx/ambient_percussion.ogg")
                pygame.mixer.music.play(1)
            except Exception:
                pass
    if not basic_graphics_enabled:
        try:
            print("\n\n\n█████▒▒░ DEATHTRAP  DUNGEON ░▒▒█████")
        except Exception:
            print("\n\n\n== DEATHTRAP DUNGEON ==")
        if basic_graphics_enabled is True:
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
    have_credits_rolled = True
    choice = input("\n\nPress [Enter] to continue... ")
    if not mute_audio:
        pygame.mixer.music.fadeout(1000)
    player.game_beaten()    # Sets the attribute 'game_beaten' to true, so the game knows that the player has completed the story.
    if expert_mode_enabled:     # Some special configuration that only comes into play if expert mode is enabled:
        restore_cached_stats()  # Restore the player's original stats and items to how they were before starting expert mode.
        player.completed_expert_mode()  # This attribute is so the game knows if the player has completed expert mode.
        expert_mode_enabled = False     # Finally disable expert mode to avoid issues.
    player.restore_health()     # Restore health
    time.sleep(1)
    ask_save()


def defeated_juniper():
    print("\nYou stand dazed, confused, wounded, shaken... but alive.")
    time.sleep(4)
    print("\nEmperor Juniper lies on the floor, mortally wounded. He coughs and splutters, then begins to talk...")
    time.sleep(4)
    print("\n'...The power... I wanted it...'")
    time.sleep(4)
    print("\n'...I saw other leaders being overthrown... being... used.'")
    time.sleep(4)
    print("\n'I... I couldn't lose my... power.'")
    time.sleep(4)
    print("\n'So... so I exerted the ultimate control... to secure my power... my legacy...'")
    time.sleep(4)
    print("\n'...But... what use is any of that... in the grand scheme of things...?'")
    time.sleep(4)
    print("\n'...One day... everyone will forget your name...'")
    time.sleep(4)
    print("\nThe Emperor's eyes roll back into his head; he smiles one last time, then grows still. ")
    time.sleep(4)
    print("\nYou stand there, in total shock. Everything is silent.")
    time.sleep(4)
    print(
        "\nYou snap back to reality. You glance back and forth between your own bloodied hands and the Emperor. He's still motionless.")
    time.sleep(4)
    print(
        "\nSomberly, you trudge back from the way you came. To release the other inmates, and then, whatever follows.")
    time.sleep(4)
    print("\nYou're shaken and wounded, the future of Medway is uncertain. But you're alive.")
    time.sleep(6)
    game_credits()


def stats_warp():   # This function is responsible for placing the player back in the correct section of the game after
    global player, enemy_ID     # viewing stats.
    save_location = player.get_save_location()
    if save_location == 0 and enemy_ID == 0:
        pre_game_multichoice()
    elif save_location == 0 and enemy_ID == 1:
        second_choice_alternate()
    elif save_location == 1:
        choice4()
    elif save_location == 2:
        chapter_3_choose_direction()
    elif enemy_ID == 1:
        second_choice_alternate()
    elif enemy_ID == 2:
        chapter_3_choose_direction()
    elif enemy_ID == 3:
        chapter_3_defeated_first_guard()
    elif enemy_ID == 4:
        chapter_4_high_rank_defeated()
    elif enemy_ID == 6:
        courtyard_guard_defeated()
    elif enemy_ID == 7:
        chapter_7_split()


def ask_view_stats():
    global player, expert_mode_enabled
    time.sleep(0.5)
    try:
        choice = int(input("\nWould you like to see your stats?\n1] Yes\n2] No\n--> "))
        if choice == 1:
            print(generate_header('YOUR STATS'))
            player_name, player_health, player_max_health, player_attack_damage = player.get_stats()
            if expert_mode_enabled:
                player_name += ' - Playing on Expert Mode'  # Show an indicator when expert mode is enabled.
            defensive_items = player.get_defensive_items()
            print(f"YOU ({player_name})\nDEFENCE: {player_health}/{player_max_health}\nATTACK: {player_attack_damage}\nHOLDING:")
            if defensive_items is not None:
                for item in defensive_items:
                    print("- " + str(item).title())
        elif choice == 2:
            pass
        else:
            print("\nPlease choose a valid option.")
            ask_view_stats()
    except ValueError:
        print("\nPlease choose a valid option.")
        ask_view_stats()
    print(" ")
    time.sleep(2)
    stats_warp()


def obtain_dropped_item(sprite, item_description, item_name, item_attack_increment, item_defense_increment, player_held_defensive_items):
    global player, expert_mode_enabled
    if item_name == "nothing" and expert_mode_enabled:
        print("\nThe guard is holding nothing of value to you, and drops no loot!")
        time.sleep(1.5)
        ask_view_stats()
    try:
        choice = int(input("\nThe guard drops a "+str(item_name)+". Pick it up?\n1] Yes\n2] No\n--> "))
        if choice == 1:
            if item_name in player_held_defensive_items or item_name.title() in player_held_defensive_items:    # If the player is already holding this item, don't let them get it a second time.
                print("\nYou already have this item, you can't carry a second!")
                ask_view_stats()
            else:
                print("\nYou obtained the "+str(item_name)+"!")
                if item_name.lower() == "hyper potion" or item_name.lower() == "healing potion":
                    player.update_inventory(item_name)  # Add inventory items to the player's inventory.
                elif item_name == "loaf of bread":
                    player.restore_health()     # Restore health if the item obtained was a healing item.
                else:
                    player.update_defensive_items(str(item_name))   # If the item gained wasn't an inventory or healing item, then it was a defensive item - update accordingly.
                    if item_attack_increment != 0:  # If the item increases attack power, update player stats accordingly
                        player.gain_attack(int(item_attack_increment))
                    if item_defense_increment != 0:  # Same as above, but for items that affect defense.
                        player.gain_defence(int(item_defense_increment))
                time.sleep(1)
                print(sprite)
                time.sleep(1)
                print(item_description)
                time.sleep(0.5)
                ask_view_stats()
        elif choice == 2:
            print("\nYou didn't pick up the "+str(item_name)+".")
            ask_view_stats()
        else:
            print("\nPlease choose a valid option.")
            obtain_dropped_item(sprite, item_description, item_name, item_attack_increment, item_defense_increment, player_held_defensive_items)
    except ValueError:
        print("\nPlease choose a valid option.")
        obtain_dropped_item(sprite, item_description, item_name, item_attack_increment, item_defense_increment, player_held_defensive_items)


def enemy_defeated(enemy_type, enemy_object, battle_logic, audio_lockout):  # Logic after the player wins battles.
    global basic_graphics_enabled, player, enemies_defeated, enemy_ID
    enemies_defeated.append(enemy_ID)
    player_held_defensive_items = player.get_defensive_items()
    if enemy_type == 'guard' or enemy_type == 'high_rank_guard':
        enemy_item = enemy_object.get_held_item()   # Get the item that the defeated enemy was holding.
        dropped_item = Items(str(enemy_item))   # Create an object using the Items class from the held item.
        if not basic_graphics_enabled:
            sprite = dropped_item.get_item_sprite()     # Show the item sprite.
        else:
            sprite = dropped_item.get_basic_sprite()    # Same as above, but for basic graphics mode.
        item_defense_increment = dropped_item.get_defense_increment()   # Get the defense value of the item.
        item_attack_increment = dropped_item.get_attack_increment()     # Same as above, but for attack.
        item_description = dropped_item.get_item_description()      # Get a description of the item, generated when the item object was created.
        item_name = str(dropped_item.get_item_name().lower())  # Retrieve the item name and make it lowercase so it can be added to a string without looking janky.
        obtain_dropped_item(sprite, item_description, item_name, item_attack_increment, item_defense_increment, player_held_defensive_items)    # Pass all the relevant variables to the obtain_dropped_item function.
    elif enemy_type == 'juniper':
        enemy_type = 'juniper_phase_two'    # Set the enemy_type variable to the correct phase, so Juniper's stats can be reset by encounter_enemy.
        time.sleep(2)
        print("\n\nEmperor Juniper staggers back, before collapsing to the floor.")
        time.sleep(3)
        print(
            "\nHe suddenly reaches into his pocket, and pulls out a vial of something. You stare, trying to work out what he's holding.")
        time.sleep(3)
        print("\nSuddenly, it clicks; he's holding a Potion of Healing.")
        time.sleep(3)
        print(
            "\nBefore you can stop him, he takes a sip. He swiftly leaps back to his feet, before charging back at you...")
        time.sleep(3.5)
        enemy_object.increment_phase()
        encounter_enemy(enemy_type)
    elif enemy_type == 'juniper_phase_two':
        enemy_type = 'juniper_phase_three'
        time.sleep(2)
        print("Emperor Juniper falls to the ground once more, coughing and spluttering.")
        time.sleep(3)
        print("\nHe lets out a guttural moaning sound, before his eyes roll back into his head and he goes limp.")
        time.sleep(3)
        print("\nOvercome with adrenaline, shock, and fear, you examine your surroundings once again.")
        time.sleep(3.5)
        print(
            "\nSuddenly, you hear a slight sound, which snaps you out of your trance-like state. Emperor Juniper has shuffled to his feet, and in his hand\nhe holds another potion. Only this one looks different...")
        time.sleep(3)
        print("\nYou freeze. Emperor Juniper is holding a Hyper Potion.")
        time.sleep(3)
        print("\nYou let out a startled yell, but its too late; Juniper has already began to drink from the vial.")
        time.sleep(3)
        print(
            "\nEmperor Juniper throws the vial aside; he lets out a violent yell as this newfound strength courses through him.")
        time.sleep(3)
        print(
            "\nHe charges over to you with incredible agility and speed. You wield your weapon and brace for impact...")
        time.sleep(4)
        enemy_object.increment_phase()
        encounter_enemy(enemy_type)
    elif enemy_type == 'juniper_phase_three':
        defeated_juniper()


def examine_enemy(enemy_type, enemy_object, battle_logic, audio_lockout):   # When the player selects 'Examine' during
    global player, expert_mode_enabled                                      # battle, this displays relevant info.
    player_name, player_health, player_max_health, player_attack_damage = player.get_stats()
    if expert_mode_enabled:
        player_name += ' - Playing on Expert Mode'
    defensive_items = player.get_defensive_items()
    enemy_stats = enemy_object.get_stats()
    enemy_name = 'EMPEROR JUNIPER:'
    if enemy_type == 'guard':
        enemy_name = "GUARD:"
    elif enemy_type == 'high_rank_guard':
        enemy_name = 'HIGH RANKING GUARD:'
    elif enemy_type == 'juniper_phase_two':
        enemy_name = 'EMPEROR JUNIPER (PHASE TWO):'
    elif enemy_type == 'juniper_phase_three':
        enemy_name = 'EMPEROR JUNIPER (PHASE THREE):'
    print(f"\nYOU ({player_name}):\nATTACK: {player_attack_damage}\nDEFENCE: {player_health}/{player_max_health}")
    if defensive_items is not None:
        print("HOLDING: "+", ".join(defensive_items))
    print("\n\n"+str(enemy_name)+str(enemy_stats))
    time.sleep(0.5)
    fight_enemy(enemy_type, enemy_object, battle_logic, audio_lockout)


def run_from_battle(enemy_type, enemy_object, battle_logic, audio_lockout):
    global expert_mode_enabled
    if enemy_type == 'juniper' or enemy_type == 'juniper_phase_two' or enemy_type == 'juniper_phase_three':
        print("\nThere's no running from this battle!")
        time.sleep(1)
        enemy_attack_player(enemy_type, enemy_object, battle_logic, audio_lockout)
    max_escape_chance = 5
    if expert_mode_enabled:
        max_escape_chance = 10
    chance = random.randint(0, int(max_escape_chance))
    if chance != 1:
        print("\nYou try to run, but the enemy blocks your path!")
        time.sleep(1)
        enemy_attack_player(enemy_type, enemy_object, battle_logic, audio_lockout)
    else:
        print("\nYou make a run for it, and you manage to escape!")
        battle_logic.stop_music()
        time.sleep(1)
        # Handle escape here


def enemy_attack_player(enemy_type, enemy_object, battle_logic, audio_lockout):
    global player, disable_critical, player_only_critical, expert_mode_enabled
    enemy_friendly_name = 'not specified'   # This variable controls the text that is shown on the enemy's turn.
    returned_value = 0  # This variable is the damage that is dealt by an enemy.
    attack_message = '\n'   # This is used to let the player know they've received a critical hit. By default, it's a new line.
    if enemy_type == 'guard':
        enemy_friendly_name = "The Guard"
    elif enemy_type == 'high_rank_guard':
        enemy_friendly_name = "The High Ranking Guard"
    elif enemy_type == 'juniper' or enemy_type == 'juniper_phase_two' or enemy_type == 'juniper_phase_three':
        enemy_friendly_name = "Emperor Juniper"
    if not disable_critical or not player_only_critical:    # Only execute this code if the player has allowed critical hits from enemies.
        if battle_logic.critical_hit(expert_mode_enabled, type="enemy"):
            returned_value = enemy_object.land_critical_hit()
            attack_message = "\nIt's a critical hit! "
        else:
            returned_value = enemy_object.get_attack()
    else:
        returned_value = enemy_object.get_attack()
    time.sleep(0.5)     # Add a slight delay, to help with reading.
    print(str(attack_message)+str(enemy_friendly_name)+" attacks, dealing "+str(returned_value)+" damage!")  # Format into a summary of the attack, which includes if a critical hit was landed and the amount of damage inflicted.
    player.sustain_damage(returned_value)
    time.sleep(0.5)
    print("\nYou have "+str(player.get_health())+" health remaining.")
    if battle_logic.is_dead(int(player.get_health())):          # Passes player health to the is_dead method.
        battle_logic.stop_music()                               # If the method returns True, then the player is dead
        battle_logic.handle_player_death()                      # and this is then handled by BattleLogic.
    else:
        fight_enemy(enemy_type, enemy_object, battle_logic, audio_lockout)


def fight_enemy(enemy_type, enemy_object, battle_logic, audio_lockout):
    global mute_audio, player, enemy_only_critical, disable_critical, expert_mode_enabled
    returned_value = 0
    attack_message = 'default'  # This is the text that is shown to the player when attacking an enemy.
    enemy_friendly_name = 'default'  # This is the name of the enemy, which is shown to the player.
    hyper_use_count = int(player.get_hyper_use_count())     # Returns the use count for the Hyper Potion item.
    if enemy_type == 'juniper' or enemy_type == 'juniper_phase_two' or enemy_type == 'juniper_phase_three':
        player.set_hyper_use_count(0)
        enemy_friendly_name = 'Emperor Juniper'
    elif enemy_type == 'guard':
        enemy_friendly_name = 'the Guard'
    elif enemy_type == 'high_rank_guard':
        enemy_friendly_name = 'the High Ranking Guard'
    if hyper_use_count > 0:
        if battle_logic.has_hyper_potion_worn_off(hyper_use_count):
            print("\nThe effects of the hyper potion have worn off! Attack and defence have been reverted to their\nprevious values.")
            player.hyper_potion_end()   # Restore stats after the Hyper Potion has worn off.
        else:
            player.reduce_hyper_potion_use()
            if debug != 0:
                print(hyper_use_count)
    if not mute_audio and not audio_lockout:
        battle_logic.play_music()
        audio_lockout = True
    try:
        choice = int(input("\nWhat will you do?\n1] Attack\n2] Use Item\n3] Examine\n4] Run\n--> "))
        if choice == 1:
            if hyper_use_count == 0:  # hyper_use_count is zero if the Hyper Potion hasn't been used.
                if enemy_only_critical is True or disable_critical is True:  # Only run through the critical hit logic if the player has not disabled this behaviour.
                    if battle_logic.critical_hit(expert_mode_enabled,
                                                 type="player"):  # If this method returns True, then the player successfully initiated a critical hit.
                        returned_value = player.land_critical_hit(int(enemy_object.get_health()))
                        attack_message = "You land a critical hit! You strike " + str(
                            enemy_friendly_name) + ", dealing "
                else:
                    returned_value = player.attack_guard(int(enemy_object.get_health()))
                    attack_message = "You attack " + str(enemy_friendly_name) + ", dealing "
            else:
                returned_value = 25
                attack_message = "You attack " + str(enemy_friendly_name) + ", dealing "
            print("\n" + str(attack_message) + str(returned_value) + " damage!")
            enemy_object.sustain_damage(int(returned_value))
            time.sleep(0.5)
            print("\n" + str(enemy_friendly_name) + " has " + str(enemy_object.get_health()) + " health remaining.")
            time.sleep(0.5)
            if battle_logic.is_dead(
                    int(enemy_object.get_health())):  # Passes enemy health to the is_dead method, to check if the enemy has any health remaining.
                if not mute_audio:  # Only call the function to stop audio if music is unmuted - not performing this check can lead to crashes if Pygame isn't installed.
                    battle_logic.stop_music()  # Stops the battle music.
                print("\nYou are victorious!")
                enemy_defeated(enemy_type, enemy_object, battle_logic, audio_lockout)
        elif choice == 2:
            inventory(enemy_type, enemy_object, battle_logic, audio_lockout)
        elif choice == 3:
            examine_enemy(enemy_type, enemy_object, battle_logic, audio_lockout)
        elif choice == 4:
            run_from_battle(enemy_type, enemy_object, battle_logic, audio_lockout)
        else:
            print("\nPlease choose a valid option.")
            fight_enemy(enemy_type, enemy_object, battle_logic, audio_lockout)
    except ValueError:
        print("\nPlease choose a valid option.")
        fight_enemy(enemy_type, enemy_object, battle_logic, audio_lockout)
    enemy_attack_player(enemy_type, enemy_object, battle_logic, audio_lockout)


def encounter_enemy(enemy_type):                   # The encounter_enemy function takes the enemy_type as a parameter, and displays
    global basic_graphics_enabled, expert_mode_enabled, enemy_ID  # the appropriate character artwork. There are two sprites; one for normal gameplay,
    enemy_encounter_message = "default"            # and one for players with Basic Graphics mode enabled. The global variable
    enemy_sprite = "default"                       # basic_graphics_enabled is used to choose the correct sprite. It also initialises the
    enemy_held_item = "default"
    if enemy_type == 'juniper' or enemy_type == 'juniper_phase_two' or enemy_type == 'juniper_phase_three':     # enemy as an object.
        if not basic_graphics_enabled:
            enemy_sprite = r"""   
                                                                             
                ██                                                                                  
                ██                                                                                  
                ██                                                                                  
                ██                                                                                  
                ██                                                                                  
              ▒▒██                                                                                  
              ▒▒██                                                                                  
              ██                                ▓▓██  ▓▓▓▓                                          
              ██                              ▓▓  ██  ▓▓  ▓▓                                        
              ██                            ▒▒    ██  ▓▓    ▒▒                                      
              ██                            ▓▓  ▒▒▒▒  ▒▒▒▒  ▓▓                                      
              ██                          ▒▒██  ██    ▒▒██  ▓▓                                      
              ██                            ██  ██    ▒▒██  ▓▓                                      
            ▒▒██                            ██  ██    ▒▒██▒▒██                                      
            ▒▒██                      ▒▒▒▒▓▓██  ▒▒▒▒▓▓▓▓  ▒▒██                                      
            ▒▒██                    ▓▓▓▓▒▒▒▒▓▓▒▒▒▒▒▒    ▒▒▒▒██                                      
            ▒▒██                  ▓▓▓▓▒▒  ▒▒▒▒▓▓▒▒  ▒▒▒▒▒▒▒▒██                                      
            ▒▒██                ██▓▓▒▒        ▒▒▓▓▒▒▒▒▒▒▒▒██                                        
            ▒▒██                ██▓▓▒▒        ▒▒▒▒▓▓▒▒▓▓██                                          
            ▒▒██              ██▓▓▒▒▓▓▒▒  ▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓██                                        
            ▒▒██              ▓▓▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒                                      
            ▒▒██            ▓▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓            ▓▓                                      
        ▒▒  ▒▒▒▒▓▓          ▓▓▒▒▓▓▓▓▒▒▒▒▓▓▓▓██▒▒████████▓▓██                                        
        ▓▓▓▓▓▓▒▒██        ██▒▒▒▒▒▒▒▒▓▓▓▓▓▓████████▒▒▒▒▓▓                                            
  ▒▒▒▒          ▒▒▒▒▒▒██  ██  ▒▒▒▒▒▒▒▒▒▒██▓▓        ▒▒██████                                        
  ▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▒▒          ████▓▓▒▒                                      
    ▓▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▓▓  ▓▓▓▓██▒▒▒▒▒▒▒▒▓▓▓▓▒▒        ▓▓██▓▓  ▒▒▒▒                                    
      ▒▒▒▒      ██▓▓████▒▒▒▒▒▒████████████▒▒▒▒▒▒▒▒▒▒▓▓▒▒      ▒▒▒▒                                  
      ▒▒▒▒      ██▓▓▒▒▒▒▒▒▒▒▒▒██▓▓██████████▒▒▒▒▒▒██▒▒▒▒      ▒▒▒▒▒▒                                
      ▒▒▒▒      ██▒▒▒▒▒▒▒▒▒▒████▓▓▒▒          ▒▒████▒▒▒▒▒▒  ▓▓    ▒▒▒▒                              
      ██▓▓      ██▒▒▒▒▒▒▒▒██████▓▓▓▓▓▓▒▒▒▒▒▒▒▒██▓▓▓▓▓▓▓▓▒▒▓▓        ▒▒▒▒██                          
      ▒▒██▓▓▒▒▒▒████▓▓▓▓████████▓▓▓▓▓▓▒▒▒▒▒▒▓▓▓▓▒▒▒▒▓▓▓▓▒▒▒▒            ▓▓                          
        ██▓▓▓▓  ▒▒▒▒██████████████████▓▓██▓▓▓▓▒▒▒▒▒▒▒▒▓▓  ▒▒        ▒▒██                            
        ██▓▓▒▒    ▒▒▒▒                ▒▒▓▓▒▒▒▒▒▒  ▒▒▒▒▒▒██      ▒▒██                                
        ██▓▓▒▒    ▒▒▒▒                ▒▒▒▒    ▒▒▒▒▒▒▒▒▓▓████████                                    
        ██▓▓▒▒    ▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒    ▒▒▒▒▓▓▓▓██████▒▒▒▒                                    
        ▒▒▓▓▓▓    ▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓██▓▓▓▓████▒▒▓▓▒▒                                  
              ▓▓▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓████▓▓██▓▓██▓▓▓▓▓▓██▓▓    ▒▒▓▓▓▓██                            
                                ██████▓▓▒▒▒▒  ▒▒▒▒▓▓▓▓▓▓▓▓      ▒▒▒▒  ▒▒▒▒▓▓██                      
                            ██████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒      ▒▒▒▒      ▒▒▒▒  ██                    
                        ████▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▒▒    ▒▒▒▒      ▒▒▒▒▒▒  ▒▒                    
                    ▓▓▓▓▓▓▓▓▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒        ▓▓▓▓▒▒▒▒▒▒      ▒▒▒▒▒▒▒▒  ▒▒                    
                  ▓▓▓▓▓▓▒▒▒▒▒▒▒▒▓▓▓▓▒▒▒▒▒▒          ▒▒██▓▓▒▒▒▒    ▒▒▒▒▒▒▒▒  ▒▒▓▓                    
                  ██▒▒▒▒▒▒▒▒▓▓▓▓████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓██▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓  ▒▒██                      
                    ▓▓▒▒▒▒    ██▓▓▓▓▒▒▒▒▒▒          ▒▒▓▓▒▒▒▒▓▓▓▓        ▒▒████                      
                    ████▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒▒▒▒▒        ▒▒▓▓▒▒▒▒▒▒▓▓████▒▒▒▒██▓▓██                      
                    ██▓▓▒▒▒▒▒▒▓▓▓▓▓▓  ▒▒▓▓▒▒▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒▒▒      ▒▒▒▒▓▓████                    
                  ▓▓▓▓▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▒▒▒▒          ▒▒▓▓▓▓▒▒▒▒▒▒      ▒▒▒▒  ▒▒▓▓▓▓                  
                ▓▓▒▒▒▒▓▓▒▒▒▒▒▒▓▓▓▓██  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒██▓▓▒▒          ▒▒  ▒▒▒▒██                  
                ██▒▒▒▒▒▒▒▒▒▒▒▒██▓▓                        ██▓▓▒▒      ▒▒▒▒  ▒▒▓▓▓▓                  
                ██▒▒▒▒▒▒▒▒▒▒▒▒██▓▓                            ██▓▓        ▒▒▓▓  ████                
                ▒▒▓▓▒▒▒▒▒▒▒▒▒▒██▓▓                            ▒▒▒▒▒▒    ▒▒▒▒    ▓▓▓▓                
                  ██▒▒▒▒▒▒▒▒▒▒▓▓▓▓                                  ▓▓        ▒▒▒▒▓▓▓▓              
                    ▓▓▒▒▒▒▒▒▒▒▒▒▓▓                                    ▓▓▓▓▓▓▒▒▓▓    ▓▓▓▓            
                      ██▒▒▒▒▒▒▒▒▒▒                                        ▒▒██▒▒      ▒▒██          
                        ██▒▒▒▒▒▒▒▒██                                          ██▒▒      ▒▒██        
                        ▓▓▓▓▒▒▒▒▒▒██                                          ▓▓▓▓▒▒      ▓▓▓▓      
                          ▒▒▒▒▒▒▒▒▓▓▓▓                                          ▒▒▓▓▒▒    ▒▒▓▓       
                    ▒▒██████▓▓▓▓▒▒▒▒██                                            ██▓▓▓▓▒▒▒▒▓▓▓▓▓▓  
                  ██▓▓    ▓▓▒▒▒▒▒▒▒▒██                                          ██  ▒▒▒▒  ▒▒    ▒▒██
              ██▓▓▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒████████████████████████████████████████████▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒▒██
              ██                    ████████████████████████████████████████████                  ██"""
        else:
            enemy_sprite = r"""
      _,.
    ,` -.)
   ( _/-\\-._
  /,|`--._,-^|            ,
  \_| |`-._/||          ,'|
    |  `-, / |         /  /
    |     || |        /  /
     `r-._||/   __   /  /
 __,-<_     )`-/  `./  /
'  \   `---'   \   /  /
    |           |./  /
    /           //  /
\_/' \         |/  /
 |    |   _,^-'/  /
 |    , ``  (\/  /_
  \,.->._    \X-=/^
  (  /   `-._//^`
   `Y-.____(__}
    |     {__)
          ()"""
        # Juniper init; sets the appropriate attack / defence levels.
        enemy_encounter_message = "Emperor Juniper draws his sword!"
        if enemy_type == 'juniper' or enemy_type == 'juniper_phase_two':
            if not expert_mode_enabled:
                enemy_object = Juniper(7, 22, 22, 0)
            else:
                enemy_object = Juniper(5, 20, 20, 0)
        elif enemy_type == 'juniper_phase_three':
            if not expert_mode_enabled:
                enemy_object = Juniper(8, 25, 25, 2)
            else:
                enemy_object = Juniper(6, 25, 25, 2)
        battle_logic = BattleLogic('juniper', 'sfx/puppets.ogg')
    elif enemy_type == 'guard':
        if not basic_graphics_enabled:
            enemy_sprite = r"""
                  ▒▒▓▓                                  
                  ▒▒▓▓░░▒▒░░                            
                  ░░▓▓▒▒    ░░░░                        
                    ██    ░░  ░░░░                      
                    ██▒▒  ░░  ░░░░                      
                    ░░▒▒  ░░  ░░  ░░                    
                    ░░▒▒░░  ░░  ░░░░                    
                                  ░░                    
            ▓▓░░                ░░      ▒▒▒▒            
            ▒▒▒▒▓▓▒▒▒▒    ░░██▓▓▒▒▒▒▓▓▒▒▓▓▓▓            
              ▒▒▒▒▒▒▓▓▓▓░░▒▒▓▓▓▓▒▒▒▒▓▓▓▓▒▒▓▓            
              ▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▒▒▒▒▓▓▓▓▓▓▒▒▓▓            
            ▒▒▓▓▒▒▒▒▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▓▓▓▓▓░░            
          ░░▓▓▒▒░░  ░░▒▒▓▓░░    ▒▒▓▓▓▓▓▓▓▓              
          ▓▓▓▓▓▓▓▓▒▒    ░░▓▓▓▓░░░░▓▓▓▓▓▓▒▒              
        ▒▒▓▓▓▓▓▓░░  ░░░░▒▒▓▓▓▓░░▒▒▓▓▓▓▓▓                
        ▒▒▓▓▓▓▓▓  ░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓                
        ▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░                
        ░░▒▒▒▒▒▒▓▓░░▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▒▒                  
              ▒▒▒▒▓▓▒▒▓▓▓▓▓▓░░▒▒▒▒▓▓                    
              ▒▒▒▒▒▒▓▓▒▒▓▓▒▒░░▒▒▒▒▓▓                    
            ▒▒▒▒▒▒▓▓▒▒▒▒▓▓▒▒▒▒▒▒▒▒░░░░                  
            ▒▒▒▒▒▒▓▓▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒░░░░              
            ▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░░░░░          
            ▓▓▓▓▓▓▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▓▓    ░░░░        
            ▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓▓▒▒      ░░░░░░    
          ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░          ░░░░  
          ▓▓▒▒▒▒▒▒▒▒▒▒▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒            ░░▒▒
          ██▒▒▒▒▒▒▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                
          ▓▓▒▒▒▒▒▒▒▒▒▒    ▓▓▒▒▒▒▒▒▒▒▒▒▒▒▒▒              
          ██▓▓▓▓▒▒▓▓      ▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░              
          ▒▒▓▓▓▓▒▒          ▓▓▒▒▒▒▓▓▓▓▒▒                                 
      ░░▓▓▓▓▓▓                  ▒▒▓▓▓▓                  
░░░░▓▓▓▓▓▓▓▓▓▓                    ▒▒▓▓▒▒                
▓▓▓▓▓▓▓▓▓▓▓▓▓▓░░                  ▓▓▓▓▓▓                
                                  ▓▓▓▓▓▓▒▒              
                                  ▓▓▓▓▓▓▓▓▓▓            
                                  ▓▓▓▓▒▒▓▓▓▓            
                                  ░░░░░░▓▓▓▓▒▒░░          
██████████▓▓████▓▓██████████████████████████████████████"""
        else:
            enemy_sprite = r"""  ,^.
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
      <\\\)     (///>"""
        # Guard init here; uses the global variable 'enemy_ID' to determine the stats of the guard.
        enemy_encounter_message = "You are challenged by a guard!"
        battle_logic = BattleLogic('guard', 'sfx/battle.ogg')
        # Logic to give the guard the correct held item for their location in-game and the difficulty setting.
        if enemy_ID == 1 and not expert_mode_enabled:
            enemy_held_item = "Wooden Spear"
        elif enemy_ID == 1 and expert_mode_enabled:
            enemy_held_item = "Healing Potion"
        elif enemy_ID == 2 and not expert_mode_enabled:
            enemy_held_item = "Wooden Shield"
        elif enemy_ID == 3 and not expert_mode_enabled:
            enemy_held_item = "Loaf of Bread"
        elif enemy_ID == 4 and not expert_mode_enabled:
            enemy_held_item = "Rusty Sword"
        elif enemy_ID == 5 and not expert_mode_enabled:
            enemy_held_item = "Hyper Potion"
        elif enemy_ID == 5 and expert_mode_enabled:
            enemy_held_item = "Healing Potion"
        elif enemy_ID == 6 and not expert_mode_enabled:
            enemy_held_item = "Rusty Chestplate"
        elif enemy_ID == 2 or enemy_ID == 3 or enemy_ID == 4 or enemy_ID == 6 and expert_mode_enabled:
            enemy_held_item = "Nothing"
        else:
            enemy_held_item = "Healing Potion"  # enemy_ID 7 and 8 both have healing potions
        enemy_object = Enemy("GUARD", 5, 20, 20, enemy_held_item)
    elif enemy_type == 'high_rank_guard':
        if not basic_graphics_enabled:
            enemy_sprite = r"""
                            ░░    ░░░░░░    ░░░░        
                            ░░  ▓▓▓▓▒▒▓▓▒▒  ░░          
                              ░░██▓▓▒▒▓▓▓▓              
                              ░░▓▓▓▓░░▓▓▓▓░░            
                      ░░      ██▓▓▒▒░░▒▒▓▓██            
                      ▒▒▒▒▒▒▒▒▓▓██▓▓▓▓▓▓▓▓▓▓▒▒▒▒░░░░    
                      ░░░░░░░░██▓▓▒▒▒▒▒▒▒▒▓▓░░░░░░░░    
                        ░░░░▒▒▓▓  ▒▒  ▒▒▒▒▒▒▒▒░░░░      
                            ▓▓▓▓          ▓▓▓▓          
                          ░░▓▓▓▓██████▓▓▓▓▓▓▓▓▒▒        
                          ▓▓▓▓░░▓▓  ░░░░░░  ▓▓▓▓        
                              ▓▓▒▒░░  ▒▒▒▒▒▒            
                            ▓▓▓▓▒▒▒▒▓▓▒▒▓▓▓▓▓▓▒▒        
                          ▓▓▓▓▒▒▓▓▓▓▒▒▓▓▓▓▒▒▓▓▓▓▒▒      
                      ░░▓▓▓▓▓▓▒▒▒▒▓▓▓▓▓▓▒▒██▒▒▓▓░░      
                    ▒▒▓▓▓▓██▓▓▒▒░░░░░░░░░░████▒▒▓▓      
                    ▓▓████▓▓██░░░░▒▒▒▒░░░░████▓▓▓▓▒▒    
                ░░▓▓▓▓██▓▓██░░▓▓▒▒▒▒▒▒▒▒▒▒▓▓██▓▓▓▓▓▓    
                ▒▒▒▒▓▓      ▓▓▓▓▓▓▒▒▓▓▒▒▓▓▓▓████▓▓██    
                ░░▒▒      ▒▒▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒▒░░    
            ░░▒▒          ▓▓▓▓▓▓▓▓▓▓▓▓▒▒▓▓▓▓▓▓░░░░░░    
          ░░░░          ▒▒████████████████▓▓██▓▓        
        ▒▒░░            ██████████████████▓▓▓▓██░░      
      ▒▒░░              ▓▓██████████████████▓▓████      
  ░░░░░░                ▓▓▓▓██████████▓▓████▓▓▓▓██      
░░░░░░                ░░████▓▓██▓▓██▓▓▓▓██████▓▓▓▓▒▒    
▒▒░░                  ░░▓▓▓▓▓▓██████░░▓▓██████▓▓▓▓▓▓    
                        ▓▓▓▓▓▓██▓▓▓▓  ▒▒▓▓████▓▓▓▓▓▓    
                        ▒▒▓▓▓▓▓▓▓▓      ░░▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                      ▓▓▓▓▓▓▓▓▓▓            ░░▒▒▒▒▒▒░░  
██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▓▓▒▒▒▒░░▒▒▒▒▒▒████▒▒▒▒████▒▒▒▒
██▓▓▓▓▓▓▒▒▒▒▓▓██████████████████████████▓▓▓▓▓▓▓▓▓▓▓▓▓▓██
████████████████████████████████████████████████████████
"""
        else:
            enemy_sprite = r"""                                  __*       
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
         ~~~~~~~~~~~~~~<\\\)~~~~~(///>~~~~~~~~~~~~~ rp"""
        # High rank init:
        enemy_encounter_message = "A High Ranking Guard approaches!"
        enemy_object = Enemy("High Ranking Guard", 6, 20, 20, "Rusty Sword")
        battle_logic = BattleLogic('high_rank_guard', 'sfx/battle.ogg')
    if not mute_audio:
        s = pygame.mixer.Sound("sfx/encounter.ogg")
        empty_channel = pygame.mixer.find_channel()
        empty_channel.play(s)
    if not basic_graphics_enabled:
        print("\n████▒▒░ FIGHT! ░▒▒████\n")
    else:
        print("\n=======\n*FIGHT!*\n=======\n")
    time.sleep(1.1)
    print(enemy_encounter_message)
    time.sleep(1)
    print(enemy_sprite)
    time.sleep(1.5)
    audio_lockout = False  # This variable is used to stop the battle music from being restarted every time the fight_enemy function is called.
    fight_enemy(enemy_type, enemy_object, battle_logic, audio_lockout)


def before_juniper_fight():
    global expert_mode_enabled
    print("\nYou push on the door, and it creaks open. The loud squeal of the hinges makes you jump.")
    time.sleep(1.5)
    try:
        choice = int(input("\nProceed through the door? [1] Yes [2] No "))
        if choice == 1:
            print(
                "\nMustering up the courage, you fight the trembles and press on forward through the door, into the unknown...")
            time.sleep(5)
            print(
                "\nYou find yourself in a huge room. Stony walls stretch upwards to a mossy ceiling. Torches cast an eerie flickering glow around the room.")
            time.sleep(3)
            print("\nHuge stone pillars line the interior of this room, and ivy creeps up all of them.")
            time.sleep(3)
            print(
                "\nSuddenly, you freeze. In the center of this room is a raised section with a throne sitting proudly on top. On this throne, sits Emperor Juniper.")
            time.sleep(3.5)
            print(
                "\nHe's unlike anything you've seen up until this point. His hair is unkempt and wild. His beard is a mess and is full of knots.")
            time.sleep(3.5)
            print(
                "\nIn his hand he holds a samurai sword. His eyes dart around the room, dancing manically. He looks nothing like he used to; a shell of his former self.")
            time.sleep(3.5)
            print("\nA sickly grin adorns his face. You stand, mouth ajar, unsure what to think.")
            time.sleep(3.5)
            print(
                "\nSuddenly, his eyes lock onto you. His expression changes; what used to be a maniacal grin is now a foreboding frown.")
            time.sleep(3.5)
            print("\nHe lets out a startling yell and points at you. You feel nauseous and your legs feel weak.")
            time.sleep(3.5)
            print("\nSwiftly, he leaps to his feet and charges at you. This is it.")
            time.sleep(5)
            encounter_enemy('juniper')
        else:
            print("\nNot quite ready to press on just yet, you evaluate your other options.")
            time.sleep(1.5)
            chapter_8_choice()
    except ValueError:
        before_juniper_fight()


def chapter_8_choice():
    global searchedChest8
    try:
        choice = int(input("\nWhat will you do? [1] to examine the door, [2] to search the chest. "))
        if choice == 1:
            print("\nYou wander over to the door. Your heart sinks. You have a feeling that whatever lies behind this door is serious.")
            time.sleep(1.5)
            before_juniper_fight()
        elif choice == 2 and searchedChest8 is True:
            print("\nThis chest has already been searched, and there is no loot remaining.")
            time.sleep(1.5)
            chapter_8_choice()
        else:
            print("\nYou wander over to the chest.")
            time.sleep(1.5)
            chest8()
    except ValueError:
        chapter_8_choice()


def start_chapter_8():
    time.sleep(0.5)
    global basic_graphics_enabled, diedToJuniper, playerMaxHealth, healingPotion, healingpotionQuantity
    if not basic_graphics_enabled:
        try:
            print("\n█▒░ Chapter Eight: Finale ░▒█")
        except Exception:
            print("\n== Chapter Eight: Finale ==")
    else:
        print("\n== Chapter Eight: Finale ==")
    if mute_audio != True:
        pygame.mixer.music.load("sfx/thud.ogg")
        pygame.mixer.music.play(1)
    time.sleep(3)
    print("\nAfter what feels like an age of walking, you freeze.")
    time.sleep(1.5)
    print(
        "\nA huge wooden door looms above you. Torches either side cast an eerie flickering glow over the area around you.")
    time.sleep(1.5)
    print("\nYou peer around, taking in this new morbid environment. You notice a chest to the left side of the door.")
    time.sleep(1.5)
    if not diedToJuniper:
        chapter_8_choice()
    else:
        diedToJuniper = False
        print(
            "\nYou also notice something glimmering on the floor in the middle of the room, something that wasn't there before...")
        time.sleep(1.5)
        print("\nYou make your way over to the shiny object, before stooping to get a closer look.")
        time.sleep(1.5)
        if player.get_health() == 20:
            discover_healing_potion_amount = 5
        else:
            discover_healing_potion_amount = 4
        # discover_healing_potion_amount = discover_healing_potion_amount - player.get_inventory_items()
        if discover_healing_potion_amount <= 0:
            print(
                "\nThe shiny object appears to be an empty vail, which looks to have previously contained a substance of some sort.")
            time.sleep(1)
            print("\nThis item is of no use, and so you leave it be.")
            time.sleep(3)
            chapter_8_choice()
        else:
            print("\n" + str(
                discover_healing_potion_amount) + " vials of a substance lay on the ground. They appear to contain a Potion of Healing.")
            time.sleep(1.5)
            print("\nYou pocket them, certain they'll come in handy...")
            time.sleep(3)
            player.update_inventory('healing potion', discover_healing_potion_amount)
            chapter_8_choice()


def chapter_7_continue_choice():
    global player, expert_mode_enabled
    print("\nYou gaze down the long, dark corridor that lays ahead of you. A familiar feeling of terror hangs over you.")
    time.sleep(1.5)
    try:
        choice = int(input("\nAre you ready to proceed? You can't return to this area later.\n1] Yes\n2] No\n--> "))
        if choice == 1:
            print("\nYou proceed onwards, into the unknown...")
            time.sleep(1)
            player.set_save_location(7)
            if not expert_mode_enabled:
                ask_save()
            else:
                start_chapter_8()
        elif choice == 2:
            print("\nNot quite finished here just yet, you backtrack to the area where the paths originally split.")
            chapter_7_split()
        else:
            invalid_selection_message()
            chapter_7_continue_choice()
    except ValueError:
        chapter_7_continue_choice()


def chest7():
    global single_use_items
    try:
        choice = int(input("\nYou refocus your attention to the chest in the corner. Would you like to search it [1], or ignore it [2]? "))
        if choice == 1:
            if search_chest('Healing Potion'):
                single_use_items.append('chapter_7_chest_2')
                print("\nYou return to the previous area where the paths split.")
                time.sleep(1.5)
                chapter_7_split()
            else:
                chapter_7_split()
        else:
            print("\nYou elect not to search the chest.")
            chapter_7_split()
    except ValueError:
        print("\nPlease choose a valid option.")
        chest7()


def chapter_7_chest():
    global single_use_items
    if 'chapter_7_key' not in single_use_items:
        if search_chest('Key'):
            single_use_items.append("chapter_7_key")
            chapter_7_continue_choice()
        else:
            print("\nYou do not take the Key.")
            chapter_7_continue_choice()
    else:
        print("\nThis chest has already been searched, and there is no loot remaining.")
        chapter_7_continue_choice()


def chapter_7_split():
    global enemies_defeated, enemy_ID, single_use_items, player
    try:
        choice = int(input("\nYou are standing at a fork in the path forward; you can either go left [1] or right [2] "))
        if choice == 1 and 7 not in enemies_defeated:
            print(
                "\nYou head left! As you trudge down the blinding corridor, you begin to see a faint figure in the distance... It's a guard!")
            time.sleep(1.5)
            print(
                "\nYou turn to run, but it's too late! The pounding of heavy boots reverberates around you, and you feel a hand on your shoulder...")
            time.sleep(0.8)
            enemy_ID = 7
            encounter_enemy('guard')
        elif choice == 1 and 7 in enemies_defeated:
            print("\nYou go left once again. The guard still lays defeated on the floor. You step over him.")
            time.sleep(1.5)
            print(
                "\nYou proceed down the corridor, and eventually come to a door. You push it, and it effortlessly glides open.")
            time.sleep(1.5)
            print("\nBehind this door is a chest, along with a corridor that leads off into the distance.")
            time.sleep(1.5)
            print(
                "\nThis corridor is a complete departure from the area you're in now; the walls are stony once again, and water drips from the ceiling.")
            time.sleep(1.5)
            print("\nThere is also no light at all. You shudder. This corridor gives off an extremely unnerving vibe.")
            chapter_7_chest()
        elif choice == 2 and 'chapter_7_key' in single_use_items:
            print("\nYou head right! As you round a corner, you come to a thick-looking metal door.")
            time.sleep(1.5)
            print("\nYou push on it, but as expected, it doesnt budge.")
            time.sleep(1.5)
            print("\nSuddenly, you remember the key you found in the chest! You raise the key to the door and turn it...")
            time.sleep(1.5)
            print("\n... And... Success! The door unlocks.")
            time.sleep(1.5)
            print(
                "\nBehind the door, you find a small room with a chest in one corner. A loaf of bread also sits on the floor. It's a little mouldy, but\nit's food. You eat it.")
            time.sleep(1.5)
            print("\nHealth has been fully restored!")
            player.restore_health()
            chest7()
        else:
            print("\nYou head right! As you round a corner, you come to a thick-looking metal door.")
            time.sleep(1.5)
            print("\nYou push on it, but as expected, it doesnt budge at all. Could the key be nearby?")
            time.sleep(1.5)
            print("\nOut of ideas for now, you return to the previous area where the paths split.")
            time.sleep(1.5)
            single_use_items.append('chapter_7_door')
            chapter_7_split()
    except ValueError:
        chapter_7_split()


def chapter_7_start():
    global basic_graphics_enabled
    time.sleep(1)
    if not basic_graphics_enabled:
        try:
            print("\n█▒░ Chapter Seven: With Great Power ░▒█")
        except Exception:
            print("\n== Chapter Seven: With Great Power ==")
    else:
        print("\n== Chapter Seven: With Great Power ==")
    if mute_audio != True:
        pygame.mixer.music.load("sfx/thud.ogg")
        pygame.mixer.music.play(1)
    time.sleep(3)
    print(
        "\nThe environment around you begins to fade into existence as your pupils contract. You're in a long corridor. The walls are smooth and painted white.")
    time.sleep(1.5)
    print(
        "\nThis place is unlike any you have been in a long time. You actually have to do a double take to ensure you haven't just imagined it.")
    time.sleep(1.5)
    print("\nCautiously, you trudge down the sterile white corridor, your footsteps echoing off of the plain walls.")
    time.sleep(1.5)
    chapter_7_split()


def chapter_6_puzzle_solved():
    global puzzleComplete, lockout
    time.sleep(1)
    print("*THUNK!*")
    time.sleep(1.5)
    print("\nThe sound makes you jump. It seemed to come from the door at the end of the room.")
    time.sleep(1.5)
    puzzleComplete = True
    lockout = True
    chapter_6_choice()


def chapter_6_right_dial_interaction():
    global rightDialPos, rightDialCorrect
    print(
        "\nThe right dial is currently pointing " + rightDialPos + " Which direction shall you turn it?\n1] Left\n2] Right\n3] Up\n4] Down\n5] Cancel")
    try:
        choice = int(input("--> "))
    except ValueError:
        chapter_6_right_dial_interaction()
    if choice == 1:
        print("The dial is now facing left!")
        rightDialPos = str("left.")
        chapter_6_choose_dial()
    elif choice == 2:
        print("The dial is now facing right!")
        rightDialPos = str("right.")
        rightDialCorrect = True
        chapter_6_choose_dial()
    elif choice == 3:
        print("The dial is now facing up, towards the door!")
        rightDialPos = str("up, towards the door.")
        chapter_6_choose_dial()
    elif choice == 4:
        print("The dial is now facing down, towards you!")
        rightDialPos = str("down, towards you.")
        chapter_6_choose_dial()
    else:
        chapter_6_choose_dial()


def chapter_6_left_dial_interaction():
    global leftDialPos, leftDialCorrect
    print(
        "\nThe left dial is currently pointing " + leftDialPos + " Which direction shall you turn it?\n1] Left\n2] Right\n3] Up\n4] Down\n5] Cancel")
    try:
        choice = int(input("--> "))
    except ValueError:
        chapter_6_left_dial_interaction()
    if choice == 1:
        print("The dial is now facing left!")
        leftDialPos = str("left.")
        leftDialCorrect = True
        chapter_6_choose_dial()
    elif choice == 2:
        print("The dial is now facing right!")
        leftDialPos = str("right.")
        chapter_6_choose_dial()
    elif choice == 3:
        print("The dial is now facing up, towards the door!")
        leftDialPos = str("up, towards the door.")
        chapter_6_choose_dial()
    elif choice == 4:
        print("The dial is now facing down, towards you!")
        leftDialPos = str("down, towards you.")
        chapter_6_choose_dial()
    else:
        chapter_6_choose_dial()


def chapter_6_choose_dial():
    if leftDialCorrect is True and rightDialCorrect is True and leverPulled is True and lockout is False:
        chapter_6_puzzle_solved()
    try:
        choice = int(input("Interact with the left dial [1] or the right dial [2], or leave them where they are [3]? "))
    except ValueError:
        chapter_6_choose_dial()
    if choice == 1:
        chapter_6_left_dial_interaction()
    elif choice == 2:
        chapter_6_right_dial_interaction()
    else:
        chapter_6_choice()


def chapter_6_inspect_dials():
    global dialogCount, leverPulled
    if dialogCount == 0:
        print(
            "\nYou examine the contraption that stands before you! Both dials have an arrow engraved into them, and appear to be able to rotate.")
        time.sleep(1.5)
        print(
            "\nYou wonder if this is some sort of combination lock. If you could just figure out the right combination...")
        time.sleep(2)
        print(
            "\nSuddenly, you think back to the cryptic message engraved into the base of the fountain:\n'Only when the light and the darkness is revealed will the path forward present itself.'")
        time.sleep(2)
        print("\nDoes this have anything to do with the task at hand?")
        time.sleep(2)
        if leverPulled:
            print("\nFurthermore, do the lit torches on the left wall have anything to do with this?")
        dialogCount = 1
        chapter_6_inspect_dials()
    else:
        time.sleep(1)
        try:
            choice = int(input("\nWill you interact with the dials? ([1] = yes, [2] = no) "))
        except ValueError:
            chapter_6_inspect_dials()
        if choice == 1:
            chapter_6_choose_dial()
        else:
            print("\nYou do not interact with the dials.")
            time.sleep(0.3)
            chapter_6_choice()


def chapter_6_lever_noticed():
    global leverPulled
    time.sleep(2)
    if leverPulled is False:
        try:
            choice = int(input(
                "\nYou pace over to the lever and trace your hands over the cold metal rod. It's currently pointing upwards. Pull it down? ([1] = yes, [2] = no) "))
        except ValueError:
            chapter_6_lever_noticed()
        if choice == 1:
            print("\nYou pull the lever down! You hear a hushed thud, then... nothing.")
            time.sleep(1.5)
            print(
                "\nJust as you begin to evaluate other options, you notice a flickering light from the other side of the room. The torches that line the left wall are slowly\nflickering to life!")
            time.sleep(2)
            print("\nYou wander back over to the center of the room.")
            leverPulled = True
            chapter_6_choice()
        else:
            print("\nYou decide against pulling the lever, and wander back to the center of the room")
            time.sleep(1)
            chapter_6_choice()
    else:
        print(
            "\nYou stand and ponder. When you pulled the lever, the torches to your left activated. Does this have something to do with the mechanism in the center\nof the room?")
        time.sleep(2)
        chapter_6_choice()


def chapter_6_choice():
    global leverPulled, leftDialCorrect, rightDialCorrect, puzzleComplete, player, expert_mode_enabled
    if leftDialCorrect is True and rightDialCorrect is True and leverPulled is True and lockout is False:
        chapter_6_puzzle_solved()
    try:
        choice = int(input(
            "\nIt's your call! Will you inspect the room further [1], examine the door [2], or examine the contraption [3]? "))
    except ValueError:
        chapter_6_choice()
    if choice == 1:
        print("\nYou glance around the room, looking for anything that may aid you.")
        time.sleep(1.5)
        print(
            "\nTorches line the walls either side of you, however none of these are lit; the chandelier is the only source of light.")
        time.sleep(1.5)
        print(
            "\nYou notice a handle on the wall, with a long rope extending up to the chandelier- this must control it's height.")
        time.sleep(1.5)
        print("\nYou also notice an unmarked lever on the wall to your right.")
        chapter_6_lever_noticed()
    elif choice == 2 and puzzleComplete is False:
        print(
            "\nYou wander over to the door! From a distance it looked sturdy, but up close it only looks even more impenetrable.")
        time.sleep(1.5)
        print(
            "\nYou extend your arm and brush your hand over the cold metal door. You push it out of curiosity, but unsurprisingly, it's locked.")
        time.sleep(1.5)
        print(
            "\nYou realize that the only way through here is by figuring out how to unlock the door. There's no keyhole, so there has to be some sort of\nmechanism keeping it closed.")
        time.sleep(1.5)
        print("\nOut of ideas for now, you head back over to the center of the room.")
        chapter_6_choice()
    elif choice == 2 and puzzleComplete is True:
        print("\nYou wander back over to the door! Tentatively, you extend your arm and once again push on the door...")
        time.sleep(2)
        print("\nAnd... success! The door pushes open. Breathing a sigh of relief, you swing the door fully open.")
        time.sleep(1.5)
        print("\nThe corridor that lays ahead is totally different to the room you were just in, as it's super bright.")
        time.sleep(1.5)
        print(
            "\nA blinding light pours out from the newly revealed path. Squinting, you wait for your eyes to re-adjust.")
        time.sleep(1.5)
        print("\nShielding your eyes, you step forward, into the light...")
        time.sleep(1.5)
        player.set_save_location(6)
        if not expert_mode_enabled:
            ask_save()
        else:
            chapter_7_start()
    elif choice == 3:
        chapter_6_inspect_dials()


def chapter_6_start():
    global expert_mode_enabled, player, basic_graphics_enabled
    time.sleep(1)
    if not basic_graphics_enabled:
        try:
            print("\n█▒░ Chapter Six: A Puzzle In Darkness ░▒█")
        except Exception:
            print("\n== Chapter Six: A Puzzle In Darkness ==")
    else:
        print("\n== Chapter Six: A Puzzle In Darkness ==")
    if mute_audio != True:
        pygame.mixer.music.load("sfx/thud.ogg")
        pygame.mixer.music.play(1)
    time.sleep(3)
    print("\nTrudging along the desolate hallway, you feel an odd sense of mundanity coming on. ")
    time.sleep(1.5)
    print(
        "\nThis place used to terrify you, and whilst it very much still does, you begin to feel a huge increase in your determination.")
    time.sleep(1.5)
    print(
        "\nAfter some more walking, you come to a door. Apprehensively, you push it open. What could possibly lie on the other side?")
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
    player.restore_health()
    time.sleep(2.5)
    print("\nHaving revitalised yourself, you peer around, examining this new enemy_ID.")
    time.sleep(1.5)
    print("\nThe surrounding area is extremely dark. You squint, waiting for your eyes to adjust.")
    time.sleep(1.5)
    print(
        "\nThis room is massive; stone pillars stretch upwards towards an intricate arched ceiling. A large chandelier hangs, but is not lit.")
    time.sleep(1.5)
    print(
        "\nOn the other side of the room lies a door, however it's unlike anything you've seen so far. It's also huge, but is made entirely of metal.")
    time.sleep(1.5)
    print("\nThe room is barren, save for a short pillar situated in the middle. A torn red carpet lines the floor.")
    time.sleep(3)
    print(
        "\nYou make your way over to the pedestal in the middle of the room. It's some sort of contraption; two dials occupy the top.")
    time.sleep(1.5)
    chapter_6_choice()


def courtyard_guard_defeated():
    print("\nThe guard lays defeated on the floor. Figuring he may have had another guard with him, you scurry back up the path you came from.")
    courtyard()


def chapter_5_return_courtyard():
    global enemies_defeated, enemy_ID
    try:
        choice = int(input(
            "\nThere must be a way forward! Will you turn around and explore the garden some more [1], or try to force the door open [2]? "))
        if choice == 1:
            courtyard()
        else:
            print(
                "\nYou decide to force the door open! Gathering up your little remaining strength, you take a few paces back...")
            time.sleep(1)
            print("\nYou dart towards the door!")
            time.sleep(1.5)
            print("\n*THUD!*")
            time.sleep(1)
            print("\nYou lie dazed on the floor. The door is still firmly shut. You curse and get back to your feet.")
            time.sleep(1)
            print("\nOut of ideas for now, you decide to head back to the main area to explore further.")
            enemies_defeated.append(enemy_ID)
            courtyard()
    except ValueError:
        invalid_selection_message()
        chapter_5_return_courtyard()


def chapter_5_leave_courtyard():
    global single_use_items, player, expert_mode_enabled
    choice = int(input(
        "\nAfter some walking, you reach a door which appears to lead back inside the dungeon. Enter [1], or continue to explore the courtyard [2]? "))
    if choice == 1:
        print(
            "\nYou head on over to the door! It's made of solid metal; grey paint flakes off with age. It looks oddly out of place.")
        time.sleep(1.5)
        print("\nYou push firmly... but it won't budge! There is a large keyhole halfway down the door.")
        time.sleep(1.5)
        if 'courtyard_key' in single_use_items:
            print(
                "\nSuddenly you remember; the key you found in the fountain! Hastily, you draw the key from your pocket and insert it into the keyhole...")
            time.sleep(1.5)
            print("\nAnd it turns! With a dull click, the door is unlocked.")
            time.sleep(1.5)
            print(
                "\nA strong, musty smell emanates from the newly revealed passageway. The pathway ahead is pitch black.")
            time.sleep(1.5)
            print("\nBreathing a sigh of relief, you nervously press on forward, into the depths of the unknown...")
            time.sleep(3)
            player.set_save_location(5)
            if not expert_mode_enabled:
                ask_save()
            else:
                chapter_6_start()
        else:
            chapter_5_return_courtyard()
    else:
        print("\nYou turn around, heading back towards the fountain.")
        time.sleep(1)
        courtyard()


def courtyard():
    global enemy_ID, courtyardKey, foundCourtyardDoor, enemies_defeated, single_use_items
    choice_message = "\nYou return to the fountain where the paths split. Do you head down the other path [1] or examine your surroundings [2]? "
    if enemy_ID not in enemies_defeated:
        choice_message = "\nYou step towards the fountain. You can either follow the path left [1] or right [2]. Which way will you go? "
    try:
        choice = int(input(choice_message))
        if choice == 1:
            if enemy_ID not in enemies_defeated:
                print("\nYou head left! Uncertain, you follow the winding path through the thick overgrown bushes.")
                time.sleep(1.8)
                print("\nAs you progress, you begin to hear a faint sound. It sounds like... whistling?")
                time.sleep(1.8)
                print("\nYou carry on, eagerly listening out. The sound only grows louder as you head down the path.")
                time.sleep(1.8)
                print(
                "\nAt first you thought your ears were deceiving you, but now you're certain; this isn't the sound of a bird, but rather of a person.")
                time.sleep(1.8)
                print(
                "\nAbruptly, the path ends. You observe your surroundings and freeze. A stone bench lays a few metres ahead. Here, a guard is sat with his back turned to you.")
                time.sleep(1.8)
                print(
                "\nYou begin to back away. If you can just make it out of the guard's general whereabouts you might be able to slip away...")
                time.sleep(1.8)
                print(
                "\nYour heart sinks as the guard turns his head... and makes eye contact with you. With a startled yell, he picks up his weapon and approaches...")
                time.sleep(3)
                enemy_ID = 6
                encounter_enemy('guard')
            else:
                print("\nYou head down the other path! ")
                time.sleep(0.9)
                chapter_5_leave_courtyard()
        elif choice == 2:
            if enemy_ID not in enemies_defeated:
                print("\nYou go right! Hesitantly, you stick to the path through the overgrown gardens.")
                time.sleep(0.9)
                chapter_5_leave_courtyard()
            elif enemy_ID in enemies_defeated and 'courtyard_key' in single_use_items:
                print(
                    "\nYou once again observe your surroundings... certain nothing is left to be discovered, you focus your attention back to your next move.")
                courtyard()
            else:
                print("\nYou peer around, wondering when this place was last used. ")
                time.sleep(0.9)
                print(
                    "\nBut wait! Out of the corner of your eye, at the base of the fountain, you think you see something gleaming.")
                time.sleep(0.9)
                print("\nYou inch closer, and begin to rummage through the thick undergrowth...")
                time.sleep(1.2)
                print("\n...And you unearth a key! You pocket it, certain it'll come in handy later.")
                single_use_items.append('courtyard_key')
                time.sleep(1.5)
                print(
                    "\nYou also notice something engraved into the stone of the fountain. It's a little hard to read, but it says: 'Only when \nthe light and the darkness is revealed will the path forward present itself.'")
                time.sleep(1)
                print("\n...")
                time.sleep(1)
                print("\nWhat could that possibly mean?")
                courtyard()
        else:
            invalid_selection_message()
    except ValueError:
        courtyard()


def chapter_5_corridor():
    choice = int(input("Do you head left [1], or venture right instead [2]? Both passages look the same. "))
    if choice == 1:
        print("\nYou decide to go left!")
        time.sleep(0.7)
        chapter_5_chest()
    elif choice == 2:
        print("\nYou head right! As you head down the stony corridor, you begin to hear something...")
        time.sleep(0.7)
        print("\nThe rustling of leaves... birds chirping... but that means...")
        time.sleep(0.7)
        print(
            "\n...You must be heading outside! Excitedly, you feel your spirits lift and you pick up the pace. Could this be your ticket out of here?\n")
        time.sleep(0.7)
        print(
            "Nearing the end of the corridor, you can see daylight creeping around a corner, and you feel a soft breeze against your face.\n")
        time.sleep(0.7)
        print("Cautiously, you near the end of the corridor and take a peek around the corner...")
        time.sleep(1.3)
        print(
            "\nYou are greeted by an overgrown courtyard! Huge trees tower above you, with ivy creeping up the trunks. Cracked stone tiles \nline the floors with weeds")
        time.sleep(0.5)
        print(
            "snaking up from between the cracks. In the middle of the garden, a crumbling fountain stands covered in ivy and moss. Two paths branch \naround the fountain, heading")
        time.sleep(0.5)
        print(
            "deeper into the garden in each direction. A large, crumbling stone wall lines the perimeter of the enemy_ID.")
        time.sleep(2.5)
        print(
            "\nConfident that there are no guards lurking, you take a step out into the abandoned garden. You take a gulp of breath air; \nwhich only seems to re-invigorate you further.")
        courtyard()


def chapter_5_start():
    global basic_graphics_enabled, enemy_ID
    time.sleep(3)
    enemy_ID = 6
    if not basic_graphics_enabled:
        try:
            print("\n█▒░ Chapter Five: A Breath Of Fresh Air ░▒█")
        except Exception:
            print("\n== Chapter Five: A Breath Of Fresh Air ==")
    else:
        print("\n== Chapter Five: A Breath Of Fresh Air ==")
    if mute_audio != True:
        pygame.mixer.music.load("sfx/thud.ogg")
        pygame.mixer.music.play(1)
    time.sleep(3)
    print("\nClambering down the steep spiral steps, you can feel that familiar sense of dread coming on once again.\n")
    time.sleep(2)
    print(
        "After what feels like an eternity of descending the depressing stairwell, you finally reach a small archway at the bottom.\n")
    time.sleep(1.3)
    print("Hesitantly, you peer around the mossy doorway and deduce that nobody is on the other side.")
    time.sleep(1.4)
    print(
        "\nYou silently slip through the opening, and observe your surroundings; you're stood in a long corridor, with two branching paths to your left and right.\n")
    chapter_5_corridor()


def chapter_4_find_exit():
    global player, expert_mode_enabled
    try:
        choice = int(
            input("\nYou must find a way forwards! [1] To continue up the corridor, [2] to return back to the closet."))
        if choice == 1:
            chapter_4_discover_chest()
        elif choice == 2:
            print("\nYou backtrack towards the closet at the end of the corridor! ")
            time.sleep(1.2)
            print("\nAs you approach the entrance to the closet, you step inside in order to get a better view of things.")
            time.sleep(1.2)
            print(
                "\nUpon stepping into the closet, you immediately notice something you hadn't before; a thick, wooden trapdoor protruding slightly above a pile of debris on the floor!")
            time.sleep(2)
            print("\nTensely, you kick aside the rubble on the floor...")
            time.sleep(1.2)
            print(
                "\nOnly to discover a heavy iron padlock keeping the trapdoor strongly wedged shut. You groan, only to remember the key you previously acquired!")
            time.sleep(1.3)
            print("\nNervously, you crouch down and insert the key into the padlock. You begin to turn the key...")
            time.sleep(2)
            print("\n*CLUNK!*")
            time.sleep(2)
            print("\nPhew! You take a deep breath as the lock releases it's grip on the trapdoor")
            time.sleep(1.2)
            print(
                "\nAs soon as you begin to lift the rotten trapdoor, the first thing you notice is a strong, musty odour emanating from the pit in the stony floor")
            time.sleep(2)
            print(
                "\nFighting the odour, you push the trapdoor open, revealing a narrow, spiral staircase leading down. With no other options, you begin to descend...")
            player.set_save_location(4)
            if not expert_mode_enabled:
                ask_save()
            else:
                chapter_5_start()
        else:
            raise ValueError
    except ValueError:
        invalid_selection_message()
        chapter_4_find_exit()


def chapter_4_high_rank_defeated():
    global single_use_items, expert_mode_enabled
    global player
    time.sleep(2)
    print("\nYou have overcome the challenge and defeated the High Ranking guard!")
    time.sleep(1.3)
    print("\nAs you gaze upon his body on the floor, you think you see something glimmer beside him")
    time.sleep(1.2)
    print(
        "\nCautiously, you glance down to where you think you saw the shimmer, only to discover a large, silver key laying beside the guard! He must have dropped it when he fell!")
    time.sleep(1.2)
    if 'chapter_4_padlock' in single_use_items:
        print(
            "\nWith shaking hands, you pick up the key dropped by the guard. Could this be the key needed to unlock the trapdoor and forge yet another path onward?")
        time.sleep(2)
        print("\nYou scurry back along the corridor, and return to the room with the trapdoor.")
        time.sleep(2)
        print("\nNervously, you crouch down and insert the key into the padlock. You begin to turn the key...")
        time.sleep(2)
        print("\n*CLUNK!*")
        time.sleep(2)
        print("\nPhew! You take a deep breath as the lock releases it's grip on the trapdoor.")
        time.sleep(2)
        print(
            "\nAs soon as you begin to lift the rotten trapdoor, the first thing you notice is a strong, musty odour emanating from the pit in the stony floor.")
        time.sleep(2)
        print(
            "\nFighting the odour, you push the trapdoor open, revealing a narrow, spiral staircase leading down. With no other options, you begin to descend...")
        player.set_save_location(4)
        if not expert_mode_enabled:
            ask_save()
        else:
            chapter_5_start()
    else:
        print("\nWith shaking hands, you pick up the key and pocket it. It may end up coming in handy...")
        chapter_4_find_exit()


def chest2():
    global single_use_items
    try:
        choice = int(input("\nAll hope is not lost, however. In the corner of the room, you spot a decrepit wooden chest. Search it? ([1] Yes, [2] No) "))
        if choice == 1 and 'chest_2' not in single_use_items:
            if search_chest("Healing Potion"):
                single_use_items.append('chest_2')
                closet()
            else:
                print("\nYou decide not to take the Potion of Healing, and return to the previous area.")
                closet()
        elif choice == 2:
            print("\nYou chose not to search the chest.")
            closet()
        elif choice == 1 and 'chest_2' in single_use_items:
            print("\nThis chest has already been searched, and there is no loot remaining.")
            closet()
        else:
            print("\nPlease select a valid option.")
            chest2()
    except ValueError:
        chest2()


def pre_high_rank_fight():
    global enemy_ID
    time.sleep(1)
    try:
        choice = int(input("\nDo you attempt to take on the guard [1]? Or return to the previous area in the hopes you'll find something to aid you in the battle [2]? "))
    except ValueError:
        print("\nOnly integers can be entered here!")
        pre_high_rank_fight()
    if choice == 1:
        print("\nYou approach the menacing-looking guard, ready for combat...")
        enemy_ID = 4
        encounter_enemy('high_rank_guard')
    elif choice == 2:
        print(
            "\nQuietly, you steal back up the corridor you just came down, in the hopes of finding something useful...")
        closet()
    else:
        print("\nI don't understand.")
        pre_high_rank_fight()


def closet():
    global single_use_items
    try:
        choice = int(input(
            "\nDo you inspect the empty room further [1], or backtrack and try to find a different path forward [2]? "))
    except ValueError:
        print("\nBad input. Only an integer can be entered here!")
        closet()
    if choice == 1:
        print(
            "\nYou decide to inspect the room further, stepping inside to get a better view. You scan every surface of the room, and find nothing.")
        time.sleep(1)
        print(
            "\nJust as you're about to give up hope, you notice a rotting wooden trapdoor beneath a pile of rubble on the floor. Tentatively, you kick the rubble away in order to get a closer look...\n")
        time.sleep(1)
        print(
            "...Only to discover it's being held firmly shut with a rusty iron padlock. You curse, then scramble to your feet. There must be another path forward!")
        time.sleep(1)
        single_use_items.append('chapter_4_padlock')
        chest2()
    elif choice == 2:
        print(
            "\nYou decide to backtrack, in order to find another path forward. As you begin to retrace your steps around the corner of the \nnarrow corridor, you hear footsteps.")
        time.sleep(1)
        print("\nYou stand in terror, as the horrifying reality dawn on you; you're not alone down here.")
        time.sleep(1)
        print(
            "\nYou decide to peer your head around the corner in order to see who you might be up against. You spot a guard, pacing around menacingly.")
        time.sleep(1.3)
        print(
            "\nBut, wait... something seems different about this guard. He almost seems... stronger... more menacing...")
        pre_high_rank_fight()
    else:
        print("\nI don't understand.")
        closet()


def chapter_4_discover_door():
    global single_use_items
    print(
        "After a few minutes of advancing down the dim corridor, you reach what appears to be a blockade; a thick, rusty iron door looms above you.")
    time.sleep(1)
    print(
        "\nThis door looks too strong to be able to force open, besides, any loud noise could alert any nearby guards to your presence!")
    time.sleep(1)
    if 'chapter_4_key' not in single_use_items and 'chapter_4_door' not in single_use_items:
        print(
            "\nA tiny keyhole situated in the middle of the huge door is the only point light from the other side seeps through. Perhaps if \nyou could find the key, you'd be able to slip through unnoticed...")
        single_use_items.append('chapter_4_door')
        time.sleep(1.2)
        print("\nOut of ideas for now, you head back up the corridor, back to the previous enemy_ID.\n")
        chapter_4_split()
    elif 'chapter_4_key' not in single_use_items and 'chapter_4_door' in single_use_items:
        print("\nThat keyhole must be the path forward! Maybe if you carry on searching, you'll find something...")
        time.sleep(1)
        print("\nOut of ideas, you head back up the corridor, back to the previous area.\n")
        chapter_4_split()
    elif 'chapter_4_key' in single_use_items:
        print("\nSuddenly, you remember; the key from the chest you've just looted! Hand shaking in anticipation, you raise they key to the lock and turn...")
        time.sleep(1.5)
        print("\n*CLICK!*")
        time.sleep(1)
        print(
            "\nPhew! You gasp a sigh of relief as you hear the thud of the lock releasing it's grasp. Tentatively, you begin to shove the door open. \nA feeling of dread comes over you. What could possibly lurk on the other side...")
        time.sleep(2)
        print("\nUpon pushing open the door, your heart sinks. There's nothing but an empty closet on the other side!")
        time.sleep(1)
        print("\nYou cry out in frustration. There must be another way!")
        time.sleep(2)
        closet()
    else:
        print("\nPlease select a valid option.")
        chapter_4_discover_door()


def chapter_4_discover_chest():
    global player, single_use_items, expert_mode_enabled
    if 'chapter_4_key' in single_use_items:
        print("\nThis chest has already been searched, and there is no loot remaining. Disappointed, you  return back to the previous area. \n")
        chapter_4_split()
    if search_chest('key'):
        single_use_items.append('chapter_4_key')
        print("\nYou pocket the key hastily, as something else in the chest catches your eye...")
        time.sleep(1)
        print("\nYou also reveal a stale loaf of bread. Starving, you gulp it down without a second thought.")
        player.restore_health()
        time.sleep(1.5)
        print(
            "\nSatisfied you've collected all of the items that may become useful, you close the chest and return to the previous area at the bottom of the stairs.\n")
        chapter_4_split()
    else:
        print("\nYou did not search the chest. You swiftly head back up the corridor you just came down. \n")
        chapter_4_split()


def chapter_4_split():
    time.sleep(1.2)
    choice = 0
    try:
        choice = int(input(
            "You reach the bottom of the stairs, and are met with two paths forward. You can either go left [1], or right [2]. Both \npassages look the same. "))
    except ValueError:
        print("\nBad input; only integers can be entered!")
        chapter_4_split()
    if choice == 1:
        print(
            "\nYou turn left! You hesitantly walk down the ominous corridor, a few flickering torches on the wall your only source of light.")
        time.sleep(1.3)
        print("\nEventually, you reach the end of the corridor. A lone wooden chest lays forlorn and forgotten in a corner.")
        chapter_4_discover_chest()
    elif choice == 2:
        print("\nYou head right! Heart racing, you tread cautiously down the dingy corridor.\n")
        time.sleep(1.3)
        chapter_4_discover_door()
    else:
        chapter_4_split()


def chapter_4_start():
    global savePoint, mute_audio, basic_graphics_enabled
    if not basic_graphics_enabled:
        try:
            print("\n█▒░ Chapter Four: What Doesn't Kill You Makes You Stronger ░▒█")
        except Exception:
            print("\n== Chapter Four: What Doesn't Kill You Makes You Stronger ==")
    else:
        print("\n== Chapter Four: What Doesn't Kill You Makes You Stronger ==")
    if not mute_audio:
        pygame.mixer.music.load("sfx/thud.ogg")
        pygame.mixer.music.play(1)
    time.sleep(3)
    print(
        "\n\nUpon re-entering, you are hit with an immense feeling of dread. Why are you doing this? Are you really willing to risk \nyour life for a load of strangers?")
    print(" ")
    time.sleep(2)
    print(
        "Slowly regaining courage, you look around. You are met with a stony staircase leading down, to what you presume to be back into the dungeon. ")
    time.sleep(1.2)
    print("\nYou begin to descend the staircase, your footsteps reverberating off of the mossy stone walls.\n")
    time.sleep(1.2)
    chapter_4_split()


def balcony():
    global player, expert_mode_enabled, single_use_items
    print("\nYou get to the door, and without thinking, fling yourself outside...")
    time.sleep(3)
    print(
        "\nYou find yourself on a precarious balcony! The floor is made of rotting wood, and there's a sheer drop below. Looking around gives you a \nclear view of all the guards circling the perimeter of the building.")
    time.sleep(3)
    print("\nYou notice another balcony below you, which looks equally dangerous.")
    time.sleep(3)
    if 'chapter_3_rope' in single_use_items:
        print(
            "\nThinking fast, you remember the rope you picked up earlier. Maybe you could use this to get to the lower balcony?")
        time.sleep(3)
        print(
            "\nHurriedly, you tie the rope around the balcony's railing, and inhale deeply. This has been your first time outdoors in ages. And it could well be \nyour last...")
        time.sleep(3)
        print(
            "\nFiguring you'd rather die this way than to the hands of those guards, you grab hold of the rope, and begin to clamber over the railing.")
        time.sleep(3)
        print(
            "\nAs the wind ruffles through your unkempt hair, you try your hardest not to look down at the drop that would lead to certain death below...")
        time.sleep(3)
        print(
            "\nSuddenly, you feel a jolt through the rope. You look up and see a guard attempting to cut through the rope with a switchblade! Panicking, you \nbegin to climb down the rope faster...")
        time.sleep(3)
        print(
            "\nSuddenly, you hear a triumphant yell from above as you begin to plummet. That guard managed to cut through the rope! This is it. The \nend... you shut your eyes and brace for impact.")
        time.sleep(3)
        print("\n*THUD!*")
        time.sleep(3)
        print("...")
        time.sleep(3)
        print("   ...")
        time.sleep(3)
        print("      ...")
        time.sleep(3)
        print("\nYou slowly come to. Your head aches, and your bones all feel shattered. But you're alive.")
        time.sleep(3)
        print("\nDid you survive an almost seven storey plunge? Surely not...")
        time.sleep(3)
        print(
            "\nYou slowly regain composure, and sit up to observe your surroundings. It's night time. How long had you been lying here? \nCome to think of it, where were you?")
        time.sleep(3)
        print(
            "\nSuddenly, you realize where you are. On the lower balcony. The rope lies severed next to you, a cruel reminder of the guard's brutality.")
        time.sleep(3)
        print(
            "\nFighting the pain, you get up and look around. A door leads back into the dungeon. Thinking of all the innocent lives at stake, you head back inside...\n")
        time.sleep(3)
        player.set_save_location(3)
        if not expert_mode_enabled:
            ask_save()
        else:
            chapter_4_start()
    else:
        print(
            "\nThinking of your next move, you suddenly remember: The rope from the dark room you hid in! That's your only ticket to escape!")
        time.sleep(2)
        print("\nAs the foolish mistake you have made dawns on you, two burly guards burst through the door. They each grab your arms, and before you can so \nmuch as scream, they toss you off the balcony...")
        time.sleep(3)
        game_over()


def chapter_3_defeated_second_guard():
    time.sleep(2)
    print(
        "\nYou have overcome the two guards, winning against all odds! Your reward should make up for any sustained injuries.")
    time.sleep(1.5)
    print(
        "\nSuddenly, you hear the crash of a door being flung open behind you. You spin around, only to be met with 3 more guards charging towards you!")
    time.sleep(1.5)
    print("\nYou race towards the door at the end of the corridor! Who knows what lies beyond...\n")
    time.sleep(1.5)
    balcony()


def chapter_3_defeated_first_guard():
    global enemy_ID
    time.sleep(1)
    print(
        "You have defeated the first guard! As he falls to the ground having been defeated in battle, his comrade takes a defensive stance and lunges towards you.")
    time.sleep(2)
    print("\nYou ready yourself for yet another battle! The payoff better be worth the risk...")
    time.sleep(2)
    enemy_ID = 5
    encounter_enemy('guard')


def chapter_3_hiding_choice():
    run = 0
    global enemy_ID
    try:
        run = int(input("""Silently, you slip out from behind the boxes. Peering your head around the door reveals the guards waiting for you at one end of the hallway. You 
can either make a dash for the door with natural light pouring through [1], or attempt to take on the guards [2] """))
    except ValueError:
        chapter_3_hiding_choice()
    if run == 1:
        print(" ")
        print(
            "You make a beeline for the door at the opposite end of the hall! The guards notice this, and begin to give chase once again.")
        print(" ")
        balcony()
    else:
        enemy_ID = 3
        print("\nYou decide to take on the guards! Swiftly, you approach the first guard and prepare to battle...")
        time.sleep(2)
        encounter_enemy('guard')


def hiding():
    global enemy_ID
    print(
        "You peer out from behind the boxes. Sure enough, you can hear the guards storming towards the room, calling your name mockingly.")
    print(" ")
    time.sleep(1.7)
    print(
        "You can just barely make out a silhouette enter the pitch black room, followed by two other menacing figures. They seem to \nhead straight for the table. Thank god you didn't hide there!")
    print(" ")
    time.sleep(2)
    print(
        "After some searching, the guards appear to give up, cursing under their breath as they exit the room. Now's your chance!")
    print(" ")
    time.sleep(1.3)
    chapter_3_hiding_choice()


def chapter_3_choose_rope():
    global single_use_items
    try:
        choice = int(input("You dive behind the boxes! Feeling around the floor, you can feel a coil of rope. Pick it up? [1] for yes, [2] for no. "))
        if choice == 1:
            print("\nYou've got the rope! You never know when it might prove useful...\n")
            single_use_items.append('chapter_3_rope')
            hiding()
        elif choice == 2:
            print("\nYou don't pick up the rope. You never know, it may have come in handy at some point...\n")
            hiding()
        else:
            invalid_selection_message()
            chapter_3_choose_rope()
    except ValueError:
        invalid_selection_message()
        chapter_3_choose_rope()


def chapter_3_choose_hiding_spot():
    hide = 0
    try:
        hide = int(input(
            "You quickly scan the dark room, and settle on two hiding spots; behind a stack of boxes [1], and under a table [2]. Choose one! "))
    except ValueError:
        chapter_3_choose_hiding_spot()
    if hide == 1:
        chapter_3_choose_rope()
    else:
        print(" ")
        print("You dive under the table! Sure enough, you hear the guards approaching the room. They sound angry!!")
        print(" ")
        time.sleep(1.5)
        print("The guards enter the room. They seem to know you're in there, as they're calling your name mockingly...")
        print(" ")
        time.sleep(1.8)
        print(
            "The room is pitch black, so they shouldn't be able to spot you easily. You place a hand over your mouth to muffle your erratic breathing.")
        time.sleep(2)
        print(" ")
        print("*CLANG!*")
        print(" ")
        time.sleep(1.2)
        print(
            "You freeze. You've just accidentally knocked over a metal bucket! The guards snap their heads in your direction. They begin \napproaching the table, guns loaded...")
        time.sleep(2)
        game_over()


def chase():
    door = 0
    try:
        door = int(input("Which door do you go through? [1] for the door at the end of the corridor, [2] for the door you've just noticed. Act fast! "))
        if door == 1:
            print(
                "\nYou continue to run for the door at the end of the corridor! Oddly enough, the guards appear to stop just short of the end of the corridor. \nHave they given up? Surely not...")
            time.sleep(2)
            print("\nWithout a second thought, you fling open the door and race out...")
            time.sleep(2)
            print(
                "\nOnly to find yourself standing on a precarious balcony above a sheer drop. The floor is made of rotting wood, and looks like it could \nbreak with the slightest movement.")
            time.sleep(2)
            print(
                "\nYou stand there, clueless about your next move. You notice an equally rotten balcony below you. If only you had some sort of rope, \nthen you could reach it...")
            time.sleep(2)
            print(
                "\nSuddenly, two strong looking guards appear in the doorway. They each grab one of your arms, and without a second thought, toss you \noff the balcony! The last thing you hear is them laughing before your world turns black...")
            time.sleep(2)
            game_over()
        elif door == 2:
            print(
                "\nYou dive for the door on your left! This seems to throw the guards off, as they run right past the entrance!")
            time.sleep(2)
            print("\nTime is of the essence! Those guards will no doubt come in here looking for you! You must hide!")
            time.sleep(1)
            chapter_3_choose_hiding_spot()
        else:
            invalid_selection_message()
            chase()
    except ValueError:
        invalid_selection_message()
        chase()


def chapter_3_discover_chest():
    global single_use_items, expert_mode_enabled
    if 'chapter_3_chest' in single_use_items:
        print("\nUnfortunately, this chest has previously been searched, and it is still empty. You wander back up the staircase.")
        time.sleep(1.5)
        chapter_3_choose_direction()
    chest_item = 'Smokescreen'
    if expert_mode_enabled:
        chest_item = 'Healing Potion'
    if search_chest(chest_item):
        single_use_items.append('chapter_3_chest')
        print("\nYou head back up the stairs to evaluate the other paths forward.")
    else:
        print("\nYou trudge empty-handed back up the stony staircase.")
    time.sleep(1)
    chapter_3_choose_direction()


def chapter_3_staircase():
    try:
        choice = int(input(
            "\nUnder the hatch, you find a staircase leading down. [1] to head down the stairs, [2] to evaluate the other options: "))
        if choice == 1:
            print("\nYou descend the stairs carefully, your footsteps echoing off of the cold stone walls...")
            time.sleep(1)
            print("\nAs you reach the bottom of the stairs, you come across a rusty looking chest.")
            time.sleep(1)
            chapter_3_discover_chest()
        elif choice == 2:
            chapter_3_choose_direction()
        else:
            invalid_selection_message()
            chapter_3_staircase()
    except ValueError:
        invalid_selection_message()
        chapter_3_staircase()


def chapter_3_choose_direction():
    global enemy_ID, expert_mode_enabled, enemies_defeated
    enemy_ID = 2
    try:
        choice = int(input(
            "\nYou ponder over which way to go. Will you go through the door on the right [1], the door on the left [2], or the trapdoor? [3] "))
        if choice == 1:
            if enemy_ID in enemies_defeated:
                print("\nThe guard's body lays in the doorway. You mustn't try to get through in case more guards are on the way!\n")
                chapter_3_choose_direction()
            else:
                print("\nYou decide to exit through the door on the right! As you near the door, you think you can hear rapidly approaching footsteps on the other side...")
                time.sleep(2)
                print("\nAs you stand there contemplating whether this was a good choice, suddenly the door is flung open by a familiar looking \nface; it's the guard who dragged you to Solitary Confinement!")
                time.sleep(3.5)
                encounter_enemy('guard')
        elif choice == 2:
            print(
                "\nYou decide on exiting through the door on the left! As you approach the heavy wooden door, your heart begins to race. What could\npossibly lurk behind this door?")
            time.sleep(2)
            print("\nHaving gained enough courage, you press your palm against the door and push it open... ")
            time.sleep(2)
            print(
                "\nAs you peer around the door, you are met with a stone-walled corridor that seems to stretch on forever. A red carpet, covered\nin ominous stains, trails along the rotting wooden floor.")
            time.sleep(2)
            print(
                "\nUpon closer inspection, you notice a door at the end of the corridor. Natural light pours in though the small gaps around the \ndoor, making this the only light source. Could this door be your ticket to freedom?")
            time.sleep(2)
            print(
                "\nAs you're pondering over your next move, you hear the sudden crash of a door being flung open behind you, as well as manic \nyelling and rapid footsteps. A guard must have spotted you and called for backup!")
            time.sleep(2)
            print(
                "\nThe chase is on! You begin to dash for the door at the end of the corridor, the guards hot on your trail!")
            time.sleep(2)
            print(
                "\nAs you near the end of the corridor, you spot a door that you hadn't previously noticed. This door looks rotten, and there's no light on the other side")
            time.sleep(2)
            chase()
        elif choice == 3:
            print("\nYou decide to check out the hatch in the floor! You slowly lift the hatch, being careful not to make too much noise.")
            time.sleep(2)
            chapter_3_staircase()
        else:
            raise ValueError
    except ValueError:
        invalid_selection_message()
        chapter_3_choose_direction()


def chapter_3_start():
    global player, mute_audio, basic_graphics_enabled
    time.sleep(2)
    if not basic_graphics_enabled:
        try:
            print("\n█▒░ Chapter Three: The Great Escape ░▒█")
        except Exception:
            print("\n== Chapter Three: The Great Escape ==")
    else:
        print("\n== Chapter Three: The Great Escape ==")
    if not mute_audio:
        pygame.mixer.music.load("sfx/thud.ogg")
        pygame.mixer.music.play(1)
    time.sleep(3)
    player.set_save_location(2)
    time.sleep(1)
    print(
        "\nHaving unlocked your cell door, you slowly push it open, being careful to minimize the shrill shrieks of the worn out hinges.")
    time.sleep(2)
    print(
        "\nYou step out into the room beyond your cell, and peer around. The floor is made of worn, rough stone, and the stone walls are lined\nwith moss.")
    time.sleep(2)
    print(
        "\nYou also notice two doors on each side of the room, and a trapdoor in the floor between the two exits. A damp, musty odour fills your nostrils.")
    time.sleep(2)
    chapter_3_choose_direction()


def chapter_2_get_keys():
    global player, expert_mode_enabled
    print("\nYou flick the rope towards the keys...")
    time.sleep(3)
    print("\nAnd... success! The keys appear to be intertwined with the small chain.")
    time.sleep(3)
    print(
        "\nYou slowly pull the rope. With every movement, the keys jingle faintly. You wince each time this happens, not wanting to\nalert any nearby guards.")
    time.sleep(3)
    print(
        "\nAttempting to free the keys from the hook they are hanging from, you give the rope a slightly harder tug. The keys fall, before\nloudly landing on the stony floor.")
    time.sleep(3)
    print(
        "\nYou freeze. After a few seconds of silence, you determine that the coast is clear. You begin to pull the rope towards you again,\nwith the keys still attached to the other end.")
    time.sleep(3)
    print(
        "\nAfter what feels like an eternity, the keys reach the bottom of the door. You continue to feed the rope back towards you extremely\ncarefully. One wrong move could cause the keys to detach from the end of the rope.")
    time.sleep(3)
    print(
        "\nWith one final tug, you pull the remainder of the rope up to the hatch. You desperately grab for the keys through the tiny opening...")
    time.sleep(3)
    print(
        "\n...And you are successful! Shakily, you bring the largest key of the bunch up to the lock in your cell door...")
    time.sleep(3)
    print("\n*CLUNK!*")
    time.sleep(3)
    print(
        "\nYou exhale sharply as the lock releases its grip on the sturdy door. You toss the rope aside, before pushing the door open slowly...")
    player.set_save_location(2)
    if not expert_mode_enabled:
        ask_save()
    else:
        chapter_3_start()

def chapter_2_combine_items():
    print("\nYou glance over the two items you found, thinking up ways they could come in handy...")
    time.sleep(3)
    print("\nSuddenly, you have a brainwave! Quickly, you tie the small length of chain to one end of the rope. ")
    time.sleep(3)
    print(
        "You figure that if you can toss the rope through the hatch and hit the keys with the chain, they may become entangled, allowing you\nto drag the keys over.")
    time.sleep(3)
    print("\nWith your newly-developed tool in hand, you run over to the door, and slide the hatch open.")
    time.sleep(3)
    print(
        "\nThe keys are so close, yet so far. Full of anticipation, you raise your hands up to the small hatch, and prepare to throw the rope...")
    time.sleep(3)
    chapter_2_get_keys()


def initiate_object_search():
    global single_use_items
    time.sleep(1)
    choice_message = "\nAfter some deliberation, you settle on three potentially useful locations to search; the small sink in the corner of the room [1], the\ncramped bed [2], or a small cupboard [3]. Which one will you examine? "
    if 'chapter_2_rope' in single_use_items and 'chapter_2_chain' in single_use_items:
        time.sleep(1)
        chapter_2_combine_items()
    if 'chapter_2_rope' in single_use_items or 'chapter_2_chain' in single_use_items or 'searched_chapter_2_cupboard' in single_use_items:
        choice_message = "\nWhere will you search next? The sink [1], the bed [2], or the cupboard [3]? "
    try:
        choice = int(input(choice_message))
        if choice == 1 and 'chapter_2_chain' not in single_use_items:
            print("\nYou quietly pad over to the small sink. It's incredibly worn, with small cracks adorning the surface.")
            time.sleep(1)
            print(
                "\nSuddenly, you notice the small, corroded chain which connects the plug to the basin. It's far too small to reach the keys, however\nit could come in handy when combined with something else...")
            time.sleep(1)
            print("\nYou silently pull the chain free, and pocket it for later use.")
            single_use_items.append('chapter_2_chain')
            initiate_object_search()
        elif choice == 1 and 'chapter_2_chain' in single_use_items:
            print("\nYou once again return to the small sink.")
            time.sleep(1)
            print("\nYou scan your eyes across the damaged porcelain surface, looking for anything that could help reach the keys.")
            time.sleep(2)
            print("\nConfident there is nothing else, you return to the center of the room and think over your other options.")
            initiate_object_search()
        elif choice == 2 and 'chapter_2_rope' not in single_use_items:
            print(
                "\nYou make your way over to the bed. It's constructed entirely out of metal, and looks extremely durable.")
            time.sleep(1)
            print(
                "\nBut wait, your eyes are suddenly drawn to something out of place. At the rear corner of the bed where two intersecting metal posts\nmeet, a rope has been tied tightly around the join.")
            time.sleep(1)
            print(
                "\nUpon further inspection, the two metal posts appear to have broken; the rope must have been added in an attempt to fix the bed.")
            time.sleep(1)
            print(
                "\nYou get down on your hands an knees, and attempt to untie the rope. After a brief struggle, you manage to get it free. You\ncoil it up and sling it over your shoulder.")
            time.sleep(1)
            single_use_items.append('chapter_2_rope')
            initiate_object_search()
        elif choice == 3 and 'searched_chapter_2_cupboard' not in single_use_items:
            print("\nYou walk over to the cupboard. It's flimsy, and made entirely of rotting wood.")
            time.sleep(1)
            print(
                "\nYou crouch down, and slowly open the door. You peer inside the cupboard; besides copious amounts of dust and cobwebs, the\ninside of the cupboard is entirely barren.")
            single_use_items.append('searched_chapter_2_cupboard')
            initiate_object_search()
        elif choice == 1 and searchedSink:
            print(
                "\nYou make your way back over to the sink. You quickly scan it, however you're certain you've already picked up anything useful.")
            initiate_object_search()
        elif choice == 2 and 'chapter_2_rope' in single_use_items:
            print(
                "\nYou wander back over to the bed. You look over it once more, however you're certain you've already picked up anything useful.")
            initiate_object_search()
        elif choice == 3 and 'searched_chapter_2_cupboard' in single_use_items:
            print("\nYou make your way back over to the cupboard.")
            time.sleep(1)
            print(
                "\nYou peer inside once again, before reaching in with your hand in order to feel for anything that wasn't visible...")
            time.sleep(1)
            print(
                "\nOnly to uncover a huge spider! You scream and flick the insect off of your hand, and it scurries away.")
            initiate_object_search()
        else:
            invalid_selection_message()
            initiate_object_search()
    except ValueError:
        invalid_selection_message()
        initiate_object_search()


def ChapterTwoGuardEscape():
    global expert_mode_enabled, player
    time.sleep(2)
    print(
        "\nYou have managed to escape the guard! In his confusion, the guard darts off out of the room outside the cell.")
    time.sleep(1)
    print("\nCould he be fetching backup? One thing's for certain, you don't want to stick around to find out...")
    if not expert_mode_enabled:
        player.set_save_location(2)
        ask_save()
    else:
        chapter_3_start()


def chapter_2_guard_defeated():
    global playerHealth, playerMaxHealth, expert_mode_enabled, player
    print(
        "\nYou gaze down at the guard laying motionless in the doorway. You take a deep breath, before stepping over the defeated guard.")
    time.sleep(1)
    print("\nYou cautiously step out of your cramped cell, into the newly revealed room...")
    if not expert_mode_enabled:
        player.set_save_location(2)
        ask_save()
    else:
        chapter_3_start()


def chapter_2_continue_yelling():
    global enemy_ID
    try:
        stop = int(input("\nDo you continue to yell [1], or stop? [2] "))
    except ValueError:
        chapter_2_continue_yelling()
    if stop == 1:
        time.sleep(0.25)
        print(
            "\nYou carry on yelling! The guard appears to snap; he storms to the other side of the room and grabs the keys.")
        time.sleep(1)
        print(
            "\nHe stomps back over to the cell door, fumbles with the lock, and throws the door open. He prepares for combat and lunges at you...")
        enemy_ID = 8
        encounter_enemy('guard')
    else:
        print("""\nYou stop yelling. The guard, seemingly regaining his composure, calmly walks over to the hatch and slides it shut. Your heart sinks
as you hear the metallic click of the lock. You are trapped with no escape...""")
        game_over()

def choice6():
    try:
        choice = int(input(
            "\nIt's your call! Will you attempt to distract a nearby guard in the hopes he'll open the door [1], or explore your cell further [2]? "))
        if choice == 1:
            print("\nYou quickly devise a way to grab a guard's attention, and begin to yell maniacally.")
            time.sleep(1)
            print(
                "\nAs expected, you hear the clamouring of heavy footsteps on the other side of the cell door, before the small hatch is \nviolently flung open. An angry pair of eyes stare you down.")
            chapter_2_continue_yelling()
        else:
            print("\nYou glance around the room, frantically looking for something that may aid you.")
            initiate_object_search()
    except ValueError:
        choice6()

def choice5():
    print(" ")
    print("You wander over to the rusty door.")
    time.sleep(1)
    print(
        "\nOut of curiosity, you outstretch an arm and touch the hatch. To your surprise, it easily slides open. It appears as though the \nguard forgot to lock it in his haste.")
    time.sleep(1)
    print(
        "\nYou raise your eyes to the hatch, and peer around the room on the other side of the cell door. It's virtually empty, without a \nguard in sight.")
    time.sleep(1)
    print(
        "\nYour eyes lock onto a set of keys dangling from a rusty hook on the opposite end of the room. Do these keys unlock this door?")
    time.sleep(1)
    print(
        "\nYou back away from the hatch, before quietly sliding it back shut to avoid suspicion. You must find a way to grab the keys...")
    choice6()

def eatCrackers():
    global player
    try:
        checkDoor = int(input("Will you examine the package of food [1], or inspect the door [2]? "))
    except ValueError:
        print("\nBad input. Only integers can be entered!")
        eatCrackers()
    if checkDoor == 1:
        print("\nYou pick up the package of food with shaky hands, and briskly unwrap it.")
        time.sleep(1)
        print("\nThe small package contains what looks to be crackers. Without a second thought, you gulp them down.")
        time.sleep(1)
        print("\nThey are extremely stale, but provide you with some much needed nourishment.")
        time.sleep(0.5)
        print("\nHealth has been fully restored!\n")
        player.restore_health()
        time.sleep(1)
        print("Having eaten the food, you decide to make your way over to the cell door.")
        time.sleep(1)
        choice5()
    elif checkDoor == 2:
        choice5()

def choice4():
    global savePoint
    global playerHealth
    global playerMaxHealth, basic_graphics_enabled
    if not basic_graphics_enabled:
        try:
            print("\n█▒░ Chapter Two: Solitary Confinement ░▒█")
        except Exception:
            print("\n== Chapter Two: Solitary Confinement ==")
    else:
        print("\n== Chapter Two: Solitary Confinement ==")
    if mute_audio != True:
        pygame.mixer.music.load("sfx/thud.ogg")
        pygame.mixer.music.play(1)
    time.sleep(3)
    savePoint = 1
    if debug > 0:
        print("SavePoint =", savePoint)
    print(
        "\nYou are now in solitary confinement. The walls are made of solid grey stone, with a few areas tinted an ominous shade of red. If the stains \nare what you think they are, you're in trouble...")
    try:
        stay = float(input(
            "\nThere is a single window. You peer out, estimating the fall to be around 6 storeys. Maybe a fall from here won't kill you? (1 to jump, 2 to remain) "))
    except ValueError:
        print(" ")
        print("Bad input. Only integers can be entered!")
        choice4()
    if stay == 1:
        print(" ")
        print(
            "You leap from the window! As the ground hurtles towards you, you begin to regret your decision. The last thing you remember is a loud crack as you hit the ground...")
        print(" ")
        time.sleep(2.75)
        game_over()
    else:
        print(" ")
        print(
            """You decide to remain in the tower! Just as you are thinking about how desperate you'd have to be  to jump out the window, you 
hear the rattling of keys as a small metal shutter slides open on the door, revealing the face of your captor...""")
        print(" ")
        time.sleep(1.5)
        print(
            """All that's visible is the eyes of the guard through the small horizontal opening in the metallic door. He tosses a small 
package of what appears to be food through the opening and promptly slams the hatch back shut.""")
        print(" ")
        time.sleep(1.5)
        eatCrackers()


def warp_debug():
    global debug, enemy_ID, player, expert_mode_enabled, player_expert_cache
    warp_location = input("\nType the location you wish to warp to, or type 'end' to quit. Upon warping to a function, debug mode will be\n"
                     "enabled automatically.\n\nWarp to where? ")
    if debug == 0:
        print("\n= Debug mode is active =\n")
        debug = 1
    player = Player(10, 200, 200, "test", inventory={'Healing Potion': 999, 'Hyper Potion': 1, 'Smokescreen': 3},
                    defensive_items=['dummy', 'dummy2'], has_beaten_game=False, has_completed_expert_mode=False, save_location=3)    # Create a dummy player so the game doesn't crash
    if warp_location == "save":
        ask_save()
    elif warp_location == "release":
        contents = input("Spoofed version number: ")
        method_of_access = input("Method of access: ")
        download_release_notes(method_of_access, contents)
    elif warp_location == "newVer" or warp_location == "newver":
        ask_download_update(method_of_access=input("Method of access = "), contents=b"3.0.1")
    elif warp_location == "end":
        menu()
    elif warp_location == 'battle':
        choice = input("Type the class of enemy to test (case sensitive:) ")
        enemy_ID = int(input("Type an int value to assign to enemy_ID: "))
        encounter_enemy(choice)
    elif warp_location == "chapter":
        warp_to_chapter(save_location=int(input("Enter a value for save_location: ")))
    elif warp_location == "crash":
        handle_error(description="Sample description generated by debug_warp", e="Sample traceback")
        warp_debug()
    elif warp_location == "expert":
        expert_mode_enabled = True
        print("\n== Expert mode enabled - select a chapter to test ==")
        chapter_replay()
        warp_debug()
    elif warp_location == 'expert complete':
        player = Player(500, 20, 20, 'dummy', inventory={'Healing Potion': 5, 'Hyper Potion': 1, 'Smokescreen': 3}, defensive_items=['Shard of Glass'], has_beaten_game=True, has_completed_expert_mode=False, save_location=7)
        player_expert_cache = player
        expert_mode_enabled = True
        game_credits()
    else:
        print("'" + warp_location + "' is not a recognised function or warp location. Check spelling and try again.\n")
        warp_debug()


def play_audio(selection, friendlyname, description):
    try:
        pygame.mixer.music.load('sfx/'+str(selection)+'.ogg')
    except Exception as e:
        description = "An error occurred when loading the audio track."
        handle_error(description, e)
        extras_music_player()
    pygame.mixer.music.play(0)
    print("\nNOW PLAYING:\n"+str(friendlyname)+"\n\nABOUT THIS TRACK:\n"+str(description))
    input("\n\nPress [Enter] to stop playback and return to the previous menu.")
    pygame.mixer.music.stop()
    extras_music_player()


def extras_music_player():
    global sound_module_error, basic_graphics_enabled, classic_theme_enabled
    selection = 'null'  # The filename of the track that is to be played
    friendlyname = 'not implemented'    # The name of the track in a more human-readable format
    description = 'not implemented'     # The description of the track shown on the Now Playing screen
    print(generate_header('MUSIC PLAYER'))
    print("Choose a track to listen to:")
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
17] Curtain Call""")
    if generate_seperator():
        print(generate_seperator())
    try:
        choice = int(input("18] Quit\n--> "))
    except ValueError:
        extras_music_player()
    if choice == 1:
        selection = 'dtd_main'
        friendlyname = 'Theme of DTD'
        description = r"""The main theme of DeathTrap Dungeon! For this theme, we really wanted it to sound adventurous, exciting,
but to also sound somewhat ominous. The original theme largely hit the nail on the head, but it certainly had some issues. The
version you're listening to came about after Charly had expressed some discontent with the original theme. First he cleaned
up the mix, before adding the drums as a finishing touch to liven it up a bit. We're both pleased with the end result!"""
    elif choice == 2:
        selection = 'dtd_main_beta'
        friendlyname = 'Theme of DTD (Beta)'
        description = r"""This is the original theme of DeathTrap Dungeon. It was only ever included in one version of the game,
and was mainly included to test if an opening theme would work at all.

There's quite a few interesting things about this theme. First of all, it was played live in one take. In essence, it was only
ever a rough mock-up. Back in early 2020 or so (during the pandemic), we were messing about with adding music to the
game. One of us raised the question about including an opening theme, and after some early attempts, Charly sent this over for 
me to add in. I instantly fell in love with it, and the basic melody has stayed the same since then.

Also of note is the fact that this version is quite a bit longer that what we have now. This was one of the problems with this
early version, as well as the poor recording quality. Charly quickly set about fixing this, and after a few more iterations, 
we ended up with the main theme we have now!"""
    elif choice == 3:
        selection = 'exploration'
        friendlyname = 'Exploration'
        description = r"""This song is basically just an extended version of the main theme of DeathTrap Dungeon! I believe it came
about when Charly was experimenting with remixing the main theme of the game for the v2.9 release. One of the 'killer features' of
that version so to speak was the remixing of many of the game's songs. I think he put this one together before trimming it back 
slightly, with the shortened version becoming the main theme. """
    elif choice == 4:
        selection = 'encounter'
        friendlyname = 'Encounter!'
        description = r"""The enemy encounter theme! This was another one of the songs remixed for DTD v2.9. The theme that was played
before was only ever intended to be for testing purposes. In fact, back when we were re-recording songs for the big release
of 2.9, Charly admitted that he couldn't even remember making the original theme!

Very quickly after this, he reached out with this theme. I feel as though this one works much better, as the instruments match 
those used for other songs. The original encounter theme used a synth, and felt somewhat out of place."""
    elif choice == 5:
        selection = 'encounter_beta'
        friendlyname = 'Encounter! (Beta)'
        description = r"""This is the original enemy encounter theme, used in older versions of the game.

This one's definitely... interesting to say the least. You'll notice that it's got a really long running time, especially because
the version that was played in-game in those older versions only used the first few seconds. The rest of this song is entirely 
improv. 

As mentioned, most of this theme was never intended to be heard, and this is the first time that it's been deliberately accessible
in-game. Enjoy this interesting piece of DTD history!"""
    elif choice == 6:
        selection = 'battle'
        friendlyname = 'Battle!'
        description = r"""The main battle theme! This track was one of those that was re-recorded for DTD v2.9, as a part
of that version's aim of providing a revisited and clean soundtrack. 

Since the original variant of the theme was added, it's been one of my personal favorites, and this remastered version
is no different. In fact, I feel as though it takes everything the original theme did well and improves upon it all
tenfold. """
    elif choice == 7:
        selection = 'puppets'
        friendlyname = 'Battle With Emperor Juniper!'
        description = r"""The theme that plays during the final battle with Emperor Juniper!

When Charly sent this song over to me, I instantly fell in love with it. Overall, I feel that it represents Juniper's
character perfectly, and it's exactly what I wanted out of the final boss theme. Traditionally in games, final battle 
themes are souped-up versions of normal battle themes. For lack of a better term, they're all very 'balls-to-the-wall' 
in nature, which is understandable.

However, for this game, I really wanted to emphasize that Juniper was once a kind man, turned insane. I thought it would 
be cool if the music could reflect this by sounding menacing, but also calm and not what the player might expect. This
track, in my opinion, hits the nail on the head!

Oh, fun fact, in the game's files, the name for this song is 'Puppets'. This is actually because I was originally using
Metallica's 'Master Of Puppets' to test the final boss battle! Unfortunately I can't include that song for legal
reasons; otherwise I'll have Lars after me :/"""
    elif choice == 8:
        selection = 'groov'
        friendlyname = "Groov"
        description = r"""No, the name isn't a typo, that's what Charly called it. This song was actually put together for
another project; back in 2021 or so, Charly made a game in AGS called Second Hand (which you should totally check out!) 

Later on down the line, Charly and I were working on a sequel to this game, which would also be built in AGS. We used the 
Second Hand game engine to test many different mechanics and ideas, and this song was carried over. Somewhere along the line,
it found its way into this game as a sound test during development, where it has remained in the files ever since."""
    elif choice == 9:
        selection = 'move'
        friendlyname = 'Move'
        description = r"""Well this is awkward... I actually can't remember how or why this song ended up in the game's
files.

If I had to guess, I'd say it was probably part of a demo that existed at one time, however I really can't say for sure.
Most likely, it was just used as a simple sound test, and I never got around to removing it from the game's files. Peak
laziness, I know."""
    elif choice == 10:
        selection = 'incident'
        friendlyname = 'Incident'
        description = r"""This is the sound that's played when you save at a checkpoint!
        
There's not much to note about this one, apart from the name. As implied, this sound was originally supposed to play whenever
an 'incident' took place, for example picking up an item or restoring health. This never made it in, however, and the name 
was never changed despite it only playing at one specific point during gameplay."""
    elif choice == 11:
        selection = 'elevator'
        friendlyname = 'Elevator'
        description = r"""You'll probably recognise this track as an extended version of the sound that's played when you
load a save file.

Back when we were working on adding more sound effects to the game, Charly thought it would be cool to have the load
jingle sound like the music that would play in an elevator. He put this together as a concept, and made the shortened
verison that was used in-game. I really liked it so it stuck!"""
    elif choice == 12:
        selection = 'load'
        friendlyname = "Load"
        description = r"""This is the jingle that's played when you load a saved game! If you haven't already, check out the
track 'Elevator' - it's an extended version of this sound!"""
    elif choice == 13:
        selection = 'gameover'
        friendlyname = "Game Over"
        description = r"""This is the theme played when you get a game over. Something interesting about this tune is that since
it was originally implemented into the game, it's never changed. Sure, it's been re-recorded and cleaned up over the years, but
the general sound and composition has never changed since the theme first debuted."""
    elif choice == 14:
        selection = 'basckground'
        friendlyname = "Background"
        description = r"""This is an interesting one - this song came about years ago; it was added in to demo a feature that never
made it to the final release. The feature in question was almost immediately scrapped, but this audio has hung about in the game's 
files - nothing but a remnant of a feature that never saw the light of day. It's actually kinda sad if you think about it.

Huh, this got weirdly philosophical. Anyways, this is the first time this song has been accessible to players in-game through
normal means! It's always been in the files though - if you know how, you can hear this in versions of DTD from years back."""
    elif choice == 15:
        selection = 'ambient'
        friendlyname = "Credits"
        description = r"""The credits theme!

This is another one of the tracks that was re-recorded by Charly for the big release of DTD v2.9. This song remained basically
the same as it always had been, it just needed the mix cleaning up slightly.

Oh fun fact, this song was officially introduced in DTD v2.9 (seeing as it plays during the credits, and that was the first
version of the game to have an ending), but the song actually existed in the files of older releases of the game, too. This
was simply a case of the song being complete before the ending was. 

This song also wasn't always going to be the credits theme - in fact, I had intended for it to play on the final chapter
before you fight Juniper. This never ended up happening, however, as I felt it fitted with the credits better. That explains
why the audio file is called 'ambient' - a common theme you'll notice is the names of audio files in this game often represent
what they were originally designed for.
"""
    elif choice == 16:
        selection = 'ambient_percussion'
        friendlyname = "Credits (Alt. Version)"
        description = r"""This is simply an alternative version of the credits theme, with drums added! 
        
This song plays when you have already beaten the game once. If you haven't heard it in-game yet, give it a shot 
by loading the save file you beat the game with, then heading into the final chapter using Chapter Replay. 
This version of the credits theme actually fits better than the version without drums, in my opinion. It's a 
little treat for defeating Juniper more than once!
"""
    elif choice == 17:
        selection = 'curtain_call'
        friendlyname = "Curtain Call"
        description = r"""This is the song that plays on the screen shown after you beat the game, either the regular
story, or on Expert Mode!

This is one of my favorite songs in the game, but it almost never made it in. Just before the release of DTD 2.9 (the
first version of the game to have an ending, so the first version to feature the post-credits screen that this song plays
on), I realised that the post-credits screen felt really empty without any music. 

This song was an extremely late addition and was originally written for a different game I believe, but I feel that it
works here really nicely.
"""
    else:
        extras_menu()
    play_audio(selection, friendlyname, description)


def sound_test():
    print(generate_header("SOUND TEST"))
    try:
        pygame.mixer.music.load("sfx/exploration.ogg")
    except Exception as e:
        description = "The test audio could not be loaded."
        handle_error(description, e)
        audio_settings()
    pygame.mixer.music.play(15)
    print("Can you hear a tune playing?\n1] Yes\n2] No\n3] Cancel")
    try:
        choice = int(input("--> "))
        pygame.mixer.music.stop()
        if choice == 1:
            print("Great, sound is configured and working properly!")
            audio_settings()
        elif choice == 2:
            print("\nHere are some things you can try:\n-Ensure volume is turned up on your device\n-Restart the program\n-Reinstall pygame (Source code users only)\n-Ensure audio isn't muted in the game\n-Ensure the game's audio files have been downloaded and saved in the same folder as the Python script\n-Uninstall and reinstall the program (Windows users only)\n\nIf none of the above steps work for you, reach out! Use the 'Report a bug' feature in the 'Settings' menu in order to report a bug.")
            audio_settings()
        elif choice == 3:
            audio_settings()
        else:
            raise ValueError
    except ValueError:
        pygame.mixer.music.stop()
        invalid_selection_message()
        sound_test()


def audio_settings():
    global sound_directory_error, basic_graphics_enabled, classic_theme_enabled, mute_audio, no_pygame
    sound_error_message = "the Pygame module could not be imported" # Gives the user a reason for not being able to unmute audio. By default, this variable is set to the message shown when Pygame isn't installed.
    if sound_directory_error:
        sound_error_message = "audio data could not be accessed"    # Change the error message shown if the audio data couldn't be accessed.
    print(generate_header("SOUND SETTINGS"))
    if mute_audio is True:
        print("1] Unmute audio\n2] Test audio")
    else:
        print("1] Mute audio\n2] Test audio")
    if generate_seperator():
        print(generate_seperator())
    try:
        choice = int(input("3] Cancel\n--> "))
    except ValueError:
        print("\nBad input. Only an integer can be entered here!")
        audio_settings()
    if choice == 1 and mute_audio is not True:
        if mute_audio != True:
            mute_audio = True
            save_settings('audio_settings', [mute_audio])
            print("Audio has been muted.")
            audio_settings()
    elif choice == 1 and mute_audio is True:
        if sound_module_error or sound_directory_error or no_pygame:
            print(f"\nYou cannot unmute audio because {sound_error_message}. \nVisit: https://reubenparfrey.wixsite.com/deathtrapdungeon/help to fix this error, then try again.")
            audio_settings()
        else:
            mute_audio = False
            save_settings('audio_settings', [mute_audio])
            print("Audio has been unmuted.")
            audio_settings()
    elif choice == 2:
        if sound_module_error or sound_directory_error or no_pygame:
            print(f"\nYou cannot access the Sound Test because {sound_error_message}. \nVisit: https://reubenparfrey.wixsite.com/deathtrapdungeon/help to fix this error, then try again.")
            audio_settings()
        else:
            sound_test()
    elif choice == 3:
        settings()
    else:
        audio_settings()


def confirm_erase_choice(savefile):
    try:
        choice = int(input("1] Erase this save file\n2] Cancel\n--> "))
        if choice == 1:
            print("Deleting data...")
            os.remove(savefile)
            print("The save file has been erased.")
            erase_save_data()
        else:
            erase_save_data()
    except ValueError:
        confirm_erase_choice(savefile)
    except FileNotFoundError as e:
        handle_error("The file could not be deleted.", e)
        erase_save_data()


def ask_erase_save(filename):
    save_data, is_corrupt, is_incompatible = load_save_data(filename)
    if not is_corrupt and save_data is not None:
        print("\nYou are about to delete this save file:")
        player_name, save_location, damage, max_health, health, game_beaten, expert_mode_beaten, inventory, defensive_items = save_data
        player_object = Player(attack_damage=damage, health=health, max_health=max_health, entered_name=player_name,
                               inventory=inventory, defensive_items=defensive_items, has_beaten_game=game_beaten,
                               has_completed_expert_mode=expert_mode_beaten, save_location=save_location)
        show_save_preview(player_object)
    elif is_corrupt:
        print("\n== This save file is corrupt, detailed save file info cannot be displayed. ==")
    elif is_incompatible:
        print("\n== This save file is incompatible, detailed save file info cannot be displayed. ==")
    elif save_data is None:
        print("\nThere is no save data stored in the selected slot.")
        erase_save_data()
    print("\nIf you continue, the save file will be permanently erased - it can't be recovered.")
    time.sleep(2)
    confirm_erase_choice(filename)


def erase_save_data():
    print(generate_header("DELETE SAVE FILE"))
    slots = [
        {'number': 1, 'filename': 'data/savedata.dat'},
        {'number': 2, 'filename': 'data/savedata2.dat'},
        {'number': 3, 'filename': 'data/savedata3.dat'}
    ]
    print("Select a save file to erase:")
    for slot_info in slots:
        display_save_slot_info(slot_info)
    if generate_seperator():
        print(generate_seperator())
    try:
        choice = int(input("4] Cancel\n--> "))
        if 1 <= choice <= 3:
            slot_info = next((slot for slot in slots if slot['number'] == choice), None)
            ask_erase_save(slot_info['filename'])
        elif choice == 4:
            advanced_settings()
        else:
            print("\nPlease select a valid option.")
            erase_save_data()
    except ValueError:
        print("\nBad input. Only integers can be entered here!")
        erase_save_data()


def auto_update_settings():
    global auto_updates_disabled
    user_feedback = "disabled."
    if not auto_updates_disabled or auto_updates_disabled is [False]:
        print("\nAutomatic Updates are enabled. With this on, DeathTrap Dungeon will periodically check for updates\nwhen it is launched, and notify you when a new version is out. Would you like to disable this?")
    else:
        print("\nAutomatic Updates are disabled. Would you like to enable them?")
    try:
        choice = int(input("1] Yes\n2] No\n--> "))
        if choice == 1:
            if not auto_updates_disabled or auto_updates_disabled is [False]:
                auto_updates_disabled = True
            else:
                auto_updates_disabled = False
                user_feedback = "enabled."
            save_settings('update_configuration', [auto_updates_disabled])
            print("Automatic Updates are now "+str(user_feedback))
            software_update_settings()
        elif choice == 2:
            software_update_settings()
        else:
            print("\nPlease select a valid option.")
            auto_update_settings()
    except ValueError:
        auto_update_settings()


def software_update_settings():
    global auto_updates_disabled, refreshed_latest_release_ver
    auto_update_toggle = "Disable "
    if auto_updates_disabled:
        auto_update_toggle = "Enable "
    print(generate_header("SOFTWARE UPDATES"))
    print("1] Check for Updates\n2] "+str(auto_update_toggle)+"Automatic Updates")
    if generate_seperator():
        print(generate_seperator())
    try:
        choice = int(input("3] Cancel\n--> "))
    except ValueError:
        software_update_settings()
    if choice == 1:
        print("Checking for updates...")
        refreshed_latest_release_ver = False    # This gets set to True when the game starts, so reset it to False so the game is getting the latest copy of the file.
        if check_network_connection():          # Returns True if there is an active network connection.
            check_for_updates(method_of_access='manual')    # The variable 'method_of_access' is set to 'manual', so
        else:                                               # the game knows that the user initiated the update check.
            print("\nYou are not connected to the internet. Check your network connection and try again.")
        software_update_settings()
    elif choice == 3:
        settings()
    elif choice == 2:
        auto_update_settings()
    else:
        software_update_settings()


def disable_basic_graphics():
    global basic_graphics_enabled, active_theme
    print("Disabling Basic Graphics mode...")
    basic_graphics_enabled = False
    active_theme = 'flow'
    save_settings('graphics_configuration', [active_theme, basic_graphics_enabled])
    print("\nBasic Graphics mode has been disabled.")
    graphics_settings()


def enable_basic_graphics():
    global basic_graphics_enabled, active_theme
    print("Applying Basic Graphics mode...")
    basic_graphics_enabled = True
    active_theme = 'basic'
    time.sleep(0.5)
    save_settings('graphics_configuration', [active_theme, basic_graphics_enabled])
    print("\nBasic Graphics mode has been enabled.")
    graphics_settings()


def ask_basic_graphics():
    global basic_graphics_enabled, auto_applied_basic_graphics
    if basic_graphics_enabled is False or basic_graphics_enabled is [False]:
        try:
            choice = int(input(
                "\nBasic Graphics mode is designed for systems that incorrectly display the game's graphics. When this setting is enabled,\ngraphics are displayed in a much more simple way. It's only recommended that you enable Basic Graphics\nmode if you're having issues with how the game's visuals are displayed.\n\nChoose an option to continue:\n1] Apply Basic Graphics Mode\n2] Cancel\n--> "))
            if choice == 1:
                enable_basic_graphics()
            elif choice == 2:
                graphics_settings()
            else:
                invalid_selection_message()
                ask_basic_graphics()
        except ValueError:
            ask_basic_graphics()
    elif (basic_graphics_enabled is True and auto_applied_basic_graphics is False or basic_graphics_enabled is
          [True] and auto_applied_basic_graphics is False):
        try:
            choice = int(input("Disable Basic Graphics mode?\n1] Yes\n2] No\n--> "))
        except ValueError:
            ask_basic_graphics()
        if choice == 1:
            disable_basic_graphics()
        else:
            graphics_settings()
    elif (basic_graphics_enabled is True and auto_applied_basic_graphics is True or basic_graphics_enabled is
          [True] and auto_applied_basic_graphics is True):
        print("\nBasic Graphics mode can't be disabled right now as your system can't render unicode characters. For more information, visit:\nhttps://reubenparfrey.wixsite.com/deathtrapdungeon/help/ ")
        graphics_settings()


def apply_new_theme(theme_to_apply):
    global active_theme, basic_graphics_enabled
    theme_description = "None specified"    # A brief description of the theme that is shown to the user before they apply it.
    if theme_to_apply == 'flow':
        theme_description = "\nThe Flow theme is the default visual style of DeathTrap Dungeon. Featuring solid, clean lines\nand subtle but stylish gradients, Flow is a modern re-imagining of the classic DeathTrap Dungeon menu design."
    elif theme_to_apply == 'classic':
        theme_description = "\nClassic Theme is a throwback to older versions of DeathTrap Dungeon. Making use of simplistic characters,\nClassic Theme transforms the look and feel of the game and is perfect for those who prefer the\nmore simplistic look of the menus in older versions of DeathTrap Dungeon."
    elif theme_to_apply == 'basic':
        theme_description = "\nFlow Basic is a variation of the Flow theme. Making use of more simplistic characters, this theme is\nperfect for those who want a modern looking theme that is easy on the eyes!"
    try:
        choice = int(input(f"{theme_description}\n\nUse this theme?\n1] Yes\n2] No\n--> "))
        if choice == 1:
            print("Applying theme...")
            active_theme = theme_to_apply
            if theme_to_apply == 'basic':
                theme_to_apply = 'flow basic'
            elif theme_to_apply == 'classic':
                theme_to_apply = 'classic theme'
            save_settings('graphics_configuration', [active_theme, basic_graphics_enabled])
            print(f"{theme_to_apply.title()} has been applied.")
            time.sleep(0.5)
            switch_theme_dialogue()
        elif choice == 2:
            switch_theme_dialogue()
        else:
            raise ValueError
    except ValueError:
        invalid_selection_message()
        apply_new_theme(theme_to_apply)


def switch_theme_dialogue():
    global classic_theme_enabled, basic_graphics_enabled, active_theme
    print(generate_header("CHANGE THEME"))
    flow_selection = "1] Flow (default) [ ]"
    basic_selection = "2] Flow Basic [ ]"
    classic_selection = "3] Classic Theme [ ]"
    print("Select the theme you'd like to use from the list below. Themes completely transform the look and \nfeel of menus, but do not affect in-game graphics.")
    if active_theme == 'classic':
        classic_selection = "3] Classic Theme [*]"
    elif active_theme == 'basic':
        basic_selection = "2] Flow Basic [*]"
    else:
        flow_selection = "1] Flow (default) [*]"
    print(f"{flow_selection}\n{basic_selection}\n{classic_selection}")
    if generate_seperator():
        print(generate_seperator())
    try:
        choice = int(input("4] Cancel\n--> "))
        if choice == 1 and active_theme == 'flow' or choice == 3 and active_theme == 'classic' or choice == 2 and active_theme == 'basic':
            print("\nThat theme is already in use. Please select a different one to use.")
            switch_theme_dialogue()
        elif choice == 1 and not basic_graphics_enabled and active_theme != 'flow':
            theme_to_apply = 'flow'
        elif choice == 1 and basic_graphics_enabled:
            print("\nYou can't use the Flow theme because Basic Graphics mode is enabled. Disable Basic Graphics mode first in \n'Settings > Graphics > Basic Graphics Mode', and try again.")
            switch_theme_dialogue()
        elif choice == 2 and active_theme != 'basic':
            theme_to_apply = 'basic'
        elif choice == 3 and active_theme != 'classic':
            theme_to_apply = 'classic'
        elif choice == 4:
            graphics_settings()
        else:
            print("\nPlease select a valid option.")
            switch_theme_dialogue()
        apply_new_theme(theme_to_apply)
    except ValueError:
        switch_theme_dialogue()


def graphics_settings():
    global basic_graphics_enabled, classic_theme_enabled
    if basic_graphics_enabled == [True]:
        basic_graphics_enabled = True
    if basic_graphics_enabled == [False]:
        basic_graphics_enabled = False
    print(generate_header("GRAPHICS SETTINGS"))
    print("1] Change Theme\n2] Basic Graphics Mode")
    if generate_seperator():
        print(generate_seperator())
    try:
        choice = int(input("3] Cancel\n--> "))
        if choice == 1:
            switch_theme_dialogue()
        elif choice == 3:
            print(" ")
            settings()
        elif choice == 2:
            ask_basic_graphics()
        else:
            raise ValueError
    except ValueError:
        invalid_selection_message()
        graphics_settings()


def launch_bug_report(diagnostic_data, description, e):
    global classic_theme_enabled
    bug_report_info = diagnostic_data   # Get diagnostic data, to display to the user.
    if description and e is not None:   # Description and e are not none if this screen was accessed through the error handler.
        bug_report_info = f"{generate_seperator()}\n{bug_report_info}\n\nERROR DETAILS:\n{description}\n{e}\n{generate_seperator()}"  # Format the data - add header and footer bars, crash details, and diagnostic data.
    else:
        bug_report_info = f"{generate_seperator()}\n{bug_report_info}\n{generate_seperator()}"    # Again, format data - no crash details necessary here as this is what is shown when the user manually initiates a bug report through the Settings menu.
    print(f"\nPlease copy and paste the following into your bug report: \n\n{bug_report_info}\n")   # Print the formatted data along with a message.
    try:
        choice = int(input("\nThe above information contains important details (such as which version of DTD you are using), which\nmassively helps when fixing bugs. When you are ready to continue, select the relevant option below.\n\n1] I have copied it, continue\n2] Cancel\n--> "))
        if choice == 1:
            webbrowser.open('https://github.com/mlaude545/DeathTrap-Dungeon/issues/new')    # Launch the bug report page.
        elif choice == 2:
            pass    # Do nothing - the function after this screen was called is loaded instead.
        else:
            invalid_selection_message()
            launch_bug_report(diagnostic_data, description, e)
        if description is None and e is None:
            settings()
        else:
            handle_error(description, e)
    except ValueError:
        invalid_selection_message()
        launch_bug_report(diagnostic_data, description, e)


def bug_report():
    print(generate_header('REPORT A BUG'))
    print("Found a bug? Select 'Report a Bug Online' to let the developers know!")
    try:
        choice = int(input("1] Report a Bug Online\n2] Cancel\n--> "))
        if choice == 1:
            launch_bug_report(diagnostic_data=str(get_diagnostics()), description=None, e=None)
        else:
            print(" ")
            settings()
    except ValueError:
        bug_report()


def apply_default_settings():
    global no_pygame, auto_applied_basic_graphics, sound_directory_error
    try:
        choice = int(input("\nAll settings will be reset to default, are you sure you'd like to continue?\n1] Yes\n2] No\n--> "))
        if choice == 1:
            print("Resetting...")
            try:
                cwd = os.getcwd()
                if os.path.exists(cwd+'/config'):
                    shutil.rmtree(cwd+"/config")
            except Exception as e:
                print(e)
            if not no_pygame and not sound_directory_error and not auto_applied_basic_graphics:
                print("All settings have been reset to default.")
                time.sleep(0.5)
                advanced_settings()
            else:
                print("\nAll settings were reset to default, except for the following:")
                if auto_applied_basic_graphics:
                    print("- Basic Graphics mode couldn't be disabled because your system can't render standard graphics.")
                if no_pygame:
                    print("- Audio couldn't be unmuted because the Pygame module is not installed.")
                if sound_directory_error:
                    print("- Audio couldn't be unmuted because there was an error accessing audio data.")
                print("\nFor more information, please visit: https://reubenparfrey.wixsite.com/deathtrapdungeon/help/")
                time.sleep(0.5)
                advanced_settings()
        else:
            advanced_settings()
    except ValueError:
        apply_default_settings()


def refresh():
    print("\nUse this option to remove unneeded data files, logs, and other temporary files. This can help improve \nperformance, or fix certain issues. Please note that some settings may be reset to default.")
    try:
        choice = int(input("1] Refresh\n2] Cancel\n--> "))
        if choice == 1:
            print("Working...")
            count = 0
            files_to_remove = ["savedprefs.dat", "displaysettings.dat", "crash.log", "graphicsproperties.dat",
                               "updateprefs.dat", "startup.dat", "config/updateprefs.dat", "config/update_configuration.dat",
                               "temp/latest_stable_ver.txt", "sdbackup.dat", "sdbackup2.dat", "sdbackup3.dat",
                               "temp/release_notes.txt"]    # List of files that aren't necessary.
            for file in files_to_remove:
                try:
                    os.remove(file)  # Remove the item
                    count += 1  # Increment a count to display to the user.
                except Exception:
                    pass
            if count == 1:
                print("Refresh complete! " + str(count) + " unneeded file was erased.")
            else:
                print("Refresh complete! " + str(count) + " unneeded files were erased.")
            advanced_settings()
        else:
            advanced_settings()
    except Exception:
        refresh()


def advanced_about():   # Exposes advanced game info to the player - this is mostly used for debugging purposes.
    print(generate_header("GAME INFO"))
    print(get_diagnostics())
    if generate_seperator():
        print(generate_seperator())
    time.sleep(0.5)
    advanced_settings()


def advanced_settings():
    print(generate_header("ADVANCED SETTINGS"))
    print("1] Refresh\n2] Default Settings\n3] View detailed game info\n4] Delete a save file")
    if generate_seperator():
        print(generate_seperator())
    try:
        choice = int(input("5] Cancel\n--> "))
    except ValueError:
        advanced_settings()
    if choice == 2:
        apply_default_settings()
    elif choice == 1:
        refresh()
    elif choice == 3:
        advanced_about()
    elif choice == 4:
        erase_save_data()
    elif choice == 5:
        settings()
    else:
        print("\nPlease select a valid option.")
        advanced_settings()


def save_gameplay_settings():
    global disable_critical, player_only_critical, enemy_only_critical, disableOverwrite, skip_overwrite_confirmation
    save_settings('gameplay_settings', [disable_critical, player_only_critical, enemy_only_critical, disableOverwrite, skip_overwrite_confirmation])
    print("\nDone!")
    gameplay_settings()


def savefile_settings():
    global skip_overwrite_confirmation, disableOverwrite
    selectedOne = False
    selectedTwo = False
    selectedThree = False
    print("\nWhen attempting to overwrite existing save files, the game should...")
    if skip_overwrite_confirmation is False and disableOverwrite is False:
        print("1] Always ask for confirmation (Default) [*]")
        selectedOne = True
    else:
        print("1] Always ask for confirmation (Default) [ ]")
    if skip_overwrite_confirmation is True:
        print("2] Never ask for confirmation [*]")
        selectedTwo = True
    else:
        print("2] Never ask for confirmation [ ]")
    if disableOverwrite is True:
        print("3] Prevent the save file from being overwritten [*]")
        selectedThree = True
    else:
        print("3] Prevent the save file from being overwritten [ ]")
    try:
        choice = int(input("4] Cancel\n--> "))
    except ValueError:
        savefile_settings()
    if choice == 4:
        gameplay_settings()
    elif choice == 1 and selectedOne:
        print("This option is already selected.")
        savefile_settings()
    elif choice == 2 and selectedTwo:
        print("This option is already selected.")
        savefile_settings()
    elif choice == 3 and selectedThree:
        print("This option is already selected.")
        savefile_settings()
    elif choice == 1:
        skip_overwrite_confirmation = False
        disableOverwrite = False
        save_gameplay_settings()
    elif choice == 2:
        skip_overwrite_confirmation = True
        disableOverwrite = False
        save_gameplay_settings()
    elif choice == 3:
        skip_overwrite_confirmation = False
        disableOverwrite = True
        save_gameplay_settings()
    else:
        print("\nPlease select a valid option.")
        savefile_settings()


def critical_hit_settings():
    global disable_critical, player_only_critical, enemy_only_critical
    print("\nChoose who can land critical hits during gameplay. This option will affect all save files.")
    selectedOne = False
    selectedTwo = False
    selectedThree = False
    selectedFour = False
    if disable_critical is False and player_only_critical is False and enemy_only_critical is False:
        print("1] Both players and enemies can land critical hits (default) [*]")
        selectedOne = True
    else:
        print("1] Both players and enemies can land critical hits (default) [ ]")
    if disable_critical:
        print("2] Nobody can land critical hits [*]")
        selectedTwo = True
    else:
        print("2] Nobody can land critical hits [ ]")
    if player_only_critical:
        print("3] Only I can land critical hits [*]")
        selectedThree = True
    else:
        print("3] Only I can land critical hits [ ]")
    if enemy_only_critical:
        print("4] Only enemies can land critical hits [*]")
        selectedFour = True
    else:
        print("4] Only enemies can land critical hits [ ]")
    try:
        choice = int(input("5] Cancel\n--> "))
    except ValueError:
        critical_hit_settings()
    if choice == 1 and selectedOne:
        print("This option is already selected.")
        critical_hit_settings()
    elif choice == 2 and selectedTwo:
        print("This option is already selected.")
        critical_hit_settings()
    elif choice == 3 and selectedThree:
        print("This option is already selected.")
        critical_hit_settings()
    elif choice == 4 and selectedFour:
        print("This option is already selected.")
        critical_hit_settings()
    elif choice == 1:
        if disable_critical:
            disable_critical = False
        if player_only_critical:
            player_only_critical = False
        if enemy_only_critical:
            enemy_only_critical = False
        save_gameplay_settings()
    elif choice == 2:
        if player_only_critical:
            player_only_critical = False
        if enemy_only_critical:
            enemy_only_critical = False
        disable_critical = True
        save_gameplay_settings()
    elif choice == 3:
        if disable_critical:
            disable_critical = False
        if enemy_only_critical:
            enemy_only_critical = False
        player_only_critical = True
        save_gameplay_settings()
    elif choice == 4:
        if disable_critical:
            disable_critical = False
        if player_only_critical:
            player_only_critical = False
        enemy_only_critical = True
        save_gameplay_settings()
    elif choice == 5:
        gameplay_settings()
    else:
        print("Please select a valid option.")
        critical_hit_settings()


def gameplay_settings():
    print(generate_header("GAMEPLAY SETTINGS"))
    print("1] Save File Options\n2] Critical Hits")
    if generate_seperator():
        print(generate_seperator())
    try:
        choice = int(input("3] Cancel\n--> "))
    except ValueError:
        gameplay_settings()
    if choice == 1:
        savefile_settings()
    elif choice == 2:
        critical_hit_settings()
    elif choice == 3:
        settings()
    else:
        print("\nPlease choose a valid option.")
        gameplay_settings()


def save_settings(file_name, data_to_save):     # This function receives the name of the data file to write to and the
    cwd = os.getcwd()                           # actual data itself, then stores it. This function is modular, which saves
    data_directory = cwd + '/config'            # me repeating the save code over and over again.
    if not os.path.exists(data_directory):
        os.mkdir(data_directory)    # Make a config directory if it doesn't exist.
    try:
        with open(data_directory+'/'+file_name+'.dat', 'wb') as f:
            pickle.dump(data_to_save, f, protocol=2)
    except Exception:
        pass


def settings():
    global auto_updates_disabled, internal_identifier, is_beta, basic_graphics_enabled
    if not basic_graphics_enabled and active_theme == 'flow':
        print(r""" 
 █ SETTINGS: ░▒▒███████████████████
█  [1] Sound                       █
█  [2] Graphics                    █
█  [3] Software Updates            █
█  [4] Gameplay                    █
█  [5] Report A Bug                █
█  [6] Advanced                    █
█  [7] Exit                        █
 ██████████████████████████████████""")
    if basic_graphics_enabled is True or active_theme != 'flow':
        print(generate_header('SETTINGS'))
        print(r"""1] Sound
2] Graphics
3] Software Updates
4] Gameplay
5] Report A Bug
6] Advanced""")
        if generate_seperator():
            print(generate_seperator())
        print("7] Exit")
    try:
        user_input = int(input("--> "))
        if user_input == 1:
            audio_settings()
        elif user_input == 2:
            graphics_settings()
        elif user_input == 3:
            software_update_settings()
        elif user_input == 4:
            gameplay_settings()
        elif user_input == 5:
            bug_report()
        elif user_input == 7:
            menu()
        elif user_input == 6:
            advanced_settings()
        else:
            raise ValueError
    except ValueError:
        invalid_selection_message()
        settings()


def story():
    print(
        "\nThe land of Medway was a quiet and soothing place. Day in and day out, people went about the mundanities of life with little more than a care in")
    time.sleep(1.5)
    print(
        "the world. The ruler of this land, Emperor Juniper, was a kind and gentle man... until one day, something changed. He isolated himself")
    time.sleep(1.5)
    print(
        "from everyone, and threw anyone who questioned his dangerous antics into the darkest, most desolate dungeon in the land. You were one of")
    time.sleep(1.5)
    print(
        "the many poor souls left to rot, and you, like many others, can't survive much longer on the scraps the guards feed all the inmates. What caused")
    time.sleep(1.5)
    print(
        "the downfall of Medway? Can you escape, put an end to Emperor Juniper's reign of terror, and return Medway to it's former glory? Only time will tell...\n")
    time.sleep(5)
    player_name_input()


def chapter_1_run():
    try:
        choice = int(input("\nAs you round the corner, you come to a fork in the passage. You must decide which way to go! Left or right? (1 for left, 2 for right):"))
        if choice == 1:
            print("\nYou decide to go left! As you round another corner, your heart sinks; you can see a heavy iron door blocking your path! You try to pull it \nopen but to no avail. It's jammed!")
            time.sleep(1.75)
            print(" ")
            print(
                "You can hear the echoing footsteps getting closer now, reverberating off the stone walls. You drop to the ground as the guard rounds the \ncorner. He cocks his gun...")
            time.sleep(1.75)
            game_over()
        elif choice == 2:
            print(" ")
            print(
                "You go right!! As you race down the grimy stone corridor, your heart drops; you can see a congestion of guards gathered at the bottom, their guns \ntrained on you.")
            print(" ")
            time.sleep(1.75)
            print("You sink to the ground in dismay and despair. There's no escape...")
            game_over()
        else:
            raise ValueError
    except ValueError:
        invalid_selection_message()
        chapter_1_run()


def choice3():
    global player
    global mute_audio, expert_mode_enabled, debug
    try:
        choice = int(
            input("\nDo you let the guard take you to solitary confinement? [1] Or do you make a break for it? [2] "))
        if choice == 1:
            time.sleep(0.75)
            print("\nYou are dragged to solitary confinement, and the heavy iron door is slammed shut behind you.")
            time.sleep(1)
            if expert_mode_enabled is False:
                time.sleep(1)
                player.set_save_location(1)
                ask_save()
            else:
                time.sleep(1)
                choice4()
        elif choice == 2:
            print(
                "\nYou start running! As you run down the grimy corridor, you can hear the rapid slams of footsteps behind you; the guard is hot on your tail.")
            time.sleep(1)
            chapter_1_run()
        else:
            raise ValueError
    except ValueError:
        invalid_selection_message()
        choice3()


def second_choice_alternate():
    global expert_mode_enabled, player
    print(
        "\nA nearby guard spots the commotion and comes running over with backup. There are too many guards to take on alone!")
    time.sleep(1)
    print(
        "\nThe guards roughly grasp you, yelling something about solitary confinement. Looks like that's where you're headed next...")
    time.sleep(2)
    player.set_save_location(1)
    time.sleep(3)
    if not expert_mode_enabled:
        ask_save()
    else:
        choice4()


def choice2():
    global item
    global enemy_ID, debug
    enemy_ID = 1
    time.sleep(1.5)
    try:
        dropSaw = int(input(
            "\nYou eye up the shard of glass. You can either threaten the guard [1], or wave the shard around and scream like a maniac [2]."))
    except ValueError:
        print(" ")
        print("Bad input. Only integers can be entered!")
        choice2()
    if dropSaw == 1:
        print("\nYou begin to shout at the guard, he turns.")
        time.sleep(1.25)
        print("\nYou raise the shard, and he raises his weapon...")
        time.sleep(1.5)
        encounter_enemy('guard')
    elif dropSaw == 2:
        time.sleep(0.75)
        print(
            "\nYou decide to scream and wave the glass shard around. The nearby guard turns and makes his way over to your cell, muttering something \nabout putting you into solitary confinement.")
        time.sleep(1.5)
        choice3()


def chapter_1_first_choice():
    global player
    try:
        choice = int(
            input("\nWhat will you do? [1] to examine your surroundings further, [2] to try rattling the cell door. "))
        if choice == 1:
            print(
                "\nYou glance around, looking for anything that could aid you. You notice a shard of glass laying in one corner.")
            time.sleep(1.5)
            print("\nYou pocket it, sure it'll come in handy.")
            player.update_defensive_items('Shard of Glass')
            choice2()
        elif choice == 2:
            print(
                "\nYou rattle the cell door! But it's no use. The guard on the other side of the door doesn't even look at you.")
            time.sleep(1.5)
            chapter_1_first_choice()
        else:
            raise ValueError
    except ValueError:
        invalid_selection_message()
        chapter_1_first_choice()


def start_chapter_1():
    global debug
    global enemy_ID, basic_graphics_enabled
    enemy_ID = 1
    if not basic_graphics_enabled:
        try:
            print("\n█▒░ Chapter One: Enter The Dungeon ░▒█")
        except Exception:
            print("\n== Chapter One: Enter The Dungeon ==")
    else:
        print("\n== Chapter One: Enter The Dungeon ==")
    if not mute_audio:
        pygame.mixer.music.load("sfx/thud.ogg")
        pygame.mixer.music.play(1)
    time.sleep(3)
    print("\nYou slowly come to. You are lying on a hard, cold wireframe bed, in the corner of your dark cell.")
    time.sleep(1.5)
    print("\nHow long had you been here for? A week? A month? Certainly long enough to lose track of time.")
    time.sleep(1.5)
    print(
        "\nYou groan, and slowly stand up. You are malnourished and weak; you know that you won't survive here much longer.")
    time.sleep(1.5)
    print(
        "\nYou glance around at this all-too-familiar environment. A single iron barred door is the only point natural light enters.")
    time.sleep(1.5)
    print("\nThe floor is made entirely of concrete, and the walls are constructed of damp, mossy stone.")
    time.sleep(1.5)
    print("\nA guard stands on the other side of the door, his back turned towards you.")
    time.sleep(1.5)
    chapter_1_first_choice()


def extras_menu():                      # The extras menu! This contains most of the stuff you unlock when the game has been beaten.
    print(generate_header('EXTRAS'))
    print("Please choose an extra from the list below:\n1] Music Player\n2] Expert Mode")
    if generate_seperator():
        print(generate_seperator())
    try:
        choice = int(input("3] Cancel\n--> "))
        if choice == 1 and no_pygame is False and sound_directory_error is False:
            print(generate_header('MUSIC PLAYER'))
            print(
                "Listen to DeathTrap Dungeon's soundtrack! All the songs that play in-game can be heard here, as well as some never-before-heard beta tracks!\n")
            extras_music_player()
        elif choice == 1 and no_pygame is True:
            print(
                "\nMusic Player can't be accessed because the required module 'Pygame' is not installed. Please refer to the readme file, or get help\nonline at: https://reubenparfrey.wixsite.com/deathtrapdungeon/help/")
            extras_menu()
        elif choice == 1 and sound_directory_error is True:
            print(
                "\nMusic Player can't be accessed because audio data could not be loaded. See the error message displayed upon starting the game for more details.")
            extras_menu()
        elif choice == 2:
            print(generate_header("EXPERT MODE"))
            print("Up for a challenge? Try the game on Expert Mode! Expert Mode cranks the difficulty up to 11, and is designed to \ntest your skills. Do you have what it takes to conquer the ultimate DTD challenge?")
            time.sleep(0.5)
            load(extra_feature='expert')    # Set the extra_feature variable to 'expert' - this tells the load function that we want to play expert mode with the selected save, instead of loading is as normal.
        elif choice == 3:
            menu()
        else:
            invalid_selection_message()
            extras_menu()
    except ValueError:
        extras_menu()


def check_if_extras_unlocked():     # The game needs to have been beaten for Extras to unlock, so this function checks if the game has been beaten.
    data_files = ['data/savedata.dat', 'data/savedata2.dat', 'data/savedata3.dat']  # Each of the data files that can exist
    can_load_extras = False
    for file in data_files:     # Load each save file that exists.
        try:
            with open(str(file), 'rb') as f:
                player_name, save_location, damage, max_health, health, game_beaten, expert_mode_beaten, inventory, defensive_items = pickle.load(
                    f)
            if game_beaten:
                can_load_extras = True  # If the game has been beaten, set can_load_extras to True so the game knows this has been unlocked.
                break
        except Exception:   # Handle errors that can result when loading save files, such as missing files or corrupt data.
            pass
    if can_load_extras:
        extras_menu()
    else:
        print("\nYou need to beat the game before you can unlock extras! Come back when you have completed the main story.")
        menu()


def confirm_game_exit():
    try:
        choice = int(input("Are you sure you'd like to quit?\n1] Keep playing\n2] Quit\n--> "))
    except ValueError:
        confirm_game_exit()
    if choice == 1:
        menu()
    elif choice == 2:
        sys.exit(0)
    else:
        print("\nPlease choose a valid option.\n")
        confirm_game_exit()


def about():
    global basic_graphics_enabled, internal_identifier
    game_title = "\nDEATHTRAP DUNGEON by REUBEN PARFREY 2019-2024"
    about_screen = r"""
Most code and all of the story by Reuben Parfrey. Thanks to Charly Sly, Joe Parfrey and Georgia Wales    ▓▓▓▓▓   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
for helping me find and fix many bugs. And of course, thanks to you; the player. Enjoy the game!         ▓▓   ▓▓    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
All music and sound effects by Charly Sly.                                                               ▓▓    ▓▓     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
                                                                                                         ▓▓   ▓▓        ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
This game is released as Open Source software under the permissive MIT License - you can play the        ▓▓▓▓▓            ▓▓▓▓▓▓▓▓▓▓▓▓▓
game, modify the code, and redistribute it all free-of-charge. As such, this software comes with                    ▓▓▓▓▓▓  ▓▓▓▓▓▓▓▓▓▓▓
absolutely no warranty. You can view a full copy of the MIT License in the 'copying' file provided       ▓▓▓          ▓▓      ▓▓▓▓▓▓▓▓▓
with this game.                                                                                          ▓▓▓▓▓        ▓▓        ▓▓▓▓▓▓▓
                                                                                                         ▓▓▓▓▓▓▓      ▓▓          ▓▓▓▓▓
Want to stay connected? Follow @deathtrap_dungeon_official on Instagram - the official DTD page!         ▓▓▓▓▓▓▓▓▓    ▓▓            ▓▓▓
Or, if you prefer, you can follow me personally at @roo_parfrey on Instagram.                            ▓▓▓▓▓▓▓▓▓▓▓
                                                                                                         ▓▓▓▓▓▓▓▓▓▓▓▓▓         ▓▓▓▓▓
This game is dedicated to Stephen Chapple - so much of this game came about because of the influence     ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓       ▓▓   ▓▓
of this amazing person. Rest easy.                                                                       ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓     ▓▓    ▓▓
                                                                                                         ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓   ▓▓   ▓▓
Found a bug? Please be sure to report this using the 'Report a Bug' feature in the 'Settings' menu.      ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ ▓▓▓▓▓"""
    if basic_graphics_enabled:
        about_screen = r"""
Most code and all of the story by Reuben Parfrey. Thanks to Charly Sly, Joe Parfrey and Georgia Wales
for helping me find and fix many bugs. And of course, thanks to you; the player. Enjoy the game! 
All music and sound effects by Charly Sly.                                                               
                                                                                                         
This game is released as Open Source software under the permissive MIT License - you can play the              
game, modify the code, and redistribute it all free-of-charge. As such, this software comes with           
absolutely no warranty. You can view a full copy of the MIT License in the 'copying' file provided           
with this game.                                                                                         
                                                                                                        
Want to stay connected? Follow @deathtrap_dungeon_official on Instagram - the official DTD page!        
Or, if you prefer, you can follow me personally at @roo_parfrey on Instagram.                           
                                                                                                       
This game is dedicated to Stephen Chapple - so much of this game came about because of the influence  
of this amazing person. Rest easy.                                                                       
                                                                                                         
Found a bug? Please be sure to report this using the 'Report a Bug' feature in the 'Settings' menu.  
"""
    return str(game_title+"\n"+internal_identifier+"\n"+about_screen)


def menu():
    global debug, checked_for_update, basic_graphics_enabled, classic_theme_enabled, auto_applied_basic_graphics, mute_audio, is_beta
    data_format_daemon()
    if not auto_updates_disabled and not checked_for_update:
        checked_for_update = True   # This is a flag to stop the update check being called every time the menu is loaded. It's global so that it doesn't get reset every time the menu is called.
        check_for_updates(method_of_access='auto')
    if is_beta:
        print("\n== This is a beta copy of DTD - for testing only ==")
    if not basic_graphics_enabled and active_theme == 'flow':
        print(r"""
 █ MAIN MENU: ░▒▒██████████████████
█  [1] New Game                    █
█  [2] Load Saved Game             █
█  [3] Extras                      █
█  [4] Settings                    █
█  [5] About DeathTrap Dungeon     █
█  [6] Quit                        █ 
 ██████████████████████████████████ """)
    else:
        print("""+------------------------------+
|      DEATHTRAP DUNGEON       |
+------------------------------+
| [1] New Game                 |
| [2] Load Saved Game          |
| [3] Extras                   |
| [4] Settings                 |
| [5] About DeathTrap Dungeon  |
| [6] Quit                     | 
+------------------------------+""")
    try:
        user_input = int(input("--> "))
        if user_input == 1:
            if mute_audio:
                if not basic_graphics_enabled and not classic_theme_enabled:
                    try:
                        print("\n█▒░ Audio is muted ░▒█")
                    except Exception:
                        print("\n== AUDIO IS MUTED ==")
                else:
                    print("\n== AUDIO IS MUTED ==")
            print("\nWelcome to...")
            time.sleep(1.25)
            print(" ")
            if not basic_graphics_enabled:
                    print("""█████▄ ▓█████ ▄▄▄     ▄▄▄█████▓ ██░ ██ ▄▄▄█████▓ ██▀███   ▄▄▄       ██▓███      
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
            else:
                print(r"""    ____             __  __  ______                             
   / __ \___  ____ _/ /_/ /_/_  __/________ _____               
  / / / / _ \/ __ `/ __/ __ \/ / / ___/ __ `/ __ \              
 / /_/ /  __/ /_/ / /_/ / / / / / /  / /_/ / /_/ /              
/_____/\___/\__,_/\__/_/ /_/_/ /_/   \__,_/ .___/               
                        / __ \__  ______ /_/__ ____  ____  ____ 
                       / / / / / / / __ \/ __ `/ _ \/ __ \/ __ \
                      / /_/ / /_/ / / / / /_/ /  __/ /_/ / / / /
                     /_____/\__,_/_/ /_/\__, /\___/\____/_/ /_/ 
                                       /____/                   """)
            if not mute_audio:
                try:
                    pygame.mixer.music.load('sfx/dtd_main.ogg')
                    pygame.mixer.music.play(1)
                except Exception:
                    print("\n\n* An unknown error occurred when loading audio - audio has been muted *\n")
                    mute_audio = True
            time.sleep(3)
            story()
        elif user_input == 2:
            load(extra_feature=None)
        elif user_input == 3:
            check_if_extras_unlocked()
        elif user_input == 6:
            confirm_game_exit()
        elif user_input == 5:
            print(str(about()))
            menu()
        elif user_input == 4:
            settings()
        elif user_input == 7:
            warp_debug()
        else:
            print("\nPlease choose a valid option.")
            menu()
    except ValueError:
        invalid_selection_message()
        menu()


if __name__ == '__main__':
    menu()  # Load the menu, which starts the game.
