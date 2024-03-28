import PyQt6.QtWidgets as qtw
from functools import partial


class PushButton(qtw.QPushButton):
    def __init__(self, text, parent=None):
        super(PushButton, self).__init__(text, parent)

        self.setText(text)
        self.setMinimumSize(qtw.QSize(50, 50))
        self.setMaximumSize(qtw.QSize(50, 50))

class MyWindow(qtw.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.rows = 5
        self.columns = 3
        
        centralWidget = qtw.QWidget()
        self.setCentralWidget(centralWidget)

        self.layout = qtw.QGridLayout(centralWidget)
        
        card_list = ['Ace', 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
        list_length = len(card_list)

        i = 0
        for row in range(self.rows):
           for column in range(self.columns): 
                button = qtw.QPushButton(f'{card_list[i]}', self)
                button.clicked.connect(partial(self.onClicked, card_list[i]))
                self.layout.addWidget(button, row+1, column)
                i += 1
                if i == list_length: break

    def onClicked(self, card):
        print(card)
        
                
if __name__ == '__main__':
    app = qtw.QApplication([])
    window = MyWindow()

    window.setWindowTitle('Cribbage Counter')
    window.show()

    app.exec()