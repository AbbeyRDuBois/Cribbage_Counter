import PyQt6.QtWidgets as qtw
from functools import partial

import crib_calc

def home_menu(window):
    window.rows = 5
    window.columns = 3
    
    centralWidget = qtw.QWidget()
    window.setCentralWidget(centralWidget)

    window.layout = qtw.QGridLayout(centralWidget)
    
    card_list = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King", "Done"]
    list_length = len(card_list)

    i = 0
    for row in range(window.rows):
        for column in range(window.columns): 
            button = qtw.QPushButton(f'{card_list[i]}', window)
            button.clicked.connect(partial(window.onClicked, card_list[i]))
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

        home_menu(self)

    def onClicked(self, card):
        print(card)
        if(card == "Done"):
            #Create cards and calculate
            button = qtw.QPushButton(f'{crib_calc.calculate()}', self)
            button.clicked.connect(partial(self.onReturnClick, None))
            self.setCentralWidget(button)
            
    def onReturnClick(self, x):
        home_menu(self)
                
if __name__ == '__main__':
    app = qtw.QApplication([])
    window = MyWindow()

    window.setWindowTitle('Cribbage Counter')
    window.show()

    app.exec()