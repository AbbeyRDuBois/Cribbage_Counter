#Foreign imports
import PyQt6.QtWidgets as qtw

#Local imports
import home
from deck import Deck


deck = Deck() #Deck you play with
players = [] #List of Discord users that are playing
points = [] #Number of points, indexed same as players
hands = [] #Hands, indexed same as players
backup_hands = [] #Hands that always have hand_size cards, indexed same as players
crib = [] #Crib cards
end = [] #List of players who wish to prematurely end the game
num_thrown = [] #Number of cards thrown in crib, indexed same as players
pegging_list = [] #List of cards in pegging round
point_goal = 121 #Number of points to win
skunk_length = 30 #Number of points from skunk line to end -1
crib_count = 4 #Number of cards in crib
hand_size = 4 #Number of cards in a hand after throwing to crib
crib_index = 0 #crib_index++ each round. Crib belongs to players%len(players).
pegging_index = 0 #(crib_index + 1) % len(players)
throw_count = 0 #How many cards each player throws, initialized upon starting game
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
    window.textBrowser = qtw.QTextBrowser()
    window.textBrowser.setOpenExternalLinks(True)
    window.textBrowser.setStyleSheet('font-size: 30px;')
    window.textBrowser.append('Link to cribbage Discord bot can be found <a href=https://github.com/AbbeyRDuBois/Cribbage_Counter>here</a>!')
    window.layout.addWidget(window.textBrowser)

#Checks if player can peg
def can_peg(hand, cur_sum):
    #Check for basic case before iterating. Probably doesn't save time for small hands, but whatever.
    if(cur_sum <= 21 and len(hand) > 0):
        return True
    else:
        for card in hand:
            if(card.to_int_15s() + cur_sum <= 31):
                return True
    return False

#Returns the player that won or None if no winner
def get_winner():
    global players
    global point_goal

    for player_index in range(len(players)):
        if(points[player_index] >= point_goal):
            return players[player_index]

    return None
        
#Resets the round by changing variables
def reset_round():
    global deck
    global pegging_phase
    global throw_away_phase
    global pegging_list
    global crib_index
    global pegging_index
    global hands
    global backup_hands
    global crib

    deck.reset_deck()
    pegging_phase = False
    throw_away_phase = True
    pegging_list = []
    crib_index += 1
    pegging_index = (crib_index + 1) % len(players)
    hands = []
    backup_hands = []
    crib = []

    for ii in range(len(num_thrown)):
        num_thrown[ii] = 0
        
#Ends the game by resetting every variable to standard cribbage
def end_game():
    global deck
    global players
    global points
    global hands
    global backup_hands
    global crib
    global end
    global num_thrown
    global pegging_list
    global point_goal
    global skunk_length
    global crib_count
    global hand_size
    global crib_index
    global pegging_index
    global throw_count
    global game_started
    global throw_away_phase
    global pegging_phase

    deck.reset_deck()
    players = []
    points = []
    hands = []
    backup_hands = []
    crib = []
    end = []
    num_thrown = []
    pegging_list = []
    point_goal = 121
    skunk_length = 30
    crib_count = 4
    hand_size = 4
    crib_index = 0
    pegging_index = 0
    throw_count = 0
    game_started = False
    throw_away_phase = False
    pegging_phase = False

#Get string of hand to print for player at given index
def get_hand_string(player_index):
    global hands

    output_string = f"Hand:\n"
    for card in [card.display() for card in sorted(hands[player_index], key=lambda x: x.to_int_runs())]:
        output_string += f"{card}, "
    output_string = output_string[:-2] + "\n"
    for card in [card for card in sorted(hands[player_index], key=lambda x: x.to_int_runs())]:
        output_string += f"!{hands[player_index].index(card)},\t\t"
    output_string = output_string[:-3] + "\n"
    return output_string

#Sets up game to work with num_players amount of people
def create_game(num_players):
    global throw_count
    global points
    global end
    global num_thrown

    if(num_players == 1):
        throw_count = 2
    elif(num_players == 2):
        throw_count = 2
    elif(num_players == 3):
        throw_count = 1
    elif(num_players == 4):
        throw_count = 1
    else:
        return
    
    #Initiate points
    for _ in range(num_players):
        points.append(0)
        end.append(False)
        num_thrown.append(0)

#Ends the game and returns a string with point details.
def get_winner_string(winner, show_hands=True):
    global players
    global points
    global point_goal
    global skunk_length
    global hands
    global backup_hands
    global crib
    global crib_index

    player_scores = ""
    player_hands = ""

    #Shows the hands
    if(show_hands):
        #Make sure that backup_hands has been initialized
        if(len(backup_hands) == len(players)):
            for hand_index in range(len(players)):
                player_hands += f"{players[hand_index]}'s hand: {[card.display() for card in backup_hands[hand_index]]}\n"

        #Make sure that crib has been initialized
        if(len(crib) == crib_count):
            player_hands += f"{players[crib_index%len(players)]}'s crib: {[card.display() for card in crib]}\n"

    #Shows the ending point totals
    for point_index in range(len(points)):
        if(points[point_index] < (point_goal - skunk_length - 1)):
            player_scores += f"{players[point_index]} got skunked x{(point_goal - points[point_index]) // skunk_length} at {points[point_index]} points.\n"
        else:
            player_scores += f"{players[point_index]} ended with {points[point_index]} points.\n"

    end_game()
    return player_hands + player_scores + f"{winner.name} has won the game! Everything will now be reset."

#Sets up game for mega hand
def mega_hand():
    global game_started
    global point_goal
    global skunk_length
    global hand_size

    if(game_started == False):
        point_goal = 241
        skunk_length = 60
        hand_size = 8