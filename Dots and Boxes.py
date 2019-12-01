###############################################################################
############  15-112 Programming Project: Dots and Boxes  #####################
###############################################################################
############       Shahrazad El Natsheh - selnatsh        #####################
###############################################################################

#################         Importing libraries        ##########################

from tkinter import *
from tkinter import messagebox
import random
import socket
import pygame
import math
import sys
sys.setrecursionlimit(10000)

##################          Game start page         ###########################


#Classes circle and drawSquare are used to create an animated background.
#Shapes are made with random colors and will move around the frame by changing
# its position with every call. 
class circle():
    colors = ["red","light blue","pink","light green",
              "yellow","purple","orange"]
    def __init__(self,x,y):
        self.x = x
        self.y = y
        #Shape will change position randomly by dy/dx.
        self.dx = random.randint(-5,5)
        self.dy = random.randint(-5,5)
        
        self.color = random.choice(circle.colors)
        
    #Function draws the 10px shapes.
    def draw(self,c):
        c.create_oval(self.x, self.y, self.x+10, self.y+10,fill=self.color,
                      outline=self.color)
    #Function will move the shape 5 pixels in any direction within the frame.
    def move(self,mx,my):
        self.x += self.dx
        self.y += self.dy
        if self.x < 0 or self.x > mx:
            self.dx = -self.dx
        if self.y < 0 or self.y > my:
            self.dy = -self.dy


class drawSquare():
    colors = ["red","light blue","pink","light green",
              "yellow","purple","orange"]
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.dx = random.randint(-5,5)
        self.dy = random.randint(-5,5)
        
        self.color = random.choice(drawSquare.colors)
    def draw(self,c):
        c.create_rectangle(self.x, self.y, self.x + 10, self.y + 10,
                           fill=self.color,outline=self.color)
    def move(self,mx,my):
        self.x += self.dx
        self.y += self.dy
        if self.x <0 or self.x >mx:
            self.dx = -self.dx
        if self.y <0 or self.y >my:
            self.dy = -self.dy

