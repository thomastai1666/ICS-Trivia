# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 09:58:31 2015

@author: thomas
"""

#==============================================================================
# Trivia Class
# Manages questions and gives answers
#==============================================================================
import random

class Trivia():

    def __init__(self, questions = 3):
        self.loadFile()
        self.usedQuestions = []
        self.currentQuestion = 0
        self.totalQuestions = len(self.data)
        self.questionLimit = questions
    
    def loadFile(self, file_name = 'gamefile.csv'):
        self.data = []
        self.file = open(file_name, 'r')
        self.header = self.file.readline()
        all_lines = self.file.readlines()
        for line in all_lines:
            line = str(line.strip())
            line_items = line.split(',')
            self.data.append(line_items)
            
    def printData(self):
        return str(self.data) + "\n"
        
    def getQuestion(self):
        if(len(self.usedQuestions) > self.questionLimit):
            return None
        questionNum = self.randomQuestion()
        while(questionNum in self.usedQuestions):
            questionNum = self.randomQuestion()
        self.usedQuestions.append(questionNum)
        self.currentQuestion = questionNum
        return self.data[questionNum][0:5]
    
    def getAnswer(self):
        return self.data[self.currentQuestion][-1]
    
    def checkAnswer(self, ans):
        if(type(ans) == int):
            return ans == self.getAnswer(ans)
        elif(type(ans) == chr):
            return ans == self.getAnswer(ord(ans) - 65)
    
    def randomQuestion(self):
        return random.randint(0,self.totalQuestions-1)
    
"""
game = Trivia()
print(game.printData())
for x in range(0,3):
    print(game.getQuestion())
    print(game.getAnswer())
"""