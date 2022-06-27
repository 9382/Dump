r""" aidan9382
The purpose of this script is to compare 2 regex search patterns and determine if one is covered on all cases by the other
This can help remove duplicate occurances or redundant entires within a large regex set

This is an absolute mess of specific rules and intertwined madness of edge case checks
While it works on like, 99% of scenarios, its likely inefficient
Notes / TODO:
* Doesnt support capture groups references (\1 | &1)
* Is weird with start/end identifiers (^ and $) (Could force a check with a \0 (null) at the start or end if no ^ or $?)
* No support for specials (like ., \w, \d) or Selection ranges ([X-Y])

Features:
* Supports regular text and escaped specials
* Supports the +, *, ?, and {} repitition characters
* Supports [] and () groups (mostly) with repitition

While capture group references are doable, we need to somehow pick them up
 (maybe scan the normal+beforeSpecial for a \\\\(\d+|[wWdDsS]) or something)

If you do use this, make sure to give it some manual scrutiny, because it needs it
"""

__all__ = ["compare","compareSet"]
import re as regex
#We use the regex to parse the regex

def _generatePossibles(current,characterset):
    newset = []
    for possibility in current:
        for characters in characterset:
            newset.append(possibility+characters)
    return newset

def _createAllScenarios(charset,depth):
    #Used by Capture Group. This gets big quick if depth > 3
    newset = []
    indexes = [0]*depth
    while True:
        newinput = ""
        for i in range(depth):
            # print("Checking",i)
            if indexes[i] == len(charset):
                # print(i,"was past limit of",indexes[i],"so we reset it")
                indexes[i] = 0
                if i+1 == depth:
                    return newset
                else:
                    indexes[i+1] += 1
            newinput += charset[indexes[i]]
        newset.append(newinput)
        indexes[0] += 1

def _skipLazy(reg):
    return reg[:1] == "?" and reg[1:] or reg #Lazy identifier doesnt matter in comparisons (or not enough for me to handle it)

_specials = "[{(+*?|"

_splitUpReg = regex.compile(f"([^{_specials}]*)([^{_specials}])([{_specials}]?[\s\S]*)")
_getUntilEnding = lambda character : regex.compile(f"(.*?)([^\\\\])(\\{character}[\s\S]*)")
def _getPotentials(reg):
    #Progressively scan the reg, stopping at each special character and handling them as necessary
    possibles = [""]
    savedPossibles = []
    while True:
        searchresult = _splitUpReg.search(reg)
        if not searchresult: #Done here
            break
        if reg[:1] in "[{(|": #Hacky but /shrug
            normal,beforeSpecial,special = "","",reg
        else:
            normal,beforeSpecial,special = searchresult.groups()
        reg = special or ""
        if special:
            if special[0] == "[": #Selection
                possibles = _generatePossibles(possibles,[normal+beforeSpecial])
                tochoose = []
                selection,lastChar,reg = _getUntilEnding("]").search(special[1:]).groups()
                reg = reg[1:]

                for character in selection + lastChar:
                    tochoose.append(character)
                    #NOTE: Does not support a-z or similar, fix this!

                if reg[:1] == "+":
                    tochoose.extend([x*3 for x in tochoose])
                    possibles = _generatePossibles(possibles,tochoose)
                    reg = reg[1:]
                    reg = _skipLazy(reg)

                elif reg[:1] == "*":
                    tochoose.extend([x*3 for x in tochoose])
                    tochoose.append("")
                    possibles = _generatePossibles(possibles,tochoose)
                    reg = reg[1:]
                    reg = _skipLazy(reg)

                elif reg[:1] == "?":
                    tochoose.append("")
                    possibles = _generatePossibles(possibles,tochoose)
                    reg = reg[1:]

                elif reg[:1] == "{":
                    selection,lastChar,reg = _getUntilEnding("}").search(reg[1:]).groups()
                    reg = reg[1:]
                    selection = selection+lastChar
                    if selection.find(",") == -1:
                        tochoose.extend([x*int(selection) for x in tochoose])
                        possibles = _generatePossibles(possibles,tochoose)
                    else:
                        ranges = selection.split(",")
                        templist = list(tochoose)
                        if ranges[1]:
                            newset = [x*int(ranges[0]) for x in tochoose]
                            newset.extend([x*int(ranges[1]) for x in tochoose])
                            possibles = _generatePossibles(possibles,newset)
                        else:
                            newset = [x*int(ranges[0]) for x in tochoose]
                            newset.extend([x*int(ranges[0])+3 for x in tochoose])
                            possibles = _generatePossibles(possibles,newset)
                    reg = _skipLazy(reg)
                else:
                    possibles = _generatePossibles(possibles,tochoose)

            elif special[0] == "(": #Capture Group
                possibles = _generatePossibles(possibles,[normal+beforeSpecial])
                #Re-fire self with the specific subgroup and extend with its result
                selection,lastChar,reg = _getUntilEnding(")").search(reg[1:]).groups()
                selection = selection+lastChar
                reg = reg[1:]
                tochoose = _getPotentials(selection)

                if reg[:1] == "+":
                    tochoose.extend(_createAllScenarios(tochoose,3))
                    possibles = _generatePossibles(possibles,tochoose)
                    reg = reg[1:]
                    reg = _skipLazy(reg)

                elif reg[:1] == "*":
                    tochoose.extend(_createAllScenarios(tochoose,3))
                    tochoose.append("")
                    possibles = _generatePossibles(possibles,tochoose)
                    reg = reg[1:]
                    reg = _skipLazy(reg)

                elif reg[:1] == "?":
                    tochoose.append("")
                    possibles = _generatePossibles(possibles,tochoose)
                    reg = reg[1:]

                elif reg[:1] == "{":
                    selection,lastChar,reg = _getUntilEnding("}").search(reg[1:]).groups()
                    reg = reg[1:]
                    selection = selection+lastChar
                    if selection.find(",") == -1:
                        tochoose.extend([x*int(selection) for x in tochoose])
                        possibles = _generatePossibles(possibles,tochoose)
                    else:
                        ranges = selection.split(",")
                        templist = list(tochoose)
                        if ranges[1]:
                            newset = [x*int(ranges[0]) for x in tochoose]
                            newset.extend([x*int(ranges[1]) for x in tochoose])
                            possibles = _generatePossibles(possibles,newset)
                        else:
                            newset = [x*int(ranges[0]) for x in tochoose]
                            newset.extend([x*int(ranges[0])+3 for x in tochoose])
                            possibles = _generatePossibles(possibles,newset)
                    reg = _skipLazy(reg)

            elif special[0] == "|": #X or Y
                possibles = _generatePossibles(possibles,[normal+beforeSpecial])
                #Simply save the current possibles and start from the start
                savedPossibles.extend(possibles)
                possibles = [""]
                reg = reg[1:]

            elif special[0] == "+": #1 or more
                possibles = _generatePossibles(possibles,[normal])
                possibles = _generatePossibles(possibles,[beforeSpecial,beforeSpecial*3])
                reg = _skipLazy(reg)

            elif special[0] == "*": #0 or more
                possibles = _generatePossibles(possibles,[normal])
                possibles = _generatePossibles(possibles,[beforeSpecial,beforeSpecial*3,""])
                reg = _skipLazy(reg)

            elif special[0] == "?": #0 or 1
                possibles = _generatePossibles(possibles,[normal])
                possibles = _generatePossibles(possibles,[beforeSpecial,""])
                reg = _skipLazy(reg)

            elif special[0] == "{": #Repitition
                possibles = _generatePossibles(possibles,[normal])
                selection,lastChar,reg = _getUntilEnding("}").search(special[1:]).groups()
                selection = selection+lastChar
                reg = reg[1:]
                if selection.find(",") == -1:
                    possibles = _generatePossibles(possibles,[beforeSpecial*int(selection)])
                else:
                    ranges = selection.split(",")
                    if ranges[1]:
                        possibles = _generatePossibles(possibles,[beforeSpecial*int(x) for x in ranges])
                    else:
                        possibles = _generatePossibles(possibles,[beforeSpecial*int(ranges[0]),beforeSpecial*(int(ranges[0])+3)])
                reg = _skipLazy(reg)
        else:
            possibles = _generatePossibles(possibles,[normal+beforeSpecial])
    possibles.extend(savedPossibles)
    return possibles

