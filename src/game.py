#Foreign imports
import PyQt6.QtWidgets as qtw
import os
import pygame
from pygame.locals import *
from PIL import Image
from math import floor
import copy
#import sys

#Local imports
import home
import deck as dk

deck = dk.Deck() #Deck you play with
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
crib_index = 0 #crib_index++ each round. Crib belongs to players[crib_index%len(players)].
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

#Gets the path for the images
def getPath(limited_path):
    # if(EXECUTABLE_MODE):
    #     return sys.executable.rsplit('\\', 1)[0] + '\\' + limited_path
    # else:
    return os.path.join(os.path.dirname(__file__), limited_path)
    
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

async def get_hand_pic(plyr_index):
    player_index = copy.copy(plyr_index)
    global hands

    asset_file_path = getPath('card_art\\all_assets.png')
    card_file_path = getPath('card_art\\card' + str(player_index) + '.png')
    index_file_path = getPath('card_art\\index' + str(player_index) + '.png')
    hand_file_path = getPath('card_art\\hand' + str(player_index) + '.png')

    output_string = ""

    #The size of the sprites
    base_card_width = 32 #Excess room on sprite sheet
    base_card_height = 32 #Excess room on sprite sheet
    card_width = 32
    card_height = 48
    num_width = 16
    num_height = 16
    base_num_width = 9 * card_width + base_card_width
    base_num_height = 4 * card_height + base_card_height + 8

    #Stores index number
    card_index = 0

    #Create empty image with place for images
    new_image = Image.new('RGB', (card_width*len(hands[player_index]), card_height), color=(0, 80, 80))

    #For each card in the hand, retrieve it from the sprite sheet and add it to hand image
    for card in [card for card in sorted(hands[player_index], key=lambda x: x.to_int_runs())]:
        #Get right column
        width_multiplier = 4 * floor((card.to_int_runs()-1) / 3)

        #Get right sub-column based on suit
        if card.suit == dk.DIAMOND:
            width_multiplier += 1
        if card.suit == dk.CLUB:
            width_multiplier += 2
        if card.suit == dk.HEART:
            width_multiplier += 3

        #Get right row
        height_multiplier = (card.to_int_runs()+2) % 3

        x_coord = card_width * width_multiplier + base_card_width
        y_coord = card_height * height_multiplier + base_card_height

        sheet = pygame.image.load(asset_file_path)
        single_image = sheet.subsurface((x_coord, y_coord, card_width, card_height))

        pygame.image.save(single_image, card_file_path)

        #Add index (![0-9]) to card
        img = Image.open(card_file_path)
        index_img = Image.new('RGB', (floor(card_width/2), floor(card_height/2)), color=(0, 0, 0))

        index = hands[player_index].index(card)

        if index != 0:
            num_width_multiplier = (index+2) % 3
            num_height_multiplier = floor((index-1) / 3)
        else:
            num_width_multiplier = 1
            num_height_multiplier = 3

        x_num_coord = num_width * num_width_multiplier + base_num_width
        y_num_coord = num_height * num_height_multiplier + base_num_height

        num_image = sheet.subsurface((x_num_coord, y_num_coord, num_width, num_height))

        pygame.image.save(num_image, index_file_path)

        index_img.paste(Image.open(index_file_path), (floor(card_width*3/16), floor(card_height*3/16)))
        img.paste(index_img, (floor(card_width/4), floor(card_height/4)))

        #Add card to line
        new_image.paste(img, (card_index*card_width, 0))

        #Add index to output string
        output_string += "!" + str(index) + '\t  '

        #Increment to next index
        card_index += 1

    #Save hand image
    new_image.save(hand_file_path)

    #Delete created images
    os.remove(card_file_path)
    os.remove(index_file_path)

    #Return image path and indexes without the final spacing
    return hand_file_path

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
    global deck

    player_scores = ""
    player_hands = ""

    #Shows the hands
    if(show_hands):
        #Make sure that backup_hands has been initialized
        if(len(backup_hands) == len(players)):
            player_hands += f"Flipped card is: {deck.get_flipped().display()}\n"
            for hand_index in range(len(players)):
                player_hands += f"{players[hand_index]}'s hand: {[card.display() for card in sorted(backup_hands[hand_index], key=lambda card:card.to_int_15s())]}\n"

        #Make sure that crib has been initialized
        if(len(crib) == crib_count):
            player_hands += f"{players[crib_index%len(players)]}'s crib: {[card.display() for card in sorted(crib, key=lambda card:card.to_int_15s())]}\n"

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