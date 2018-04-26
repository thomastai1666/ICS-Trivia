"""
Created on Sun Apr  5 00:00:32 2015
@author: zhengzhang
"""
from admin_utils import *
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

    def proc(self, my_msg, peer_msg):
        self.out_msg = ''
#==============================================================================
# Admin client does not respond to S_CHATTING events
# The only state it currently is allowed to be in is S_LOGGEDIN
# The admin client allows for server side commands that the client should not see
#==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            
            if len(peer_msg) > 0:
                peer_msg = json.loads(peer_msg)
                if peer_msg["action"] == "leave":
                    self.out_msg += 'You have been disconnected from the server.\n'
                    self.state = S_OFFLINE
                    
            if len(my_msg) > 0:

                if my_msg == 'quit':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, json.dumps({"action":"time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, json.dumps({"action":"list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg == 'kick':
                    user = my_msg[5:]
                    self.out_msg += 'Not implemented'
                        
                elif my_msg == 'shutdown':
                    mysend(self.s, json.dumps({"action":"shutdown"}))
                    self.out_msg += 'Server successfully shut down\n'
                    
                elif my_msg == 'start':
                    mysend(self.s, json.dumps({"action":"start"}))
                    self.out_msg += 'Trivia is starting...\n'
                        
                elif my_msg[:9] == 'broadcast':
                    text = my_msg[10:]
                    msg_to_send = json.dumps({"action":"broadcast","message":text})
                    mysend(self.s, msg_to_send)
                    self.out_msg += 'Message sent\n'
                    
                else:
                    self.out_msg += menu

#==============================================================================
# invalid state
#==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg