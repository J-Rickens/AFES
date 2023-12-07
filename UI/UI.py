

# give menu options following proper format
# it will prompt user for their choice and ensure it is a listed choice
def menu(menuText):
    uchoice = ""
    menuNumList = menuText.split('\n')# split by menu option
    numList = []
    for id, line in enumerate(menuNumList):# determin valid number options
        menuNumList[id] = line.split(':')
        if(menuNumList[id][0].isdigit()):
            numList.append(int(menuNumList[id][0]))
    
    while(uchoice not in numList):# menu loop (loops till there is a valid entry)
        uchoice = " "
        while(uchoice.isdigit() == False):# loops till the entry is a digit
            uchoice = input(menuText)# Ask user and display menu
            if(uchoice.isdigit() == False):# provides an error statment if not digit
                print("Please enter just the number.")
        uchoice = int(uchoice)# provides an error statment if not a valid number
        if(uchoice not in numList):
            print("Please enter only the numbers provided")
    return int(uchoice)

def getNum(prompt, min = 0, max = 999999999, isInt = True):
    if (max < min):# check if max is less then min and switch if needed
        temp = max
        max = min
        min = max
    
    uchoice = ""
    flag1 = True
    while (flag1):# loops till between min and max values
        flag2 = True
        while(flag2):# loops till the entry is a digit and is int if isInt
            uchoice = input(prompt)# Ask user and display menu
            if (uchoice.lower() == "exit"):# check if the user want to exit
                return "exit"
            elif (uchoice.lower() == "back"):# check if user want to go back
                return "back"
            if (isInt):# check if input is int or double based on isInt
                try:
                    uchoice = int(uchoice)
                    flag2 = False
                except ValueError:
                    print("Please enter just the number (int).")
                    flag2 = True
            else:
                try:
                    uchoice = double(uchoice)
                    flag2 = False
                except ValueError:
                    print("Please enter just the number (float).")
                    flag2 = True

        if(uchoice >= min and uchoice <= max):# check if num in range
            flag1 = False
        else:# provides an error statment if not in range
            print("Please enter a number between", min, "and", max, ".")
    return uchoice

def getLoc(isExist = True):
    while (True):
        loc = input("Enter location and file name (Ex: .\\example.txt or C:\\Users\\user\\Desktop\\example.txt):\n")
        if (loc.lower() == "exit"):
            return 1
        elif (loc.lower() == "back"):
            return 0

        elif (isExist):
            if (os.path.isfile(loc)):# check if file and path exist
                return loc
            else:
                print("Invalid location or file name")

        elif (not isExist):
            if (os.path.isfile(loc)):# check if file and path exist
                return loc
            else:
                loc = loc.split("\\")# split the file and path to check if file is valid name and path
                path = "\\".join(loc[:-1])
                if (not os.path.exists(path)):# check if path exist
                    print("Invalid location path (must use \\)")
                    continue
                file = loc[-1].split(".")
                if (len(file) == 2):
                    return "\\".join(loc)
                else:
                    print("Invalid filename")


