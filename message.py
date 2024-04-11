#Foreign imports
import re
import copy
import discord

#Local imports
import game
import calculate_points as cp

RULES = '''
**Object of the Game**
The goal is to be the first player to score 121 points. (Some games are to 61 points.) Players earn points during play and for making various card combinations.

**The Crib**
Each player looks at their six cards and "lays away" two of them face down to reduce the hand to four. The four cards laid away together constitute "the crib". The crib belongs to the dealer, but these cards are not exposed or used until after the hands have been played.

**Before the Play**
After the crib is laid away, the non-dealer cuts the pack. The dealer turns up the top card of the lower packet and places it face up on top of the pack. This card is the "starter." If the starter is a jack, it is called "His Heels," and the dealer pegs (scores) 2 points at once. The starter is not used in the play phase of Cribbage , but is used later for making various card combinations that score points.

**The Play**
After the starter is turned, the non-dealer lays one of their cards face up on the table. The dealer similarly exposes a card, then non-dealer again, and so on - the hands are exposed card by card, alternately except for a "Go," as noted below. Each player keeps their cards separate from those of their opponent.

As each person plays, they announce a running total of pips reached by the addition of the last card to all those previously played. (Example: The non-dealer begins with a four, saying "Four." The dealer plays a nine, saying "Thirteen".) The kings, queens and jacks count 10 each; every other card counts its pip value (the ace counts one).

**The Go**
During play, the running total of cards may never be carried beyond 31. If a player cannot add another card without exceeding 31, he or she says "Go" and the opponent pegs 1. After gaining the Go, the opponent must first lay down any additional cards he can without exceeding 31. Besides the point for Go, he may then score any additional points that can be made through pairs and runs (described later). If a player reaches exactly 31, he pegs two instead of one for Go.

The player who called Go leads for the next series of plays, with the count starting at zero. The lead may not be combined with any cards previously played to form a scoring combination; the Go has interrupted the sequence.
The person who plays the last card pegs one for Go, plus one extra if the card brings the count to exactly 31. The dealer is sure to peg at least one point in every hand, for he will have a Go on the last card if not earlier.

**Pegging**
The object in play is to score points by pegging. In addition
to a Go, a player may score for the following combinations:

Fifteen: For adding a card that makes the total 15 Peg 2

Pair: For adding a card of the same rank as the card just played Peg 2
(Note that face cards pair only by actual rank: jack with jack, but not jack with queen.)
Triplet: For adding the third card of the same rank. Peg 6

Four: (also called "Double Pair" or "Double Pair Royal")
For adding the fourth card of the same rank Peg 12

Run (Sequence): For adding a card that forms, with those just played:

For a sequence of three Peg 3

For a sequence of four. Peg 4

For a sequence of five. Peg 5

(Peg one point more for each extra card of a sequence. Note that runs are independent of suits, but go strictly by rank; to illustrate: 9, 10, J, or J, 9, 10 is a run but 9, 10, Q is not.)

It is important to keep track of the order in which cards are played to determine whether what looks like a sequence or a run has been interrupted by a "foreign card." Example: Cards are played in this order: 8, 7, 7, 6. The dealer pegs 2 for 15, and the opponent pegs 2 for pair, but the dealer cannot peg for run because of the extra seven (foreign card) that has been played. Example: Cards are played in this order: 9, 6, 8, 7. The dealer pegs 2 for fifteen when he or she plays the six and pegs 4 for run when he plays the seven (the 6, 7, 8, 9 sequence). The cards were not played in sequential order, but they form a true run with no foreign card.

Counting the Hands
When play ends, the three hands are counted in order: non-dealer's hand (first), dealer's hand (second), and then the crib (third). This order is important because, toward the end of a game, the non-dealer may "count out" and win before the dealer has a chance to count, even though the dealer's total would have exceeded that of the opponent. The starter is considered to be a part of each hand, so that all hands in counting comprise five cards. The basic scoring formations are as follows:

Combination Counts
Fifteen. Each combination of cards that totals 15 2

Pair. Each pair of cards of the same rank 2

Run. Each combination of three or more 1 cards in sequence (for each card in the sequence)

Flush. Four cards of the same suit in hand 4 (excluding the crib, and the starter)

Four cards in hand or crib of the same 5 suit as the starter
(There is no count for four-flush in the crib that is not of same suit as the starter)

His Nobs. Jack of the same suit as starter in hand or crib 1

**Combinations**
Each and every combination of two cards that make a pair, of two or more cards that make 15, or of three or more cards that make a run, count separately.

Example: A hand (including the starter) comprised of 8, 7, 7, 6, 2 scores 8 points for four combinations that total 15: the 8 with one 7, and the 8 with the other 7; the 6, 2 with each of the two 7s. The same hand also scores 2 for a pair, and 6 for two runs of three (8, 7, 6 using each of the two 7s). The total score is 16. An experienced player computes the hand thus: "Fifteen 2, fifteen 4, fifteen 6, fifteen 8, and 8 for double run is 16."

Note that the ace is always low and cannot form a sequence with a king. Further, a flush cannot happen during the play of the cards; it occurs only when the hands and the crib are counted.

Certain basic formulations should be learned to facilitate counting. For pairs and runs alone:

A. A triplet counts 6.

B. Four of a kind counts 12.

C. A run of three, with one card duplicated (double run) counts 8.

D. A run of four, with one card duplicated, counts 10.

E. A run of three, with one card triplicated (triple run), counts 15.

F. A run of three, with two different cards duplicated, counts 16.

A PERFECT 29!

The highest possible score for combinations in a single Cribbage deal is 29, and it may occur only once in a Cribbage fan's lifetime -in fact, experts say that a 29 is probably as rare as a hole-in-one in golf. To make this amazing score, a player must have a five as the starter (upcard) and the other three fives plus the jack of the same suit as the starter - His Nobs: 1 point - in their hand. The double pair royal (four 5s) peg another 12 points; the various fives used to hit 15 can be done four ways for 8 points; and the jack plus a 5 to hit 15 can also be done four ways for 8 points. Total = 29 points.
'''


