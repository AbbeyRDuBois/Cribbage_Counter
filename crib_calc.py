import itertools
import copy
import time
import math

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

#Get the value of a card for when counting to 15
def get_card_points_15(value):
    # Define the logic to calculate points for a card value here
    if value in ["K", "Q", "J"]:
        return 10
    elif value == "A":
        return 1
    else:
        return int(value)

#Getting a value for a card when evaluating runs
def get_card_points_runs(value):
    # Define the logic to calculate points for a card value here
    if value == "K": 
        return 13
    elif value == "Q":
        return 12
    elif value == "J":
        return 11
    elif value == "A":
        return 1
    else:
        return int(value)

#Finding Nibs  
def nibs(flipped):
    points = 0

    #For Nibs (flipping a jack)
    if flipped.value == "J":
        print("Nibs for 2")
        points += 2

    return points

#Finding Nobs
def nobs(hand, flipped, points, output_string):
    #For Nobs (suit of jack in hand matches the flipped suit)
    for card in hand:
        if card.suit == flipped.suit and card.value == "J":
            output_string += "Nobs for 1\n"
            points += 1
            break

    return [points, output_string]

#Finding 15s
def find_15s(hand, flipped, points, output_string):
    hand = copy.copy(hand)
    hand.append(flipped)

    for subset_size in range(1, len(hand) + 1):
        for subset in itertools.combinations(hand, subset_size):
            subset_values = [card.value for card in subset]
            subset_sum = sum(get_card_points_15(value) for value in subset_values)

            if subset_sum == 15:
                points += 2
                subset_expression = " + ".join(f"{card.value}" for card in subset)
                output_string += f"{subset_expression} = 15 ({points})\n"
                
    return [points, output_string]

#Finding Pairs
def find_pairs(hand, flipped, points, output_string):
    hand = copy.copy(hand)
    hand.append(flipped)

    for card1, card2 in itertools.combinations(hand, 2):
        if card1.value == card2.value:
            points += 2
            output_string += f"Pair {card1.value} / {card2.value} ({points})\n"
            
    return [points, output_string]

#Finding Runs
def find_runs(hand, flipped, points, output_string):
    #Initialize list of card values
    card_values = [get_card_points_runs(card.value) for card in hand]
    card_values.append(get_card_points_runs(flipped.value))
    card_values.sort(reverse=True)
    
    #Set up variables
    multiplier_count = 0 #Counts duplicates in runs for displaying
    total_multiplier = 1 #Total run multiplier (duplicates)
    multiplier = 1 #Local multiplier (duplicates)
    run_length = 1 #Length of the current run

    #Loop through each card
    for index in range(len(card_values)):
        if(index+1 < len(card_values)): #Ensure that overflow doesn't occur
            if(card_values[index] == card_values[index+1]): #If duplicate, add to multiplier
                multiplier += 1
            else:
                if(card_values[index] != card_values[index+1] and multiplier > 1): #If duplicate needs resetting
                    multiplier_count += multiplier-1
                    total_multiplier *= multiplier
                    multiplier = 1
                if(card_values[index]-1 == card_values[index+1]): #If next card continues run (since duplicates are taken care of)
                    run_length += 1
                elif(run_length >= 3): #If valid run, add points, display, and reset variables
                    multiplier_count += multiplier-1
                    total_multiplier *= multiplier
                    points += run_length * total_multiplier
                    output_string += f"{total_multiplier} run(s) of {run_length}{sorted(set([card_values[i] for i in range(index+1-run_length-multiplier_count, index+1)]))} for {run_length * total_multiplier} ({points})\n"

                    multiplier_count = 0
                    total_multiplier = 1
                    multiplier = 1
                    run_length = 1
                else: #If invalid run, reset variables
                    multiplier_count = 0
                    total_multiplier = 1
                    multiplier = 1
                    run_length = 1
        else: #If no more cards after this one, so wrap up with current variables
            if(run_length >= 3):
                multiplier_count += multiplier-1
                total_multiplier *= multiplier
                points += run_length * total_multiplier
                output_string += f"{total_multiplier} run(s) of {run_length}{sorted(set([card_values[i] for i in range(index+1-run_length-multiplier_count, index+1)])).rep} for {run_length * total_multiplier} ({points})"
                
            #Reset variables just to be safe
            multiplier_count = 0
            total_multiplier = 1
            multiplier = 1
            run_length = 1

    return [points, output_string]

#Finding Flush
def find_flush(hand, flipped, points, output_string):
    first_suit = hand[0].suit
    local_points = 0

    if all(card.suit == flipped.suit for card in hand):
        local_points += len(hand) + 1
    elif all(card.suit == first_suit for card in hand):
        local_points += len(hand)

    if(local_points != 0):
        points += local_points
        output_string += f"Flush of {first_suit} for {local_points}\n"

    return [points, output_string]

#Calculate the score
def calculate(hand, flipped):
    startTime = time.time()
    points = 0
    output_string = ""

    #Organize the hand
    hand = sorted(hand, key=lambda x: x.value)
    
    output_string += f"Flipped:\n{flipped.value}\n\nHand:\n"
    for card in reversed(hand):
        output_string += f"{card.value}\n"
    
    output_string += "------------------------\n"

    #Calculate points
    [points, output_string] = find_15s(hand, flipped, points, output_string)
    [points, output_string] = find_pairs(hand, flipped, points, output_string)
    [points, output_string] = find_runs(hand, flipped, points, output_string)
    [points, output_string] = find_flush(hand, flipped, points, output_string)
    [points, output_string] = nobs(hand, flipped, points, output_string)

    output_string += "------------------------\n"
    output_string += f"Total points: {points}"

    endTime = time.time()

    print(output_string)
    print(f"\nCalculationTime: {endTime - startTime}s")

    return points, output_string