# -*- coding: utf-8 -*-
"""
Created on Sat Jul  5 11:38:58 2014

@author: zzhang
"""
import pickle

class Index:
    def __init__(self, name):
        self.name = name
        self.msgs = [];
        self.index = {}
        self.total_msgs = 0
        self.total_words = 0
        
    def get_total_words(self):
        return self.total_words
        
    def get_msg_size(self):
        return self.total_msgs
        
    def get_msg(self, n):
        return self.msgs[n]
        
    # implemented: Append words to list
    def add_msg(self, m):
        #Add message to class list and increment counter
        self.msgs.append(m)
        self.total_msgs += 1
        
    def add_msg_and_index(self, m):
        #Call add message function, then index the current message
        self.add_msg(m)
        line_at = self.total_msgs - 1
        self.indexing(m, line_at)

    # implemented: Index words 
    def indexing(self, m, l):
        #Split message into words (Spaces ini between)
        words = m.split(" ")
        #For each word, add to dictionary with line number
        for word in words:
            word = word.strip()
            if(word != ""):
                #If word is not in dictionary, initialize list
                if word not in self.index:
                    self.index[word] = []
                self.index[word].append(l)
                #Increment total words counter variable
                self.total_words += 1

    # implement: query interface      
    def search(self, term):
        '''
        return a list of tupple. if index the first sonnet (p1.txt), then
        call this function with term 'thy' will return the following:
        [(7, " Feed'st thy light's flame with self-substantial fuel,"),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (9, ' Thy self thy foe, to thy sweet self too cruel:'),
         (12, ' Within thine own bud buriest thy content,')]
                  
        ''' 
        msgs = []
        #Look for line number of word, otherwise return false
        search_linenums = self.index.get(term, False)
        if(search_linenums != False):
            #For each line number given, add to tuple along with the line in poem
            for search_eachnum in search_linenums:
                tuple_to_add = tuple([search_eachnum, self.msgs[search_eachnum]])
                #Improvement: ignore duplicates
                if(tuple_to_add not in msgs):
                    msgs.append(tuple_to_add)
        return msgs

class PIndex(Index):
    def __init__(self, name):
        super().__init__(name)
        roman_int_f = open('roman.txt.pk', 'rb')
        self.int2roman = pickle.load(roman_int_f)
        roman_int_f.close()
        self.load_poems()
        
    # implemented: 1) open the file for read, then call
    # the base class's add_msg_and_index
    def load_poems(self):
        #Open file and break up into a list of lines
        poem_file = open(self.name, 'r')
        self.entire_text = poem_file.read().split("\n")
        #Add each message (Line)
        for x in self.entire_text:
            self.add_msg_and_index(x)
    
    # implemented: p is an integer, get_poem(1) returns a list,
    # each item is one line of the 1st sonnet
    def get_poem(self, p):
        poem = []
        #Get current and next poem roman numerals to be used as markers
        #If unable to find poem, function will return empty list
        roman_num = self.int2roman.get(p,False)
        next_roman_num = self.int2roman.get(p+1,False)
        #Check to make sure roman numeral is valid and found
        if(roman_num != False and next_roman_num != False):
            begin_line_list = self.search(roman_num + ".")
            end_line_list = self.search(next_roman_num + ".")
            #Check to make sure we found roman numeral in the poem
            if(len(begin_line_list) > 0 and len(end_line_list) > 0):
                begin_line = begin_line_list[0][0]
                end_line = end_line_list[0][0]
                #Append line to list until we reach the next poem
                for x in range(begin_line,end_line):
                    line = self.get_msg(x)
                    poem.append(line)
            #Second case: Poem is last in file, return entire poem until end of file
            if(len(begin_line_list) > 0 and len(end_line_list) == 0):
                begin_line = begin_line_list[0][0]
                while(begin_line < self.get_msg_size()):
                    poem.append(self.get_msg(begin_line))
                    begin_line += 1
        return poem

if __name__ == "__main__":
    sonnets = PIndex("AllSonnets.txt")
    # the next two lines are just for testing
    p3 = sonnets.get_poem(3)
    s_love = sonnets.search("love")
    print(p3)
    print("\n")
    print(s_love)