import pygame, random, csv, datetime
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
    grid.mode = 1
    grid.setmode(grid.mode)
    
    while True:
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                return
            
            if event.type == MOUSEBUTTONDOWN:
                
                if event.button == 1 and grid.mode == 0:

                    x, y = event.pos
                    
                    if x < GRID_SIZE[0]:
                        ant = classes.Free4AllAnt(grid, len(grid.ants) + 1, int(x), int(y), (1 + len(grid.ants) % (len(grid.colors) - 1)), random.randint(0,3))

                elif event.button == 3 and grid.mode == 0:
                    
                    x, y = event.pos
                    
                    if x < GRID_SIZE[0]:
                        ant = classes.RainbowAnt(grid, len(grid.ants) + 1, int(x), int(y), 1, random.randint(0,3))

            if event.type == KEYDOWN:

                #Modes
                if event.key == K_1:
                    running = False
                    grid.setmode(1)

                if event.key == K_2:
                    running = False
                    grid.setmode(2)

                if event.key == K_0:
                    running = False
                    grid.setmode(0)

                if event.key == K_l and grid.mode == 2 and grid.total_steps == 0:
                    grid.antscheme += "L"
                    grid.statslabels()

                if event.key == K_r and grid.mode == 2 and grid.total_steps == 0:
                    grid.antscheme += "R"
                    grid.statslabels()

                #Pause/Start simulation
                if event.key == K_SPACE:
                    if len(grid.antscheme) > 1:
                        running = not running
                
                #Clear key
                if event.key == K_c:
                    grid.setmode(grid.mode)
                    running = False

                #Load key
                if event.key == K_d and grid.mode == 0:
                    Tkinter.Tk().withdraw() # Close the root window
                    csv_path = tkFileDialog.askopenfilename()
                    #Turn around to set back focus on main window
                    screen = pygame.display.set_mode((w, h+1), 0, 32)
                    screen = pygame.display.set_mode((w, h), 0, 32)

                    grid.clear()
                    running = False

                    with open(csv_path, 'rb') as csvfile:
                        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                        for row in csv_reader:
                            x = int(row[0])
                            y = int(row[1])
                            direction = int(row[2])
                            ant = classes.Free4AllAnt(grid, len(grid.ants) + 1, int(x), int(y), 1 + len(grid.ants) % (len(grid.colors) - 1), direction)

                #Save key
                if event.key == K_s  and grid.mode == 0:
                    now = datetime.datetime.now()
                    with open(now.strftime("(" + str(len(grid.ants)) + ") "  "%Y-%m-%d %H.%M.%S") + '.csv', 'wb') as csvfile:
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
                for ant in grid.ants:
                    ant.move()
            grid.total_steps += grid.frame_skip

        for ant in grid.ants:
            ant.render(screen)

        grid.updatestats()

        pygame.display.update()
    
if __name__ == "__main__":
    run()