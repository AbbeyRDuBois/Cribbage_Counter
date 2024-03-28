import PyQt6.QtWidgets as qtw
from functools import partial

import crib_calc

flipped = None
hand = []

def home_menu(window, func):
    window.rows = 5
    window.columns = 3
    
    centralWidget = qtw.QWidget()
    window.setCentralWidget(centralWidget)

    window.layout = qtw.QGridLayout(centralWidget)
    
    card_list = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', "Done"]
    list_length = len(card_list)

    i = 0
    for row in range(window.rows):
        for column in range(window.columns): 
            button = qtw.QPushButton(f'{card_list[i]}', window)
            button.clicked.connect(partial(func, card_list[i]))
            window.layout.addWidget(button, row+1, column)
            i += 1
            if i == list_length: break

class PushButton(qtw.QPushButton):
    def __init__(self, text, parent=None):
        super(PushButton, self).__init__(text, parent)

        self.setText(text)
        self.setMinimumSize(qtw.QSize(50, 50))
        self.setMaximumSize(qtw.QSize(50, 50))

class MyWindow(qtw.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        home_menu(self, self.onClicked)

    def onClicked(self, card):
        global hand
        print(card)

        if(card == "Done"):
            #Navigate to get flipped card
            home_menu(self, self.onFlippedClick)
        else:
            hand.append(crib_calc.Card(card, "heart"))

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
    app = qtw.QApplication([])
    window = MyWindow()

    window.setWindowTitle('Cribbage Counter')
    window.show()

    app.exec()