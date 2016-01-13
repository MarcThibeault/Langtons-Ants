import pygame, random, csv, datetime
import Tkinter, tkFileDialog
from pygame.locals import *

import classes
        
def run():

    pygame.init()

    STATS_WIDTH = 100
    GRID_SIZE = (900 - STATS_WIDTH, 600)

    w = GRID_SIZE[0] + STATS_WIDTH
    h = GRID_SIZE[1]
    screen = pygame.display.set_mode((w, h), 0, 32)
    
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, 22)
    
    pygame.display.set_caption("Langton's Ants on Steroids")

    grid = classes.AntGrid(screen, *GRID_SIZE)
    grid.ants = []
    grid.ants_couters.append(0)
    grid.statslabels()
    running = False
    
    while True:
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                return
            
            if event.type == MOUSEBUTTONDOWN:
                
                if event.button == 1:

                    x, y = event.pos
                    
                    if x < GRID_SIZE[0]:
                        ant = classes.Ant(grid, len(grid.ants) + 1, int(x), int(y), grid.colors[len(grid.ants) % len(grid.colors)], random.randint(0,3))

                elif event.button == 3:
                    
                    x, y = event.pos
                    
                    if x < GRID_SIZE[0]:
                        ant = classes.RainbowAnt(grid, len(grid.ants) + 1, int(x), int(y), grid.colors[0], random.randint(0,3))

            if event.type == KEYDOWN:
                
                if event.key == K_SPACE:
                    running = not running
                
                #Clear key
                if event.key == K_c:
                    grid.clear()
                    running = False

                #Load key
                if event.key == K_l:
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
                            ant = classes.Ant(grid, len(grid.ants) + 1, int(x), int(y), grid.colors[len(grid.ants) % len(grid.colors)], direction)

                #Save key
                if event.key == K_s:
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