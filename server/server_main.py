"""
Created on Tue Jul 22 00:47:05 2014

@author: alina, zzhang
"""

import time
import socket
import select
import sys
import string
import json
import pickle as pkl
from server_chatutil import *
import server_groups as grp
import server_trivia as trivia

class Server:
    def __init__(self):
        #Client variables
        self.new_clients = [] #list of new sockets of which the user id is not known
        self.logged_name2sock = {} #dictionary mapping username to socket
        self.logged_sock2name = {} # dict mapping socket to user name
        self.all_sockets = []
        self.group = grp.Group()
        #start server
        self.server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(5)
        self.all_sockets.append(self.server)
        self.serverOnline = True
        #Trivia variables
        self.Trivia = trivia.Trivia()
        self.gameState = False
        self.waitingForQuestion = False

    def new_client(self, sock):
        #add to all sockets and to new clients
        print('new client...')
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def login(self, sock):
        #read the msg that should have login code plus username
        try:
            msg = json.loads(myrecv(sock))
            if len(msg) > 0:

                if msg["action"] == "login":
                    name = msg["name"]
                    if self.group.is_member(name) != True:
                        #move socket from new clients list to logged clients
                        self.new_clients.remove(sock)
                        #add into the name to sock mapping
                        self.logged_name2sock[name] = sock
                        self.logged_sock2name[sock] = name
                        print(name + ' logged in')
                        self.group.join(name)
                        mysend(sock, json.dumps({"action":"login", "status":"ok"}))
                    else: #a client under this name has already logged in
                        mysend(sock, json.dumps({"action":"login", "status":"duplicate"}))
                        print(name + ' duplicate login attempt')
                else:
                    print ('wrong code received')
            else: #client died unexpectedly
                self.logout(sock)
        except:
            self.all_sockets.remove(sock)

    def logout(self, sock):
        #remove sock from all lists
        name = self.logged_sock2name[sock]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        self.all_sockets.remove(sock)
        self.group.leave(name)
        sock.close()

#==============================================================================
# main command switchboard
#==============================================================================
    def handle_msg(self, from_sock):
        #read msg code
        msg = myrecv(from_sock)
        if len(msg) > 0:
            
#==============================================================================
#           #Client: ping
#==============================================================================
            msg = json.loads(msg)
            if msg["action"] == "ping":
                from_name = self.logged_sock2name[from_sock]
                msg = json.dumps({"action":"pong"})
                mysend(from_sock, msg)
                
#==============================================================================
#           Client: Answer exchange
#==============================================================================
            elif msg["action"] == "exchange":
                # Find the list of people to send to and index message!!
                from_name = self.logged_sock2name[from_sock]
                from_msg = msg["message"]
                self.group.set_answer(from_name, from_msg)
                #print("Debug: Message from " + from_name + ": " +from_msg)

#==============================================================================
#           Unused: Disconnect (AKA Bye)
#==============================================================================
            elif msg["action"] == "disconnect":
                pass
                
#==============================================================================
#           Admin: start trivia game
#==============================================================================
            elif msg["action"] == "start":
                self.playTrivia()

#==============================================================================
#           Admin: shutdown server
#==============================================================================
            elif msg["action"] == "shutdown":
                self.serverOnline = False
                
#==============================================================================
#           Admin: kick client
#==============================================================================
            elif msg["action"] == "kick":
                admin_name = self.logged_sock2name[from_sock]
                user = msg["user"]
                socket = self.logged_name2sock[user]
                self.sendGlobalMessage(admin_name + " kicked "  + user)
                disconnect_msg = json.dumps({"action":"leave"})
                mysend(socket, disconnect_msg)
                
#==============================================================================
#           Admin: broadcast message
#==============================================================================
            elif msg["action"] == "broadcast":
                from_name = self.logged_sock2name[from_sock]
                message = msg["message"]
                self.sendGlobalMessage("(" + from_name + ") " + message)
                
#==============================================================================
#           Client: List all players
#==============================================================================
            elif msg["action"] == "list":
                #pass
                from_name = self.logged_sock2name[from_sock]
                message = self.group.list_all()
                mysend(from_sock, json.dumps({"action":"list", "results":message}))
                
#==============================================================================
#           Client: Send "me" message
#==============================================================================
            elif msg["action"] == "me":
                #pass
                from_name = self.logged_sock2name[from_sock]
                message = from_name + " says " + msg["message"]
                self.sendGlobalMessage(message)
                
#==============================================================================
#           Client: Display time
#==============================================================================
            elif msg["action"] == "time":
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                mysend(from_sock, json.dumps({"action":"time", "results":ctime}))

        else:
            #client died unexpectedly
            self.logout(from_sock)
    