def help_message():
    return '''The bot knows the following commands:

    Cribbage:
      Start Game:
        '**!join**': Let the bot know that you'd like to play cribbage.
        '**!unjoin**': Let the bot know that you changed your mind and don't want to play.
        '**!unjoinall**': Remove all players from lobby. Only use if someone forgot to !unjoin.
        '**!standard**': Play a regular game of cribbage (default).
        '**!mega**': Play a game of mega hand (8 cards, twice as many points).
        '**!start**': Starts a game with up to 4 players who have done !join.

      Throw Into Crib:
        '**![0-9]+**': Puts the card with the given index into the current crib.

      Counting:
        '**![0-9]+**': Plays the card with the given index.

      End Early:
        '**!end**': All players must type in the command to end the game early.
      Rules:
        '**!rules**': Display the rules of cribbage.

    Other:
    '**!treasurelady**', '**!tl**': Change role to Treasure Lady.
    '**!garbageman**', '**!gm**': Change role to Garbage Man.
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
    
    #Cribbage commands
    elif(message == '!join'):
        return join(msg.author)
    elif(message == '!unjoin'):
        return unjoin(msg.author)
    elif(message == '!unjoinall'):
        return unjoinall(msg.author)
    elif(message == '!standard'):
        return standard(msg.author)
    elif(message == '!mega'):
        return mega(msg.author)
    elif(message == '!start'):
        return await start(msg.author)
    elif(re.search('![0-9]+', message) != None):
        return await card_select(msg.author, int(message[1:]))
    elif(message == '!end'):
        return end(msg.author)
    elif(message == '!rules'):
        return RULES
    
    #Roles
    elif(message == '!gm' or message == '!garbageman'):
        return await give_role(msg.author, "Garbage Man")
    elif(message == '!tl' or message == '!treasurelady'):
        return await give_role(msg.author, "Treasure Lady")
    
    #Default case (orders bot doesn't understand)
    return ''

def join(author):
    if(game.game_started == False):
        #Add person to player list and send confirmation message
        if(author not in game.players):
            if(len(game.players) < 4):
                game.players.append(author)
                return f"Welcome to the game, {author.name}! Type !start to begin game with {len(game.players)} players."
            else:
                return f"Sorry, {author.name}. This game already has 4 players {[player.name for player in game.players]}. If this is wrong, type !unjoinall."
        else:
            return f"You've already queued for this game, {author.name}. Type !start to begin game with {len(game.players)} players."
    return ''
    
def unjoin(author):
    if(game.game_started == False):
        #Remove person from player list and send confirmation message
        if(author in game.players):
            game.players.remove(author)
            return f"So long, {author.name}."
        else:
            return f"You never queued for this game, {author.name}."
    return ''
        
def unjoinall(author):
    if(game.game_started == False):
        #Remove person from player list and send confirmation message
        game.players = []
        return f"{author.name} has purged the player list."
    return ''
    
def standard(author):
    if(game.game_started == False):
        game.end_game()
        return f"{author.name} has changed game mode to standard. Consider giving !mega a try, or use !start to begin."

def mega(author):
    if(game.game_started == False):
        game.mega_hand()
        return f"{author.name} has changed game mode to mega. Use !standard to play regular cribbage and !start to begin."
    
async def start(author):
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

            #Send hands to DMs
            for player_index in range(len(game.players)):
                await game.players[player_index].send(game.get_hand_string(player_index))

            return f'''{author.name} has started the game. It is {game.players[game.crib_index % len(game.players)]}'s crib.'''
        else:
            return f"You can't start a game you aren't queued for, {author.name}."
    return ''
        
