from tools import setManipulator as sm
from tools import tempGenerator as tg
from tools import recTool as rt
from tools import keyGenerator as rkg
from tools import encrypter as e
from tools import decrypter as d
from ui import ui
import os
import random
import importlib
import hashlib
import json
import codecs


def encrypterMenu(choice):
    return 0

def decrypterMenu(choice):
    return 0

def rsakeyMenu(choice):
    while (True):
        choice = ui.menu('''\nEnter a number from the Settings menu
                \n0: Back
                \n1: Exit
                \n2: Display Keys
                \n3: Make new Keys
                \n''')
        
        choice = choice.split(".")
        if (choice[0] == 0):
            return 0
        elif (choice[0] == 1):
            return 1
        elif (choice[0] == 2):
            choice.pop(0)
            pubkeys, prikeys = importKeys()
            menuStr = '''\nEnter a number from the Settings menu
                \n0: Back
                \n1: Exit
                \n'''
            for key in pubkeys:
                menuStr += "public_" + key + "\n"
            for key in prikeys:
                menuStr += "private_" + key + "\n"
            if (1 == ui.menu(menuStr)):
                return 1
        elif (choice[0] == 3):
            choice.pop(0)
            name = input("Enter the key names: ")
            rkg.genKeys(name)

def selectSetting(setChoice):
    setList = sm.returnInfo(0)
    menuList = '''\nEnter a number from the Settings menu
                \n0: Back
                \n1: Exit
                \n2: All
                \n'''
    for i, set in enumerate(setList):
        menuList += str(i+3) + ": " + set + "\n"
    
    return ui.menu(menuList)

def settingsMenu(choice):
    while (True):
        choice = ui.menu('''\nEnter a number from the Settings menu
                \n0: Back
                \n1: Exit
                \n2: Display
                \n3: Edit
                \n4: Export
                \n5: Import
                \n''')
        
        choice = choice.split(".")
        if (choice[0] == 0):
            return 0
        elif (choice[0] == 1):
            return 1
        
        setChoice = selectSetting()
        if (setChoice[0] == 0):
            return 0
        elif (setChoice[0] == 1):
            continue
        elif (choice[0] == 2):
            if (setChoice == 2):
            else:
                sm.display(setChoice-3)
        elif (choice[0] == 3):
            choice.pop(0)
            choice = decrypterMenu(".".join(choice))
        elif (choice[0] == 4):
            choice.pop(0)
            choice = rsakeyMenu(".".join(choice))
        elif (choice[0] == 5):
            choice.pop(0)
            choice = settingsMenu(".".join(choice))
        
        if (choice == 1):
            return 0
    return 0

def mainMenu():
    while (True):
        choice = ui.menu('''\nEnter a number from the menu
                \n1: Exit
                \n2: Encrypt
                \n3: Decrypt
                \n4: RSA Keys
                \n5: Settings
                \n''')
        
        choice = choice.split(".")
        if (choice[0] == 1):
            return 0
        elif (choice[0] == 2):
            choice.pop(0)
            choice = encrypterMenu(".".join(choice))
        elif (choice[0] == 3):
            choice.pop(0)
            choice = decrypterMenu(".".join(choice))
        elif (choice[0] == 4):
            choice.pop(0)
            choice = rsakeyMenu(".".join(choice))
        elif (choice[0] == 5):
            choice.pop(0)
            choice = settingsMenu(".".join(choice))
        
        if (choice == 1):
            return 0

mainMenu()