#Takes 2 regex strings and returns which regex is inferior (if any)
def compare(reg1,reg2,printResult=True):
    # print(reg1,reg2)
    r1 = regex.compile(reg1)
    r2 = regex.compile(reg2)
    reg1Checks = _getPotentials(reg1)
    reg2Checks = _getPotentials(reg2)
    if not reg1Checks or not reg2Checks:
        print(f"One or more of the 2 regexs from the comparison of {reg1} and {reg2} failed")
        return
    failed = False
    for check in reg1Checks:
        find = r2.search(check)
        if not find:
            failed = True
        elif check[:1] == "^" and find.start() != 0:
            failed = True
        elif check[-1:] == "$" and find.end() != len(check):
            failed = True
        if failed:
            break
    if not failed:
        if printResult:
            print(reg1,"is inferior to",reg2)
        return 1
    failed = False
    for check in reg2Checks:
        find = r1.search(check)
        if not find:
            failed = True
        elif check[:1] == "^" and find.start() != 0:
            failed = True
        elif check[-1:] == "$" and find.end() != len(check):
            failed = True
        if failed:
            break
    if not failed:
        if printResult:
            print(reg2,"is inferior to",reg1)
        return 2
    return 0

#Takes a list of regexs and pairs them all up, returning an optimised list with no inferiors
def compareSet(regset,printResult=True):
    dontinclude = []
    for i in range(len(regset)):
        for ii in range(len(regset)):
            if ii > i:
                inferior = compare(regset[i],regset[ii],printResult)
                if inferior == 1:
                    dontinclude.append(regset[i])
                elif inferior == 2:
                    dontinclude.append(regset[ii])
    final = []
    for item in regset:
        if not item in dontinclude:
            final.append(item)
    if printResult:
        print("Before:",regset)
        print("After:",final)
    return final

## Test cases
# compare("abcd+fl+k","abc[de]+fl*k")
# compare("[Ll][Ee][Aa][Dd] ?missing","[Ll]ead ?missing")
# compare("hey therewhat","hey (there|what)+")
# compare("hey ?therewhat","hey (there|what)+")
