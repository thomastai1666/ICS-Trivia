# import the library
from appJar import gui
from client_class import *

# handle button events
class TriviaGui:
    
    def __init__(self):
        self.app = gui("Trivia")
        self.app.thread(self.main)
        self.draw_login()
        self.app.go()
        self.usr = ""
    
    def press(self,button):
        if button == "Exit Game":
            self.app.stop()
        elif button == "Cancel":
            self.app.stop()
        elif button == "Exit Lobby":
            self.app.stop()
        elif button == "One" or button == "Two" or button == "Three" or button == "Four":
            print("Answer", button)
        elif button == "Send":
            chat = self.app.getEntry("Chat")
            print("Chat Event:", chat)
            self.app.clearEntry("Chat")
        
        elif button == "Submit":
            self.usr = self.app.getEntry("Username")
            self.app.removeAllWidgets()
            self.draw_menu()
            print("User:", self.usr)
        else:
            print("Else")
    
    # create a GUI variable called app
    def draw_game(self):
        self.app.setTitle("Trivia")
        self.app.setBg("white")
        self.app.setSize("400x600")
        self.app.setFont(20)
    
        # add & configure widgets - widgets get a name, to help referencing them later
        self.app.addLabel("title", "Trivia Has Started")
        self.app.setLabelBg("title", "purple")
        self.app.setLabelFg("title", "white")
    
        # link the buttons to the function called press
    
        self.app.addLabel("q1", "Question #1")
        self.app.addButton("One", self.press)
        self.app.addLabel("q2", "Question #2")
        self.app.addButton("Two", self.press)
        self.app.addLabel("q3", "Question #3")
        self.app.addButton("Three", self.press)
        self.app.addLabel("q4", "Question #4")
        self.app.addButton("Four", self.press)
        self.app.addLabelEntry("Chat")
        self.app.addButtons(["Send", "Exit Lobby"], self.press)
    
        self.app.setFocus("Chat")
        
    def draw_menu(self):
        self.app.setTitle("Waiting for Trivia to Start")
        self.app.setBg("white")
        self.app.setSize("400x600")
        self.app.setFont(20)
    
        # add & configure widgets - widgets get a name, to help referencing them later
        self.app.addLabel("title", "Trivia Global Lobby")
        self.app.setLabelBg("title", "purple")
        self.app.setLabelFg("title", "white")
    
        # link the buttons to the function called press
    
        self.app.addLabel("playerlist", "Player List")
        self.app.addTextArea("players")
        self.app.addLabel("chat", "Live Chat")
        self.app.addTextArea("chatbox")
        self.app.addLabelEntry("Chat")
        self.app.addButtons(["Send", "Exit Game"], self.press)
        
        # testing
        self.app.setTextArea("players", "PlayerOne\n", end=True, callFunction=True)
        self.app.setTextArea("players", "PlayerTwo\n", end=True, callFunction=True)
        self.app.setTextArea("players", "PlayerThree\n", end=True, callFunction=True)
        
        self.app.setTextArea("chatbox", "[Playerone]: Hello world!", end=True, callFunction=True)
    
        self.app.setFocus("Chat")
        
    def draw_login(self):
        self.app.setTitle("Login to Trivia")
        self.app.setSize("250x150")
        self.app.setBg("white")
        self.app.setFont(18)
    
        # add & configure widgets - widgets get a name, to help referencing them later
        self.app.addLabel("title", "Welcome to Trivia")
        self.app.setLabelBg("title", "purple")
        self.app.setLabelFg("title", "white")
        
        self.app.addLabelEntry("Username")
        #app.addLabelEntry("Server IP")
        
        # link the buttons to the function called press
        self.app.addButtons(["Submit", "Cancel"], self.press)
        
        self.app.setFocus("Username")
        
    def process_input(self):
        pass
            
    def main(self):
        import argparse
        parser = argparse.ArgumentParser(description='chat client argument')
        parser.add_argument('-d', type=str, default=None, help='server IP addr')
        args = parser.parse_args()
    
        client = Client(args)
        client.run_chat()
        
Trivia = TriviaGui()