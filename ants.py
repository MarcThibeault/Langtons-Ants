import pygame, random, csv, datetime, re
import Tkinter, tkFileDialog
from pygame.locals import *

import classes
        
def run():

    pygame.init()

    STATS_WIDTH = 150
    GRID_SIZE = (1280 - STATS_WIDTH, 800)

    w = GRID_SIZE[0] + STATS_WIDTH
    h = GRID_SIZE[1]
    screen = pygame.display.set_mode((w, h), 0, 32)
    
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, 22)
    
    pygame.display.set_caption("Langton's Ants on Steroids")

    grid = classes.AntGrid(screen, *GRID_SIZE)
    grid.ants = []
    grid.ants_couters.append(0)
    running = False
    grid.setmode(1, "RL")
    
    while True:
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                return
            
            if event.type == MOUSEBUTTONDOWN:
                
                #Left click
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

            if event.type == KEYDOWN:

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
                if event.key == K_d and grid.mode == 0:
                    Tkinter.Tk().withdraw() # Close the root window
                    csv_path = tkFileDialog.askopenfilename()
                    #Turn around to set back focus on main window
                    screen = pygame.display.set_mode((w, h+1), 0, 32)
                    screen = pygame.display.set_mode((w, h), 0, 32)
                    
                    #Retrieving mode and scheme
                    match = re.search(r"^.*?\[[^\d]*(\d+)[^\d]*\-.*$", csv_path)
                    newmode = int(match.group(1))
                    match = re.search(r"\-([RL]*)\]", csv_path)
                    newscheme = match.group(1)

                    grid.setmode(newmode, newscheme)
                    running = False

                    with open(csv_path, 'rb') as csvfile:
					csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
					grid.loadlist = list(csv_reader)
					grid.loadlist.sort(key=lambda x: int(x[3]))

					for row in grid.loadlist:
						#Loading only ants that are due to appear at step 0
						if row[3] == '0':
							x = int(row[0])
							y = int(row[1])
							direction = int(row[2])
							ant = classes.Free4AllAnt(grid, len(grid.ants) + 1, int(x), int(y), 1 + len(grid.ants) % (len(grid.colors) - 1), direction)

					#Removing previously loaded ants from the load list
					for row in grid.loadlist[:]:
						if row[3] == '0':
							grid.loadlist.remove(row)
                
                #Save key
                if event.key == K_s  and grid.mode == 0:
                    now = datetime.datetime.now()
                    with open(now.strftime("save/(" + str(len(grid.ants)) + ")[" + str(grid.mode) + "-" + grid.scheme + "] " "%Y-%m-%d %H.%M.%S") + '.csv', 'wb') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        for ant in grid.ants:
                            csv_writer.writerow(ant.starting_params)

                # Speed setting
                if event.key == K_KP_MINUS and grid.frame_skip>1:
                    grid.frame_skip = grid.frame_skip / 4
                    grid.updatespeed()

                if event.key == K_KP_PLUS and grid.frame_skip<262144:
                    grid.frame_skip = grid.frame_skip * 4
                    grid.updatespeed()
    
        if running:
            for step_no in xrange(grid.frame_skip):

            	if len(grid.loadlist) > 0:
            		if int(grid.loadlist[0][3]) == grid.total_steps:
						x = int(grid.loadlist[0][0])
						y = int(grid.loadlist[0][1])
						direction = int(grid.loadlist[0][2])
						ant = classes.Free4AllAnt(grid, len(grid.ants) + 1, int(x), int(y), 1 + len(grid.ants) % (len(grid.colors) - 1), direction)
						del grid.loadlist[0]

                for ant in grid.ants:
                    ant.move()

            	grid.total_steps += 1

        for ant in grid.ants:
            ant.render(screen)

        grid.updatestats()

        pygame.display.update()
    
if __name__ == "__main__":
    run()