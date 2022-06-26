""" aidan9382
The purpose of this script is to compare 2 regex search patterns and determine if one is covered on all cases by the other
This can help remove duplicate occurances or redundant entires within a large regex set

This is an absolute mess of specific rules and intertwined madness of edge case checks
While it works on like, 99% of scenarios, its likely inefficient
Note that it also doesnt (as of now) support capture groups ( () ) or pipes (|) or start/end identifiers (^ and $)
 as they are much more complicated to code and its 11PM so its not like im doing it now :)

If you do use this, make sure to give it some manual scrutiny, because it needs it
"""

import re as regex
#We use the regex to parse the regex

def _generatePossibles(current,characterset):
    newset = []
    for possibility in current:
        for characters in characterset:
            newset.append(possibility+characters)
    return newset

def _skipLazy(reg):
    return reg[:1] == "?" and reg[1:] or reg #Lazy identifier doesnt matter in comparisons (or not enough for me to handle it)

_specials = "[{(+*?|"

_splitUpReg = regex.compile(f"([^{_specials}]*)([^{_specials}])([{_specials}]?[\s\S]*)")
_getUntilEnding = lambda character : regex.compile(f"(.*?)([^\\\\])(\\{character}[\s\S]*)")
def _getPotentials(reg):
    #Progressively scan the reg, stopping at each special character and handling them as necessary
    possibles = [""]
    while True:
        searchresult = _splitUpReg.search(reg)
        if not searchresult: #Done here
            break
        if reg[:1] in ["[","{","("]: #Hacky but /shrug
            normal,beforeSpecial,special = "","",reg
        else:
            normal,beforeSpecial,special = searchresult.groups()
        # print(normal,beforeSpecial,special)
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
                #This is complicated to handle and currently unimplemented
                print("EXITED OUT OF THE COMPARE CAUSE WE HAVE A CAPTURE GROUP")
                return
            elif special[0] == "|": #X or Y
                #This is complicated to handle and currently unimplemented
                print("EXITED OUT OF THE COMPARE CAUSE WE HAVE A PIPE")
                return
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
    return possibles

def compare(reg1,reg2):
    # print(reg1,reg2)
    r1 = regex.compile(reg1)
    r2 = regex.compile(reg2)
    reg1Checks = _getPotentials(reg1)
    reg2Checks = _getPotentials(reg2)
    if not reg1Checks or not reg2Checks:
        print(f"One or more of the 2 regexs from the comparison of {reg1} and {reg2} failed")
        return
    failed = 0
    for check in reg1Checks:
        if not r2.search(check):
            failed += 1
    if failed == 0:
        print(reg2,"fits all possible cases of",reg1)
    else:
        pass# print(f"{reg2} worked on {len(reg1Checks)-failed} out of {len(reg1Checks)} cases from {reg1}")
    failed = 0
    for check in reg2Checks:
        if not r1.search(check):
            failed += 1
    if failed == 0:
        print(reg1,"fits all possible cases of",reg2)
    else:
        pass# print(f"{reg1} worked on {len(reg2Checks)-failed} out of the {len(reg2Checks)} cases from {reg2}")
