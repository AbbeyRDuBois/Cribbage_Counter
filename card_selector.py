import sys
import PyQt6.QtWidgets as qtw

import crib_calc

class Main_Window(qtw.QMainWindow):
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
            suit = self.card_layout.itemAtPosition(self.cards-1,0).widget()
            rank = self.card_layout.itemAtPosition(self.cards-1,1).widget()
            self.card_layout.removeWidget(suit)
            self.card_layout.removeWidget(rank)
            self.cards -= 1

    #Creates the Main Window
    def initUI(self):
        self.flipped = None
        self.hand = []
        self.cards = 0

        #Set widgets to be displayed (central widget necessary)
        centralWidget = qtw.QWidget()
        self.setCentralWidget(centralWidget)
        self.layout = qtw.QVBoxLayout(centralWidget)

        #Add the Add Card button to top of window
        add_card = qtw.QPushButton("Add Card")
        add_card.clicked.connect(self.add_new_card)
        self.layout.addWidget(add_card)

        #Add the Remove Card button to top of window
        remove_card = qtw.QPushButton("Remove Card")
        remove_card.clicked.connect(self.delete_card)
        self.layout.addWidget(remove_card)

        #Flipped Card
        self.layout.addWidget(qtw.QLabel("Flipped Card"))
        self.flipped_layout = qtw.QGridLayout()
        self.layout.addLayout(self.flipped_layout)
        self.flipped_layout.addWidget(self.make_suit_box(), 0, 0)
        self.flipped_layout.addWidget(self.make_rank_box(), 0, 1)

        #Set up the new card layout
        self.layout.addWidget(qtw.QLabel("Personal Hand"))
        self.card_layout = qtw.QGridLayout()
        self.layout.addLayout(self.card_layout)

        #Add the Done Button to Bottom of window (will always stay at bottom)
        self.done = qtw.QPushButton("Done")
        self.done.clicked.connect(self.make_cards)
        self.layout.addWidget(self.done)

        #Have 4 cards already in window
        for i in range(4):
            self.add_new_card()
            i += 1

    #Does calculation once "Done" is clicked
    def make_cards(self):
        suit = self.flipped_layout.itemAtPosition(0,0).widget()
        rank = self.flipped_layout.itemAtPosition(0,1).widget()
        if isinstance(suit, qtw.QComboBox) and isinstance(rank, qtw.QComboBox):
            suit = suit.currentText()
            rank = rank.currentText()
        self.flipped = crib_calc.Card(rank, suit)

        #Make a card for every entry in form and add it to Card Array
        for i in range(self.cards):
            suit = self.card_layout.itemAtPosition(i,0).widget()
            rank = self.card_layout.itemAtPosition(i,1).widget()
            if isinstance(suit, qtw.QComboBox) and isinstance(rank, qtw.QComboBox):
                suit = suit.currentText()
                rank = rank.currentText()
                self.hand.append(crib_calc.Card(rank, suit))

        #Display score until clicked
        button = qtw.QPushButton(f'{crib_calc.calculate(self.hand, self.flipped)} points', self)
        button.clicked.connect(self.initUI)
        self.setCentralWidget(button)

    #Add suits to combo box same way calculator takes them
    def make_suit_box(self):
        suit_box = qtw.QComboBox()
        suit_box.addItem("Heart")
        suit_box.addItem("Diamond")
        suit_box.addItem("Spade")
        suit_box.addItem("Club")
        return suit_box
    
    #Add cards to combo box same way that calculator takes them
    def make_rank_box(self):
        rank_box = qtw.QComboBox()
        rank_box.addItem("A")
        rank_box.addItem("2")
        rank_box.addItem("3")
        rank_box.addItem("4")
        rank_box.addItem("5")
        rank_box.addItem("6")
        rank_box.addItem("7")
        rank_box.addItem("8")
        rank_box.addItem("9")
        rank_box.addItem("10")
        rank_box.addItem("J")
        rank_box.addItem("Q")
        rank_box.addItem("K")
        return rank_box

#Run window
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    window = Main_Window()
    window.setWindowTitle('Cribbage Counter')
    window.setGeometry(100,100,400,300)
    window.show()
    sys.exit(app.exec())