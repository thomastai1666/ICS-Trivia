# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 09:58:31 2015

@author: zhengzhang
"""

#==============================================================================
# Group class:
#==============================================================================
import prettytable

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
        #print(self.answers[name])
        return self.answers[name]

    def increase_score(self, name, add = 10):
        self.members[name] += add
        
    def list_scores(self):
        full_list = "\nScoreboard: " + "\n"
        count = 1
        full_list += "Name | Score\n" 
        for user in sorted(self.members.keys()):
            full_list += "%d.) %s %s\n" % (count, user, self.members[user])
            count += 1
        return full_list
    
    def get_highscore(self):
        user = max(self.members, key=lambda i: self.members[i])
        return user, self.members[user]
        
    def is_member(self, name):
        return name in self.members.keys()

    def leave(self, name):
        print(name + " has left")
        del self.members[name]

    def list_all(self):
        full_list = ""
        for name in self.members.keys():
            full_list += name + "\n"
        return full_list
        """
        full_list = "Players: ------------" + "\n"
        count = 0
        for user in self.answers.keys():
            full_list += str(count) + ".) " + user + "\n"
            count += 1
        """
        
    
    def list_members(self):
        return self.members.keys()
    
g = Group()
