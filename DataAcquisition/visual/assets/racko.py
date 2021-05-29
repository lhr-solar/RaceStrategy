# File: racko.py
# Description: A program that simulates the card and number game
# Rack-O. Players use the keyboard and take turns.
# Assignment Number: 10
#
# Name: <YOUR NAME>
# EID:  <YOUR EID>
# Email: <YOUR EMAIL>
# Grader: <YOUR GRADER'S NAME Irena OR Noah OR Skyler OR Tyler>
#
# On my honor, <YOUR NAME>, this programming assignment is my own work
# and I have not provided this code to any other student. 

import random


# Play one game of Rack-O.
def main():
    # Get the rack size, create the deck, and deal the initial racks.
    rack_size = prep_game()
    deck = list(range(1, 61))
    random.shuffle(deck)
    player = 1
    player_1_rack = get_rack(deck, rack_size)
    player_2_rack = get_rack(deck, rack_size)
    discard = [deck.pop(0)]

    # CS303e students. Complete the main method to play
    # one complete game of Rack-O using the specified functions.
    

# Get ready to play 1 game.
# Show the instructions if the user wants to see them.
# Set the seed for the random number generator.
# Return the size of the rack to use.
def prep_game():
    print('----- Welcome to Rack - O! -----')
    if input('Enter y to display instructions: ') == 'y':
        instructions()
    print()
    random.seed(eval(input('Enter number for initial seed: ')))
    rack_size = eval(input('Enter the size of the rack to use. '
                            + 'Must be between 5 and 10: '))
    while not 5 <= rack_size <= 10:
        print(rack_size, 'is not a valid rack size.')
        rack_size = eval(input('Enter the size of the rack to use. '
                            + 'Must be between 5 and 10: '))
    print()
    return rack_size


# Print the instructions of the game.
def instructions():
    print()
    print('The goal of the game is to get the cards in your rack of cards')
    print('into ascending order. Your rack has ten slots numbered 1 to 10.')
    print('During your turn you can draw the top card of the deck or take')
    print('the top card of the discard pile.')
    print('If you draw the top card of the deck, you can use that card to')
    print('replace a card in one slot of your rack. The replaced card goes to')
    print('the discard pile.')
    print('Alternatively you can simply choose to discard the drawn card.')
    print('If you take the top card of the discard pile you must use it to')
    print('replace a card in one slot of your rack. The replaced card goes')
    print('to the top of the discard pile.')


# Take the player's turn. Give them the choice of drawing or taking
# the top card of the discard pile. If they draw they can replace
# a card or discard the draw. If they take the top card of the discard
# pile they must replace a card in their rack.
def take_turn(deck, discard, player_rack):
    


# Ask the player which card to replace in their rack.
# Replace it with the given new card. Place the card removed
# from the player's rack at the top of the discard pile.
# Error checks until player enters a card that is currently
# in their rack.
def place_card(player_rack, new_card, discard):
    

           
# Return True if this rack is sorted in ascending order, False otherwise.
# Do not create any new lists in this function.
def is_sorted(rack):
    

# Deal the top 10 cards of the deck into a new rack. The first
# card goes in the first slot, the second card goes in the second
# slot, and so forth. We assume len(deck) >= rack_size. Return the
# list of ints representing the rack.
def get_rack(deck, rack_size):

    
main()
    
