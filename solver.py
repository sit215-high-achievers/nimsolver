#!/usr/bin/python3

import random


def check_empty(list):
    for i in list:
        if i != 0:
            return False
    return True

def check_win(list, misere, computer):
    empty = check_empty(list)
    if not empty:
        return False
    # For a normal game, a shortcut we can take here is just flipping who made the last turn.
    # Saves a few checks :)
    if not misere:
        computer = not computer
    print("You won!") if computer else print("The computer won!")
    return True

def get_computer_move(list):
    if misere:
        num_piles_greater_one = sum(1 for x in list if x > 1)
        # We only need to apply misere strategy if there is one or fewer piles with more than one piece. Otherwise continue as normal.
        if num_piles_greater_one <= 1:
            # Get the number of piles with tokens still on them
            piles_left = sum(1 for x in list if x > 0)
            # Get the size of the largest pile
            max_size = max(list)
            # Get the index of the largest pile
            max_idx = list.index(max_size)
            # If there are an even number of piles left or the largest pile is of size 1, empty the pile
            if piles_left % 2 == 0 or max_size == 1:
                list[max_idx] -= max_size
                print(f"The computer removed {max_size} from pile {max_idx}.")
            # Otherwise, reduce the largest pile to size 1
            else:
                list[max_idx] -= max_size-1
                print(
                    f"The computer removed {max_size-1} from pile {max_idx}.")
            return list

    # Try to make a move that makes the nim sum zero
    for idx, val in enumerate(list):
        # xor nim sum value with current pile
        xor_val = group_nimsum(list) ^ val
        # If the xor value is less than the value of the pile, make the xor value the new value for the pile
        if xor_val < val:
            old_val = val
            list[idx] = xor_val
            # If the new nim sum is zero, make the move
            if group_nimsum(list) == 0:
                print(
                    f"The computer removed {old_val-xor_val} from pile {idx}.")
                return list
            # If the new nim sum wasn't zero, restore the old value and move to the next pile
            list[idx] = old_val
     # If no valid nim sum zeroing move was found, remove a random number from a random stack
    while True:
        pile = random.randint(0, len(list)-1)
        if list[pile] != 0:
            num = random.randint(1, list[pile])
            list[pile] -= num
            print(f"The computer removed {num} from pile {pile}.")
            return list

def get_user_move(list):
    # Get the user's move
    pile = 0
    numdiscs = 0
    while True:
        # Try-catch here to handle the integer conversion
        try:
            pile = int(
                input(f"Which pile do you want to take from? (0-{len(list)-1}):  "))
            if pile < 0 or pile > len(list)-1 or list[pile] < 1:
                print(
                    "Pile number must be within range and have at least one item in the pile")
            else:
                break
        except:
            print("Invalid selection!")
    while True:
        try:
            numdiscs = int(
                input(f"How many discs do you want to take? (1-{list[pile]}):  "))
            if numdiscs > 0 and numdiscs <= list[pile]:
                break
        except:
            print("Invalid selection!")
    # Take the discs off the pile
    list[pile] -= numdiscs
    print(f"You removed {numdiscs} from pile {pile}.\n")
    return list


def group_nimsum(list):
    # The nimsum is the xor of the number of discs in each pile
    sum = 0
    for item in list:
        sum ^= item
    return sum

def print_board(list):
    for i, j in enumerate(list):
        print(f"Pile {i}: {j}")
    print()

def initialise_piles():
    numPiles = random.randint(2, 5)

    # Set the min number of initial tokens to n+1
    # We can initialise each stack with 1 to make up the additional n,
    # meeting the minimum 2n+1 requirement as well as making sure there
    # are no empty piles at the start
    totalPieces = random.randint(numPiles+1, numPiles*4)

    # Initialise piles with 1 token each
    discs = [1] * numPiles

    # Distribute tokens randomly amongst piles
    for i in range(totalPieces):
        idx = random.randint(0, numPiles-1)
        discs[idx] += 1
    return discs


# Change this to run in misere mode
misere = False
computerMove = False
gameOver = False
discs = initialise_piles()

while not gameOver:
    print_board(discs)
    if not computerMove:
        discs = get_user_move(discs)
    else:
        discs = get_computer_move(discs)
    gameOver = check_win(discs, misere, computerMove)
    computerMove = not computerMove
