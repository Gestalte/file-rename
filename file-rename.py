import os
import re 

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
    return input.title()

def ruleTrim(input:str):
    return input.strip()

rules = [
    ruleReplaceDash,
    ruleReplaceUnderscore,
    ruleReplacePeriod,
    ruleTitleCase,
    ruleTrim
]

def renameFile(inputName:str):
    newName:str = inputName
    for rule in rules:
        newName = rule(newName)
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