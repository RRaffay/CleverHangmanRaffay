'''

@author: Rana Raffay ar534
'''
import random

def handleUserInputDebugMode():
    '''
    THis function asks the user if they want to play in debug mode or play mode and then returns
    a boolean where true means they want to play debug and false means play mode
    '''
    debugOrNo = input("Do you want to play in (d)ebug mode or (p)lay mode?: ")
    if debugOrNo == 'd':
        return True
    else:
        return False


def handleUserInputWordLength():
    '''
    this asks the user to input how long they want the word to be and returns it as an integer
    '''
    length = input("How long should the word be? ")
    return int(length)


def createTemplate(currTemplate, letterGuess, word):
    '''
    This function creates a template for a word based on the letter guessed and whether or not it was in the word or not
    '''
    lstCurrTemp = list(currTemplate)
    for i in range(len(word)):
        if word[i] == letterGuess:
            lstCurrTemp[i] = letterGuess
    strNewTemp = ''.join(lstCurrTemp)
    return strNewTemp


def getNewWordList(currTemplate, letterGuess, wordList, DEBUG):
    '''
    This function takes the current available words and determines what the new list of words is
    based on the templates created by calling createTemplate
    Also if DEBUG is true, it prints out certain statistics that help the user see the possible keys and the word
    
    '''
    len1 = len(wordList)
    tempDict = {}
    for word in wordList:
        temp = createTemplate(currTemplate, letterGuess, word)
        if temp not in tempDict:
            tempDict[temp] = []
        tempDict[temp].append(word)
    wordLst = [(key,tempDict[key]) for key in tempDict]
    debugLst = wordLst[:]
    debugLst = sorted(debugLst,key = lambda x: x[0])
    maxLst = (0,[])
    for word in wordLst:
        if len(word[1]) > (len(maxLst[1])):
            maxLst = (word[0],word[1])
        elif len(word[1]) == (len(maxLst[1])):
            
            count1 = word[0].count("_")
            count2 = maxLst[0].count("_")
            if count1>count2:
                maxLst = (word[0],word[1])
                
            
    if len(maxLst[1])!=0:
        word = random.choice(maxLst[1])
    
    if DEBUG:
        for key in debugLst:
            print(key[0] + " : " + str(len(key[1])))
            '''
            if len(key[1]) > (len(maxLst)):
                maxLst = (key[0],key[1])
            '''
        print("# keys = " + str(len(debugLst)))
        print("word is: " + word)
        print("Number of possible words: " + str(len(maxLst[1])))
    
    tup = (maxLst[0],maxLst[1])
    
    return tup 


def processUserGuessClever(guessedLetter, hangmanWord, missesLeft):
    '''
    This function takes the guessed letter and template version of the word and how many
    misses are left and determines whether or not the user missed
    It returns a list with the updated misses and a boolean of whether or not the user missed
    '''
    miss = True
    if guessedLetter not in hangmanWord:
        missesLeft -= 1
        miss = False
    else:
        miss = True
    
    return [missesLeft,miss]






def handleUserInputDifficulty():
    '''
    This function asks the user if they would like to play the game in (h)ard or (e)asy mode, then returns the 
    corresponding number of misses allowed for the game. 
    '''
    print("How many misses do you want? Hard has 8 and Easy has 12.")
    userInput = input("(h)ard or (e)asy> ")
    if userInput == 'h' or userInput == 'H':
        return 8
    else:
        return 12








def createDisplayString(lettersGuessed, missesLeft, hangmanWord):
    '''
    Creates the string that will be displayed to the user, using the information in the parameters.
    '''    
    retString = "letters not yet guessed: "
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    alpha_list = list(alphabet)
    for let in alpha_list:
        if let in lettersGuessed:
            alpha_list[alpha_list.index(let)] = " "
    retString += ''.join(alpha_list)
    
    '''
    for let in lettersGuessed:
        retString = retString + (let + " ")
    '''
    retString += ("\n")
    retString += ("misses remaining = " + str(missesLeft) + "\n")
    for let in hangmanWord:
        retString += (let + " ")
    
        
    return retString 




def handleUserInputLetterGuess(lettersGuessed, displayString):
    '''
    Prints displayString, then asks the user to input a letter to guess.
    This function handles the user input of the new letter guessed and checks if it is a repeated letter.
    '''
    print(displayString)
    letter = True
    
    while letter:
        inLetter = input("Input a letter> ")
        if inLetter in lettersGuessed:
            print("you already guessed that")
        else:
            letter = False
            
            return inLetter
    





def runGame(filename):
    '''
    This function sets up the game, runs each round, and prints a final message on whether or not the user won.
    True is returned if the user won the game. If the user lost the game, False is returned.
    
    file = os.path("lowerwords.txt")
    f = open(file)
    wordsClean = [w.strip() for w in f.read().split()]
    print(wordsClean[0:30])
    '''
    
    all_words = []
    
    words = open(filename,'r')
    for line in words:
        x = line.split()
        for y in x:
            all_words.append(y)
    
               
    DEBUG = handleUserInputDebugMode()
    wordLength = handleUserInputWordLength()
   
    missesLeft = handleUserInputDifficulty()
    mL = missesLeft
    firstWord = []
    
    for word in all_words:
        
        if len(word) == int(wordLength):
            
            firstWord.append(word)
   
    fWord = random.choice(firstWord)
    hangmanWord = ["_"] * int(wordLength)
    count = 0
    lettersGuessed = []
    wordList = firstWord
    while missesLeft > 0 and "_" in hangmanWord:
        
        count+=1
        displayString = createDisplayString(lettersGuessed, missesLeft, hangmanWord)
        
        guessedLetter = handleUserInputLetterGuess(lettersGuessed, displayString)
        lettersGuessed.append(guessedLetter)
        
        hangmanWord = ''.join(hangmanWord)
        newWordLst = getNewWordList(hangmanWord, guessedLetter, wordList, DEBUG)#wordList was firstWord
        
        
        wordList = newWordLst[1]
        hangmanWord = newWordLst[0]
        
        missLeftAndMiss = processUserGuessClever(guessedLetter, hangmanWord, missesLeft) #was newWordLst before
        
        missesLeft = missLeftAndMiss[0]
        miss = missLeftAndMiss[1]
        if not miss:
            print("You missed: " + guessedLetter + " not in word")
    if missesLeft == 0:
        print("you're hung \n word is: " + random.choice(wordList))
        print("You made "+ str(count) + " guesses with " + str(mL) + " misses" )
        return False
    elif "_" not in hangmanWord:
        print("you guessed the word: " + hangmanWord)
        print("you made " + str(count) + " guesses with " + str(mL - missesLeft) + " misses")
        return True
    
    

if __name__ == "__main__":
    '''
    Running Hangman.py should start the game, which is done by calling runGame, therefore, we have provided you this code below.
    '''
    wins = 0
    games = 0
    
    play = True
    while play:
        result = runGame('lowerwords.txt')
        if result == True:
            wins += 1
        games += 1
        userInput = input("Do you want to play again? (y)es or (n)o ")
        if userInput == 'n':
            play = False
    print("You won " + str(wins) + " game(s), and lost " + str(games-wins) + " game(s)")    


