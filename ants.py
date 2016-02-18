import pygame, random, csv, datetime, re
import Tkinter, tkFileDialog
from pygame.locals import *

import classes
		
def run():

	pygame.init()

	STATS_WIDTH = 130
	GRID_SIZE = (1280 - STATS_WIDTH, 800)

	w = GRID_SIZE[0] + STATS_WIDTH
	h = GRID_SIZE[1]

	screen = pygame.display.set_mode((w, h), 0, 32)
	FULLSCREEN = False

	pygame.display.set_caption("Langton's Ants Simulator")

	grid = classes.AntGrid(screen, *GRID_SIZE)
	grid.ants = []
	grid.ants_couters.append(0)
	running = False
	grid.setmode(1, "RL")
	
	while True:
		
		for event in pygame.event.get():
			
			if event.type == QUIT:
				return
			
			#Mouse events
			if event.type == MOUSEBUTTONDOWN:
				
				#Left click (Add new ant)
				if event.button == 1:

					x, y = event.pos
					
					if x < GRID_SIZE[0]:
						#Langton mode
						if grid.mode == 1:
							ant = classes.ClassicAnt(grid, len(grid.ants) + 1, int(x), int(y), 0)
						#Turk-Propp mode
						elif grid.mode == 2:
							ant = classes.ClassicAnt(grid, len(grid.ants) + 1, int(x), int(y), 0)
						#Free4All mode
						elif grid.mode == 0:
							ant = classes.Free4AllAnt(grid, len(grid.ants) + 1, int(x), int(y), (1 + len(grid.ants) % (len(grid.colors) - 1)), random.randint(0,3))

			   	#Right click (Rainbow ant in Free4All mode)
				elif event.button == 3 and grid.mode == 0 and grid.rainbow == False:

					x, y = event.pos

					if x < GRID_SIZE[0]:
						ant = classes.RainbowAnt(grid, len(grid.ants) + 1, int(x), int(y), 1, random.randint(0,3))

			#Keyboard events
			if event.type == KEYDOWN:

				#Quit
				if event.key == K_ESCAPE:
					return
				
				#Toggle Fullscreen
				if event.key == K_F11:

					if FULLSCREEN:
						GRID_SIZE = (1280 - STATS_WIDTH, 800)

						w = GRID_SIZE[0] + STATS_WIDTH
						h = GRID_SIZE[1]

						screen = pygame.display.set_mode((w, h), 0, 32)
					else:
						root = Tkinter.Tk()
						screen_width = root.winfo_screenwidth()
						screen_height = root.winfo_screenheight()

						GRID_SIZE = (screen_width - STATS_WIDTH, screen_height)

						w = GRID_SIZE[0] + STATS_WIDTH
						h = GRID_SIZE[1]

						screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
					
					grid = classes.AntGrid(screen, *GRID_SIZE)

					grid.setmode(1, "RL")

					FULLSCREEN = not FULLSCREEN
					running = False

				#Modes
				if event.key == K_1:
					running = False
					grid.setmode(1, "RL")

				if event.key == K_2:
					running = False
					grid.setmode(2, "")

				if event.key == K_0:
					running = False
					grid.setmode(0, "RL")

				#Moving scheme
				if event.key == K_l and grid.mode == 2 and grid.total_steps == 0:
					grid.scheme += "L"
					grid.statslabels()

				if event.key == K_r and grid.mode == 2 and grid.total_steps == 0:
					grid.scheme += "R"
					grid.statslabels()

				if event.key == K_BACKSPACE and grid.mode == 2 and grid.total_steps == 0:
					grid.scheme = grid.scheme[:-1]
					grid.statslabels()

				#Pause/Start simulation
				if event.key == K_SPACE:
					if len(grid.scheme) > 1:
						running = not running
				
				#Clear key
				if event.key == K_c:
					grid.setmode(grid.mode, grid.scheme)
					running = False

				#Load key
				if event.key == K_d:
					running = False

					#Disable fullscreen for open file dialog
					screen = pygame.display.set_mode((w, h), 0, 32)

					Tkinter.Tk().withdraw() # Close the root window
					csv_path = tkFileDialog.askopenfilename()

					#Get back to fullscreen, or reset window size to regain focus
					if FULLSCREEN:
						screen = pygame.display.set_mode((w, h), pygame.FULLSCREEN)
					else:
						screen = pygame.display.set_mode((w, h+1), 0, 32)
						screen = pygame.display.set_mode((w, h), 0, 32)
					
					grid.load(csv_path)
				
				#Save key
				if event.key == K_s:
					grid.save()

				# Speed setting
				if (event.key == K_KP_MINUS or event.key == K_MINUS) and grid.frame_skip>1:
					grid.frame_skip = grid.frame_skip / 4
					grid.updatespeed()

				if (event.key == K_KP_PLUS or event.key == K_PLUS or event.key == K_EQUALS) and grid.frame_skip<262144:
					grid.frame_skip = grid.frame_skip * 4
					grid.updatespeed()
	
		if running:
			for step_no in xrange(grid.frame_skip):

				#Check if there are ants to be loaded later in the simulation
				if len(grid.loadlist) > 0:
					if int(grid.loadlist[0][3]) == grid.total_steps:
						x = int(grid.loadlist[0][0])
						y = int(grid.loadlist[0][1])
						direction = int(grid.loadlist[0][2])
						if grid.mode == 1:
							#Langton Mode
							ant = classes.ClassicAnt(grid, len(grid.ants) + 1, int(x), int(y), direction)
						elif grid.mode == 2:
							#Turk-Propp Mode
							ant = classes.ClassicAnt(grid, len(grid.ants) + 1, int(x), int(y), direction)
						elif grid.mode == 0:
							#Free4All Mode
							ant = classes.Free4AllAnt(grid, len(grid.ants) + 1, int(x), int(y), 1 + len(grid.ants) % (len(grid.colors) - 1), direction)
						del grid.loadlist[0]

				#Updating each ant's position
				for ant in grid.ants:
					ant.move()

				grid.total_steps += 1

		grid.updatestats()

		pygame.display.update()
	
if __name__ == "__main__":
	run()
