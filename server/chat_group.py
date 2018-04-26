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
        self.answers = {}

    def join(self, name):
        self.members[name] = 0
        self.answers[name] = ""
        
    def set_answer(self, name, ans):
        self.answers[name] = ans
        
    def clearAnswer(self):
        for name in self.answers.keys():
            self.answers[name] = ""
        
    def get_answer(self, name):
        print(self.answers)
        return self.answers[name]

    def increase_score(self, name, add = 10):
        self.members[name] += add
        
    def is_member(self, name):
        return name in self.members.keys()

    def leave(self, name):
        print(name + " has left")
        del self.members[name]

    def list_all(self):
        full_list = "Scoreboard: ------------" + "\n"
        full_list += str(self.members) + "\n"
        return full_list
    
    def list_members(self):
        return self.members.keys()
    
g = Group()