#Class creates the tkinter start page window. 
class mainwnd(): 
    def __init__(self,root):
        self.root = root
        self.mainFrame = Frame(root)
        self.mainFrame.pack()
        self.shapes = [] #Will store the background shapes

        #Canvas will contain the moving shapes.
        self.canv = Canvas(self.mainFrame,width = 600, height = 600)
        self.drawShapes() #Function will draw create the animated background.
        self.canv.pack()

        #Placing the title image onto frame. Font from:
        #https://www.dafont.com/
        self.background = PhotoImage(file = "bg.png")
        self.bgLbl = Label(self.mainFrame, image = self.background)
        self.mainFrame.after(50,self.refresh)

        #Buttons showing the choices to play single, mutliplayer or online.
        self.choiceOffline = Button(self.mainFrame,
                                    text="Play with friend",
                                    width = 12, height = 5,
                                    fg = "white",
                                    bg = "light coral",
                                    font = "Rockwell 11 bold",
                                    command = self.playOffline)
        self.choiceAI = Button(self.mainFrame,
                               text="Play against AI",
                               width = 12, height = 5,
                               fg = "white",
                               bg = "light coral",
                               font = "Rockwell 11 bold",
                               command = self.playAI)
        self.choiceOnline = Button(self.mainFrame,
                                   text="Play  Online",
                                   width = 12, height = 5,
                                   fg = "white",
                                   bg = "light coral",
                                   font = "Rockwell 12 bold",
                                   command = self.playOnline)


        #placing the widgets on the frame.
        self.bgLbl.place(x=120, y = 20)
        self.choiceOffline.place(x=75,y=400)   
        self.choiceAI.place(x=240,y=400)   
        self.choiceOnline.place(x=400,y=400)   


    #Depending on the choice made, it will call the window for instructions
    #on how to play (Instructions are written on an image)
    #Once clicked on ok, window to take in user input appears(color and username).
    def playOffline(self):
        self.instruct = Toplevel()
        self.instruct.geometry("400x530")
        self.instruct.title("Instructions")
        self.instructFrame = Frame(self.instruct)
        self.instructFrame.pack()
        self.instructions = PhotoImage(file = "instructOffline.png")
        self.instructLbl = Label(self.instructFrame, image = self.instructions)
        
        self.okButton = Button(self.instructFrame,
                               text = 'Ok!', fg = 'blue',
                               bg = 'white', font = 'Rockwell 10 bold',
                               command = lambda :
                               [self.instruct.destroy(),userChoices(self.root,2,0)])

        self.instructLbl.pack()
        self.okButton.pack()


    #Instead of an 'ok' button for instructions, there will be the choice for
    #game difficulty, before the window for user inputs appears.
    def playAI(self):
        self.instruct = Toplevel()
        self.instruct.geometry("400x530")
        self.instruct.title("Instructions")
        self.instructFrame = Frame(self.instruct)
        self.instructFrame.pack()
        self.instructions = PhotoImage(file = "instructAI.png")
        self.instructLbl = Label(self.instructFrame, image = self.instructions)
        
        self.easy = Button(self.instructFrame,
                           text = 'Easy', fg = 'white',
                           bg = 'green', font = 'Rockwell 10 bold',
                           command = lambda :
                           [self.instruct.destroy(),userChoices(self.root,1,1)])
        self.medium = Button(self.instructFrame,
                             text = 'Medium', fg = 'white',
                             bg = 'orange', font = 'Rockwell 10 bold',
                             command = lambda :
                             [self.instruct.destroy(),userChoices(self.root,1,2)])
        self.hard = Button(self.instructFrame,
                           text = '  Hard  ', fg = 'white',
                           bg = 'red', font = 'Rockwell 10 bold',
                           command = lambda :
                           [self.instruct.destroy(),userChoices(self.root,1,3)])

        self.instructLbl.pack()
        self.easy.pack(side = LEFT, padx = 40)
        self.medium.pack(side = LEFT, padx = 40)
        self.hard.pack(side = LEFT, padx = 30)

    #If online, the function will establish a server connection and load the
    #login window after the instructions page.
    def playOnline(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.s.connect(("86.36.46.10", 15112))

        self.instruct = Toplevel()
        self.instruct.geometry("400x530")
        self.instruct.title("Instructions")
        self.instructFrame = Frame(self.instruct)
        self.instructFrame.pack()
        self.instructions = PhotoImage(file = "instructOnline.png")
        self.instructLbl = Label(self.instructFrame, image = self.instructions)
        
        self.okButton = Button(self.instructFrame, text = 'Ok!', fg = 'blue',
                               bg = 'white', font = 'Rockwell 10 bold',
                               command = lambda :
                               [self.instruct.destroy(),self.loginWnd()])

        self.instructLbl.pack()
        self.okButton.pack()

    #Function will draw 30 circles and squares, will assign a
    #   coordinates values from within the frame (600x600)
    def drawShapes(self):
        for i in range (0,30):
            self.x = random.randint(0,599)
            self.y = random.randint(0,599)
            self.shapes.append(circle(self.x,self.y))
        for i in range (0,30):
            self.x = random.randint(0,599)
            self.y = random.randint(0,599)
            self.shapes.append(drawSquare(self.x,self.y))

    #Function will refresh the window every 70 milliseconds,
    #to animate the background. 
    def refresh(self):
        for shape in self.shapes:
            shape.move(600,600)
        self.canv.delete(ALL)
        for shape in self.shapes:
            shape.draw(self.canv)
        self.mainFrame.after(70,self.refresh)

    #Initializing login window.
    def loginWnd(self):
        self.wnd = Toplevel()
        self.wnd.geometry("200x150")
        self.wnd.title("Login")
        self.loginPage = loginServer(self.wnd,self.s)
  
####################    Online helper functions     ###########################

#Helper function calculates the sum of the ASCII of each character of string.
def sumASCII(string):
    M = str(string[:32]) #Finds it for each 32 characters.
    totalSum = 0
    for ch in M:
        totalSum += ord(ch) #Ord finds the ASCII value.
    return totalSum
#Helper function for the Hash decoder
def leftrotate(x,c):
    return (x<<c) & 0xFFFFFFFF | (x >> (32 - c) & 0x7FFFFFFF >> (32 - c))

#Verifies login details using hash algorithm.
def loginVerify (s, username, password):
    #Converts message of login to bytes, sends to server.
    s.send((b"LOGIN ") + bytes(str(username),'utf-8')+ b"\n")
    #Recieves a challenge from the server, converted into a string and sliced.
    message = s.recv(100)
    message = str(message,'utf-8')
    if 'NOT FOUND' in message:
        return False
    else:
        challenge = message.split()[2]
    #Following variables create the 512 character string, ending with the PD+CH. 
    length = len(password)+len(challenge)
    zeros = 511 - length - (len(str(length))) #finds number of zeros needed.
    string = password + challenge + '1' + ('0'*zeros) + str(length)
    M = []
    #Splitting the string into 16, 32-character chunks.
    for i in range(16):
         #Find the sum of ASCII values of each character of each chunk.

        ASCII = sumASCII(string) #Calls helper function.
        M.append(ASCII) #Saves the sums in a list called M.
        string = string[32:]

    #Following code follows the MD5 pseudocode. 
    lst = [7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,5,9,
           14,20,5,9,14,20,5,9,14,20,5,9,14,20,4,11,16,23,4,
           11,16,23,4,11,16,23,4,11,16,23,6,10,15,21,6,10,15,
           21,6,10,15,21,6,10,15,21]
    K = [0xd76aa478,0xe8c7b756,0x242070db,0xc1bdceee,0xf57c0faf,
         0x4787c62a,0xa8304613,0xfd469501,0x698098d8,0x8b44f7af,
         0xffff5bb1,0x895cd7be,0x6b901122,0xfd987193,0xa679438e,
         0x49b40821,0xf61e2562,0xc040b340,0x265e5a51,0xe9b6c7aa,
         0xd62f105d,0x02441453,0xd8a1e681,0xe7d3fbc8,0x21e1cde6,
         0xc33707d6,0xf4d50d87,0x455a14ed,0xa9e3e905,0xfcefa3f8,
         0x676f02d9,0x8d2a4c8a,0xfffa3942,0x8771f681,0x6d9d6122,
         0xfde5380c,0xa4beea44,0x4bdecfa9,0xf6bb4b60,0xbebfbc70,
         0x289b7ec6,0xeaa127fa,0xd4ef3085,0x04881d05,0xd9d4d039,
         0xe6db99e5,0x1fa27cf8,0xc4ac5665,0xf4292244,0x432aff97,
         0xab9423a7,0xfc93a039,0x655b59c3,0x8f0ccc92,0xffeff47d,
         0x85845dd1,0x6fa87e4f,0xfe2ce6e0,0xa3014314,0x4e0811a1,
         0xf7537e82,0xbd3af235,0x2ad7d2bb,0xeb86d391]
    #Intializing Variables
    a0 = 0x67452301
    b0 = 0xefcdab89
    c0 = 0x98badcfe
    d0 = 0x10325476
    A = a0
    B = b0
    C = c0
    D = d0
    for i in range(64):
        if 0 <= i <= 15:
            F = (B & C) | ((~B) & D)
            F = F & 0xFFFFFFFF
            g = i
        elif 16 <= i <= 31:
            F = (D & B) | ((~D) & C)
            F = F & 0xFFFFFFFF
            g = (5*i + 1) % 16
        elif 32 <= i <= 47:
            F = B ^ C ^ D
            F = F & 0xFFFFFFFF
            g = (3*i + 5) % 16
        elif  48 <=  i <= 63:
            F = C ^ (B | (~D))
            F = F & 0xFFFFFFFF
            g = (7*i) % 16
        dTemp = D
        D = C
        C = B
        B = B + leftrotate((A + F + K[i] + M[g]), lst[i])
        B = B & 0xFFFFFFFF
        A = dTemp
    a0 = (a0 + A) & 0xFFFFFFFF
    b0 = (b0 + B) & 0xFFFFFFFF
    c0 = (c0 + C) & 0xFFFFFFFF
    d0 = (d0 + D) & 0xFFFFFFFF

    messageDigest = '' + str(a0) + str(b0) + str(c0) + str(d0)

    #Sends the message digest in bytes to the server.
    s.send(b"LOGIN " + bytes(str(username) + ' ',"utf-8")
           + bytes(str(messageDigest),'utf-8')+ b"\n")

    #Checks the server response, returns true if correct password, false otherwise.
    response = s.recv(100)
    response = str(response,'utf-8')
    response = response.split()
    if response[0] == 'WRONG':
        return False
    else:
        return True

#Function to send friend requests to users.
def sendFriendRequest(s, friend):
    friend = '@' + friend
    size = len('@00000@request@friend\n') + len(friend) #Finds the size.
    size = '@' + str("%05d" % (size))   #Makes size a 5 digit value, converts format.
    #Friend Request is sent in correct command format. 
    s.send(bytes((size),'utf-8') + b"@request@friend"
           + bytes(str(friend),'utf-8') + b"\n")

    #Checks server response, returns true if response is ok, false otherwise.
    response = s.recv(100)
    response = str(response,'utf-8')
    response = response.split('@')
    if response[2] == 'ok':
        return True
    else:
        return False

#Function accepts friend requests.
def acceptFriendRequest(s, friend):
    friend = '@' + friend
    size = len('@00000@accept@friend\n') + len(friend) #Finds the size.
    size = '@' + str("%05d" % (size))   #Makes size a 5 digit value, and formats.

    #Accept Request is sent in correct command format. 
    s.send(bytes((size),'utf-8') + b"@accept@friend"
           + bytes(str(friend),'utf-8') + b"\n")

    #Checks server response, returns true if response is ok, false otherwise.
    response = s.recv(100)
    response = str(response,'utf-8')
    response = response.split('@')
    if response[2] == 'ok':
        return True
    else:
        return False

#Function sends a message to a specified user across the server.
def sendMessage(s, friend, message):
    sendMsg = '@' + friend + '@' + message
    size = len('@00000@sendmsg\n') + len(sendMsg) #Finds the size.
    size = '@' + str("%05d" % (size)) #Makes size a 5 digit value, and formats.
    #Accept Request is sent in correct command format. 
    s.send(bytes((size),'utf-8') + b"@sendmsg"
           + bytes(str(sendMsg),'utf-8') + b"\n")

    #Checks server response, returns true if response is ok, false otherwise.
    response = s.recv(100)
    response = str(response,'utf-8')
    response = response.split('@')
    if response[2] == 'ok':
        return True
    else:
        return False

#Helper function for the messages recieved (for getMail function)
def messages(mails):
    mailUsers = [] #List of users
    mailMsg = []   #List of messages (same index as users)
    recievedMessages = []
    #For number of mail, index all users.
    
    #Goes through mail and appends the usernames to mailUsers.
    for i in range(1,len(mails),3): 
        mailUsers.append(mails[i])
    #Goes through mail and appends the messages to mailMsg.
    for i in range(2,len(mails),3):
        mailMsg.append(mails[i])
    #Appends to the list (username,file) to recievedFiles.
    for i in range(len(mailUsers)): 
        recievedMessages.append((mailUsers[i], mailMsg[i]))
    return recievedMessages #Returns list of (user,message)

#Function retrieves all mail recieved which includes messages and files.
def recieveMsg(s):
    s.send(b"@rxmsg\n")
    size = s.recv(6) #Finds the size of the mail.
    size = str(size,'utf-8')
    size = int(size[1:])
    mail = s.recv(size) #Making sure to recieve everything using the size.
    mail = str(mail,'utf-8')
    mail = mail.split('@') #Splits the mail by '@'.

    #If there are messages and no files recieved...
    if 'msg' in mail:
        #Indexes the messages from server response.
        messageMail = mail[2:]
        #Creates list of messages using helper function.
        recievedMail = messages(messageMail)
        return recievedMail
    else:
        return []

##################         The online login         ###########################

#Class defines the login window, connecting to the server.
class loginServer:
    def __init__(self,root,socket):
        #Creating a frame for the login.
        self.window = root
        self.s = socket
        self.mainFrame = Frame(self.window)
        self.mainFrame.pack()
        #Adding widgets to form the login window.
        self.user = Label(self.mainFrame,
                          text="Username",
                          font = "Rockwell 11 bold",fg = 'dodger blue').pack()

        self.username = Entry(self.mainFrame,
                              bg = 'white',
                              fg = 'medium aquamarine',
                              relief = GROOVE)#Takes username input.
        self.username.pack()

        self.userPass = Label(self.mainFrame,
                              text="Password",
                              font = "Rockwell 11 bold ",fg = 'dodger blue').pack()

        #Takes a password input and displays as *.
        self.password = Entry(self.mainFrame,
                              show = '*', bg = 'white',
                              fg = 'dark turquoise', relief = GROOVE)
        self.password.pack()

        #Verifies credentials when button is pressed.
        self.okBtn = Button(self.mainFrame,text="OK", command = self.login,
                            fg = "white", bg = "light coral",
                            font = "forte 8 ").pack(pady = 5)


    #Defining the login functionality of this class.
    def login(self):
        #Retrieves credentials.
        self.userName = self.username.get()
        self.userPass = self.password.get()
        #Calls the helper function for verification.
        self.verify = loginVerify(self.s,self.userName,self.userPass)
        #Once the user is verified, the window is destroyed and main page called.
        if self.verify == True:
            wnd.withdraw()
            self.window.destroy()
            self.server()
        #If the wrong credentials are entered, a pop up will appear.
        elif self.verify == False:
             messagebox.showerror('',
                                  'Wrong Username or Password, '+
                                  'please re-enter credentials.')

    #Intializing the game server window. 
    def server(self):
        self.wnd = Toplevel()
        self.wnd.geometry("500x300")
        self.wnd.title("Game Server")
        self.gameNetwork = gameServer(self.wnd,self.s,self.userName)   

###############################################################################
##################         The game server          ###########################
###############################################################################

class gameServer:
    def __init__(self,root,sock,userName):
        #Creating the main screen frame.
        self.root = root
        self.serverWindow = self.root
        self.mainFrame = Frame(self.root)
        self.mainFrame.pack()
        self.s = sock
        
        #Adding widgets  of main screen using grid display.
        #Labels
        self.usersLbl = Label(self.mainFrame,text ='All Users',
                              fg = "dodger blue", font = "Rockwell 11 underline")
        self.usersLbl.grid(row=0,column=0)
        self.friendsLbl = Label(self.mainFrame,text ='Your Friends',
                                fg = "lime green", font = "Rockwell 11 underline")
        self.friendsLbl.grid(row=0,column=1)
        self.reqLbl = Label(self.mainFrame,text ='Pending Requests',
                            fg = "salmon", font = "Rockwell 11 underline")
        self.reqLbl.grid(row=0,column=2)

        #All Users list.
        self.usersBox = Listbox(self.mainFrame,
                                font = 'verdana 9',
                                fg = 'steel blue', justify = CENTER)
        self.usersBox.grid(row=1,column=0)
        #Friends list.
        self.friendsBox = Listbox(self.mainFrame,
                                  font = 'verdana 9',
                                  fg = 'medium turquoise', justify = CENTER)
        self.friendsBox.grid(row=1,column=1)

        #Requests list.
        self.reqBox = Listbox(self.mainFrame,
                              font = 'verdana 9',
                              fg = 'indian red', justify = CENTER)
        self.reqBox.grid(row=1,column=2)

        #Buttons calls corresponding functions.
        self.sendReq = Button(self.mainFrame,
                              text="Send Request", command = self.sendRequest,
                              fg = "white", bg = "dodger blue",
                              font = "Rockwell 10 bold")
        self.sendReq.grid(row=2,column=0,pady = 5)

        self.startChat = Button(self.mainFrame,text="Start Game",
                                command = self.startChatting,
                                fg = "white", bg = "lime green",
                                font = "Rockwell 10 bold")
        self.startChat.grid(row=2,column=1,pady = 5)

        self.accReq = Button(self.mainFrame,text="Accept Request",
                             command = self.acceptRequest,
                             fg = "white", bg = "salmon",
                             font = "Rockwell 10 bold")
        self.accReq.grid(row=2,column=2,pady = 5)

        #Allows the user to return to the main window.
        self.Back = Button(self.mainFrame,text="Log Out",
                             command = self.back,
                             fg = "white", bg = "gray",
                             font = "forte 10 ")
        self.Back.grid(row=3,column=1,pady = 5)

        #Stores the user's name to be used in game.
        self.userName = userName



        #Empty lists of users, friends, requests and openchats
        #in order to reset when refreshed.
        self.users = []
        self.getUsers()
        
        self.friends = []
        self.getFriends()
        
        self.requests = []
        self.getRequests()

        self.recvMessages() #Function retrieves all mail.

        #Empty dictrionary to store open chats.
        #Refreshes in 5 seconds to recieve any new messages.
        self.mainFrame.after(8000,self.recvMessages)
    #Function to return to the main window.
    def back(self):
        wnd.deiconify()
        self.serverWindow.destroy()

    #Function retrieves all users on network.
    def getUsers(self):
        self.s.send(b"@Users\n")
        size = self.s.recv(6)   #Checks the size of the string.
        size = str(size,'utf-8')
        if size[0] != '@':
            self.getUsers()
        else:
            size = int(size[1:])
            users = self.s.recv(size) #Making sure to recieve everything using size.
            users = str(users,'utf-8')
            users = users.split('@') #Splits into list by '@'.
            users = users[3:] #Returns users as a list of users excluding the number.
            self.users = users

        #Deletes all users in order to refresh.
        self.usersBox.delete(0,END)
        for i in self.users: #Inserts all refreshed users.
            self.usersBox.insert(END, i)
        #Recalls the function.
        self.mainFrame.after(5000,self.getUsers)

    #Function retrieves all friends over the network.
    def getFriends(self):
        self.s.send(b"@friends\n")
        size = self.s.recv(6)    #Checks the size of the string.
        size = str(size,'utf-8')
        if size[0] != '@':
            self.getFriends()
        else:
            size = int(size[1:])    #Indexes out the '@'.
            friends = self.s.recv(size)  #Making sure to recieve everything.
            friends = str(friends,'utf-8')
            friends = friends.split('@')
            self.friends = friends[3:] #Returns friends as a list.

        #Deletes all friends in order to refresh.
        self.friendsBox.delete(0,END)
        for i in self.friends: #Inserts new list of friends.
            self.friendsBox.insert(END, i)
        #Recalls the function.
        self.mainFrame.after(5000,self.getFriends)

    #Function retrieves the list of friend requests from server.
    def getRequests(self):
        self.s.send(b"@rxrqst\n")
        size = self.s.recv(6) #Finds the size of the command to be sent.
        size = str(size,'utf-8')
        if size[0] != '@':
            self.getRequests()
        else:
            size = int(size[1:]) #Indexes out the '@'.
            requests = self.s.recv(size) #Making sure to recieve everything.
            requests = str(requests,'utf-8')
            requests = requests.split('@') #Splits the list of requests by '@'.
            self.requests = requests[2:] #Returns list of friend requests.

        #Deletes content to add refreshed list of requests.
        self.reqBox.delete(0,END)
        for i in self.requests:
            self.reqBox.insert(END, i)
        #recalls function.
        self.mainFrame.after(5000,self.getRequests)

    #Function sends a friend request to selected user, and displays message.
    def sendRequest(self):
        self.userSelect = self.usersBox.get(ANCHOR)
        self.sentRequest = sendFriendRequest(self.s,self.userSelect)
        messagebox.showinfo('Request sent', 'Friend request sent to '
                            + self.userSelect)

    #Function accepts selected request and displays message.
    def acceptRequest(self):
        self.userReq = self.reqBox.get(ANCHOR)
        self.accepted = acceptFriendRequest(self.s,self.userReq)
        messagebox.showinfo('Added Friend','Added ' + self.userReq
                            + ' as a Friend.')


    #Calls the chat class to open a chat window with selected user.
    def startChatting(self):
        self.userMsg = self.friendsBox.get(ANCHOR)
        sendMessage(self.s, self.userMsg, 'Game Request')
        messagebox.showinfo('Request sent', 'Game request sent to ' + self.userMsg)

    #Recieves all mail over the server.
    def recvMessages(self):
        Messages = recieveMsg(self.s)
        #If the messages are not empty, actions are made depending on the message...
        if Messages != ['', '0']:
            for (u, m) in Messages:
                #If a request is recieved, a pop up appears to ask if they'd like to play.
                if m == 'Game Request':
                    MsgBox = messagebox.askquestion('Game Request',
                                                    str(u) + ' would like to play!')
                    #If a user chooses to play, a message is sent to the user and
                    #the game window is loaded, this person will be player 2.
                    if MsgBox == 'yes':
                        self.serverWindow.withdraw()
                        sendMessage(self.s,u,'Lets play')
                        self.myGame = DotsAndBoxes(self.userName,u,
                                                   'blue','green',False,self.s)
                        self.myGame.start()
                        self.serverWindow.deiconify()
                        return
                #If a user recieves an accepted game request, it loads the game
                #This user will be player 1.
                if m == "Lets play":
                        self.serverWindow.withdraw()
                        self.myGame = DotsAndBoxes(self.userName,u,
                                                   'green','blue',True,self.s)
                        self.myGame.start()
                        self.serverWindow.deiconify()
                        return
                    

        #retrieves messages every 5 seconds.
        self.mainFrame.after(5000,self.recvMessages)


###############################################################################
###################         User selection          ###########################
###############################################################################
#Classes handle the user inputs to be used in the pygame.
#userChoices is used by all 3 game options, taking in number of players
#and the difficulty of the AI if any. 
class userChoices:
    def __init__(self,root,number,difficulty):
        #Initalizing a window.
        self.root = root
        self.wnd = Toplevel()
        self.wnd.grab_set() #Freezes the start page.
        self.wnd.geometry("300x200")
        self.mainFrame = Frame(self.wnd)
        self.mainFrame.pack()
        self.nPlayer = number #Takes the number of players.
        #Calls function in the event of quit. 
        self.wnd.protocol("WM_DELETE_WINDOW",self.closeWindow)

        #Stores the AI player with the difficulty number.
        self.AIplayer = 'AI' + str(difficulty)
        
        #Taking a playername input.
        self.enterName1 = Label(self.mainFrame,
                                text = 'Enter player name:',
                                font = 'Rockwell 18',fg = 'slate gray')
        self.playerName1 = Entry(self.mainFrame, bg = 'light grey')

        self.enterName1.pack(pady = 10)
        self.playerName1.pack()

        #If there is one player(AI), initialize the game with name and color. 
        if self.nPlayer == 1:
            self.chooseColor = Label(self.mainFrame,
                                     text = 'Choose your color to start',
                                     font = 'Rockwell 18',
                                     fg='slate gray', pady = 20)
            self.redChoice = Button(self.mainFrame,
                                    width = 2,height = 1,
                                    bg = 'red',pady = 5,
                                    command = lambda :
                                    self.playerInput(str(self.playerName1.get()),
                                                     self.AIplayer,
                                                     'red','blue'))
            self.blueChoice = Button(self.mainFrame, width = 2,
                                     height = 1,bg = 'light blue',pady = 5,
                                     command = lambda :
                                     self.playerInput(str(self.playerName1.get()),
                                                      self.AIplayer,
                                                      'blue','green'))
            self.purpleChoice = Button(self.mainFrame, width = 2,
                                       height = 1,bg = 'orchid',pady = 5,
                                       command = lambda :
                                       self.playerInput(str(self.playerName1.get()),
                                                        self.AIplayer,
                                                        'purple','yellow'))
            self.greenChoice = Button(self.mainFrame, width = 2,
                                      height = 1,bg = 'light green',pady = 5,
                                      command = lambda :
                                      self.playerInput(str(self.playerName1.get()),
                                                       self.AIplayer,
                                                       'green','blue'))
            self.yellowChoice = Button(self.mainFrame, width = 2,
                                       height = 1,bg = 'lemon chiffon',pady = 5,
                                          command = lambda :
                                       self.playerInput(str(self.playerName1.get()),
                                                        self.AIplayer,
                                                        'yellow','green'))

        #If it is multiplayer, take in inputs for the first player,
            #Load another the other choices class (userChoices2) to take in the
            #other user's choices.
        if self.nPlayer == 2:
            self.chooseColor = Label(self.mainFrame, text = 'Player 1, choose a color',
                                     font = 'Rockwell 18',
                                     fg='slate gray', pady = 20)
            self.redChoice = Button(self.mainFrame, width = 2,
                                    height = 1,bg = 'red',pady = 5,
                                    command = lambda :
                                    userChoices2(self.root,self.wnd,
                                                 str(self.playerName1.get()),'red'))
            self.blueChoice = Button(self.mainFrame, width = 2,height = 1,
                                     bg = 'light blue',pady = 5,
                                     command = lambda :
                                     userChoices2(self.root,self.wnd,
                                                  str(self.playerName1.get()),'blue'))
            self.purpleChoice = Button(self.mainFrame, width = 2,height = 1,
                                       bg = 'orchid',pady = 5,
                                       command = lambda :
                                       userChoices2(self.root,self.wnd,
                                                    str(self.playerName1.get()),'purple'))
            self.greenChoice = Button(self.mainFrame, width = 2,height = 1,
                                      bg = 'light green',pady = 5,
                                      command = lambda :
                                      userChoices2(self.root,self.wnd,
                                                   str(self.playerName1.get()),'green'))
            self.yellowChoice = Button(self.mainFrame, width = 2,height = 1,
                                       bg = 'lemon chiffon',pady = 5,
                                          command = lambda :
                                       userChoices2(self.root,self.wnd,
                                                    str(self.playerName1.get()),'yellow'))

        #Placing the choice widgets onto the window.
        self.chooseColor.pack()
        self.redChoice.pack(side = LEFT,padx=15)
        self.blueChoice.pack(side = LEFT,padx=15)
        self.purpleChoice.pack(side = LEFT,padx=15)
        self.greenChoice.pack(side = LEFT,padx=15)
        self.yellowChoice.pack(side = LEFT,padx=15)

    #Takes in the player inputs, destroys the window and hides the main window
    #Then launches the game.
    def playerInput(self,player1,player2,color1,color2):
        self.wnd.destroy()
        wnd.withdraw()
        self.myGame = DotsAndBoxes(player1,player2,color1,color2,'NA','NA')
        self.myGame.start()
        wnd.deiconify()

        
    #Incase of quit, unfreeze the main page and destroy the window.
    def closeWindow(self):
        self.wnd.grab_release()
        self.wnd.destroy()



#Class used for multiplayer choice.
#Class is the same as the previous userChoices class,
# but takes in another user choices, loads the game using
# player 1's choices which were input parameters, and will take
# in player 2's inputs, launching the game. 
class userChoices2:
    def __init__(self,root,player1wnd,player1,color1):
        player1wnd.destroy()
        self.wnd = Toplevel()
        self.wnd.grab_set()
        self.wnd.geometry("300x200")
        self.mainFrame = Frame(self.wnd)
        self.mainFrame.pack()
        self.playerName1 = player1
        self.color1 = color1
        
        self.wnd.protocol("WM_DELETE_WINDOW",self.closeWindow)

        self.enterName2 = Label(self.mainFrame,
                                text = 'Enter other player name:',
                                font = 'Rockwell 18',fg = 'slate gray')
        self.playerName2 = Entry(self.mainFrame, bg = 'light grey')


        self.enterName2.pack(pady = 10)
        self.playerName2.pack()

        self.chooseColor = Label(self.mainFrame,
                                 text = 'Choose your color to start', font = 'Rockwell 18',
                                 fg='slate gray', pady = 20)
        self.redChoice = Button(self.mainFrame, width = 2,height = 1,bg = 'red',pady = 5,
                                command = lambda :
                                self.playerInput(self.playerName1,str(self.playerName2.get()),
                                                 self.color1,'red'))
        self.blueChoice = Button(self.mainFrame, width = 2,height = 1,
                                 bg = 'light blue',pady = 5,
                                 command = lambda :
                                 self.playerInput(self.playerName1,str(self.playerName2.get()),
                                                  self.color1,'blue'))
        self.purpleChoice = Button(self.mainFrame, width = 2,height = 1,bg = 'orchid',pady = 5,
                                   command = lambda :
                                   self.playerInput(self.playerName1,str(self.playerName2.get()),
                                                    self.color1,'purple'))
        self.greenChoice = Button(self.mainFrame, width = 2,height = 1,bg = 'light green',pady = 5,
                                  command = lambda :
                                  self.playerInput(self.playerName1,str(self.playerName2.get()),
                                                   self.color1,'green'))
        self.yellowChoice = Button(self.mainFrame, width = 2,height = 1,bg = 'lemon chiffon',pady = 5,
                                   command = lambda :
                                   self.playerInput(self.playerName1,str(self.playerName2.get()),
                                                    self.color1,'yellow'))

        #Placing the window widgets onto the screen.
        self.chooseColor.pack()
        self.redChoice.pack(side = LEFT,padx=15)
        self.blueChoice.pack(side = LEFT,padx=15)
        self.purpleChoice.pack(side = LEFT,padx=15)
        self.greenChoice.pack(side = LEFT,padx=15)
        self.yellowChoice.pack(side = LEFT,padx=15)


        #If statements will remove the color player 1 has chosen,
        #in order to not have both players with the same color.
        if self.color1 == 'red':
            self.redChoice.destroy()
        elif self.color1 == 'blue':
            self.blueChoice.destroy()
        elif self.color1 == 'purple':
            self.purpleChoice.destroy()
        elif self.color1 == 'green':
            self.greenChoice.destroy()
        elif self.color1 == 'yellow':
            self.yellowChoice.destroy()

    #Takes in the player inputs, destroys the window and hides the main window
    #Then launches the game.
    def playerInput(self,player1,player2,color1,color2):
        self.wnd.destroy()
        wnd.withdraw()
        self.myGame = DotsAndBoxes(player1,player2,color1,color2,'NA','NA')
        self.myGame.start()
        wnd.deiconify()

    #Incase quit, the startpage is released and window destroyed.
    def closeWindow(self):
        self.wnd.grab_release()
        self.wnd.destroy()

##################################################################################################################
######################################    Dots and Boxes Game    #################################################
##################################################################################################################
       
class DotsAndBoxes():
    def __init__(self,player1,player2,color1,color2,isOnline,socket):
        pass
        #Initializes pygame and fonts.
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Dots and Boxes")
        self.screen = pygame.display.set_mode((600,600))
        self.isOnline = isOnline

        #Establishing player names.
            #If the game is against the AI..
        if 'AI' in player2:
            self.player1 = player1
            self.player2 = 'AI'
            self.difficulty = int(player2[-1]) #Takes the difficulty from the passed AI name.
        else:
            self.player1 = player1
            self.player2 = player2

        
        #Sets the pygame clock.
        self.clock=pygame.time.Clock()


        #Initializing player colors.
        self.color1 = color1
        self.color2 = color2

        #Stores player turn, True for player 1 and False for 2.
        self.turn = True
        self.ownerDigit = ['1','2']

        #Establishing socket if any.
        self.s = socket
        
        #Variables store the scores for players.
        self.playerOneScore = 0
        self.playerTwoScore = 0


        #Function loads the images to be used in game graphics.
        self.gameImages()

        #Dictionary stores the colored boxes and their respective calls.
        self.playerColor = {'blue':self.bluePlayer,'green':self.greenPlayer,
                            'yellow':self.yellowPlayer,'purple':self.purplePlayer,
                            'red':self.redPlayer}

        #List contains the call to boxes of chosen colors.
        self.playerBox = [self.playerColor[self.color1],self.playerColor[self.color2]]


        #setting False for horizontal and vertical lines of board.
        self.boardH = [[False for x in range(5)] for y in range(6)]
        self.boardV = [[False for x in range(6)] for y in range(5)]
        
        #List to hold ownership of each box, initially '0'.
        self.owner = [['0' for x in range(5)] for y in range(5)]

        #If the isOnline variable is false, meaning the user is player 2, changes made accordingly.
        if self.isOnline == False:
            self.turn = False
            self.ownerDigit = ['2','1']
            self.playerBox[0],self.playerBox[1] = self.playerBox[1],self.playerBox[0]


        #Dictionary contains the RGB values of colors. 
        self.textColor = {'blue':(0,100,255),'green':(0,200,0),
                            'yellow':(250,190,0),'purple':(100,0,100),
                            'red':(200,0,0)}
        #Definng the font for turns.
        self.fontTurn = pygame.font.SysFont("forte", 32)
        #Defining the fonts for the names and scores.
        self.fontScore = pygame.font.SysFont("forte", 40)
        self.fontName = pygame.font.SysFont("forte", 20)

        #Stores a variable incase the user quits.
        self.quit = False

    #Function starts the game by calling the main function in a while loop.
    def start(self):
        #Game runs as long as the game is not over and the user has not quit.
        while self.gameOver() != False and self.quit == False:
            self.update()
        pygame.quit()

        #ONce the game is over, show a pop up of who the winner is based on bigger score.
        #If the user starts as player 2, the winner would be the opposite.
        if self.isOnline == False:
            if self.playerOneScore > self.playerTwoScore:
                messagebox.showinfo("GAME OVER", str(self.player2) + " won!")
                    
            if self.playerOneScore < self.playerTwoScore:
                messagebox.showinfo("GAME OVER", str(self.player1) + " won!")

            if self.playerOneScore == self.playerTwoScore:
                messagebox.showinfo("GAME OVER", "Game Over!")

        else:
            if self.playerOneScore > self.playerTwoScore:
                messagebox.showinfo("GAME OVER", str(self.player1) + " won!")
                    
            if self.playerOneScore < self.playerTwoScore:
                messagebox.showinfo("GAME OVER", str(self.player2) + " won!")

            if self.playerOneScore == self.playerTwoScore:
                messagebox.showinfo("GAME OVER", "Game Over!")

        return
        
#Function called to update the game screen after every event.
    def update(self):       
        #Makes the game 60 fps.
        self.clock.tick(60)

        #Sets background color and calls drawboard for GUI components.
        self.screen.fill((255,255,255))
        self.drawBoard()

        #If user closes window, quit and assign the quit variable.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True

#Most of the following code for handling the game board functionality (the position of the line
# and the line hovering functionality is thanks to Julian Meyer, the website:
#https://www.raywenderlich.com/2614
        #Gets the coordinates of the click, returned as [x,y].
        mouse = pygame.mouse.get_pos()
        #Finding the position of the click on the grid based on line midpoints.
        xpos = int(math.ceil((mouse[0]-47)/94.0))
        ypos = int(math.ceil((mouse[1]-47)/94.0))
        
        #Differentiates between horizontal and vertical.
            #If the coordinates has a large x range than y, it is horizontal. 
        is_horizontal = abs(mouse[1] - ypos*94) < abs(mouse[0] - xpos*94)

        ypos = ypos - 1 if mouse[1] - ypos*94 < 0 and not is_horizontal else ypos
        xpos = xpos - 1 if mouse[0] - xpos*94 < 0 and is_horizontal else xpos

        #For showing a hovering line:
        #Define a new board, defined depending on the orientation of the line.
        if is_horizontal:
            board = self.boardH
        else:
            board = self.boardV 

        outOfBounds=False #Incase the mouse is beyond the board...

        #Drawing the hoverline, unless already drawn, taking into consideration if vertical/horizontal.
        #try/except for if it is out of bounds
        try:  #If the line is not already placed,
                #Depending on line orientation, load line on screen.
            if not board[ypos][xpos]:
                if is_horizontal:
                    self.screen.blit(self.hoverH,[xpos*94+5,ypos*94])
                else:
                    self.screen.blit(self.hoverV,[xpos*94,ypos*94+5])

        except: #Exception to if the mouse is out of the board.
            outOfBounds=True
            pass

        if not outOfBounds: #As the line is True (placed) on board,
            alreadyPlaced = board[ypos][xpos] #Position is set to placed.
        else: #Otherwise, it is not already placed.
            alreadyPlaced = False

#If the game is online, the pygame will call to recieve the board from the other
#As they wait for their turn
        if self.isOnline != 'NA':
            if self.turn == False:
                pygame.time.delay(1000)
                self.recvBoard()
            if self.turn == True:
                pass

    #If mouse is clicked, draws a line, if not already drawn and is within the board.
        if pygame.mouse.get_pressed()[0] and not alreadyPlaced and not outOfBounds:

            #if position clicked is horizontal, accesses the horizontal board.
            if is_horizontal:
                self.boardH[ypos][xpos] = True
            #Otherwise, access the vertical board.
            else:
                self.boardV[ypos][xpos]=True

    #End of code gotten by source (Julian Meyer).
            #If a horizontal line is placed:
            if is_horizontal:
                #If its the first row, only check for bottom boxes.
                if ypos ==0:
                    if self.bottomBox(ypos,xpos):
                        #If box made, increment score accordingly.
                        self.addOne()
                    else: #Otherwise switch turns.
                        self.turn = not self.turn

                #If the last row, only check for top boxes.
                elif ypos ==5:
                    if self.topBox(ypos,xpos):
                        self.addOne()
                    else:
                        self.turn = not self.turn
                #Otherwise, check both top and bottom.
                    #If both boxes made, increment by two, otherwise one.
                else:
                    if self.bottomBox(ypos,xpos) and self.topBox(ypos,xpos):
                        self.addTwo()
                    elif self.bottomBox(ypos,xpos) or self.topBox(ypos,xpos):
                        self.addOne()
                    else:
                        self.turn = not self.turn

            #If a vertical line is placed:
            elif not is_horizontal:
                #If the first column, only check the right box.
                if xpos == 0:
                    if self.rightBox(ypos,xpos):
                        self.addOne()
                    else:
                        self.turn = not self.turn

                #If the last column, only check the left box.
                elif xpos ==5:
                    if self.leftBox(ypos,xpos):
                        self.addOne()
                    else:
                        self.turn = not self.turn
                #Otherwise, check both left and right.
                else:
                    if self.leftBox(ypos,xpos) and self.rightBox(ypos,xpos):
                        self.addTwo()
                    elif self.leftBox(ypos,xpos) or self.rightBox(ypos,xpos):
                        self.addOne()
                    else:
                        self.turn = not self.turn

            #If it is the AI's turn, call the AI function.
            if self.turn == False and self.player2 == 'AI':
                self.AI()

            #If the game is online, and the user's turn is finished, send the board
                #to the other player.
            if self.isOnline != 'NA' and self.turn == False:
                    self.sendString = str(self.boardH)+';'+str(self.boardV)+';'+str(self.owner)
                    sendMessage(self.s,self.player2,self.sendString)
            else:
                pass
                

        #Calls function to draw the boxes with every display flip.
        for x in range (5):
            for y in range (5):
                if self.gameOver() !=False:
                    self.drawBox(x,y)

        #Calls the score board GUI, updating after every score.
        self.drawScoreBoard()
        #Updates the pygame interface once a line is drawn.
        pygame.display.flip()



    #Function that accesses the message of the board
    def recvBoard(self):
        #Uses recieve message function to retrieve the sent message.
        self.moveRecieved = recieveMsg(self.s)
        for (u,m) in self.moveRecieved:
            #The board should be over 100 characters, so this ignores other messages.
            if len(m) > 100:
                #Splitting the message, and reseting the strings back to lists, reassigning
                #the board with the new updated board recieved.
                recvLists = m.split(';')
                self.boardH = eval(recvLists[0])

                self.boardV = eval(recvLists[1])

                self.owner = eval(recvLists[2])
                
                #The scores are determined by counting the boxes made using helper function.
                self.playerOneScore = sum(owner == '1' for owner in self.allElements(self.owner))
                self.playerTwoScore = sum(owner == '2' for owner in self.allElements(self.owner))
                #Changes the turn (so it is the current users turn after updating the board).
                self.turn = not self.turn

    #Helper function to access the owner's list to count the scores.
    def allElements(self,lst):
        for sublist in lst:
            for own in sublist:
                yield own


#Functions take a line x and y and returns True if a box is made with it.
#The x and y values represent the top left corner of the line, checks accordingly. 
    def leftBox(self,ypos,xpos):
        #If the line parallel and perpendicular to the line are true...
        if self.boardH[ypos][xpos-1] and self.boardH[ypos+1][xpos-1] and self.boardV[ypos][xpos-1]:
            if self.turn: #Depending on who's turn, set the box's owner as the player.
                #access the owner list according to the top left of box.
                self.owner[xpos-1][ypos] = self.ownerDigit[0]
            else:
                self.owner[xpos-1][ypos]= self.ownerDigit[1]
                
            return True
        return False

#Following three functions perform the same as the leftBox function,
    #but checks at a different orientation.
    def rightBox(self,ypos,xpos):
        if self.boardH[ypos][xpos] and self.boardH[ypos+1][xpos] and self.boardV[ypos][xpos+1]:
            if self.turn:
                self.owner[xpos][ypos] = self.ownerDigit[0]
            else:
                self.owner[xpos][ypos]= self.ownerDigit[1]
            return True
        return False
    
    def topBox(self,ypos,xpos):
        if self.boardH[ypos-1][xpos] and self.boardV[ypos-1][xpos] and self.boardV[ypos-1][xpos+1]:
            if self.turn:
                self.owner[xpos][ypos-1] = self.ownerDigit[0]
            else:
                self.owner[xpos][ypos-1]= self.ownerDigit[1]
            return True
        return False

    def bottomBox(self,ypos,xpos):
        if self.boardH[ypos+1][xpos] and self.boardV[ypos][xpos] and self.boardV[ypos][xpos+1]:
            if self.turn:
                self.owner[xpos][ypos] = self.ownerDigit[0]
            else:
                self.owner[xpos][ypos]= self.ownerDigit[1]
            return True
        return False



#Functions increment the player score depending on who's turn it is.    
    def addOne(self):
        if self.isOnline == False:
            self.playerTwoScore +=1

        elif self.turn == True and self.isOnline !=False:
            self.playerOneScore +=1
        else:
            self.playerTwoScore +=1
#Function increments by two incase two boxes were made simultaneously.
    def addTwo(self):
        if self.isOnline == False:
            self.playerTwoScore +=2

        elif self.turn == True:
            self.playerOneScore +=2
        else:
            self.playerTwoScore +=2



####################################    Aritificial Intelligence   ###############################################
#When the AI function is called, it calls the AI function that corresponds with the chosen difficulty.
    def AI(self):
        #First checks if the game ended before calling a move.
        if self.gameOver() == False:
            return

        #Difficulty 1 represents easy, 2 represents medium and 3 for hard.
        if self.difficulty == 1:
            self.AI1()

        if self.difficulty == 2:
            self.AI2()

        if self.difficulty == 3:
            self.AI3()

    #The easy difficulty randomizes a move on the board.
    def AI1(self):
        #first randomizes the orientation choice.
        lst = ['vertical','horizontal']
        choice = random.choice(lst)

        if choice == 'horizontal':
            x = random.randint(0,4)
            y = random.randint(0,5)

            #If the random line is not already placed, place it.
            #Check if a box is made, increment the score and recursively
            #call the AI. 
            if self.boardH[y][x] == False:
                self.boardH[y][x] = True
                
                #Checks if it made a box, recursion if it did.
                if y ==0:
                    if self.bottomBox(y,x):
                        self.addOne()
                        
                        self.AI()
                    else:
                        self.turn = True
                elif y ==5:
                    if self.topBox(y,x):
                        self.addOne()
                        self.AI()
                    else:
                        self.turn = True
                else:
                    if self.bottomBox(y,x) and self.topBox(y,x):
                        self.addTwo()
                        self.AI()

                    elif self.bottomBox(y,x) or self.topBox(y,x):
                        self.addOne()
                        self.AI()
                    else:
                        self.turn = True

            #If line is already placed, calls AI again.
            else:
                self.AI()
        #If the random choice was vertical...
        #Perform the same actions as for horizontal (check boxes).
        if choice == 'vertical':
            x = random.randint(0,5)
            y = random.randint(0,4)
            if self.boardV[y][x] == False:
                self.boardV[y][x] = True

                if x == 0:
                    if self.rightBox(y,x):
                        self.addOne()
                        self.AI()
                    else:
                        self.turn = True

                elif x ==5:
                    if self.leftBox(y,x):
                        self.addOne()
                        self.AI()                        
                    else:
                        self.turn = True

                else:
                    if self.leftBox(y,x) and self.rightBox(y,x):
                        self.addTwo()
                        self.AI()
                        
                    elif self.leftBox(y,x) or self.rightBox(y,x):
                        self.addOne()
                        self.AI()
                    else:
                        self.turn = True

            else:
                self.AI()

    #The function for the medium level would randomise wether the AI makes a horizontal
    #or vertical move, but checks if the move would make a box or would give a box away
    #(maximises win, minimises loss). However, does not check both orientations,
    #Making it easier but still smart.
    def AI2(self):
        self.movesPossibleH = self.possibleH()
        self.movesPossibleV = self.possibleV()

        lst = ['vertical','horizontal']
        choice = random.choice(lst)

        #If horizontal, and there are possible moves,
        # calls the function (accessH) to check all horizontal moves.
        if choice == 'horizontal':
            if self.movesPossibleH == []:
                self.accessV(self.movesPossibleV)
            else:
                self.accessH(self.movesPossibleH)

        #If vertical, and there are possible moves,
        # calls the function (accessV) to check all vertical moves.
        elif choice == 'vertical':
            if self.movesPossibleV == []:
                self.accessH(self.movesPossibleH)
            else:
                self.accessV(self.movesPossibleV)
            

    #Function loops through all possible moves to find the best horizontal move to make.
    def accessH(self,possibleH):
        self.movesPossibleH = possibleH

        #First loop checks if any of the moves can make a box.
        #If there is such a move, increment the score and call the AI again.
            #It is impossible to make a box if only 1 horizontal line is made,
            #Thus makes the first possible move found.
        for i in self.movesPossibleH: 
            if len(self.movesPossibleH) > 29: 
                self.boardH[i[0]][i[1]] = True
                self.turn = not self.turn
                return
            #If first row, only check bottom boxes.
            if i[0] == 0:
                if self.bottomBox(i[0],i[1]):
                    self.boardH[i[0]][i[1]] = True
                    self.addOne()
                    self.AI()
                    return

            #If last row, only check top boxes.
            elif i[0] == 5:
                if self.topBox(i[0],i[1]):
                    self.boardH[i[0]][i[1]] = True
                    self.addOne()
                    self.AI()
                    return
            #Otherwise, check both top and bottom.
            else:
                if self.bottomBox(i[0],i[1]):
                    if self.topBox(i[0],i[1]):
                        self.boardH[i[0]][i[1]] = True
                        self.addTwo()
                        self.AI()
                        return

                    else:
                        self.boardH[i[0]][i[1]] = True
                        self.addOne()
                        self.AI()
                        return
                    
                else:
                    if self.topBox(i[0],i[1]):
                        self.boardH[i[0]][i[1]] = True
                        self.addOne()
                        self.AI()
                        return

    #Otherwise enters second loop, checks if the move would make a potential box, otherwise makes it
    #and swithces the turn.
        for i in self.movesPossibleH:
            #If the first row, only check bottom boxes.
            if i[0] == 0:
                if self.checkBoxBottomH(i[0],i[1]) == False:
                    self.boardH[i[0]][i[1]] = True
                    self.turn = not self.turn
                    return

            #If the last row, only check top boxes.
            elif i[0] ==5:
                if self.checkBoxTopH(i[0],i[1]) == False:
                    self.boardH[i[0]][i[1]] = True
                    self.turn = not self.turn
                    return

            #Otherwise, makes sure if the move will not make a potential box both
            #top and bottom.
            else:
                if (self.checkBoxBottomH(i[0],i[1]) == False) and (self.checkBoxTopH(i[0],i[1])== False):
                    self.boardH[i[0]][i[1]] = True
                    self.turn = not self.turn
                    return
            
        #If all moves would not make a box and all make potential boxes, make any move.
        self.boardH[i[0]][i[1]] = True
        self.turn = not self.turn
        return
            

        #First loop checks if any of the moves can make a box.
        #If there is such a move, increment the score and call the AI again.
            #It is impossible to make a box if only 1 vertical line is made,
            #Thus makes the first possible move found.


    #Function loops through all possible moves to find the best vertical move to make.
    def accessV(self,possibleV):
        self.movesPossibleV = possibleV
        for i in self.movesPossibleV:
            if len(self.movesPossibleV) > 29:
                self.boardV[i[0]][i[1]] = True
                self.turn = not self.turn
                return

            #If first column, only check right boxes.
            if i[1] == 0:
                if self.rightBox(i[0],i[1]):
                    self.boardV[i[0]][i[1]] = True
                    self.addOne()
                    self.AI()
                    return

            #If last column, only check left boxes.
            elif i[1] == 5:
                if self.leftBox(i[0],i[1]):
                    self.boardV[i[0]][i[1]] = True
                    self.addOne()
                    self.AI()
                    return
            #Otherwise, check both left and right.
            else:
                if self.rightBox(i[0],i[1]):
                    if self.leftBox(i[0],i[1]):
                        self.boardV[i[0]][i[1]] = True
                        self.addTwo()
                        self.AI()
                        return
                    else:
                        self.boardV[i[0]][i[1]] = True
                        self.addOne()
                        self.AI()
                        return
                
                else:
                    if self.leftBox(i[0],i[1]):
                        self.boardV[i[0]][i[1]] = True
                        self.addOne()
                        self.AI()
                        return

    #Otherwise enters second loop, checks if the move would make a potential box, otherwise makes it
    #and swithces the turn.        
        for i in self.movesPossibleV:
            #If the first column, only check right boxes.
            if i[1] == 0:
                if self.checkBoxRightV(i[0],i[1]) == False:
                    self.boardV[i[0]][i[1]] = True
                    self.turn = not self.turn
                    return
            #If the last column, only check left boxes.
            elif i[1] == 5:
                if self.checkBoxLeftV(i[0],i[1]) == False:
                    self.boardV[i[0]][i[1]] = True
                    self.turn = not self.turn
                    return

            #Otherwise, makes sure if the move will not make a potential box both
            #top and bottom.
            else:
                if self.checkBoxRightV(i[0],i[1]) == False and self.checkBoxLeftV(i[0],i[1]) == False:
                    self.boardV[i[0]][i[1]] = True
                    self.turn = not self.turn
                    return
        #otherwise make any possible move.
        self.boardV[i[0]][i[1]] = True
        self.turn = not self.turn
        return




    #This function contains both horizontal and vertical loops,
    #It will check for boxes both horizontal and vertical, and check the boxes
    #It would never miss a box, and would avoid all moves that would make a potential box. 
    def AI3(self):
        self.movesPossibleH = self.possibleH()
        self.movesPossibleV = self.possibleV()
            
        for i in self.movesPossibleH:
            if len(self.movesPossibleH) > 29:
                self.boardH[i[0]][i[1]] = True
                self.turn = not self.turn
                return

            if i[0] == 0:
                if self.bottomBox(i[0],i[1]):
                    self.boardH[i[0]][i[1]] = True
                    self.addOne()
                    self.AI()
                    return

            elif i[0] == 5:
                if self.topBox(i[0],i[1]):
                    self.boardH[i[0]][i[1]] = True
                    self.addOne()
                    self.AI()
                    return

            else:
                if self.bottomBox(i[0],i[1]):
                    if self.topBox(i[0],i[1]):
                        self.boardH[i[0]][i[1]] = True
                        self.addTwo()
                        self.AI()
                        return

                    else:
                        self.boardH[i[0]][i[1]] = True
                        self.addOne()
                        self.AI()
                        return
                    
                else:
                    if self.topBox(i[0],i[1]):
                        self.boardH[i[0]][i[1]] = True
                        self.addOne()
                        self.AI()
                        return

        for i in self.movesPossibleV:
            if len(self.movesPossibleV) > 29:
                self.boardV[i[0]][i[1]] = True
                self.turn = not self.turn
                return

            if i[1] == 0:
                if self.rightBox(i[0],i[1]):
                    self.boardV[i[0]][i[1]] = True
                    self.addOne()
                    self.AI()
                    return

            elif i[1] == 5:
                if self.leftBox(i[0],i[1]):
                    self.boardV[i[0]][i[1]] = True
                    self.addOne()
                    self.AI()
                    return

            else:
                if self.rightBox(i[0],i[1]):
                    if self.leftBox(i[0],i[1]):
                        self.boardV[i[0]][i[1]] = True
                        self.addTwo()
                        self.AI()
                        return
                    else:
                        self.boardV[i[0]][i[1]] = True
                        self.addOne()
                        self.AI()
                        return

                else:
                    if self.leftBox(i[0],i[1]):
                        self.boardV[i[0]][i[1]] = True
                        self.addOne()
                        self.AI()
                        return


        for i in self.movesPossibleH:
            if i[0] == 0:
                if self.checkBoxBottomH(i[0],i[1]) == False:
                    self.boardH[i[0]][i[1]] = True
                    self.turn = not self.turn
                    return

            elif i[0] ==5:
                if self.checkBoxTopH(i[0],i[1]) == False:
                    self.boardH[i[0]][i[1]] = True
                    self.turn = not self.turn
                    return


            else:
                if (self.checkBoxBottomH(i[0],i[1]) == False) and (self.checkBoxTopH(i[0],i[1])== False):
                    self.boardH[i[0]][i[1]] = True
                    self.turn = not self.turn
                    return
            

        for i in self.movesPossibleV:
            if i[1] == 0:
                if self.checkBoxRightV(i[0],i[1]) == False:
                    self.boardV[i[0]][i[1]] = True
                    self.turn = not self.turn
                    return

            elif i[1] == 5:
                if self.checkBoxLeftV(i[0],i[1]) == False:
                    self.boardV[i[0]][i[1]] = True
                    self.turn = not self.turn
                    return

            else:
                if self.checkBoxRightV(i[0],i[1]) == False and self.checkBoxLeftV(i[0],i[1]) == False:
                    self.boardV[i[0]][i[1]] = True
                    self.turn = not self.turn
                    return

        self.boardV[i[0]][i[1]] = True
        self.turn = not self.turn
        return


#Helper functions 'possible' find the possible moves it can make on the board,
#Returns a list of the coordinates of the lines.
    def possibleH(self): #For horizontal moves.
        self.movesH = []
        for x in range(0,5):
            for y in range(0,6):
                if self.boardH[y][x] == False:
                    self.movesH.append([y,x])
        return self.movesH

    def possibleV(self): #For vertical moves.
        self.movesV = []
        for x in range(0,6):
            for y in range(0,5):
                if self.boardV[y][x] == False:
                    self.movesV.append([y,x])

        return self.movesV

#following 4 helper functions check if a 3 sided box would be made with the input coordinates.
    #Checks if potential box made below the line.
    def checkBoxBottomH(self,y,x):
        count = 1
        #If 2 of the 3 lines are already made, then the move would make a potential box
        if self.boardH[y+1][x]:
            count +=1
        if self.boardV[y][x]:
            count +=1
        if self.boardV[y][x+1]:
            count +=1
        if count == 3:
            #returns true if a potential box would be made, otherwise false.
            return True
        else:
            return False


    #Checks if potential box made above the line.
    def checkBoxTopH(self,y,x):
        count = 1
        if self.boardH[y-1][x]:
            count +=1
        if self.boardV[y-1][x]:
            count +=1
        if self.boardV[y-1][x+1]:
            count +=1
        if count ==3:
            return True
        else:
            return False


    #Checks if potential box made right of the line.
    def checkBoxRightV(self,y,x):
        count = 1
        if self.boardH[y][x]:
            count +=1
        if self.boardH[y+1][x]:
            count +=1
        if self.boardV[y][x+1]:
            count +=1
        if count ==3:
            return True
        else:
            return False

    #Checks if potential box made left of the line.
    def checkBoxLeftV(self,y,x):
        count = 1
        if self.boardH[y][x-1]:
            count +=1
        if self.boardH[y+1][x-1]:
            count +=1
        if self.boardV[y][x-1]:
            count +=1
        if count ==3:
            return True
        else:
            return False

###################################     Graphical User Interface    ##############################################
#Function loads the images for graphics as variables. 
    def gameImages(self):
        #Loads the line vertically and horizontally.
        self.lineV=pygame.image.load("normalline.png")
        self.lineH=pygame.transform.rotate(pygame.image.load("normalline.png"), -90)

        #Loads the hovering line vertically and horizontally.
        self.hoverV=pygame.image.load("hoverline.png")
        self.hoverH=pygame.transform.rotate(pygame.image.load("hoverline.png"), -90)

        #Loads the dot for the board interface.
        self.dots=pygame.image.load("dot.png")

        #Loads the boxes of all color options.
        self.greenPlayer=pygame.image.load("greenplayer.png")
        self.bluePlayer=pygame.image.load("blueplayer.png")
        self.yellowPlayer=pygame.image.load("yellowplayer.png")
        self.redPlayer=pygame.image.load("redplayer.png")
        self.purplePlayer=pygame.image.load("purpleplayer.png")


    def drawBoard(self):
        #Adds the scores graphics on the screen.
        if self.gameOver() == False:
            return
        #If the a horizontal line is placed, load the line on screen.
        for x in range(5):
            for y in range(6):
                #If the line is true, then place the line image.
                if self.boardH[y][x]:
                    self.screen.blit(self.lineH, [(x)*94+5, (y)*94])

        #If the a vertical line is placed, load the line on screen.
        for x in range(6):
            for y in range(5):
                if self.boardV[y][x]:
                    self.screen.blit(self.lineV, [(x)*94, (y)*94+5])

        #draw dots as a grid on game interface.
        for x in range(6):
            for y in range(6):
                self.screen.blit(self.dots, [x*94, y*94])
        
                   


#Function create the interface of the scoreboard and turns.    
    def drawScoreBoard(self):
        if self.gameOver() == False:
            return
        #Defining the the player name depending on the who's turn.
        if self.turn == True:
            self.playerTurn = str(self.player1)
        else:
            self.playerTurn = str(self.player2)

        #creates the text for turns and places them on the screen.
        label = self.fontTurn.render("Turn:", 1, (0,0,200))
        player = self.fontTurn.render(self.playerTurn, 1, (0,0,0))
        self.screen.blit(label, (10, 540))
        self.screen.blit(player, (100, 540))

        #Creating the text for turns and their scores.
        #Player text colored according to chosen color. 
        scoreOne = self.fontScore.render(str(self.playerOneScore), 1, (0,0,0))
        scoreTwo = self.fontScore.render(str(self.playerTwoScore), 1, (0,0,0))
        scoreOneText = self.fontName.render(str(self.player1), 1, self.textColor[self.color1])
        scoreTwoText = self.fontName.render(str(self.player2), 1, self.textColor[self.color2])

        #If the game is not online/or the player started as player 1:
        if self.isOnline != False:
            scoreOne = self.fontScore.render(str(self.playerOneScore), 1, (0,0,0))
            scoreTwo = self.fontScore.render(str(self.playerTwoScore), 1, (0,0,0))

        #If the player started as player 2, show scores accordingly(otherwise is swapped).
        if self.isOnline == False:
            scoreOne = self.fontScore.render(str(self.playerTwoScore), 1, (0,0,0))
            scoreTwo = self.fontScore.render(str(self.playerOneScore), 1, (0,0,0))

        #Places the texts on the screen. 
        self.screen.blit(scoreOneText, (520, 100))
        self.screen.blit(scoreOne, (540, 150))
        self.screen.blit(scoreTwoText, (520, 300))
        self.screen.blit(scoreTwo, (540, 350))



#Function draws the boxes, depending on the owner's list.
        #Places the box according to the xy indexes of owner, and if player 1's or 2's.
    def drawBox(self,x,y):
        if self.gameOver() == False:
            return
        if self.owner[x][y]=="1":
            self.screen.blit(self.playerBox[0], (x*94+5, y*94+5))
        if self.owner[x][y]=="2":
            self.screen.blit(self.playerBox[1], (x*94+5, y*94+5))



#Function checks if the game is over, by checking if the score is 25
#As there are 25 possible boxes.
    def gameOver(self):
        #If all 25 boxes are owned, end the game.
        #Display a tkinter pop up of winner
        #Quite the pygame and restores the main window. 
        if (self.playerOneScore + self.playerTwoScore == 25):
            #If the game is online, and it is the last turn, the player will send
            #the final board in order to update to a game over for the other user as well.
            if self.isOnline != 'NA' and self.turn == True:
                    self.overMsg = str(self.boardH)+';'+str(self.boardV)+';'+str(self.owner)
                    sendMessage(self.s,self.player2,self.overMsg)
                    self.recvBoard()
            return False #Returns false if the game is over.
        return True #True if the game isnt over.


####################################    Main Loop   ###############################################

#Creates the main window, and calls the main window for the game.
wnd = Tk()
wnd.geometry("600x600")
wnd.title("Dots and Boxes")

theApp = mainwnd(wnd)

#Assigns the game window the mainloop.
wnd.mainloop()
