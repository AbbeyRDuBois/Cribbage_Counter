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
end = [] #List of players who wish to prematurely end the game
num_thrown = [] #Number of cards thrown in crib, indexed same as players
pegging_list = [] #List of cards in pegging round
point_goal = 121 #Number of points to win
skunk_line = 90 #Number of points to skunk line
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

#Checks if player can peg
def can_peg(hand, cur_sum):
    #Check for basic case before iterating. Probably doesn't save time for small hands, but whatever.
    if(cur_sum <= 21 and len(hand) > 0):
        print("whoops")
        return True
    else:
        for card in hand:
            if(card.to_int_15s() + cur_sum <= 31):
                print("Whelps")
                return True
    print("Take that, Jones!")
    return False

#Returns the player that won or None if no winner
def get_winner():
    for player_index in range(len(players)):
        if(points[player_index] >= point_goal):
            return players[player_index]
        else:
            return None
        
#Resets the round by changing variables
def reset_round():
    global pegging_phase
    global throw_away_phase
    global pegging_list
    global crib_index
    global pegging_index
    global hands
    global crib

    pegging_phase = False
    throw_away_phase = True
    pegging_list = []
    crib_index += 1
    pegging_index = (crib_index + 1) % len(players)
    hands = []
    crib = []

    for ii in range(num_thrown):
        num_thrown[ii] = 0
        
#Ends the game by resetting every variable
def end_game():
    global deck
    global players
    global points
    global hands
    global crib
    global end
    global num_thrown
    global pegging_list
    global point_goal
    global skunk_line
    global card_count
    global hand_size
    global crib_index
    global pegging_index
    global throw_count
    global num_for_good_luck
    global game_started
    global throw_away_phase
    global pegging_phase

    deck.reset_deck()
    players = []
    points = []
    hands = []
    crib = []
    end = []
    num_thrown = []
    pegging_list = []
    point_goal = 121
    skunk_line = 90
    card_count = 4
    hand_size = 0
    crib_index = 0
    pegging_index = 0
    throw_count = 0
    num_for_good_luck = 0
    game_started = False
    throw_away_phase = False
    pegging_phase = False

#Get string of hand to print for player at given index
def get_hand_string(player_index):
    global hands

    output_string = f'''Hand:\n'''
    for card in hands[player_index]:
        output_string += f"{card.display()},  "
    output_string = output_string[:-3] + "\n"
    for card_index in range(len(hands[player_index])):
        output_string += f"!{card_index},      "
    output_string = output_string[:-7] + "\n"
    return output_string