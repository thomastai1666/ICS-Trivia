# import the library
from appJar import gui

# handle button events
def press(button):
    if button == "Cancel":
        app.stop()
    else:
        usr = app.getEntry("Username")
        server = app.getEntry("Server IP")
        print("User:", usr, "Server IP: ", server)

# create a GUI variable called app
app = gui("Login Window", "400x200")
app.setBg("white")
app.setFont(18)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "Welcome to Trivia")
app.setLabelBg("title", "purple")
app.setLabelFg("title", "white")

app.addLabelEntry("Username")
app.addLabelEntry("Server IP")

# link the buttons to the function called press
app.addButtons(["Submit", "Cancel"], press)

app.setFocus("Username")

# start the GUI
app.go()