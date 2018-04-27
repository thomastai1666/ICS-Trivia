# import the library
from appJar import gui

# handle button events
def press(button):
    if button == "Exit Game":
        app.stop()
    elif button == "One" or button == "Two" or button == "Three" or button == "Four":
        print("Answer", button)
    elif button == "Send":
        chat = app.getEntry("Chat")
        print("Chat Event:", chat)
        app.clearEntry("Chat")
    else:
        print("Else")

# create a GUI variable called app
app = gui("Trivia", "400x600")
app.setBg("white")
app.setFont(20)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Welcome to Trivia")
app.setLabelBg("title", "purple")
app.setLabelFg("title", "white")

# link the buttons to the function called press

app.addLabel("q1", "Question #1")
app.addButton("One", press)
app.addLabel("q2", "Question #2")
app.addButton("Two", press)
app.addLabel("q3", "Question #3")
app.addButton("Three", press)
app.addLabel("q4", "Question #4")
app.addButton("Four", press)
app.addLabelEntry("Chat")
app.addButtons(["Send", "Exit Game"], press)

app.setFocus("Chat")

# start the GUI
app.go()
