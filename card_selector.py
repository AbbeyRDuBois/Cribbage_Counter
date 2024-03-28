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
    #Initializes the class as a QMainWindow and calls initUI
    def __init__(self):
        super().__init__()
        self.initUI()

    #Creates new rank and suit boxes adds it to layout then increments how many cards you have
    def add_new_card(self):
        self.card_layout.addWidget(self.make_suit_box(), self.cards, 0)
        self.card_layout.addWidget(self.make_rank_box(), self.cards, 1)
        self.cards += 1

    #Removes last card in the list
    def delete_card(self):
        if self.cards != 1:
            self.card_layout.removeRow(self.cards - 1)
            self.cards -= 1

    #Creates the Main Window
    def initUI(self):
        self.cardArray = []
        self.cards = 0
        self.setWindowTitle('Cribbage Counter')
        self.main_layout = qtw.QVBoxLayout()
        self.setLayout(self.main_layout)

        #Add the Add Card button to top of window
        add_card = qtw.QPushButton("Add Card")
        add_card.clicked.connect(self.add_new_card)
        self.main_layout.addWidget(add_card)

        #Add the Remove Card button to top of window
        remove_card = qtw.QPushButton("Remove Card")
        remove_card.clicked.connect(self.delete_card)
        self.main_layout.addWidget(remove_card)

        #flipped Card
        self.main_layout.addWidget(qtw.QLabel("Flipped Card"))
        self.flipped_layout = qtw.QGridLayout()
        self.main_layout.addLayout(self.flipped_layout)
        self.flipped_layout.addWidget(self.make_suit_box(), 0, 0)
        self.flipped_layout.addWidget(self.make_rank_box(), 0, 1)

        #Set up the new card layout
        self.main_layout.addWidget(qtw.QLabel("Personal Hand"))
        self.card_layout = qtw.QGridLayout()
        self.main_layout.addLayout(self.card_layout)

        #Add the Done Button to Bottom of window (will always stay at bottom)
        self.done = qtw.QPushButton("Done")
        self.done.clicked.connect(self.make_cards)
        self.main_layout.addWidget(self.done)

        #Have 4 cards already in window
        for i in range(4):
            self.add_new_card()
            i += 1

    def make_cards(self):
        suit = self.flipped_layout.itemAtPosition(0,0).widget()
        rank = self.flipped_layout.itemAtPosition(0,1).widget()
        if isinstance(suit, qtw.QComboBox) and isinstance(rank, qtw.QComboBox):
            suit = suit.currentText()
            rank = rank.currentText()
        self.flipped = Card(suit, rank)

        #make a card for every entry in form and add it to Card Array
        for i in range(self.cards):
            suit = self.card_layout.itemAtPosition(i,0).widget()
            rank = self.card_layout.itemAtPosition(i,1).widget()
            if isinstance(suit, qtw.QComboBox) and isinstance(rank, qtw.QComboBox):
                suit = suit.currentText()
                rank = rank.currentText()
                self.cardArray.append(Card(suit, rank))

        #After Done Print out Cards
        #TODO: Change from a print and hook up the Card array/flipped card to the calculator
        print("Flipped Card: ", end="")
        print(self.flipped.get_suit(), end=" ")
        print(self.flipped.get_rank())
        print("Hand:")
        for i in range(self.cards):
            print(self.cardArray[i].get_suit(), end=" ")
            print(self.cardArray[i].get_rank())

    def make_suit_box(self):
        suit_box = qtw.QComboBox()
        suit_box.addItem("Heart")
        suit_box.addItem("Diamond")
        suit_box.addItem("Spade")
        suit_box.addItem("Club")
        return suit_box
    
    def make_rank_box(self):
        rank_box = qtw.QComboBox()
        rank_box.addItem("Ace")
        rank_box.addItem("1")
        rank_box.addItem("2")
        rank_box.addItem("3")
        rank_box.addItem("4")
        rank_box.addItem("5")
        rank_box.addItem("6")
        rank_box.addItem("7")
        rank_box.addItem("8")
        rank_box.addItem("9")
        rank_box.addItem("10")
        rank_box.addItem("Jack")
        rank_box.addItem("Queen")
        rank_box.addItem("King")
        return rank_box

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def get_suit(self):
        return self.suit 
      
    def get_rank(self):
        return self.rank

#    def onFlippedClick(self, card):
#        global flipped
#        global hand
#        print(card)

#       if((card == "Done") and (flipped != None)):
            #Create cards and calculate
#            button = qtw.QPushButton(f'{crib_calc.calculate(hand, flipped)}', self)
#            button.clicked.connect(self.onReturnClick)
#            self.setCentralWidget(button)
#        else:
#            flipped = crib_calc.Card(card, "heart")
        
#    def onReturnClick(self):
#        global flipped
#        global hand

#        flipped = None
#        hand = []

#        home_menu(self, self.onClicked)

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = Main_Window()
    window.setGeometry(100,100,400,300)
    window.show()
    sys.exit(app.exec())