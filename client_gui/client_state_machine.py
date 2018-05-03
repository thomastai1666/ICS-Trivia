"""
Created on Sun Apr  5 00:00:32 2015
@author: zhengzhang
"""
from client_utils import *
import json

class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action":"connect", "target":peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += 'You are connected with '+ self.peer + '\n'
            return (True)
        elif response["status"] == "busy":
            self.out_msg += 'User is busy. Please try again later\n'
        elif response["status"] == "self":
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return(False)

    def disconnect(self):
        msg = json.dumps({"action":"disconnect"})
        mysend(self.s, msg)
        #self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Once logged in, do a few things: get peer listing, connect, search
# And, of course, if you are so bored, just go
# This is event handling instate "S_LOGGEDIN"
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'quit':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in
                    
                elif my_msg == 'help' or my_msg == 'menu':
                    self.out_msg += menu

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg == 'ping':
                    mysend(self.s, json.dumps({"action":"ping"}))
                    
                elif my_msg[:2] == 'me':
                    msg = my_msg[3:]
                    mysend(self.s, json.dumps({"action":"me","message":msg}))

                else:
                    self.out_msg += menu
                    
            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.peer = peer_msg["from"]
                    #self.out_msg += 'Connected to Game Server ' + self.peer + '\n'
                    self.state = S_CHATTING
                elif peer_msg["action"] == "leave":
                    self.out_msg += 'ACTION,CHAT_IN,[Server]: Disconnected from server\n'
                    self.state = S_OFFLINE
                elif peer_msg["action"] == "pong":
                    self.out_msg += "Pong!\n"
                elif peer_msg["action"] == "begingame":
                    self.out_msg += "ACTION,BEGIN_GAME"
                elif peer_msg["action"] == 'updatepeers':
                    allPeers = peer_msg["name"]
                    self.out_msg += "ACTION,PEER_CONNECT," + allPeers

#==============================================================================
# Start chatting, 'bye' for quit
# This is event handling instate "S_CHATTING"
#==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:     # my stuff going out
                msg = my_msg[3:]
                mysend(self.s, json.dumps({"action":"exchange", "from":"[" + self.me + "]", "message":msg}))
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''
            if len(peer_msg) > 0:    # peer's stuff, coming in
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "connect":
                    self.out_msg += "(" + peer_msg["from"] + " joined)\n"
                elif peer_msg["action"] == "disconnect":
                    self.state = S_LOGGEDIN
                elif peer_msg["action"] == "leave":
                    self.out_msg += 'You have been disconnected from the server.\n'
                    self.state = S_OFFLINE
                elif peer_msg["action"] == "exchange":
                    self.out_msg += "ACTION,CHAT_IN," + peer_msg["from"] + peer_msg["message"]
                else:
                    self.out_msg += "DEBUG:" + peer_msg


            # Display the menu again
            #if self.state == S_LOGGEDIN:
            #    self.out_msg += menu
#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg