#Foreign imports
import re
import copy
import discord
import os

#Local imports
import game
import calculate_points as cp

hand_messages = [] #Variable to hold most recent hand message so that it can be modified as needed

def help_message():
    return '''The bot knows the following commands:

    Cribbage:
      Start Game:
        '**!join**': Let the bot know that you'd like to play cribbage.
        '**!unjoin**': Let the bot know that you changed your mind and don't want to play.
        '**!unjoinall**': Remove all players from lobby. Only use if someone forgot to !unjoin.
        '**!standard**': Play a regular game of cribbage (default).
        '**!mega**': Play a game of mega hand (8 cards, twice as many points to win).
        '**!joker**': Play a game of joker mode (2 wild cards).
        '**![A2-9JQK] [HDCS]**': Used to transform the joker into the desired card.
        '**!start**': Starts a game with up to 8 players who have done !join.
        '**!teams [0-9]+**': Splits players into teams with the specified number of players on each team. Will automatically start the game.

      Private Commands:
        '**/hand**': View your hand
        '**/calcs**': View how points were obtained in the previous round (hands and crib)

      Throw Into Crib:
        '**![0-9]+**': Puts the card with the given index into the current crib.

      Counting:
        '**![0-9]+**': Plays the card with the given index.

      End Early:
        '**!end**': All players must type in the command to end the game early.

    Other:
    '**!treasurelady**', '**!tl**': Change role to Treasure Lady.
    '**!garbageman**', '**!gm**': Change role to Garbage Man.
    '**!help**', '**!bot**': Display orders that the bot can execute.'''


async def process_message(msg):
    try:
        bot_feedback = await handle_user_messages(msg)
        if(len(bot_feedback) > 0):
            for item in bot_feedback:
                if(item[1] == False): #Not a file
                    await msg.channel.send(item[0])
                else:
                    #Check for valid path
                    if not os.path.exists(os.path.dirname(item[0])):
                        print(f"Invalid path: {item[0]}")
                        return
                    await msg.channel.send(content=f"Flipped card: {game.deck.get_flipped()}", file=discord.File(item[0]))
                    os.remove(item[0])

    except Exception as error:
        print(error)

def add_return(return_list, return_string, isFile=False, index=None):
    if(index == None):
        index = len(return_list)

    if(index >= len(return_list)):
        return_list.append([return_string, isFile])
    elif(index < len(return_list)):
        return_list.insert(index, [return_string, isFile])

    return return_list

async def handle_user_messages(msg):
    message = msg.content.lower()
    return_list = []

    #Weed out excess messages
    if(message[0] != '!'):
        return return_list
    
    #Help message
    if(message == '!help' or message == '!bot'):
        return add_return(return_list, help_message())
    
    #Cribbage commands
    elif(re.search('^![0-9]+$', message) != None):
        return await card_select(msg.author, int(message[1:]))
    elif(message == '!join' or message == '!jion'):
        return join(msg.author)
    elif(message == '!unjoin' or message == '!unjion'):
        return unjoin(msg.author)
    elif(message == '!unjoinall'):
        return unjoinall(msg.author)
    elif(message == '!standard'):
        return standard(msg.author)
    elif(message == '!mega'):
        return mega(msg.author)
    elif(message == '!joker'):
        return joker(msg.author)
    elif(message == '!start'):
        return await start(msg.author)
    elif(re.search('^!teams [0-9]+$', message) != None):
        return await form_teams(msg.author, int(message[7:]))
    elif(re.search('^![a2-9jqk] [hdcs]$', message) != None):
        return await make_joker(msg.author, message)
    elif(message == '!end'):
        return end(msg.author)
    
    #Roles
    elif(message == '!gm' or message == '!garbageman'):
        return await give_role(msg.author, "Garbage Man")
    elif(message == '!tl' or message == '!treasurelady'):
        return await give_role(msg.author, "Treasure Lady")
    
    #Default case (orders bot doesn't understand)
    return return_list

def join(author):
    return_list = []

    if(game.game_started == False):
        #Add person to player list and send confirmation message
        if(author not in game.players):
            if(len(game.players) < 8):
                game.players.append(author)
                return add_return(return_list, f"Welcome to the game, {author.name}! Type !start to begin game with {len(game.players)} players.")
            else:
                return add_return(return_list, f"Sorry, {author.name}. This game already has 8 players {[player.name for player in game.players]}. If this is wrong, type !unjoinall.")
        else:
            return add_return(return_list, f"You've already queued for this game, {author.name}. Type !start to begin game with {len(game.players)} players.")
        
    return return_list
    
