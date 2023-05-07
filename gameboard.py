import tkinter as tk
from tkinter import messagebox

class BoardClass:

    #creating the container for class variables
    currentboard = 0
    username_player1 = 0
    username_player2 = 0
    lastplayer = 0
    totalgamesplayed = 0
    wins = 0
    ties = 0
    losses = 0
    
    def __init__(self):
        #creating the instance variables
        self.currentboard = [['', '', ''],['', '' , ''],['', '', '']] #the tic tac toe game 
        self.username_player1 = ''
        self.username_player2 = ''
        self.lastplayer = ''
        self.totalgamesplayed = 0
        self.wins = 0
        self.ties = 0
        self.losses = 0
        
    def playMoveOnBoard(self, player, row, column):
        #play moves on the fake board
        if player == 'player2':
            self.currentboard[row][column] = 'X'
        if player == 'player1':
            self.currentboard[row][column] = 'O'
                        
    def getcurrentboard(self): #extra method
        return self.currentboard
    
    def recordGamePlayed(self): #record how many games is played
        self.totalgamesplayed += 1

    def getTotalGamesPlayed(self): #the getter for recordGamePlayed
        return self.totalgamesplayed
        
    def resetGameBoard(self): #clears board for new game if player 2 wants to
        for row in range(3):
            for column in range(3):
                self.currentboard[row][column] = ''
                
    
    def isBoardFull(self): #check if no more move is avaaible, often results in a tie
        for row in range(len(self.currentboard)):
            for column in range(len(self.currentboard)):
                if self.currentboard[row][column] == '':
                    return False #because the board is not full because there is an empty space or spaces
        self.ties+= 1
        return True #because there are no empty space
    
        
    def isGameFinished(self, player):
        
        #returns true if it is tie since no possible winners or moves open
        if self.isBoardFull() == True: 
            return True #returns True because it is tie, so game is like finished

        # row horizonal win for players
        for row in range(len(self.currentboard)):
            if self.currentboard[row][0] == 'X':
                if self.currentboard[row][1] == 'X':
                    if self.currentboard[row][2] == 'X':
                        if player == 'player2':
                            self.wins += 1
                        else:
                            self.losses += 1
                        return 'X Win'                   
        for row in range(len(self.currentboard)):
            if self.currentboard[row][0] == 'O':
                if self.currentboard[row][1] == 'O':
                    if self.currentboard[row][2] == 'O':
                        if player == 'player1':
                            self.wins += 1
                        else:
                            self.losses += 1
                        return 'O Win'
                        

        # vertical win for players
        for column in range(len(self.currentboard)):
            if self.currentboard[0][column] == 'X':
                if self.currentboard[1][column] == 'X':
                    if self.currentboard[2][column] == 'X':
                        if player == 'player2':
                            self.wins += 1
                        else:
                            self.losses +=1
                        return 'X Win'
        for column in range(len(self.currentboard)):
            if self.currentboard[0][column] == 'O':
                if self.currentboard[1][column] == 'O':
                    if self.currentboard[2][column] == 'O':
                        if player == 'player1':
                            self.wins += 1
                        else:
                            self.losses +=1
                        return 'O Win'

                        
        #diagonal wins for players
        if self.currentboard[0][0] == 'X':
            if self.currentboard[1][1] == 'X':
                if self.currentboard[2][2] == 'X':
                    if player == 'player2':
                        self.wins += 1
                    else:
                        self.losses += 1
                    return 'X Win'
        if self.currentboard[0][2] == 'X':
            if self.currentboard[1][1] == 'X':
                if self.currentboard[2][0] == 'X':
                    if player == 'player2':
                        self.wins += 1
                    else:
                        self.losses += 1
                    return 'X Win'
        if self.currentboard[0][0] == 'O':
            if self.currentboard[1][1] == 'O':
                if self.currentboard[2][2] == 'O':
                    if player == 'player1':
                        self.wins += 1
                    else:
                        self.losses += 1
                    return 'O Win'
        if self.currentboard[0][2] == 'O':
            if self.currentboard[1][1] == 'O':
                if self.currentboard[2][0] == 'O':
                    if player == 'player1':
                        self.wins += 1
                    else:
                        self.losses += 1
                    return 'O Win'
                
        return False #no one wins, lost, or tie, so game goes on
        
                    
        
    
    def computeStats(self):
        #printing in the shell bc i'm allow to??
        print("Player 1's Username: " + str(self.username_player1))
        print("Player 2's Username: " + str(self.username_player2))
        print("Last Player To Go: " + str(self.lastplayer))
        print("Total Games Played: " + str(self.totalgamesplayed))
        print("Your Total Wins: " + str(self.wins))
        print("Your Total Ties: " + str(self.ties))
        print("Your Total Losses: " + str(self.losses))
        
        return self.username_player1, self.username_player2, self.lastplayer, self.totalgamesplayed, self.wins, self.ties, self.losses


    #other methods that is helpful for me
    def setusername_player1(self, name):
        (self.username_player1) = name

    def getusername_player1(self):
        return self.username_player1

    def setusername_player2(self, name):
        self.username_player2 = name

    def getusername_player2(self):
        return self.username_player2

    def setlastplayer(self, player):
        self.lastplayer = player

    def getlastplayer(self):
        return self.lastplayer
