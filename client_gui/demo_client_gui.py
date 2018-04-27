# import the library
from appJar import gui

# handle button events
def press(button):
    if button == "Exit Game":
        app.stop()
    elif button == "One" or button == "Two" or button == "Three":
        print("Answer", button)
    elif button == "Send":
        print("Chat Event: Send")
    else:
        chat = app.getEntry("Chat")
        print("Chat Event:", chat)

# create a GUI variable called app
app = gui("Trivia", "400x600")
app.setBg("white")
app.setFont(18)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Welcome to Trivia")
app.setLabelBg("title", "purple")
app.setLabelFg("title", "white")

app.addLabelEntry("Chat")

# link the buttons to the function called press

app.addButton("One", press)
app.addButton("Two", press)
app.addButton("Three", press)
app.addButton("Four", press)
app.addButtons(["Send", "Exit Game"], press)

app.setFocus("Chat")

# start the GUI
app.go()
