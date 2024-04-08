#Foreign imports
import re

#Local imports
import game
import calculate_points as cp


def help_message():
    return '''The bot knows the following commands:

    Cribbage:
     - Start Game:
        '**!join**': Let the bot know that you'd like to play cribbage.
        '**!unjoin**': Let the bot know that you changed your mind and don't want to play.
        '**!unjoinall**': Remove all players from lobby. Only use if someone forgot to !unjoin.
        '**!cards[0-9]+**': Games will use the set number of cards.
        '**!start**': Starts a game with up to 4 players who have done !join.

     - Throw Into Crib:
        '**![0-9]+**': Puts the card with the given index into the current crib.

     - Counting:
        '**![0-9]+**': Plays the card with the given index.

     - End Early:
        '**!end**': All players must type in the command to end the game early.

    Other:
    '**!help**', '**!bot**': Display orders that the bot can execute.'''


async def process_message(msg):
    try:
        bot_feedback = await handle_user_messages(msg)
        if(bot_feedback != ''):
            await msg.channel.send(bot_feedback)

    except Exception as error:
        print(error)

async def handle_user_messages(msg):
    message = msg.content.lower()

    #Weed out excess messages
    if(message[0] != '!'):
        return ''
    
    #Help message
    if(message == '!help' or message == '!bot'):
        return help_message()
    
    #Links to other media
    elif(message == '!join'):
        return join(message.author)
    elif(message == '!unjoin'):
        return unjoin(message.author)
    elif(message == '!unjoinall'):
        return unjoinall()
    elif(message == '!start'):
        return start()
    elif(re.search('![0-9]+') != None):
        return card_select(message.author, int(message[1:]))
    elif(message == '!end'):
        return end(message.author)
    
    #Default case (orders bot doesn't understand)
    return ''

def join(author):
    if(game.game_started == False):
        #Add person to player list and send confirmation message
        if(author not in game.players):
            if(len(game.players < 4)):
                game.players.append(author)
                return f"Welcome to the game, {author.name}! Type !start to begin game with {len(game.players)} players."
            else:
                return f"Sorry, {author.name}. This game already has 4 players {[player.name for player in game.players]}. If this is wrong, type !unjoinall."
        else:
            return f"You've already queued for this game, {author.name}. Type !start to begin game with {len(game.players)} players."
    
def unjoin(author):
    if(game.game_started == False):
        #Remove person from player list and send confirmation message
        if(author in game.players):
            game.players.remove(author)
            return f"So long, {author.name}."
        else:
            return f"You never queued for this game, {author.name}."
        
def unjoinall(author):
    if(game.game_started == False):
        #Remove person from player list and send confirmation message
        game.players = []
        return f"{author.name} has purged the player list."
    
def start(author):
    if(game.game_started == False):
        #Start game
        if(author in game.players):
            #Change game phase
            game.game_started = True
            game.throw_away_phase = True
            game.pegging_index = (game.crib_index + 1) % len(game.players)

            #Initiate game vars
            num_players = len(game.players)
            if(num_players == 1):
                game.throw_count = 2
                game.num_for_good_luck = 2
                game.hand_size = 6
            elif(num_players == 2):
                game.throw_count = 2
                game.num_for_good_luck = 0
                game.hand_size = 6
            elif(num_players == 3):
                game.throw_count = 1
                game.num_for_good_luck = 1
                game.hand_size = 5
            elif(num_players == 4):
                game.throw_count = 1
                game.num_for_good_luck = 0
                game.hand_size = 5

            #Initiate points
            for _ in range(num_players):
                game.points.append(0)

            #Get hands
            game.hands = game.deck.get_hands(num_players, game.card_count + game.throw_count)

            #Send hands to DMs
            for player_index in range(game.players):
                game.players[player_index].send(f"Hand: {[f'!{card_index} -> {game.hands[player_index][card_index]}' for card_index in range(game.hands[player_index])]}")

            return f'''{author.name} has started the game. It is {game.players[game.cribIndex % num_players]}'s crib.'''
        else:
            return f"You can't start a game you aren't queued for, {author.name}."
        
def card_select(author, card_index):
    if(author in game.players):
        #Get player index
        player_index = game.players.index(author)

        if(game.game_started == True):
            if(game.throw_away_phase == True):
                #Make sure player isn't throwing extra away
                if(game.num_thrown[player_index] < game.throw_count):
                    #Add card to crib and remove from hand
                    card = game.hands[player_index][card_index]
                    game.crib.append(card)
                    game.hands[player_index].remove(card)
                    game.num_thrown[player_index] += 1

                    #Send confirmation to DMs
                    author.send(f"Sent {card.display()} to {game.players[game.cribIndex % len(game.players)]}. Choose {game.throw_count - game.num_thrown[player_index]} more.\nHand: {[f'!{card_index} -> {game.hands[player_index][card_index]}' for card_index in range(game.hands[player_index])]}")

                    if(game.num_thrown[player_index] == game.throw_count):
                        #TODO: Check if everyone is done. If so, game.throw_away_phase = False and display appropriately.
                        return f'''{author.name} has finished putting cards in the crib.'''
                    else:
                        return ''
            elif(game.pegging_phase == True):
                #Make sure it's the author's turn and sum <= 31
                cur_sum = sum(game.pegging_list) + card.to_int_15s()
                if(player_index == game.pegging_index and cur_sum <= 31):
                    #Remove card from hand, get points, and add to pegging list
                    card = game.hands[player_index][card_index]
                    game.hands[player_index].remove(card)
                    points = cp.check_points(card, game.pegging_list, cur_sum)
                    game.points[player_index] += points
                    game.pegging_list.append(card)

                    #TODO: If pegged out, end game

                    #Make sure next person can play. If go, the reset.
                    can_play = False
                    pegging_done = True
                    for ii in range(len(game.players)):
                        if(len(game.hands[game.pegging_index % len(game.players)]) > 0):
                            pegging_done = False
                        game.pegging_index += 1
                        if(game.can_peg(game.hands[game.pegging_index % len(game.players)], cur_sum)):
                            can_play = True
                            break

                    #If a player who can play was found, let them play. Otherwise, increment to next player and reset.
                    if(can_play):
                        return f'''It is now {author.name}'s turn to play.'''
                    elif(pegging_done):
                        #TODO: Change vars and display points for everyone.
                        game.pegging_phase = False
                        return f'''Everyone is done pegging.'''
                    else:
                        game.pegging_index += 2
                        game.pegging_list = []
                        f'''It is now {author.name}'s turn to play.'''