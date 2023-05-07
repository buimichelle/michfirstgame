"""player two / client"""
 
import socket, threading
import tkinter as tk
from gameboard import BoardClass
from tkinter import messagebox

class PlayerTwo():

    def __init__(self):

        #creating the instance variables
        self.yourturn = True #player two goes first
        self.startGame = False #turns true after user establish player connections
        self.buttonlist = []
        self.serverSocket = ''
        self.clientSocket =''
        self.clientData = ''
        self.currentplayerlabel = '' #set the player's name
        self.serverSocket = ''
        self.clientSocket =''
        self.clientData = ''

        #importing the BoardClass
        self.board = BoardClass()

        #calling functions to start and create the game
        self.canvasSetup()
        self.initTKVariables()
        self.pluggingInHostInfo()
        self.mainLoop()
        
        
    def initTKVariables(self):
        #initalizing the instance variables
        self.hostAddress = tk.StringVar(self.master)
        self.hostPort = tk.IntVar(self.master)
        self.player2name = tk.StringVar(self.master)
        self.player1name = tk.StringVar(self.master)
        
    def canvasSetup(self):
        #creating the canvas set up window
        self.master = tk.Tk()
        self.master.title('Tic Tac Toe: Player 2')
        self.master.geometry('650x700')
        self.master.configure(background='#D7BDE2')
        self.master.resizable(0,0)
        self.title = tk.Label(self.master, text='tic tac toe by michelle bui :)', font='courier 20 bold', bg='#D7BDE2', pady=10).pack()
        self.quitButton = tk.Button(self.master, text='quit!', font = 'Courier', command= self.master.destroy, width = 10, height=2).place(x=285, y=625)

    def pluggingInHostInfo(self):
         #asking player 2 the host information
        self.welcomeLabel = tk.Label(self.master, text='*✧･ﾟ:* welcome player 2, fill it out to start*:･ﾟ✧*', bg='#D7BDE2', width=50, height=14, anchor='n', font='Courier 18 bold')
        self.welcomeLabel.place(x=55, y=105)
        self.welcomeLabel2 = tk.Label(self.master, text="you're playing tic tac toe",bg='#D7BDE2', width=50, height=14, anchor='n', font='Courier 18')
        self.welcomeLabel2.place(x=55, y=125)
        self.entryAddressLabel = tk.Label(self.master, text="enter host's host name or ip address below:", bg='#D7BDE2', width=42, height=6, anchor='n', font='Courier')
        self.entryAddressLabel.place(x=165, y=175)
        self.entryAddressEntry = tk.Entry(self.master, textvariable = self.hostAddress, width=40, font='courier')
        self.entryAddressEntry.place(x=165, y=198)
        self.entryPortLabel = tk.Label(self.master, text="enter host's port number below:", bg='#D7BDE2',width=40, height=3, anchor='n', font='courier')
        self.entryPortLabel.place(x=165, y=235)
        self.entryPortEntry = tk.Entry(self.master, textvariable = self.hostPort, width=40, font='courier')
        self.entryPortEntry.place(x=165, y=255)
        self.entrySubmit = tk.Button(self.master, text='submit!', command = self.startSocketConnection, font='Courier', width = 10, height=2)
        self.entrySubmit.place(x=285, y=295)
        self.master.bind('<Return>', lambda event: (threading.Thread(target=self.startSocketConnection)).start())
        
    def startSocketConnection(self):
       #establishing the socket connection with the information the user provided

        self.hostAddress.set(self.entryAddressEntry.get())
        self.hostPort.set(self.entryPortEntry.get())

        #to delete it easier
        buttons = [self.entryAddressEntry, self.entryAddressLabel, self.entryPortEntry, self.entryPortLabel,self.entrySubmit,
                        self.welcomeLabel, self.welcomeLabel2] 
        for button in buttons:
            button.destroy()
        
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.connect((self.hostAddress.get(), self.hostPort.get()))
            self.userNameLabel = tk.Label(self.master, text='enter your alphanumerical username below' +'\nto join your host:', bg='#D7BDE2', font='courier', width=41, height=3, anchor='n')
            self.userNameLabel.place(x=165, y=200) 
            self.userNameEntry = tk.Entry(self.master, textvariable=self.player1name, font='courier', width=40)
            self.userNameEntry.place(x=165, y=225)
            self.userNameSubmit = tk.Button(self.master, text='submit', width=10, height=2, font='Courier', command=lambda: threading.Thread(target=self.sendUserName).start())
            self.userNameSubmit.place(x=285, y=260)
            self.master.bind('<Return>', lambda event: (threading.Thread(target=self.sendUserName)).start())
        except:
            self.connecting_yes_no = tk.messagebox.askyesno(title='failed', message='do you want to try to connect again??')

            if self.connecting_yes_no == True:
                #trying again!
                self.pluggingInHostInfo()
            else:
                #because the user does not to play anymore
                self.master.destroy()
                
            
    def retypingName(self):
        #only if the user name is blank or is not alphanumerical sooooo
        self.userNameLabel = tk.Label(self.master, text='enter your alphanumerical username below:', bg='#D7BDE2', font='courier', width=41, height=3, anchor='n')
        self.userNameLabel.place(x=165, y=200) 
        self.userNameEntry = tk.Entry(self.master, textvariable=self.player1name, font='courier', width=40)
        self.userNameEntry.place(x=165, y=220)
        self.userNameSubmit = tk.Button(self.master, text='submit', width=10, height=2, font='Courier', command=lambda: threading.Thread(target=self.sendUserName).start())
        self.userNameSubmit.place(x=285, y=260)
        self.master.bind('<Return>', lambda event: (threading.Thread(target=self.sendUserName).start()))


    def sendUserName(self):
        #sending the username through and also recieving it
        
        if (self.userNameEntry.get() == '') or (self.userNameEntry.get().isalnum() == False): #checking the username
            self.retypeName = tk.messagebox.showerror(title='error', text='name given was not alphanumerical, try again')
            self.retypeName.pack()
            self.userNameLabel.destroy()
            self.userNameEntry.destroy()
            self.userNameSubmit.destroy()
            self.retypingName()
        else: #the username works!

            #sending the username and setting their own username
            self.serverSocket.send(self.userNameEntry.get().encode())
            self.board.setusername_player2(self.userNameEntry.get())
            self.player2name.set(self.userNameEntry.get())

            #destroying the label in the previous spot
            self.userNameLabel.destroy()
            self.userNameEntry.destroy()
            self.userNameSubmit.destroy()
            self.confirmLabel = tk.Label(self.master, text= 'Sent ' + str(self.player2name.get()) +'. Waiting for Player 1 (Host) to send username...', pady=2, font='courier', bg='#D7BDE2')
            self.confirmLabel.pack()

            #recieiving data from player one and decoding it, also setting it
            self.serverData= self.serverSocket.recv(1024)
            self.player1_name = self.serverData.decode('ascii')
            self.player1name.set(self.player1_name)
            self.board.setusername_player1(self.player1_name)
            self.confirmLabel.destroy()

            #click to start the game
            self.startgamemessage = tk.messagebox.askyesno(title="player 1's name", message="click yes to start playing with " + self.board.getusername_player1())
            if self.startgamemessage == True:
                #is player two agrees, the game starts!
                self.setUpButtons()
                self.gameLoop()
            else:
                self.play_withanotherplayer = tk.messagebox.showinfo(title='Say Bye to Player 1.', message ='Going Back To Host Info Input Screen!')
                self.pluggingInHostInfo()

    def gameLoop(self):

        #player two needs to press move so their turn is true!
        self.confirmLabel.destroy()
        self.board.setlastplayer(self.board.getusername_player2())
        self.currentplayerLabel= tk.Label(self.master, text=(self.board.getusername_player2()) +"'s turn!", font='courier 15 bold', bg='#C39BD3', pady=10)
        self.currentplayerLabel.pack()
        self.board.recordGamePlayed()
        self.startGame = True
        self.yourturn = True
            
                
    def recieveMove(self):
    #when it's player one turn so they start the game off

        if self.yourturn == False: 
            self.serverData = self.serverSocket.recv(1024)
            self.slotLocation = list(self.serverData.decode('ascii')) 
            if len(self.slotLocation) == 2:       
                row=self.slotLocation[0]
                column = self.slotLocation[1]    
                self.playGame('player1', None, row, column)
            else: #if all else fails, go back
                self.currentplayerLabel.destroy()
                self.pluggingInHostInfo()
                
            
            
        
    def playGame(self, player, slot, rows, cols):
    #changing the buttons
        if self.startGame == True:
            if player == 'player2':
                if self.yourturn == True:
                    if slot["text"] == '':
                        slot["text"] = "X"
                        self.stringTosend = str(rows) + str(cols)
                        self.serverSocket.send(str(self.stringTosend).encode())
                        self.board.playMoveOnBoard(player, rows, cols)
                        self.yourturn = False
                        self.finishGame = self.board.isGameFinished('player2')
                        if self.finishGame == False:
                            self.board.setlastplayer(self.board.getusername_player1())
                            self.currentplayerLabel["text"] = self.board.getlastplayer() + "'s turn!"
                            self.recievingMove = threading.Thread(target=self.recieveMove)
                            self.recievingMove.daemon = True
                            self.recievingMove.start()
                            
                        elif self.finishGame == True:
                            self.currentplayerLabel["text"] = 'tie!'
                            self.startGame = False
                            self.master.after(1000, self.gamefinished)
                        elif self.finishGame == 'O Win':
                            self.currentplayerLabel["text"] = 'you lost!'
                            self.startGame = False
                            self.master.after(1000, self.gamefinished)
                        elif self.finishGame == 'X Win':
                            self.currentplayerLabel["text"] = 'you won!!'
                            self.startGame = False
                            self.master.after(1000, self.gamefinished)
                        
                    else:
                        self.errorMessage = tk.messagebox.showerror(title='taken', message='spot already taken!')
                else:
                    self.errorMessage = tk.messagebox.showerror(title='stop!', message='not your turn!')
            elif player == 'player1':
                rows = int(rows)
                cols = int(cols)
                self.buttonList[rows][cols]["text"] = "O"
                self.board.playMoveOnBoard('player1', rows, cols)
                self.yourturn = True
                self.finishGame = self.board.isGameFinished('player2')
                if self.finishGame == False:
                    self.board.setlastplayer(self.board.getusername_player2())
                    self.currentplayerLabel["text"] = self.board.getlastplayer() + "'s turn!"
                elif self.finishGame == True:
                    self.currentplayerLabel["text"] = 'tie!'
                    self.startGame = False
                    self.master.after(1000, self.gamefinished)
                elif self.finishGame == 'O Win':
                    self.currentplayerLabel["text"] = 'you lost!'
                    self.startGame = False
                    self.master.after(1000, self.gamefinished)
                elif self.finishGame == 'X Win':
                    self.currentplayerLabel["text"] = 'you won!'
                    self.startGame = False
                    self.master.after(1000, self.gamefinished)
        elif self.startGame == False:
            self.errorMessage = tk.messagebox.showerror(title="stop!", message='GAME HAS NOT STARTED YET.')      
                                
                
    def gamefinished(self):
        
        self.playerOne, self.playerTwo, self.lastPlayertoGo, self.totalgames, self.totalwins, self.totalties, self.totallosses = self.board.computeStats()

        self.stats_player1 = "Player 1's Username: " + str(self.playerOne)
        self.stats_player2 = "Player2's Username: " + str(self.playerTwo)
        self.stats_lastplayer = "Last Player To Go: " + str(self.lastPlayertoGo)
        self.stats_totalgames =   "Total Games Played: " + str(self.totalgames)
        self.stats_totalwins = "Your Total Wins: " + str(self.totalwins)
        self.stats_totalties = "Your Total Ties: " + str(self.totalties)
        self.stats_totallosses = "Your Total Losses: " + str(self.totallosses)
            
        self.playagainmessage = tk.messagebox.askyesno(title='finish game!', message = 'would you like to play again?')

        if self.playagainmessage == True:
            self.serverSocket.send(b'Play Again')
            for row in self.buttonList:
                for button in row:
                    button['text'] = ''
            self.board.resetGameBoard()

            self.yourturn = True
            self.startGame = True
            self.board.recordGamePlayed()
            self.board.setlastplayer(self.board.getusername_player2())
            self.currentplayerLabel["text"] = self.board.getlastplayer() + "'s turn!"
             
            
        else:
            self.serverSocket.send(b'Fun Times')
            self.currentplayerLabel.destroy()
            for row in self.buttonList:
                for button in row:
                    button.destroy()
                
            self.statsTY = tk.Label(self.master, text='thank you for playing!! <3', bg='#D7BDE2', font='courier 15 bold', height=16).pack()
            self.statsLabel_p1 = tk.Label(self.master, text= self.stats_player1, font='courier', bg='#D7BDE2').pack()
            self.statsLabel_p2 = tk.Label(self.master, text=self.stats_player2, font='courier', bg='#D7BDE2').pack()
            self.statsLabel_lplayer = tk.Label(self.master, text=self.stats_lastplayer, font='courier', bg='#D7BDE2').pack()
            self.statsLabel_tgames = tk.Label(self.master, text=self.stats_totalgames, font='courier', bg='#D7BDE2').pack()
            self.statsLabel_twins = tk.Label(self.master, text=self.stats_totalwins, font='courier', bg='#D7BDE2').pack()
            self.statsLabel_tties = tk.Label(self.master, text=self.stats_totalties, font='courier', bg='#D7BDE2').pack()
            self.statsLabel_tlosses = tk.Label(self.master, text=self.stats_totallosses, font='courier', bg='#D7BDE2').pack()
            self.serverSocket.close()
                
                        
    def setUpButtons(self):
        #creating the buttons
        self.slotOne = tk.Button(self.master, text= '', command=lambda: self.playGame('player2', self.slotOne, 0, 0), width=14, height = 9)
        self.slotOne.place(x=125, y=155)
        
        self.slotTwo = tk.Button(self.master, text= '', command=lambda: self.playGame('player2', self.slotTwo, 0, 1), width=14, height = 9)
        self.slotTwo.place(x=257, y=155)

        self.slotThree = tk.Button(self.master, text= '', command=lambda: self.playGame('player2', self.slotThree, 0, 2), width=14, height = 9)
        self.slotThree.place(x=389, y=155)

        self.slotFour = tk.Button(self.master, text= '', command=lambda: self.playGame('player2', self.slotFour, 1, 0), width=14, height = 9)
        self.slotFour.place(x=125, y=305)

        self.slotFive = tk.Button(self.master, text= '', command=lambda: self.playGame('player2', self.slotFive, 1, 1), width=14, height = 9)
        self.slotFive.place(x=257, y=305)

        self.slotSix = tk.Button(self.master, text= '', command=lambda: self.playGame('player2', self.slotSix, 1, 2), width=14, height = 9)
        self.slotSix.place(x=389, y=305)

        self.slotSeven = tk.Button(self.master, text= '', command=lambda: self.playGame('player2', self.slotSeven, 2, 0), width=14, height = 9)
        self.slotSeven.place(x=125, y=455)

        self.slotEight = tk.Button(self.master, text= '',command=lambda: self.playGame('player2', self.slotEight, 2, 1), width=14, height = 9)
        self.slotEight.place(x=257, y=455)

        self.slotNine = tk.Button(self.master, text= '', command=lambda: self.playGame('player2', self.slotNine, 2, 2), width=14, height = 9)
        self.slotNine.place(x=389, y=455)

        self.buttonList = [[self.slotOne, self.slotTwo, self.slotThree], [self.slotFour, self.slotFive, self.slotSix], [self.slotSeven, self.slotEight, self.slotNine]]

    def mainLoop(self):
        self.master.mainloop()
        
if __name__ == '__main__':
    PlayerTwo()    
            
