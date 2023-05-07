"""PLAYER ONE / SERVER """

import socket, threading
import tkinter as tk
from tkinter import messagebox
from gameboard import BoardClass

#host address: michs-macbook.frontierlocal.net

class PlayerOne():

    #initializing my class variables
    def __init__(self):
        self.yourturn = False #player two goes first, so this is false 
        self.startGame = False #goes true when game/round starts
        self.buttonlist = [] #for the button to be find easily

        #the socket stuff
        self.serverSocket = ''
        self.clientSocket =''
        self.clientData = ''
        self.currentplayerlabel = ''
        
        #importing the BoardClass
        self.board = BoardClass()

        #calling to set up the basic canvas/window
        self.canvasSetup()
        self.initTKVariables()
        self.pluggingInHostInfo()
        self.mainLoop()
        self.serverSocket = ''
        self.clientSocket =''
        self.clientData = ''
        
    def initTKVariables(self):
        #creating the tkinter variables
        self.hostAddress = tk.StringVar(self.master)
        self.hostPort = tk.IntVar(self.master)
        self.player2name = tk.StringVar(self.master)
        self.player1name = tk.StringVar(self.master)
        
    def canvasSetup(self):
        #creating the canvas/window with the quit button! 
        self.master = tk.Tk()
        self.master.title('Tic Tac Toe: Player 1')
        self.master.geometry('650x700')
        self.master.configure(background='#F9E79F')
        self.master.resizable(0,0) #i didn't want to mess it the formating 
        self.title = tk.Label(self.master, text='tic tac toe by michelle bui :)', font='courier 20 bold', bg='#F9E79F', pady=10).pack()
        self.quitButton = tk.Button(self.master, text='quit!', font = 'Courier', command= self.master.destroy, width = 10, height=2).place(x=285, y=625)

    #creating the area to plug in host info
    def pluggingInHostInfo(self):
        #a little introduction
        self.welcomeLabel = tk.Label(self.master, text='*✧･ﾟ:* welcome player 1, fill it out to start* :･ﾟ✧*', bg='#F9E79F', width=50, height=14, anchor='n', font='Courier 18 bold')
        self.welcomeLabel.place(x=55, y=105)
        self.welcomeLabel2 = tk.Label(self.master, text="you're playing tic tac toe", bg='#F9E79F', width=50, height=14, anchor='n', font='Courier 18')
        self.welcomeLabel2.place(x=55, y=125)
        #the entry area
        self.entryAddressLabel = tk.Label(self.master, text="enter your host name or ip address below:", bg='#F9E79F', width=40, height=6, anchor='n', font='Courier')
        self.entryAddressLabel.place(x=165, y=175)
        self.entryAddressEntry = tk.Entry(self.master, font= 'courier', textvariable = self.hostAddress, width=37)
        self.entryAddressEntry.place(x=165, y=198)
        self.entryPortLabel = tk.Label(self.master, text="enter your port number below:", bg= '#F9E79F',width=40, height=3, anchor='n', font='courier')
        self.entryPortLabel.place(x=165, y=235)
        self.entryPortEntry = tk.Entry(self.master, font='courier', textvariable = self.hostPort, width=37)
        self.entryPortEntry.place(x=165, y=255)
        #submitting the information
        self.entrySubmit = tk.Button(self.master, text='submit!', command = lambda : (threading.Thread(target=self.startSocketConnection)).start(), font='Courier', width = 10, height=2)
        self.entrySubmit.place(x=285, y=295)
        self.master.bind('<Return>', lambda event: (threading.Thread(target=self.startSocketConnection)).start())

    def startSocketConnection(self):
        #creating the socket connection between the players
        
        try: #if fails, it raises the connection error message box
            self.hostAddress.set(self.entryAddressEntry.get())
            self.hostPort.set(self.entryPortEntry.get())

            #making all the label and button in the previous part into a list
            buttons = [self.entryAddressEntry, self.entryAddressLabel, self.entryPortEntry, self.entryPortLabel,self.entrySubmit,
                        self.welcomeLabel, self.welcomeLabel2] 
            for button in buttons:
                button.destroy()

            #getting/looking for the connections
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.bind((self.hostAddress.get(), self.hostPort.get()))
            self.serverSocket.listen(10) #made it ten to make it easier to find connections...
            self.serverCounter=0

            #the string because idk how to put it in the label looking like that
            self.addressAndportInfo = 'your address: ' + str(self.hostAddress.get()) + '\nyour port: ' + str(self.hostPort.get()) + '\n\nwaiting for player 2...'
            self.confirmLabel = tk.Label(self.master, text= self.addressAndportInfo, bg='#F9E79F', font='courier 15', pady=150)
            self.confirmLabel.pack()
            
            while self.serverCounter!=10:
                
                self.clientSocket, self.clientAddress = self.serverSocket.accept()

                print('client connected!')
                
                self.serverCounter += 1 #because one player connected
                self.clientData = self.clientSocket.recv(1024)
                self.player2_name = (self.clientData.decode('ascii'))
                self.board.setusername_player2(self.player2_name) #got sent the username, so they put it in the tkinter vairable
                self.player2name.set(self.player2_name)
                self.acceptRequest = tk.messagebox.askyesno(title='request!', message='do you want to play with ' + self.player2_name + '?')                

                if(self.acceptRequest == True): #accepting requests!!
                    self.confirmLabel.destroy()
                    self.player2name.set(self.player2_name)
                    if self.player2_name != '':
                        self.opponentLabel = tk.Label(self.master, text='playing with: ' + self.player2_name, width=38, height=10, anchor='n', pady=2, font='courier 15 bold', bg='#F9E79F')
                        self.opponentLabel.place(x=165, y=175)
                        self.userNameLabel = tk.Label(self.master, text='enter your alphanumerical username below:', bg='#F9E79F', font='courier', width=41, height=3, anchor='n')
                        self.userNameLabel.place(x=165, y=200) 
                        self.userNameEntry = tk.Entry(self.master, textvariable=self.player1name, font='courier', width=40)
                        self.userNameEntry.place(x=165, y=220)
                        self.userNameSubmit = tk.Button(self.master, text='submit', width=10, height=2, font='Courier', command=lambda: threading.Thread(target=self.sendUserName).start())
                        self.userNameSubmit.place(x=285, y=260)
                        self.master.bind('<Return>', lambda event: (threading.Thread(target=sendUserName)).start())
                        break
                    elif self.player2_name == '':
                        #most likely the player disconnected
                        self.connectionFailed = tk.messagebox.showerror(title='FAIL', message='Fail Connection') #something probably wrong with connection regarding socket
                        self.pluggingInHostInfo() 
                        
                #if they reject, they just look for another player or wait in this case
        except:
            self.connectionFailed = tk.messagebox.showerror(title='FAIL', message='Fail Connection') #something probably wrong with connection regarding socket
            self.pluggingInHostInfo() #so they can retype it

    def retypingName(self): #just in case the user does not have an alphanumerical username
        self.opponentLabel = tk.Label(self.master, text='playing with: ' + self.player2_name, width=38, height=10, anchor='n', pady=2, font='courier 15 bold', bg='#F9E79F')
        self.opponentLabel.place(x=165, y=175)
        self.userNameLabel = tk.Label(self.master, text='enter your alphanumerical username below:', bg='#F9E79F', font='courier', width=41, height=3, anchor='n')
        self.userNameLabel.place(x=165, y=200) 
        self.userNameEntry = tk.Entry(self.master, textvariable=self.player1name, font='courier', width=40)
        self.userNameEntry.place(x=165, y=220)
        self.userNameSubmit = tk.Button(self.master, text='submit', width=10, height=10, font='Courier', command=lambda: threading.Thread(target=self.sendUserName).start())
        self.userNameSubmit.place(x=285, y=260)
        self.master.bind('<Return>', lambda event: (threading.Thread(target=self.sendUserName).start()))


    def sendUserName(self):
        if (self.userNameEntry.get() == '') or ((self.userNameEntry.get()).isalnum() == False): #if blank or not alphanumerical, it sends to the reypingName function to retype it 
            self.retypeName = tk.messagebox.showerror(self.master, text='name given was not alphanumerical, try again!')
            self.retypeName.pack()
            self.opponentLabel.destroy()
            self.userNameLabel.destroy()
            self.userNameEntry.destroy()
            self.submitButton.destroy()
            self.retypingName()
            
        else: #if the name is input correctly, player 1 send it to player 2
            self.clientSocket.send(self.userNameEntry.get().encode())
            self.board.setusername_player1(self.userNameEntry.get())
            self.player1name.set(self.userNameEntry.get())
            #destroying label and buttons
            self.opponentLabel.destroy()
            self.userNameLabel.destroy()
            self.userNameEntry.destroy()
            self.userNameSubmit.destroy()
            
            self.confirmLabel = tk.Label(self.master, text= 'sent ' + str(self.player1name.get()) +'. waiting ' + str(self.board.getusername_player2()) + ' to send move.', pady=2, font='courier', bg='#F9E79F')
            self.confirmLabel.pack()
            #this basically thanks game when they recieve player two's moves
            self.gameLoop()


    def gameLoop(self):
        #yay starting the game!!
        self.board.setlastplayer(self.board.getusername_player2())
        self.currentplayerLabel= tk.Label(self.master, text=(self.board.getusername_player2()) +"'s turn!", font='courier 15 bold', bg='#F4D03F', pady=10)
        self.currentplayerLabel.pack()
        self.confirmLabel.destroy()

        #setting up the buttons because game is starting nowwwww
        self.setUpButtons()
        
        self.startGame = True #game starts
        self.yourturn = False #but not player 1's turn so they can not click buttons 
        self.board.recordGamePlayed() #record the game

        #since they are player one, they recieve it first through a thread
        self.recievingMove = threading.Thread(target=self.recieveMove)
        self.recievingMove.daemon = True
        self.recievingMove.start()

    def recieveMove(self):
        #getting the move from player two
        if self.yourturn == False:
            self.clientData = self.clientSocket.recv(1024)
            self.slotLocation = list(self.clientData.decode('ascii'))  #it is a string with two inputs so i turned it into a list so it was easier for me   
            if len(self.slotLocation) == 2: #making sure row and column are both sent
                row = self.slotLocation[0]
                column = self.slotLocation[1]
                self.startGame = True
                self.playGame('player2', None, row, column)
            else: #if all else fails, go back
                self.currentplayerLabel.destroy()
                self.pluggingInHostInfo()
        
            
            

    def playGame(self, player, slot, rows, cols):
        #this is where the button changes
        if self.startGame == True: #incase the player press the button when they aren't suppose to
            if player == 'player1': #changing the button for them!
                if self.yourturn == True: 
                    if slot["text"] == '':
                        slot["text"] = "O"
                        self.stringTosend = str(rows) + str(cols) #created a string because it was easier to switch to list
                        self.clientSocket.send(str(self.stringTosend).encode())
                        self.board.playMoveOnBoard(player, rows, cols)
                        self.yourturn = False   #turns False because it is now player two's turn                                     
                        self.finishGame = self.board.isGameFinished('player1')
                        
                        if self.finishGame == False: #games continues :D
                            self.board.setlastplayer(self.board.getusername_player2())
                            self.currentplayerLabel["text"] = self.board.getlastplayer() + "'s turn!"
                            self.recievingMove = threading.Thread(target=self.recieveMove)
                            self.recievingMove.daemon = True
                            self.recievingMove.start()

                        #when the game ends:
                        elif self.finishGame == True: #tie, no more moves
                            self.startGame = False
                            self.currentplayerLabel["text"] = 'Tie!'
                            self.finishGame = tk.Label(self.master, text='Waiting for Player 2...')
                            self.finishGame.pack() 
                            self.threadgamefinished = threading.Thread(target= self.gamefinished)
                            self.threadgamefinished.start()
                        elif self.finishGame == 'O Win': #o wins in any sort of way
                            self.startGame = False
                            self.currentplayerLabel["text"] = 'You Won!'
                            self.finishGame = tk.Label(self.master, text='Waiting for Player 2...')
                            self.finishGame.pack()
                            self.threadgamefinished = threading.Thread(target= self.gamefinished)
                            self.threadgamefinished.start()
                            
                        elif self.finishGame == 'X Win': #x wins in any sort of possible way
                            self.startGame = False
                            self.currentplayerLabel["text"] = 'You Lost!'
                            self.finishGame = tk.Label(self.master, text='Waiting for Player 2...')
                            self.finishGame.pack()
                            self.threadgamefinished = threading.Thread(target= self.gamefinished)
                            self.threadgamefinished.start()
                    else:
                        self.errorMessage = tk.messagebox.showerror(title='pick again', message='spot already taken!')
                else:
                    self.errorMessage = tk.messagebox.showerror(title='stop!', message='not your turn!')
            #moves the board bc player 2 sent it through
            elif player == 'player2':  
                rows = int(rows)
                cols = int(cols)
                self.buttonList[rows][cols]["text"] = "X"
                self.board.playMoveOnBoard('player2', rows, cols)            
                self.finishGame = self.board.isGameFinished('player1')
                self.yourturn = True            
                if self.finishGame == False:
                    self.board.setlastplayer(self.board.getusername_player1())
                    self.currentplayerLabel["text"] = self.board.getlastplayer() + "'s turn!"

                #has the waiting for player 2... bc player2 is is in charge of ending or continuing the game
                elif self.finishGame == True:
                    self.startGame = False
                    self.currentplayerLabel["text"] = 'tie!'
                    self.finishGame = tk.Label(self.master, text='waiting for player 2...', font='courier', pady=5, bg='#F4D03F')
                    self.finishGame.pack()   
                    self.threadgamefinished = threading.Thread(target= self.gamefinished)
                    self.threadgamefinished.start()                
                elif self.finishGame == 'O Win':
                    self.startGame = False
                    self.currentplayerLabel["text"] = 'you won!'
                    self.finishGame = tk.Label(self.master, text='Waiting for Player 2...')
                    self.finishGame.pack()
                    self.gamefinished()
                    self.threadgamefinished = threading.Thread(target= self.gamefinished)
                    self.threadgamefinished.start()                
                elif self.finishGame == 'X Win':
                    self.currentplayerLabel["text"] = 'you lost!'
                    self.finishGame = tk.Label(self.master, text='Waiting for Player 2...', font='courier', pady=5, bg='#F4D03F')
                    self.finishGame.pack()
                    self.threadgamefinished = threading.Thread(target= self.gamefinished)
                    self.threadgamefinished.start()
                    
        elif self.startGame == False:
            self.errorMessage = tk.messagebox.showerror(title="stop!", message='GAME HAS NOT STARTED.')

        
    def gamefinished(self):
        self.playerOne, self.playerTwo, self.lastPlayertoGo, self.totalgames, self.totalwins, self.totalties, self.totallosses = self.board.computeStats()
        self.stats_player1 = "Player 1's Username: " + str(self.playerOne)
        self.stats_player2 = "Player2's Username: " + str(self.playerTwo)
        self.stats_lastplayer = "Last Player To Go: " + str(self.lastPlayertoGo)
        self.stats_totalgames =   "Total Games Played: " + str(self.totalgames)
        self.stats_totalwins = "Your Total Wins: " + str(self.totalwins)
        self.stats_totalties = "Your Total Ties: " + str(self.totalties)
        self.stats_totallosses = "Your Total Losses: " + str(self.totallosses)
        self.finishGame.destroy() #the label where it is waiting for player 2
        
        self.clientData = self.clientSocket.recv(1024)
        self.playagainmessage = self.clientData.decode('ascii')
        
        if self.playagainmessage == 'Play Again':        
            for row in self.buttonList:
                for button in row:
                    button['text'] = ''
            self.board.resetGameBoard()
            self.yourturn = False
            self.board.recordGamePlayed()
            self.board.setlastplayer(self.board.getusername_player2())
            self.currentplayerLabel["text"] = self.board.getlastplayer() + "'s turn!"
            self.startGame = True
            self.recievingMove = threading.Thread(target=self.recieveMove)
            self.recievingMove.daemon = True
            self.recievingMove.start()

        elif self.playagainmessage == 'Fun Times':
            for row in self.buttonList:
                for button in row:
                    button.destroy()
            self.currentplayerLabel.destroy()  
            self.statsTY = tk.Label(self.master, text='thank you for playing!! <3', bg='#F9E79F', font='courier 15 bold', height=16).pack()
            self.statsLabel_p1 = tk.Label(self.master, text= self.stats_player1, font='courier', bg='#F9E79F').pack()
            self.statsLabel_p2 = tk.Label(self.master, text=self.stats_player2, font='courier', bg='#F9E79F').pack()
            self.statsLabel_lplayer = tk.Label(self.master, text=self.stats_lastplayer, font='courier', bg='#F9E79F').pack()
            self.statsLabel_tgames = tk.Label(self.master, text=self.stats_totalgames, font='courier', bg='#F9E79F').pack()
            self.statsLabel_twins = tk.Label(self.master, text=self.stats_totalwins, font='courier', bg='#F9E79F').pack()
            self.statsLabel_tties = tk.Label(self.master, text=self.stats_totalties, font='courier', bg='#F9E79F').pack()
            self.statsLabel_tlosses = tk.Label(self.master, text=self.stats_totallosses, font='courier', bg='#F9E79F').pack()
            self.serverSocket.close()

        

                        
    def setUpButtons(self):
        
        #when clicked, it makes a move
        #you can't click on them when the startGame is False fyi
        
        self.slotOne = tk.Button(self.master, text= '', command=lambda: self.playGame('player1', self.slotOne, 0, 0), width=14, height = 9)
        self.slotOne.place(x=125, y=155)
        
        self.slotTwo = tk.Button(self.master, text= '', command=lambda: self.playGame('player1', self.slotTwo, 0, 1), width=14, height = 9)
        self.slotTwo.place(x=257, y=155)

        self.slotThree = tk.Button(self.master, text= '', command=lambda: self.playGame('player1', self.slotThree, 0, 2), width=14, height = 9)
        self.slotThree.place(x=389, y=155)

        self.slotFour = tk.Button(self.master, text= '', command=lambda: self.playGame('player1', self.slotFour, 1, 0), width=14, height = 9)
        self.slotFour.place(x=125, y=305)

        self.slotFive = tk.Button(self.master, text= '', command=lambda: self.playGame('player1', self.slotFive, 1, 1), width=14, height = 9)
        self.slotFive.place(x=257, y=305)

        self.slotSix = tk.Button(self.master, text= '', command=lambda: self.playGame('player1', self.slotSix, 1, 2), width=14, height = 9)
        self.slotSix.place(x=389, y=305)

        self.slotSeven = tk.Button(self.master, text= '', command=lambda: self.playGame('player1', self.slotSeven, 2, 0), width=14, height = 9)
        self.slotSeven.place(x=125, y=455)

        self.slotEight = tk.Button(self.master, text= '',command=lambda: self.playGame('player1', self.slotEight, 2, 1), width=14, height = 9)
        self.slotEight.place(x=257, y=455)

        self.slotNine = tk.Button(self.master, text= '', command=lambda: self.playGame('player1', self.slotNine, 2, 2), width=14, height = 9)
        self.slotNine.place(x=389, y=455)

        self.buttonList = [[self.slotOne, self.slotTwo, self.slotThree], [self.slotFour, self.slotFive, self.slotSix], [self.slotSeven, self.slotEight, self.slotNine]]

        #creating the mainloop function
    def mainLoop(self):
        self.master.mainloop()
        
if __name__ == '__main__':
    PlayerOne()