async def card_select(author, card_index):
    #Get player index
    try:
        player_index = game.players.index(author)
    except:
        return ''

    if(author in game.players):
        #Check for valid index or return
        if(card_index >= len(game.hands[player_index])):
            return ''

        if(game.game_started == True):
            if(game.throw_away_phase == True):
                return await throw_away_phase_func(author, card_index)
            elif(game.pegging_phase == True):
                return await pegging_phase_func(author, card_index)

    return ''

async def throw_away_phase_func(author, card_index):
    #Get player index
    try:
        player_index = game.players.index(author)
    except:
        return ''

    #Make sure player isn't throwing extra away
    if(game.num_thrown[player_index] < game.throw_count):
        #Add card to crib and remove from hand
        card = game.hands[player_index][card_index]
        game.crib.append(card)
        game.hands[player_index].remove(card)
        game.num_thrown[player_index] += 1

        #Send confirmation to DMs
        await author.send(f"Sent {card.display()} to {game.players[game.crib_index % len(game.players)]}'s crib. Choose {game.throw_count - game.num_thrown[player_index]} more.\n{game.get_hand_string(player_index)}")

        if(game.num_thrown[player_index] == game.throw_count):
            all_done = True
            for player_index in range(len(game.num_thrown)):
                if(game.num_thrown[player_index] < game.throw_count):
                    all_done = False
                    break

            #Check if everyone is done. If so, get flipped card and begin pegging round.
            if(not all_done):
                return f'''{author.name} has finished putting cards in the crib.'''
            else:
                flipped = game.deck.get_flipped()

                #Calculate nibs and possibly end game
                num_points = cp.nibs(flipped)
                game.points[game.crib_index % len(game.players)] += num_points

                #Check for winner
                if(game.get_winner() != None):
                    return game.get_winner_string(game.get_winner())
                
                #Make sure crib has proper number of cards
                while(len(game.crib) < game.crib_count):
                    game.crib.append(game.deck.get_card())
                
                #Make sure variables are set up for pegging round
                game.throw_away_phase = False
                game.pegging_phase = True
                game.backup_hands = copy.deepcopy(game.hands)

                if(num_points == 0):
                    return f'''{author.name} has finished putting cards in the crib.\nFlipped card is: {flipped.display()}.\nPegging will now begin with **{game.players[game.pegging_index]}**.'''
                else:
                    return f'''{author.name} has finished putting cards in the crib.\nFlipped card is: {flipped.display()}.\n{game.players[game.crib_index % len(game.players)]} gets nibs for 2.\nPegging will now begin with **{game.players[game.pegging_index]}**.'''
        else:
            return ''
    return ''