def unjoin(author):
    return_list = []

    if(game.game_started == False):
        #Remove person from player list and send confirmation message
        if(author in game.players):
            game.players.remove(author)
            return add_return(return_list, f"So long, {author.name}.")
        else:
            return add_return(return_list, f"You never queued for this game, {author.name}.")
        
    return return_list
        
def unjoinall(author):
    return_list = []

    if(game.game_started == False):
        #Remove person from player list and send confirmation message
        game.players = []
        return add_return(return_list, f"{author.name} has purged the player list.")
    
    return return_list
    
def standard(author):
    return_list = []

    if(game.game_started == False):
        game.end_game()
        return add_return(return_list, f"{author.name} has changed game mode to standard. Consider giving !mega and !joker a try, or use !start to begin.")
    
    return return_list

def mega(author):
    return_list = []

    if(game.game_started == False):
        game.mega_hand()
        return add_return(return_list, f"{author.name} has changed game mode to mega. Use !standard to play regular cribbage or !start to begin.")
    
    return return_list

def joker(author):
    return_list = []

    if(game.game_started == False):
        game.joker_mode()
        return add_return(return_list, f"{author.name} has changed game mode to joker mode. Use !standard to play regular cribbage or !start to begin.")
    
    return return_list
    
async def start(author):
    return_list = []

    if(game.game_started == False):
        #Start game
        if(author in game.players):
            #Change game phase
            game.game_started = True
            game.throw_away_phase = True
            game.pegging_index = (game.crib_index + 1) % len(game.players)

            #Initiate game vars
            game.create_game(len(game.players))
            for _ in range(len(game.players)):
                hand_messages.append(None)
            
            #Get hands
            game.hands = game.deck.get_hands(len(game.players), game.hand_size + game.throw_count)

            #Update hand if applicable
            if(hand_messages[game.players.index(author)] != None):
                hand_pic = await game.get_hand_pic(game.players.index(author))
                await hand_messages[game.players.index(author)].edit_original_response(attachments=[discord.File(hand_pic)])
                os.remove(hand_pic)

            return add_return(return_list, f'''{author.name} has started the game.\nThrow {game.throw_count} cards into **{game.players[game.crib_index % len(game.players)]}**'s crib.\n*Use "/hand" to see your hand.*''')
        else:
            return add_return(return_list, f"You can't start a game you aren't queued for, {author.name}.")
        
    return return_list

#Function to form teams of two if applicable
async def form_teams(author, count):
    return_list = []
    num_players = len(game.players)

    #If teams are even, start game
    if (num_players % game.team_count == 0):
        game.team_count = count

        return_list = await start(author)

        #Get the list of teams
        team_list = ""
        num_teams = int(num_players / count)
        for team_num in range(count):
            team_list += f"Team {team_num}: "
            for player in range(num_teams):
                team_list += f"{game.players[player*count + team_num]}, "
            team_list = team_list[:-2] + "\n"

        #Add the teams to be printed before the start returns (index=0)
        add_return(return_list, f"Teams of {count} have been formed:\n{team_list}", index=0)
    else:
        add_return(return_list, "There must be an equal number of players on each team in order to form teams.")
    
    return return_list

