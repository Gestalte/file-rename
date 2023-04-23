import os
import re 

# TODO: Handle editions i.e 1st, 2nd etc. so that they don't come out as 1St, 2Nd etc.
# TODO: Accept a list of acronyms/exceptions that should conform to a specific format. i.e. WPF instead of Wpf and .NET instead of Net

specialCases = [".NET","WPF","GUI","SQL"]

def getSpecialCases(input:str):
    output = []
    for case in specialCases:
        if case == input:
            output.append(case)

class Renamable:
    def __init__(self,name):
        self.beforeName = name
        self.specialCases = getSpecialCases(name)

def ruleReplaceDash(input:str):
    return input.replace("-"," ")
    
def ruleReplaceUnderscore(input:str):
    return input.replace("_"," ")

def ruleReplacePeriod(input:str):
    splits = input.split(".")
    nameSplit = splits[0:len(splits)-1]
    extension = splits[len(splits)-1:len(splits)][0]
    name = " ".join(nameSplit)
    return  name + "." + extension

def ruleTitleCase(input:str):
    splits = input.split(".")
    return splits[0].title() + "." + splits[1]

def ruleTrim(input:str):
    return input.strip()

rules = [
    ruleReplaceDash,
    ruleReplaceUnderscore,
    ruleReplacePeriod,
    ruleTitleCase,
    ruleTrim
]

def saveSpecialCases(input:str):
    output = []
    count = 0
    input = input.lower()
    for case in specialCases:
        if input.find(case.lower()) != -1:
            placeholder = "§" + str(count)
            count = count + 1
            input = input.replace(case.lower(),placeholder)
            output.append((placeholder,case))
    print("input",input)
    print("output",output)
    return (input, output)

def renameFile(inputName:str):
    print("inputName",inputName)
    specials = saveSpecialCases(inputName)
    newName:str = str(specials[0])
    for rule in rules:
        newName = rule(newName)
        print("newName",newName)
    for special in specials[1]:
        newName = newName.replace(special[0],special[1])
        print("newName",newName)
    #os.rename(inputName, newName)

def renameAll():
    names = os.listdir()
    for name in names:
        if name != ".git" and name != ".vscode" and name != "file-rename.py":
            renameFile(name)

def main(argv):
    if len(argv) == 1:
        renameAll()

if __name__ == '__main__':
    import sys
    main(sys.argv)