#==============================================================================

    def sendGlobalMessage(self, text):
        #Sends a single message to all clients
        self.startServerChat(text)
        self.endServerChat()
        
            
    def startServerChat(self,text = " "):
        #Start chat exchange for trivia game
        everyone = list(self.group.list_members())
        msg = json.dumps({"action":"exchange", "from": "[Server]: ", "message":text})
        status_msg = json.dumps({"action":"connect", "status":"request", "from":"[Server]"})
        for person in everyone:
            to_sock = self.logged_name2sock[person]
            mysend(to_sock, status_msg)
            mysend(to_sock, msg)
            
    def sendMessage(self,text,label = True):
        #Send message through chat exchange
        everyone = list(self.group.list_members())
        if label:
            msg = json.dumps({"action":"exchange", "from": "[Server]: ", "message":text})
        else:
            msg = json.dumps({"action":"exchange", "message":text})
        for person in everyone:
            to_sock = self.logged_name2sock[person]
            mysend(to_sock, msg)
        
    def endServerChat(self):
        #Disconnect client from server chat
        disconnect_msg = json.dumps({"action":"disconnect"})
        everyone = list(self.group.list_members())
        for person in everyone:
            to_sock = self.logged_name2sock[person]
            mysend(to_sock, disconnect_msg)
            
    def playTrivia(self):
        #Initialize game
        self.startServerChat("Trivia has started!")
        self.gameState = True
        #Loop through x number of questions
        for x in range(0, self.Trivia.questionLimit):
            #Use decimal character to label questions
            prefix = 65
            questionList = self.Trivia.getQuestion()
            self.sendMessage("Question: " + questionList[0])
            #Loop through question and choices
            for question in questionList[1:]:
                self.sendMessage(chr(prefix) + ".) " + question)
                prefix += 1
            #Get client response (wait 10 seconds)
            self.sendMessage("You have ten seconds to answer.")
            time.sleep(10)
            self.processMessages()
            self.checkQuestions()
        #End game
        print("Trivia has Ended. Thanks for playing!")
        winner, score = self.group.get_highscore()
        self.sendMessage("Highest score is " + str(winner) + " with core: " +str(score))
        self.sendMessage(self.group.list_scores())
        self.gameState = False
        self.endServerChat()
        
    def processMessages(self):
        #Server does not update messages when in a loop, so manually process it within this scope
        read,write,error=select.select(self.all_sockets,[],[])
        for logc in list(self.logged_name2sock.values()):
            if logc in read:
                self.handle_msg(logc)
    
    def checkQuestions(self):
        #Check answer to see if it is correct
        #Cycle through each player to ask questions
        for player in self.group.list_members(): 
                #Check if answer is correct
                playeranswer = self.group.get_answer(player)
                correctAnswer = self.Trivia.getAnswer()
                correct = self.Trivia.checkAnswer(playeranswer)
                msg = ""
                #Correct, give 10 points
                if(correct):
                    msg = json.dumps({"action":"exchange", "from": "[Server]: ", \
                                      "message":"Answer correct! +10 Points"})
                    self.group.increase_score(player,10)
                #Incorrect, send right answer
                else:
                    msg = json.dumps({"action":"exchange", "from": "[Server]: ", \
                                      "message":"Incorrect. The right answer was: " + str(chr(65+int(correctAnswer)))})
                #Send messages to player
                to_sock = self.logged_name2sock[player]
                mysend(to_sock, msg)
    
    def endGameStats(self):
        #Shows highest scoring players
        pass

    def closeServer(self, sock):
        #Close server socket, disconnect users, then shut down server
        print("Server shutting down...")
        everyone = list(self.group.list_members())
        for person in everyone:
            disconnect_msg = json.dumps({"action":"leave"})
            socket = self.logged_name2sock[person]
            mysend(socket, disconnect_msg)
        time.sleep(3)
        print("Server has been shut down.")
        sock.close()

#==============================================================================
# main loop, loops *forever*
#==============================================================================
    def run(self):
        print ('starting server...')
        while(1):
           read,write,error=select.select(self.all_sockets,[],[])
           print('checking logged clients..')
           for logc in list(self.logged_name2sock.values()):
               if logc in read:
                   self.handle_msg(logc)
           print('checking new clients..')
           for newc in self.new_clients[:]:
               if newc in read:
                   self.login(newc)
           print('checking for new connections..')
           if self.server in read :
               #new client request
               sock, address=self.server.accept()
               self.new_client(sock)
           if self.serverOnline == False:
               self.closeServer(newc)
               break

def main():
    server=Server()
    server.run()

main()