#Function to turn joker into another card
async def make_joker(author, message):
    return_list = []

    if author in game.players:
        value = ''
        suit = ''

        #Split message into number and suit letter
        try:
            value_list = message[1:].split()

            #Get value of card
            match value_list[0]:
                case 'a':
                    value = game.dk.ACE
                case 'j':
                    value = game.dk.JACK
                case 'q':
                    value = game.dk.QUEEN
                case 'k':
                    value = game.dk.KING
                case _:
                    value = value_list[0]

            #Get suit of card
            match value_list[1]:
                case 'h':
                    suit = game.dk.HEART
                case 'd':
                    suit = game.dk.DIAMOND
                case 'c':
                    suit = game.dk.CLUB
                case 's':
                    suit = game.dk.SPADE
        except:
            return add_return(return_list, "Failed to parse joker message.")
        
        #Create card and get player index
        card = game.dk.Card(value, suit)
        player_index = game.players.index(author)

        #Change joker in hand to specified card
        for card_index in range(len(game.hands[player_index])):
            if game.hands[player_index][card_index].value == game.dk.JOKER:
                game.hands[player_index][card_index] = card
                #Update hand if applicable
                if(hand_messages[game.players.index(author)] != None):
                    hand_pic = await game.get_hand_pic(game.players.index(author))
                    await hand_messages[game.players.index(author)].edit_original_response(attachments=[discord.File(hand_pic)])
                    os.remove(hand_pic)
                return add_return(return_list, f"Joker in hand has been made into {card.display()}.")
            
        #Change joker in crib or as flipped card to specified card
        if (game.crib_index % len(game.players)) == player_index:
            #Change joker as flipped card to specified card and initialize variables for next round
            if game.deck.get_flipped() == game.dk.JOKER:
                game.deck.flipped = card
                game.throw_away_phase = False
                game.pegging_phase = True
                return add_return(return_list, f"Flipped joker has been made into {card.display()}.\nPegging will now begin with **{game.players[game.pegging_index]}**")
            
            #Change joker in crib to specified card
            for card_index in range(len(game.crib)):
                if game.crib[card_index].value == game.dk.JOKER:
                    game.crib[card_index] = card
                    add_return(return_list, f"Joker in crib has been made into {card.display()}.")
                    await finished_pegging(return_list)
                    return return_list

        return add_return(return_list, f"You need to have a joker in order to use this command, {author.name}.")
    
    return add_return(return_list, f"You need to be in the game to play, {author.name}. Use !join to join.")
        
async def card_select(author, card_index):
    #Get player index
    try:
        player_index = game.players.index(author)
    except:
        return []

    if(author in game.players):
        #Check for valid index or return
        if(card_index >= len(game.hands[player_index])):
            return []

        if(game.game_started == True):
            if(game.throw_away_phase == True):
                return await throw_away_phase_func(author, card_index)
            elif(game.pegging_phase == True):
                return await pegging_phase_func(author, card_index)

    return []

async def throw_away_phase_func(author, card_index):
    return_list = []

    #Get player index
    try:
        player_index = game.players.index(author)
    except:
        return return_list
    
    #If player has joker card (joker mode), force them to make joker something before anybody throws.
    for hand_index in range(len(game.hands)):
        for card in game.hands[hand_index]:
            if card.value == game.dk.JOKER:
                return add_return(return_list, f"You can't throw away cards until {game.players[hand_index]} has chosen which card to turn their joker into.")

    #Make sure player isn't throwing extra away
    if(game.num_thrown[player_index] < game.throw_count):
        #Add card to crib and remove from hand
        card = game.hands[player_index][card_index]
        game.crib.append(card)
        game.hands[player_index].remove(card)
        game.num_thrown[player_index] += 1

        #Update hand if applicable
        if(hand_messages[game.players.index(author)] != None):
            hand_pic = await game.get_hand_pic(game.players.index(author))
            await hand_messages[game.players.index(author)].edit_original_response(attachments=[discord.File(hand_pic)])
            os.remove(hand_pic)

        if(game.num_thrown[player_index] == game.throw_count):
            all_done = True
            for player_index in range(len(game.num_thrown)):
                if(game.num_thrown[player_index] < game.throw_count):
                    all_done = False
                    break

            #Check if everyone is done. If so, get flipped card and begin pegging round.
            if(not all_done):
                return add_return(return_list, f'''{author.name} has finished putting cards in the crib.''')
            else:
                game.backup_hands = copy.deepcopy(game.hands)
                flipped = game.deck.get_flipped()

                #Calculate nibs and possibly end game
                num_points = cp.nibs(flipped)
                game.points[game.crib_index % len(game.players)] += num_points

                #Add display text
                if(num_points == 0):
                    add_return(return_list, f'''{author.name} has finished putting cards in the crib.\nFlipped card is: {flipped.display()}.''')
                else:
                    add_return(return_list, f'''{author.name} has finished putting cards in the crib.\nFlipped card is: {flipped.display()}.\n{game.players[game.crib_index % len(game.players)]} gets nibs for 2.''')
                
                #Check for winner
                if(game.get_winner() != None):
                    return add_return(return_list, game.get_winner_string(game.get_winner()))
                
                #Make sure crib has proper number of cards
                while(len(game.crib) < game.crib_count):
                    game.crib.append(game.deck.get_card())
                
                #Make sure variables are set up for pegging round
                if flipped.value != game.dk.JOKER:
                    game.throw_away_phase = False
                    game.pegging_phase = True
                    add_return(return_list, f"Pegging will now begin with **{game.players[game.pegging_index]}**.")
                else:
                    add_return(return_list, f"***{author.name} must choose which card to turn the flipped joker into before game can proceed.***")
        else:
            return return_list
        
    return return_list

