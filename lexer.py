""" This is the small lexer for simple English text.
    Lessons are assumed to begin with lesson identifier
     - (\d+).
    Then words are identified with the following regex
     - ([\w|’]+)[ |.]
    Stemming may be performed..

    To run this lexer, use the followring command
    python3 lexer.py filename.txt
"""

import sys
import re
import collections

def removeDigits(line):
    strings = re.match(r"\D+", line)
    if strings:
        return strings.group(0)
    else:
        return ""

def getWordsFromLine(line):
    words = []
    for m in re.finditer(r"([\w|’]+)[ |.]", line):
        words.append(m.group(1))
    return words

def toLower(words):
    wordsInLower = []
    for w in words:
        wordsInLower.append(w.lower())
    return wordsInLower

def addWordsToDictonary(dict, words, currLessonNo):
    for w in words:
        if w in dict:
            currLessonList = dict[w]
            if currLessonNo in currLessonList:
                currLessonList[currLessonNo] += 1
            else:
                currLessonList[currLessonNo] = 1
        else:
            dict[w] = {currLessonNo:1}

def sortDictionary(dict):
    outDict = collections.OrderedDict(sorted(dict.items()))
    return outDict

def sortWordDictionary(dict):
    cacheDict = {}
    for k in dict:
        cacheDict[k] = sortDictionary(dict[k])
    return sortDictionary(cacheDict)

# main function
def main():
    print ("Lexer started. ")
    Input = open(sys.argv[1])

    print("File name: ", Input.name)
    print("File mode: ",Input.mode)

    globalDict = {}
    currentLessonNo = 0

    for line in Input:
        LessonTag = re.search(r'(\d+).', line)
        if LessonTag:
            print("Processing Lesson ", LessonTag.group(1))
            currentLessonNo = int(LessonTag.group(1))
            line = removeDigits(line)
        wordsInLine = toLower(getWordsFromLine(line))
        addWordsToDictonary(globalDict, wordsInLine,currentLessonNo)

    outputDict = sortWordDictionary(globalDict)

    for w,v in outputDict.items():
        print(w, " ", v)


if __name__=="__main__":
    main()
