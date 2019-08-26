#!/usr/bin/python3

import random

def check_empty(list):
	for i in list:
		if i != 0:
			return False
	return True

def check_win(list, misere, computer):
	empty = check_empty(list)
	if (empty and misere and not computer) or (empty and not misere and computer):
		print("The computer won!")
		exit()
	elif (empty and not misere and not computer) or (empty and misere and computer):
		print("You won!")
		exit()

def get_computer_move(list):
	print_board(list)
	print(group_nimsum(list))
	if group_nimsum(list) == 0:
		# Computer will lose unless user makes mistake
		count = 0
		while count < len(list):
			if list[count] > 0:
				list[count] = 0
				break
			count += 1
	else:
		individual_nimsums = [list[i] ^ group_nimsum(list) for i in range(len(list))]
		count = 0
		while count < len(list):
			print(str(count) + ": " + str(individual_nimsums[count]) + " " + str(list[count]))
			if individual_nimsums[count] < list[count]:
				list[count] = individual_nimsums[count]
				break
			count += 1
	return list

def get_user_move(list):
	# Print the current board
	print_board(list)

	# Get the user's move
	pile = ""
	numdiscs = 0
	while True:
		pile = input("Which pile do you want to take from? ")
		for x in range(len(list)):
			if str(x) == pile:
				pile = x
		if type(pile) == int and list[pile] > 0:
			break
		print("Invalid selection!")
	while True:
		try:
			numdiscs = int(input("How many discs do you want to take? "))
			if numdiscs > 0 and numdiscs <= list[pile]:
				break
		except:
			print("Invalid selection!")

	# Take the discs off the pile
	list[pile] -= numdiscs
	return list

# The nimsum is the xor of the number of discs in each pile
def group_nimsum(list):
	sum = 0
	for item in list:
		sum ^= item
	return sum

def print_board(list):
	count = 0
	while count < len(list):
		print(str(list[count]) + " ", end='')
		count += 1
	print()
	count = 0
	while count < len(list):
		print (str(count) + " ", end='')
		count += 1
	print()

numpiles = random.randint(2,5)

# Change this to run in misere mode
misere = False

# This is a minimum number of pieces as per the specification
# You can experiment with increasing it.
totalpieces = 2 * numpiles + 1
piecesremaining = totalpieces

# Create starting position
count = 0
discs = []
while count < numpiles:
	if count == numpiles - 1:
		discs.append(piecesremaining)
	else:
		numdiscstoadd = random.randint(0, piecesremaining)
		discs.append(numdiscstoadd)
		piecesremaining -= numdiscstoadd
	count += 1

while True:
	discs = get_user_move(discs)
	check_win(discs, misere, False)
	discs = get_computer_move(discs)
	check_win(discs, misere, True)