async def finished_pegging(return_list):
    #Variable to hold output for speed
    output_string = f"Flipped card: {game.deck.flipped.display()}\n"

    #Reset calc_string so that it can be filled with new data
    game.calc_string = ""

    #Calculate points
    for player_index in range(len(game.players)):
        #Add points from hand
        [get_points, get_output] = cp.calculate_hand(game.hands[(player_index + game.crib_index + 1) % len(game.players)], game.deck.get_flipped())
        game.points[(player_index + game.crib_index + 1) % len(game.players)] += get_points

        #Send calculation to variable in game.py
        game.calc_string += f"**{game.players[(player_index + game.crib_index + 1) % len(game.players)]}'s Hand**:\n" + get_output + "\n\n"

        #Add data to group output
        output_string += f"{game.players[(player_index + game.crib_index + 1) % len(game.players)].name}'s hand: {[hand_card.display() for hand_card in sorted(game.hands[(player_index + game.crib_index + 1) % len(game.players)], key=lambda x: x.to_int_runs())]} for {get_points} points.\n"

        #Check for winner
        if(game.get_winner() != None):
            return add_return(return_list, game.get_winner_string(game.get_winner()))

    #Calculate crib
    [get_points, get_output] = cp.calculate_crib(game.crib, game.deck.flipped)
    game.points[game.crib_index % len(game.players)] += get_points
    output_string += f"{game.players[game.crib_index % len(game.players)].name}'s crib: {[crib_card.display() for crib_card in sorted(game.crib, key=lambda x: x.to_int_runs())]} for {get_points} points."
    
    #Send calculation to variable in game.py
    game.calc_string += f"**{game.players[game.crib_index % len(game.players)]}'s Crib**:\n" + get_output + "\n\n"

    #Add total points for each person to the group chat variable
    output_string += f"\nTotal Points:\n{game.get_point_string()}"

    #Check for winner
    if(game.get_winner() != None):
        return add_return(return_list, game.get_winner_string(game.get_winner()))

    #Reset variables for the next round
    game.reset_round()

    #Get hands for next round
    game.hands = game.deck.get_hands(len(game.players), game.hand_size + game.throw_count)
    game.backup_hands = []

    #Update hand if applicable
    for player_index in range(len(game.players)):
        if(hand_messages[player_index] != None):
            hand_pic = await game.get_hand_pic(player_index)
            await hand_messages[player_index].edit_original_response(attachments=[discord.File(hand_pic)])
            os.remove(hand_pic)

    #Finalize and send output_string to group chat
    output_string += f'''\nThrow {game.throw_count} cards into **{game.players[game.crib_index % len(game.players)]}**'s crib.\n*Use "/hand" to see your hand.*'''

    return add_return(return_list, output_string)

