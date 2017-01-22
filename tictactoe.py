import pygame, sys, time
from random import randint

#Loading images for X,O, and text
O = pygame.image.load("O.png")
X = pygame.image.load("X.png")
win = pygame.image.load("win.png")
lose = pygame.image.load("lose.png")
tie = pygame.image.load("tie.png")

#color of board
COLOR = (12,231,213)

#Variable pertaning to the tictactoe board, 0 if empty, 1 if X, 2 if 0
board = [0,0,0,0,0,0,0,0,0]

#Variable pertaining to the current turn, 0 if comp, 1 if player
turn = 1

#Player's turn function
#Inputs: Int {0,1}, Tuple of Int len = 2
#Requires: inputs be take from mouse.get_pressed()[0] and mouse.get_pos()
#Effects: modifies board variable
#Returns: Int {0,1}

def pturn(mousepre,mousepos):
	global board

	#Checking if mouse is being pressed in different boxes
	if mousepre:
		if mousepos[0] > 20 and mousepos[0] < 128:
			if mousepos[1] > 20 and mousepos[1] < 128 and board[0] == 0:
				board[0] = 1
				return 0
			if mousepos[1] > 138 and mousepos[1] < 263 and board[3] == 0:
				board[3] = 1
				return 0
			if mousepos[1] > 273 and mousepos[1] < 380 and board[6] == 0:
				board[6] = 1
				return 0
		if mousepos[0] > 138 and mousepos[0] < 263:
			if mousepos[1] > 20 and mousepos[1] < 128 and board[1] == 0:
				board[1] = 1
				return 0
			if mousepos[1] > 138 and mousepos[1] < 263 and board[4] == 0:
				board[4] = 1
				return 0
			if mousepos[1] > 273 and mousepos[1] < 380 and board[7] == 0:
				board[7] = 1
				return 0
		if mousepos[0] > 273 and mousepos[0] < 380:
			if mousepos[1] > 20 and mousepos[1] < 128 and board[2] == 0:
				board[2] = 1
				return 0
			if mousepos[1] > 138 and mousepos[1] < 263 and board[5] == 0:
				board[5] = 1
				return 0
			if mousepos[1] > 273 and mousepos[1] < 380 and board[8] == 0:
				board[8] = 1
				return 0
	return 1

#Computer's turn function
#Inputs:
#Effects: modifies board variable
#Returns: Int {0,1}

def cturn():
	time.sleep(1)
	global board

	#checking rows for player almost winning
	for i in range(3):
		row = [board[0+3*i],board[1+3*i],board[2+3*i]]
		if row.count(1) == 2 or row.count(2) == 2:
			for j in range(3):
				if row[j] == 0:
					board[i*3+j] = 2
					return 1

	#checking columns for player almost winning
	for i in range(3):
		col = [board[0+i],board[3+i],board[6+i]]
		if col.count(1) == 2 or col.count(2) == 2:
			for j in range(3):
				if col[j] == 0:
					board[j*3+i] = 2
					return 1

	#checking diagonals for player almost winning		
	diag1 = [board[0],board[4],board[8]]
	if diag1.count(1) == 2 or diag1.count(2) == 2:
		for j in range(3):
			if diag1[j] == 0:
				board[j*4] = 2
				return 1

	diag2 = [board[2], board[4], board[6]]
	if diag2.count(1) == 2 or diag2.count(2) == 2:
		for j in range(3):
			if diag2[j] == 0:
				board[(j+1)*2] = 2
				return 1

	#If not at risk of loosing choose random square
	while 1:
		index = randint(0,8)
		if board[index] == 0:
			board[index] = 2
			return 1

#Main function
def main():
	#Setup for Pygame window
	pygame.init()
	width,height = 400,400
	screen = pygame.display.set_mode((width,height))

	global turn
	global board

	#Is the game still going
	game = True

	#Did the player or computer win the game
	winner = None

	#Main loop
	while True:

		#Event loop, mostly exit conditions
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

		#Checking if the game is still going
		if game:
			#Running either player or computer turn
			if turn == 0:
				turn = cturn()

			if turn == 1:
				turn = pturn(pygame.mouse.get_pressed()[0],pygame.mouse.get_pos())

			#Drawing board onto screen
			screen.fill((0,0,0))
			pygame.draw.rect(screen, COLOR , [20, 128, 360, 10])
			pygame.draw.rect(screen, COLOR , [20, 263, 360, 10])
			pygame.draw.rect(screen, COLOR , [128, 20, 10, 360])
			pygame.draw.rect(screen, COLOR , [263, 20, 10, 360])

			#Drawing x and o on screen
			for i in range(3):
				for j in range(3):
					if board[(3*i)+j] == 1:
						Xrect = X.get_rect(center = (74+128*j,74+128*i))
						screen.blit(X,Xrect)
					if board[(3*i)+j] == 2:
						Orect = O.get_rect(center = (74+128*j,74+128*i))
						screen.blit(O,Orect)

			#check for endgame conditions
			for i in range(3):
				for j in range(2):
					row = [board[0+3*i],board[1+3*i],board[2+3*i]].count(j+1)
					col = [board[0+i],board[3+i],board[6+i]].count(j+1)
					diag1 = [board[0],board[4],board[8]].count(j+1)
					diag2 = [board[2],board[4],board[6]].count(j+1)
					if row == 3 or col == 3 or diag1 == 3 or diag2 == 3:
						game = False
						winner = not j
			if board.count(0) == 0:
				game = False
				winner = 2

		#If any of the end game conditions were met
		if not game:
			screen.fill((0,0,0))

			#Check if game was a tie, a draw or a win for the player
			if winner == 2:
				tierect = tie.get_rect(center = (200,200))
				screen.blit(tie,tierect)
			elif winner:
				winrect = win.get_rect(center = (200,200))
				screen.blit(win,winrect)
			else:
				loserect = lose.get_rect(center = (200,200))
				screen.blit(lose,loserect)
			pygame.display.flip()
			time.sleep(3)

			#Reset Game
			board = [0,0,0,0,0,0,0,0,0]
			winner = None
			game = True

		pygame.display.flip()

if __name__ == '__main__':
	main()