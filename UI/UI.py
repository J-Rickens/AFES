

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

def getInt(prompt, min = 0, max = 999999999):
    if (max < min):# check if max is less then min and switch if needed
        temp = max
        max = min
        min = max
    
    uchoice = ""
    flag = True
    while (flag):# loops till between min and max values
        uchoice = " "
        while(uchoice.isdigit() == False):# loops till the entry is a digit
            uchoice = input(prompt)# Ask user and display menu
            if (uchoice.lower() == "exit"):# check if the user want to exit
                return 1
            elif (uchoice.lower() == "back"):# check if user want to go back
                return 0
            if (uchoice.isdigit() == False):# provides an error statment if not digit
                print("Please enter just the number.")
        uchoice = int(uchoice)# provides an error statment if not a valid number
        if(uchoice >= min and uchoice <= max):
            flag = False
        else:
            print("Please enter a number between", min, "and", max, ".")
    return uchoice
        