async def pegging_phase_func(author, card_index):
    return_list = []

    #Get player index
    try:
        player_index = game.players.index(author)
    except:
        return return_list

    #Make sure it's author's turn
    if(game.players[game.pegging_index % len(game.players)] != game.players[player_index]):
        return return_list

    card = game.hands[player_index][card_index]
    cur_sum = sum([my_card.to_int_15s() for my_card in game.pegging_list]) + card.to_int_15s()

    #Make sure sum <= 31
    if(cur_sum <= 31):
        #Remove card from hand, get points, and add to pegging list
        game.hands[player_index].remove(card)
        points = cp.check_points(card, game.pegging_list, cur_sum)
        game.points[player_index] += points
        game.pegging_list.append(card)

        #Make sure next person can play. If go, then reset.
        can_play = False
        pegging_done = True
        for ii in range(len(game.players)):
            if(len(game.hands[game.pegging_index % len(game.players)]) > 0):
                pegging_done = False
            game.pegging_index += 1
            if(game.can_peg(game.hands[game.pegging_index % len(game.players)], cur_sum)):
                game.players[game.pegging_index % len(game.players)]
                can_play = True
                break

        #If player is out of cards, add message to print. Else, update hand.
        if(len(game.hands[player_index]) <= 0):
            add_return(return_list, f"{author.name} has played their last card.\n")
        else:
            if(hand_messages[game.players.index(author)] != None):
                hand_pic = await game.get_hand_pic(game.players.index(author))
                await hand_messages[game.players.index(author)].edit_original_response(attachments=[discord.File(hand_pic)])
                os.remove(hand_pic)

        #If a player who can play was found, let them play. Otherwise, increment to next player and reset.
        if(can_play):
            #Display data
            if(points > 0):
                add_return(return_list, f'''{author.name} played {card.display()}, gaining {points} points and bringing the total to {cur_sum}.\nIt is now **{game.players[game.pegging_index % len(game.players)].name}**'s turn to play.''')
            else:
                add_return(return_list, f'''{author.name} played {card.display()}, bringing the total to {cur_sum}.\nIt is now **{game.players[game.pegging_index % len(game.players)].name}**'s turn to play.''')
        elif(pegging_done):
            #prepare for next round
            game.pegging_phase = False
            my_sum = sum([my_card.to_int_15s() for my_card in game.pegging_list])
            game.pegging_index += 1
            game.pegging_list = []

            #Restore the siphoned hands to their former glory
            game.hands = game.backup_hands

            #Prepare variable to hold group chat data
            if(my_sum != 31):
                game.points[(game.pegging_index-1) % len(game.players)] += 1
                add_return(return_list, f'''{game.players[(game.pegging_index-1) % len(game.players)].name} played {card.display()}, got {1 + points} point(s) including last card. Total is reset to 0.\n''')
            else:
                add_return(return_list, f'''{game.players[(game.pegging_index-1) % len(game.players)].name} played {card.display()}, got {points} points and reached 31. Total is reset to 0.\n''')
            
            add_return(return_list, f"Everyone is done pegging.\n")

            #If pegged out, end game
            if(game.get_winner() != None):
                return add_return(return_list, game.get_winner_string(game.get_winner()))
    
            #Check if there is a joker in the crib. If so, then don't calculate hands yet
            is_joker = False
            for card in game.crib:
                if card.value == game.dk.JOKER:
                    is_joker = True
            
            if not is_joker:
                await finished_pegging(return_list)
            else:
                add_return(return_list, f"***{game.players[game.crib_index % len(game.players)].name} must choose which card to turn the joker in their crib into before game can proceed.***")
                hand_pic = await game.get_hand_pic(-1)
                add_return(return_list, hand_pic, isFile=True)

            return return_list
        else:
            #Prepare variables for next iteration (up to 31)
            my_sum = sum([my_card.to_int_15s() for my_card in game.pegging_list])
            game.pegging_list = []
            cur_pegging_index = game.pegging_index
            game.pegging_index += 1

            #Make sure next person has a hand. If not, then increment. (Somebody has a hand if we got here)
            can_play = False
            for ii in range(len(game.players)):
                if(len(game.hands[game.pegging_index % len(game.players)]) > 0):
                    break
                else:
                    game.pegging_index += 1

            #Display depending on if they reached 31, and add the point for last card since summing to 31 was already calculated
            if(my_sum != 31):
                game.points[cur_pegging_index % len(game.players)] += 1
                add_return(return_list, f'''{game.players[cur_pegging_index % len(game.players)].name} played {card.display()}, got {1 + points} point(s) including last card. Total is reset to 0.\nIt is now **{game.players[game.pegging_index % len(game.players)].name}**'s turn to play.''')
            else:
                add_return(return_list, f'''{game.players[cur_pegging_index % len(game.players)].name} played {card.display()}, got {points} points and reached 31. Total is reset to 0.\nIt is now **{game.players[game.pegging_index % len(game.players)].name}**'s turn to play.''')

    #If pegged out, end game
    if(game.get_winner() != None):
        return add_return(return_list, game.get_winner_string(game.get_winner()))

    return return_list

def end(author):
    if(author in game.players):
        #Get player index
        try:
            player_index = game.players.index(author)
        except:
            return ''

        if(game.game_started == True):
            game.end[player_index] = True
            
            #Check to see if all players agree
            game_over = True
            for ii in range(len(game.end)):
                if(game.end[ii] == False):
                    game_over = False
                    break

            if(game_over == True):
                winner = 0
                for point_index in range(1, len(game.points)):
                    if(game.points[point_index] > game.points[winner]):
                        winner = point_index
                winner = game.players[winner]

                return add_return([], f"Game has been ended early by unanimous vote.\n" + game.get_winner_string(winner))
            else:
                return add_return([], f"{author.name} wants to end the game early. Type !end to agree.")
        else:
            return add_return([], f"You can't end a game that hasn't started yet, {author.name}. Use !unjoin to leave queue.")
        
    return []

#Give role to user
async def give_role(member, role):
    await member.edit(roles=[discord.utils.get(member.guild.roles, name=role)])
    return add_return([], member.name + ' is now a ' + role + '!')