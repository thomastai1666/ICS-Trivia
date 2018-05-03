# import the library
from appJar import gui

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

# start the GUI
app.go()