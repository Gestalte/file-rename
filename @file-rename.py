import os
import re

# List of acronyms/exceptions that should conform to a specific format
# i.e. WPF instead of Wpf and .NET instead of Net
# Compound form like ASP.NET has to come before standalone form like ASP and .NET
specialCases = [
    "ASP.NET", ".NET", "ASP", "WPF", "GUI",
    "SQL", "SQLite", "JS", "PHP", "IO",
    "MVC", "APIs", "API", "AI", "HTML5",
    "HTML", "LoRa", "MicroPython", "IoT",
    "LLM", "EF", "TCP", "IP", "DuckDB"
]

ordinalIndicaters = ["st", "rd", "th"]


def ruleReplaceHex92(input: str):
    split = tuple(input.rsplit(".", 1))
    extension = split[1]
    name = split[0]
    name = name.replace("’", "'")
    return name + "." + extension


def ruleAnnaTruncateAfterDoubleDash(input: str):
    split = tuple(input.rsplit(".", 1))
    extension = split[1]
    name = split[0]
    while True:
        index = name.rfind("--")
        if index == -1:
            break
        name = name[0:index]
    return name + "." + extension


def ruleRemoveBracketContent(input: str):
    split = tuple(input.rsplit(".", 1))
    extension = split[1]
    name = split[0]
    while True:
        index = name.rfind("(")
        if index == -1 or index == 0:
            break
        name = name[0:index]
    return name + "." + extension


def ruleReplaceDash(input: str):
    return input.replace("-", " ")


def ruleReplaceUnderscore(input: str):
    return input.replace("_", " ")


def ruleReplacePeriod(input: str):
    splits = input.split(".")
    nameSplit = splits[0:len(splits)-1]
    extension = splits[len(splits)-1:len(splits)][0]
    name = " ".join(nameSplit)
    return name + "." + extension


def ruleTitleCase(input: str):
    splits = input.split(".")
    return splits[0].title() + "." + splits[1]


def rulePreserveApostrophe(input: str):
    split = tuple(input.rsplit(".", 1))
    extension = split[1]
    name = split[0]
    newName = name.replace("'S", "'s")
    return newName + "." + extension


def ruleOrdinalIndicatorCase(input: str):
    var = input
    for rTup in re.findall(r"(\d(Nd|Rd|Th))", input):
        var = var.replace(rTup[0], rTup[0].lower())
    return var


def ruleTrim(input: str):
    splits = input.split(".")
    extension = splits[1].strip()
    name = splits[0]
    nameSplits = name.split(" ")
    outputList = []
    for s in nameSplits:
        s = s.strip()
        if s != "":
            outputList.append(s)
            s = s + " "
            print("nameSplit", s)
    newName = " ".join(outputList)
    return newName  + "." + extension 


rules = [
    ruleAnnaTruncateAfterDoubleDash,
    #ruleRemoveBracketContent,
    ruleReplaceHex92,
    ruleReplaceDash,
    ruleReplaceUnderscore,
    ruleReplacePeriod,
    ruleTitleCase,
    ruleOrdinalIndicatorCase,
    rulePreserveApostrophe,
    ruleTrim
]


def saveSpecialCases(input: str):
    output = []
    count = 0
    split = tuple(input.rsplit(".", 1))
    nameOnly = split[0].lower()
    for case in specialCases:
        pattern = "(^|\\s)" + case.lower() + "(\\s|$)"
        if re.search(pattern, nameOnly):
            placeholder = "§" + str(count)
            count = count + 1
            nameOnly = nameOnly.replace(case.lower(), placeholder)
            output.append((placeholder, case))
    print("input", nameOnly, "SpecialCases:", output)
    return (nameOnly + "." + split[1], output)


def renameFile(inputName: str):
    print("inputName", inputName)
    specials = saveSpecialCases(inputName)
    newName: str = str(specials[0])
    for rule in rules:
        alteredName = rule(newName)
        if newName != alteredName:
            print("newName", newName, "rule:", rule.__name__)
        newName = alteredName
    for special in specials[1]:
        newName = newName.replace(special[0], special[1])
        print("newNameWithSpecials", newName, "special:", special)
    print()
    os.rename(inputName, newName)


def renameAll():
    names = os.listdir()
    for name in names:
        if name != ".git" and name != ".vscode" and name != "@file-rename.py":
            renameFile(name)


def main(argv):
    if len(argv) == 1:
        renameAll()


if __name__ == '__main__':
    import sys
    main(sys.argv)
