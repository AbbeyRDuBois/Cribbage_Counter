#Foreign imports
import PyQt6.QtWidgets as qtw

#Local imports
import home


#Creates the GUI
def initUI(window, num_cards):
    #Set widgets to be displayed (central widget necessary)
    centralWidget = qtw.QWidget()
    window.setCentralWidget(centralWidget)
    window.layout = qtw.QVBoxLayout(centralWidget)

    #Add the back to home button
    window.home = qtw.QPushButton("Back to Home")
    window.home.clicked.connect(lambda x: home.initUI(window))
    window.layout.addWidget(window.home)
    window.layout.addWidget(qtw.QLabel("Cribbage Discord bot coming soon (hopefully)!"))