async def pegging_phase_func(author, card_index):
    #Get player index
    try:
        player_index = game.players.index(author)
    except:
        return ''

    #Make sure it's author's turn
    if(game.players[game.pegging_index % len(game.players)] != game.players[player_index]):
        return ''

    card = game.hands[player_index][card_index]
    cur_sum = sum([my_card.to_int_15s() for my_card in game.pegging_list]) + card.to_int_15s()

    #Make sure sum <= 31
    if(cur_sum <= 31):
        #Remove card from hand, get points, and add to pegging list
        game.hands[player_index].remove(card)
        points = cp.check_points(card, game.pegging_list, cur_sum)
        game.points[player_index] += points
        game.pegging_list.append(card)

        #If pegged out, end game
        if(game.get_winner() != None):
            return game.get_winner_string(game.get_winner())

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

        #If player still has cards, send them to their hand. Else, add mesage to print.
        no_hand = ""
        if(len(game.hands[player_index]) > 0):
                await game.players[player_index].send(game.get_hand_string(player_index))
        else:
            no_hand = f"{author.name} has played their last card.\n"

        #If a player who can play was found, let them play. Otherwise, increment to next player and reset.
        if(can_play):
            #Display data
            if(points > 0):
                return no_hand + f'''{author.name} played {card.display()}, gaining {points} points and bringing the total to {cur_sum}.\nIt is now **{game.players[game.pegging_index % len(game.players)].name}**'s turn to play.'''
            else:
                return no_hand + f'''{author.name} played {card.display()}, bringing the total to {cur_sum}.\nIt is now **{game.players[game.pegging_index % len(game.players)].name}**'s turn to play.'''
        elif(pegging_done):
            #prepare for next round
            my_sum = sum([my_card.to_int_15s() for my_card in game.pegging_list])
            game.pegging_index += 1
            game.pegging_list = []

            #Restore the siphoned hands to their former glory
            game.hands = game.backup_hands

            #Prepare variable to hold group chat data
            output_string = ""
            if(my_sum != 31):
                game.points[(game.pegging_index-1) % len(game.players)] += 1

                #If pegged out, end game
                if(game.get_winner() != None):
                    return game.get_winner_string(game.get_winner())

                output_string += f'''{game.players[(game.pegging_index-1) % len(game.players)].name} played {card.display()}, got {1 + points} point(s) including last card. Total is reset to 0.\n'''
            else:
                output_string += f'''{game.players[(game.pegging_index-1) % len(game.players)].name} played {card.display()}, got {points} points and reached 31. Total is reset to 0.\n'''
            output_string += f"Everyone is done pegging.\nFlipped card: {game.deck.flipped.display()}\n"

            #Calculate points
            for player_index in range(len(game.players)):
                #Add points from hand
                [get_points, get_output] = cp.calculate_hand(game.hands[(player_index + game.crib_index + 1) % len(game.players)], game.deck.get_flipped())
                game.points[(player_index + game.crib_index + 1) % len(game.players)] += get_points

                #Send calculation to DMs
                await game.players[(player_index + game.crib_index + 1) % len(game.players)].send("Hand:\n" + get_output)

                #Add data to group output
                output_string += f"{game.players[(player_index + game.crib_index + 1) % len(game.players)].name}'s hand: {[hand_card.display() for hand_card in sorted(game.hands[(player_index + game.crib_index + 1) % len(game.players)], key=lambda x: x.to_int_runs())]} for {get_points} points.\n"

                #Check for winner
                if(game.get_winner() != None):
                    return game.get_winner_string(game.get_winner())

            #Calculate crib
            [get_points, get_output] = cp.calculate_crib(game.crib, game.deck.flipped)
            game.points[game.crib_index % len(game.players)] += get_points
            output_string += f"{game.players[game.crib_index % len(game.players)].name}'s crib: {[crib_card.display() for crib_card in sorted(game.crib, key=lambda x: x.to_int_runs())]} for {get_points} points.\n"

            #Check for winner
            if(game.get_winner() != None):
                return game.get_winner_string(game.get_winner())
            
            #Send calculation to DMs
            await game.players[game.crib_index % len(game.players)].send("Crib:\n" + get_output)

            #Add total points for each person to the group chat variable
            output_string += "\nTotal Points:\n"
            for player_index in range(len(game.players)):
                output_string += f"{game.players[player_index].name} has {game.points[player_index]} points.\n"

            #Reset variables for the next round
            game.reset_round()

            #Get hands for next round
            game.hands = game.deck.get_hands(len(game.players), game.hand_size + game.throw_count)
            game.backup_hands = copy.deepcopy(game.hands)

            #Send hands to DMs
            for player_index in range(len(game.players)):
                await game.players[player_index].send(game.get_hand_string(player_index))

            #Finalize and send output_string to group chat
            output_string += f'''\nIt is {game.players[game.crib_index % len(game.players)]}'s crib.'''

            return output_string
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

                #If pegged out, end game
                if(game.get_winner() != None):
                    return game.get_winner_string(game.get_winner())
        
                return no_hand + f'''{game.players[cur_pegging_index % len(game.players)].name} played {card.display()}, got {1 + points} point(s) including last card.\nIt is now **{game.players[game.pegging_index % len(game.players)].name}**'s turn to play.'''
            else:
                return no_hand + f'''{game.players[cur_pegging_index % len(game.players)].name} played {card.display()}, got {points} points and reached 31.\nIt is now **{game.players[game.pegging_index % len(game.players)].name}**'s turn to play.'''

    return ''

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

                return f"Game has been ended early by unanimous vote.\n" + game.get_winner_string(winner)
            else:
                return f"{author.name} wants to end the game early. Type !end to agree."
        else:
            return f"You can't end a game that hasn't started yet, {author.name}. Use !unjoin to leave queue."
        
    return ''

#Give role to user
async def give_role(member, role):
    await member.edit(roles=[discord.utils.get(member.guild.roles, name=role)])
    return member.name + ' is now a ' + role + '!'