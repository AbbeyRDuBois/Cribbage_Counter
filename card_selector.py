import sys
import PyQt6.QtWidgets as qtw
from functools import partial

import crib_calc

flipped = None
hand = []

def home_menu(window, func):
    window.rows = 5
#    window.rows = 5
#    window.columns = 3
    
#    centralWidget = qtw.QWidget()
#    window.setCentralWidget(centralWidget)

#    window.layout = qtw.QGridLayout(centralWidget)
    
#    card_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', "Done"]
#    list_length = len(card_list)

#    i = 0
#    for row in range(window.rows):
#        for column in range(window.columns): 
#            button = qtw.QPushButton(f'{card_list[i]}', window)
#            button.clicked.connect(partial(func, card_list[i]))
#            window.layout.addWidget(button, row+1, column)
#            i += 1
#            if i == list_length: break

class PushButton(qtw.QPushButton):
    def __init__(self, text, parent=None):
        super(PushButton, self).__init__(text, parent)

        self.setText(text)
        self.setMinimumSize(qtw.QSize(50, 50))
        self.setMaximumSize(qtw.QSize(50, 50))

class Main_Window(qtw.QWidget):
    cards = 0

    #Initializes the class as a QMainWindow and calls initUI
    def __init__(self):
        super().__init__()
        self.initUI()

    #Creates new rank and suit boxes adds it to layout then increments how many cards you have
    def add_new_card(self):
        new_suit = SuitBox()
        new_rank = RankBox()
        #Need the + 1 Offset for the Add Card Button
        self.main_layout.addWidget(new_suit, self.cards + 1, 0)
        self.main_layout.addWidget(new_rank, self.cards + 1, 1)
        self.cards += 1

    #Creates the Main Window
    def initUI(self):
        #self.setWindowTitle('Cribbage Counter')
        #Set Main window as a Grid Layout
        self.main_layout = qtw.QGridLayout()
        self.setLayout(self.main_layout)

        #Add the Add Card button to top of window
        add_card = qtw.QPushButton("Add Card")
        add_card.clicked.connect(self.add_new_card)
        self.main_layout.addWidget(add_card, 0, 0, 1, 2)

        #Have 4 cards already in window
        i = 0
        while (i < 4):
            self.add_new_card()
            i += 1

#Defines the Combo box for selecting Suit
class SuitBox(qtw.QComboBox):
    def __init__(self):
        super().__init__()
        self.initBox()

    def initBox(self):
        self.addItem("Heart")
        self.addItem("Diamond")
        self.addItem("Spade")
        self.addItem("Club")

#Defines the Combo box for selecting Card Rank
class RankBox(qtw.QComboBox):
    def __init__(self):
        super().__init__()
        self.initBox()

    def initBox(self):
        self.addItem("Ace")
        self.addItem("1")
        self.addItem("2")
        self.addItem("3")
        self.addItem("4")
        self.addItem("5")
        self.addItem("6")
        self.addItem("7")
        self.addItem("8")
        self.addItem("9")
        self.addItem("10")
        self.addItem("Jack")
        self.addItem("Queen")
        self.addItem("King")

#    def __init__(self):
#        super(MyWindow, self).__init__()

#        home_menu(self, self.onClicked)

#    def onClicked(self, card):
#        global hand
#        print(card)

#        if(card == "Done"):
            #Navigate to get flipped card
#            home_menu(self, self.onFlippedClick)
#        else:
#            hand.append(crib_calc.Card(card, "heart"))

    def onFlippedClick(self, card):
        global flipped
        global hand
        print(card)

        if((card == "Done") and (flipped != None)):
            #Create cards and calculate
            button = qtw.QPushButton(f'{crib_calc.calculate(hand, flipped)}', self)
            button.clicked.connect(self.onReturnClick)
            self.setCentralWidget(button)
        else:
            flipped = crib_calc.Card(card, "heart")
        
    def onReturnClick(self):
        global flipped
        global hand

        flipped = None
        hand = []

        home_menu(self, self.onClicked)

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = Main_Window()
    window.setGeometry(100,100,400,300)
    window.show()
    sys.exit(app.exec())