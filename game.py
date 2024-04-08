#Foreign imports
import PyQt6.QtWidgets as qtw

#Local imports
import home
from deck import Deck


deck = Deck() #Deck you play with
players = [] #List of Discord users that are playing
points = [] #Number of points, indexed same as players
hands = [] #Hands, indexed same as players
crib = [] #Crib cards
num_thrown = [] #Number of cards thrown in crib, indexed same as players
pegging_list = [] #List of cards in pegging round
card_count = 4 #Number of cards in crib
hand_size = 0
crib_index = 0 #Crib belongs to players%len(players)
pegging_index = 0 #(crib_index + 1) % len(players)
throw_count = 0 #How many cards each player throws, initialized upon starting game
num_for_good_luck = 0 #How many cards needed from the deck in the crib
game_started = False #True if the game has begun, else False
throw_away_phase = False #True if players still need to throw cards away
pegging_phase = False #True if players are in the pegging phase

#Creates the GUI
#TODO: Maybe have the GUI do something?
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

#Function to go through throw away phase
def throw_away():
    return

#Function to see if player can peg
def can_peg(hand, cur_sum):
    #Check for basic case before iterating. Probably doesn't save time for small hands, but whatever.
    if(cur_sum <= 21):
        return True
    else:
        for card in hand:
            if(card.to_int_15s() + cur_sum <= 31):
                return True
    return False

#Function to go through hand counting phase
def counting():
    return