

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