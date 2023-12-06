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

def textMenu(textChoice):
    while (True):
        textChoice = ui.menu('''\nEnter a number from the text menu
                \n0: Back
                \n1: Exit
                \n2: Type Text
                \n3: Chose file
                \n''')
    
        if (textChoice == 0):
            return 0, 0
        elif (textChoice == 1):
            return 1, 1
        elif (textChoice == 2):
            return 2, input("Enter Text:\n")
        elif (textChoice == 3):
            while (True):
                loc = input("Enter location and file name (Ex: .\\example.txt or C:/Users/user/Desktop/example.txt):\n")
                if (loc.lower() == "exit"):
                    return 1, 1
                elif (loc.lower() == "back"):
                    break
                elif (os.path.isfile(loc)):
                    return 3, loc
                else:
                    print("Invalid location or file name")
            

def encrypterMenu():
    while (True):
        choice = ui.menu('''\nEnter a number from the encrypter menu
                    \n0: Back
                    \n1: Exit
                    \n2: Default Encrypt
                    \n3: Quick Encrypt
                    \n4: Long Encrypt
                    \n5: Encrypt with just RSA
                    \n6: Default Encrypt with RSA
                    \n7: Quick Encrypt with RSA
                    \n8: Long Encrypt with RSA
                    \n9: Custom Encrypt
                    \n10: Define Default, Quick, and Long settings
                    \n''')
    
        if (choice == 0):
            return 0
        elif (choice == 1):
            return 1
        
        textChoice, text = textMenu()
        if (textChoice == 1):
            return 1
        elif (textChoice == 0):
            continue
        elif (choice == 2):
            if (textChoice == 2):
                encrypt(text = text, isPassword = True)
            elif (textChoice == 3):
                encrypt(locText = text, isPassword = True)
            else:
                print("Error choice selection: textChoice",textChoice)
        elif (choice == 3):
            if (textChoice == 2):
                encrypt(layers = 2, sizeMulti = 1, text = text)
            elif (textChoice == 3):
                encrypt(layers = 2, sizeMulti = 1, locText = text)
            else:
                print("Error choice selection: textChoice",textChoice)
        elif (choice == 4):
            if (textChoice == 2):
                encrypt(layers = 2, sizeMulti = 1, text = text)
            elif (textChoice == 3):
                encrypt(layers = 2, sizeMulti = 1, locText = text)
            else:
                print("Error choice selection: textChoice",textChoice)

encrypt(layers = 3, sizeMulti = 0, text = "", locText = "", locSave = "", isPassword = False, isRSA = False, mainkey = "", genkey = 0):
def decrypterMenu():
    return 0

def rsakeyMenu():
    while (True):
        choice = ui.menu('''\nEnter a number from the Settings menu
                \n0: Back
                \n1: Exit
                \n2: Display Keys
                \n3: Make new Keys
                \n''')
        
        if (choice == 0):
            return 0
        elif (choice == 1):
            return 1
        elif (choice == 2):
            pubkeys, prikeys = importKeys()
            menuStr = '''\nEnter a number from the menu
                \n0: Back
                \n1: Exit
                \n'''
            for key in pubkeys:
                menuStr += "public_" + key + "\n"
            for key in prikeys:
                menuStr += "private_" + key + "\n"
            if (1 == ui.menu(menuStr)):
                return 1
        elif (choice == 3):
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
