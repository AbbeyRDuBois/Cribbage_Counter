#Foreign imports
import re
import copy
import discord
import os

#Local imports
import game
import calculate_points as cp

SEND_PUBLIC = "general" #Variable that signifies an echo to the server. Otherwise, send message using user info.

def help_message():
    return '''The bot knows the following commands:

    Cribbage:
      Start Game:
        '**!join**': Let the bot know that you'd like to play cribbage.
        '**!unjoin**': Let the bot know that you changed your mind and don't want to play.
        '**!unjoinall**': Remove all players from lobby. Only use if someone forgot to !unjoin.
        '**!standard**': Play a regular game of cribbage (default).
        '**!mega**': Play a game of mega hand (8 cards, twice as many points).
        '**!joker**': Play a game with 2 wild cards. (Not yet implemented.)
        '**![A2-9JQK] [HDCS]**': Used to transform the joker into the desired card. (Not yet implemented.)
        '**!start**': Starts a game with up to 4 players who have done !join.

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
                if(item[0] == SEND_PUBLIC):
                    await msg.channel.send(item[1])
                # else:
                #     #If not a filepath, send text.
                #     if not item[2]:
                #         await item[0].send(item[1])
                #     #If a filepath (hand), then send pictures.
                #     else:
                #         #Check for valid path
                #         if not os.path.exists(os.path.dirname(item[1])):
                #             print(f"Invalid path: {item[1]}")
                #             return
                #         await item[0].send(content="Number in center of card is index.", file=discord.File(item[1])) #TODO: please delete for posterity
                #         os.remove(item[1])

    except Exception as error:
        print(error)

def add_return(return_list, return_string, send=SEND_PUBLIC, index=-1, isFile=False):
    if(index < 0):
        index = len(return_list)

    if(index >= len(return_list)):
        return_list.append([send, return_string, isFile])
    else:
        return_list[index] = [send, return_string, isFile]

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
    elif(message == '!start'):
        return await start(msg.author)
    elif(re.search('^![0-9]+$', message) != None):
        return await card_select(msg.author, int(message[1:]))
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
            if(len(game.players) < 4):
                game.players.append(author)
                return add_return(return_list, f"Welcome to the game, {author.name}! Type !start to begin game with {len(game.players)} players.")
            else:
                return add_return(return_list, f"Sorry, {author.name}. This game already has 4 players {[player.name for player in game.players]}. If this is wrong, type !unjoinall.")
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
        return add_return(return_list, f"{author.name} has changed game mode to standard. Consider giving !mega a try, or use !start to begin.")
    
    return return_list

def mega(author):
    return_list = []

    if(game.game_started == False):
        game.mega_hand()
        return add_return(return_list, f"{author.name} has changed game mode to mega. Use !standard to play regular cribbage and !start to begin.")
    
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
            
            #Get hands
            game.hands = game.deck.get_hands(len(game.players), game.hand_size + game.throw_count)

            # #Send hands to DMs
            # for player_index in range(len(game.players)):
            #     hand_pic = await game.get_hand_pic(player_index)
            #     add_return(return_list, hand_pic, game.players[player_index], isFile=True)

            return add_return(return_list, f'''{author.name} has started the game.\nThrow {game.throw_count} cards into **{game.players[game.crib_index % len(game.players)]}**'s crib.\n*Use "/hand" to see your hand.*''')
        else:
            return add_return(return_list, f"You can't start a game you aren't queued for, {author.name}.")
        
    return return_list
        
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

    #Make sure player isn't throwing extra away
    if(game.num_thrown[player_index] < game.throw_count):
        #Add card to crib and remove from hand
        card = game.hands[player_index][card_index]
        game.crib.append(card)
        game.hands[player_index].remove(card)
        game.num_thrown[player_index] += 1

        #Send confirmation to DMs
        # add_return(return_list, f"Sent {card.display()} to {game.players[game.crib_index % len(game.players)]}'s crib. Choose {game.throw_count - game.num_thrown[player_index]} more.", game.players[player_index])
        # hand_pic = await game.get_hand_pic(player_index)
        # add_return(return_list, hand_pic, game.players[player_index], isFile=True)

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
                    add_return(return_list, f'''{author.name} has finished putting cards in the crib.\nFlipped card is: {flipped.display()}.\nPegging will now begin with **{game.players[game.pegging_index]}**.''')
                else:
                    add_return(return_list, f'''{author.name} has finished putting cards in the crib.\nFlipped card is: {flipped.display()}.\n{game.players[game.crib_index % len(game.players)]} gets nibs for 2.\nPegging will now begin with **{game.players[game.pegging_index]}**.''')
                
                #Check for winner
                if(game.get_winner() != None):
                    return add_return(return_list, game.get_winner_string(game.get_winner()))
                
                #Make sure crib has proper number of cards
                while(len(game.crib) < game.crib_count):
                    game.crib.append(game.deck.get_card())
                
                #Make sure variables are set up for pegging round
                game.throw_away_phase = False
                game.pegging_phase = True
        else:
            return return_list
        
    return return_list

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

        #If player is out of cards, add message to print.
        if(len(game.hands[player_index]) <= 0):
            add_return(return_list, f"{author.name} has played their last card.\n")

        #If a player who can play was found, let them play. Otherwise, increment to next player and reset.
        if(can_play):
            #Display data
            if(points > 0):
                return add_return(return_list, f'''{author.name} played {card.display()}, gaining {points} points and bringing the total to {cur_sum}.\nIt is now **{game.players[game.pegging_index % len(game.players)].name}**'s turn to play.''')
            else:
                return add_return(return_list, f'''{author.name} played {card.display()}, bringing the total to {cur_sum}.\nIt is now **{game.players[game.pegging_index % len(game.players)].name}**'s turn to play.''')
        elif(pegging_done):
            #Variable to hold output for speed
            output_string = ""

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
                output_string += f'''{game.players[(game.pegging_index-1) % len(game.players)].name} played {card.display()}, got {1 + points} point(s) including last card. Total is reset to 0.\n'''
            else:
                output_string += f'''{game.players[(game.pegging_index-1) % len(game.players)].name} played {card.display()}, got {points} points and reached 31. Total is reset to 0.\n'''
            
            output_string += f"Everyone is done pegging.\n"

            #If pegged out, end game
            if(game.get_winner() != None):
                add_return(return_list, output_string)
                return add_return(return_list, game.get_winner_string(game.get_winner()))
            
            output_string += f"Flipped card: {game.deck.flipped.display()}\n"

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
                    return add_return([], game.get_winner_string(game.get_winner()))

            #Calculate crib
            [get_points, get_output] = cp.calculate_crib(game.crib, game.deck.flipped)
            game.points[game.crib_index % len(game.players)] += get_points
            output_string += f"{game.players[game.crib_index % len(game.players)].name}'s crib: {[crib_card.display() for crib_card in sorted(game.crib, key=lambda x: x.to_int_runs())]} for {get_points} points."
            
            #Send calculation to variable in game.py
            game.calc_string += f"**{game.players[game.crib_index % len(game.players)]}'s Crib**:\n" + get_output + "\n\n"

            #Add total points for each person to the group chat variable
            output_string += "\nTotal Points:\n"
            for player_index in range(len(game.players)):
                output_string += f"{game.players[player_index].name} has {game.points[player_index]} points.\n"

            #Check for winner
            if(game.get_winner() != None):
                return add_return([], game.get_winner_string(game.get_winner()))

            #Reset variables for the next round
            game.reset_round()

            #Get hands for next round
            game.hands = game.deck.get_hands(len(game.players), game.hand_size + game.throw_count)
            game.backup_hands = []

            # #Send hands to DMs
            # for player_index in range(len(game.players)):
            #     hand_pic = await game.get_hand_pic(player_index)
            #     add_return(return_list, hand_pic, game.players[player_index], isFile=True)

            #Finalize and send output_string to group chat
            output_string += f'''\nThrow {game.throw_count} cards into **{game.players[game.crib_index % len(game.players)]}**'s crib.\n*Use "/hand" to see your hand.*'''

            return add_return(return_list, output_string)
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