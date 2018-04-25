# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 09:58:31 2015

@author: zhengzhang
"""

#==============================================================================
# Group class:
#==============================================================================

class Group:

    def __init__(self):
        self.members = {}

    def join(self, name):
        self.members[name] = 0

    def is_member(self, name):
        return name in self.members.keys()

    def leave(self, name):
        print(name + " has left")
        del self.members[name]

    def list_all(self):
        # a simple minded implementation
        full_list = "Scoreboard: ------------" + "\n"
        full_list += str(self.members) + "\n"
        return full_list
    
    def list_members(self):
        return self.members.keys()
    
g = Group()
