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
from chat_utils import *
import chat_group as grp

class Server:
    def __init__(self):
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
# handle connect request this is implemented for you
#==============================================================================
            msg = json.loads(msg)
            if msg["action"] == "join":
                self.sendGlobalMessage("Waiting for game to start...")
                """
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = json.dumps({"action":"connect", "status":"self"})
                # connect to the peer
                elif self.group.is_member(to_name):
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)
                    msg = json.dumps({"action":"connect", "status":"success"})
                    for g in the_guys[1:]:
                        to_sock = self.logged_name2sock[g]
                        mysend(to_sock, json.dumps({"action":"connect", "status":"request", "from":from_name}))
                else:
                    msg = json.dumps({"action":"connect", "status":"no-user"})
                mysend(from_sock, msg)
                """
#==============================================================================
# handle messeage exchange: IMPLEMENT THIS
#==============================================================================
            elif msg["action"] == "exchange":
                # Find the list of people to send to and index message!!
                from_name = self.logged_sock2name[from_sock]
                print("Message from " + from_name + ": " +msg["message"])
                """
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                from_name = self.logged_sock2name[from_sock]
                from_msg = msg["message"]
                the_guys = self.group.list_me(from_name)[1:]
                #Index for current user
                msg_to_save = ctime + ") " + from_name + " : " + from_msg
                self.indices[from_name].add_msg_and_index(msg_to_save)
                for g in the_guys:
                    #Index for other members of group chat
                    self.indices[g].add_msg_and_index(msg_to_save)
                    to_sock = self.logged_name2sock[g]
                    msg = json.dumps({"action":"exchange", "from": "[" + from_name + "]", "message":from_msg})
                    mysend(to_sock, msg)
                """

#==============================================================================
# the "from" guy has had enough (talking to "to")!
#==============================================================================
            elif msg["action"] == "disconnect":
                pass
                #from_name = self.logged_sock2name[from_sock]
                #self.group.leave(from_name)
#==============================================================================
#                 listing available peers: IMPLEMENT THIS (Done)
#==============================================================================
            elif msg["action"] == "list":
                #pass
                from_name = self.logged_sock2name[from_sock]
                msg = self.group.list_all()
                mysend(from_sock, json.dumps({"action":"list", "results":msg}))
#==============================================================================
#                 time
#==============================================================================
            elif msg["action"] == "time":
                ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
                mysend(from_sock, json.dumps({"action":"time", "results":ctime}))

#==============================================================================
#                 the "from" guy really, really has had enough
#==============================================================================

        else:
            #client died unexpectedly
            self.logout(from_sock)
    
    def sendGlobalMessage(self, text):
        everyone = list(self.group.list_members())
        msg = json.dumps({"action":"exchange", "from": "[Server]: ", "message":text})
        status_msg = json.dumps({"action":"connect", "status":"request", "from":"[Server]"})
        for person in everyone:
            to_sock = self.logged_name2sock[person]
            mysend(to_sock, status_msg)
            mysend(to_sock, msg)
            
    def endServerChat(self):
        disconnect_msg = json.dumps({"action":"disconnect"})
        everyone = list(self.group.list_members())
        for person in everyone:
            mysend(to_sock, disconnect_msg)
        

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

def main():
    server=Server()
    server.run()

main()
