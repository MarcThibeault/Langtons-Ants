import pygame, random, csv, datetime
import Tkinter, tkFileDialog
from pygame.locals import *
import globalfunctions

class AntGrid(object):
    
    colors = ["#FF0000", "#FF7000", "#FFFF00", "#00FF00", "#00FFFF",  "#0000FF", "#9900FF", "#FFFFFF"]
    total_steps = 0
    frame_skip = 1
    explored = 0
    nb_ants = 0
    ants = []
    ants_couters = []

    def __init__(self, screen, width, height):
        
        self.screen = screen
        self.width = width
        self.height = height
        self.clear()
    
    def clear(self):
        
        del self.ants[:]
        self.ants_couters = []
        self.ants_couters.append(0)
        self.rows = []
        for col_no in xrange(self.height):
            new_row = []
            self.rows.append(new_row)
            for row_no in xrange(self.width):
                new_row.append("X")
        self.screen.fill((0, 0, 0))
        self.explored = 0
        self.total_steps = 0
        self.frame_skip = 1
        self.nb_ants = 0

        self.statslabels()
        self.updatespeed()
        self.updatestats()
    
    # Swaps grid pixels from black to color or color to black
    def colorswap(self, x, y, ant_id, color):
        if self.rows[y][x] == "X":
            self.rows[y][x] = ant_id
            self.screen.set_at((x, y), color)
            self.explored += 1
            self.ants_couters[ant_id] += 1
        elif self.rows[y][x] == 0:
            self.rows[y][x] = ant_id
            self.screen.set_at((x, y), color)
            self.ants_couters[ant_id] += 1
        else:
            self.ants_couters[self.rows[y][x]] -= 1
            self.rows[y][x] = 0
            self.screen.set_at((x, y), (0, 0, 0))

    # Stats area static labels and vertical line
    def statslabels(self):
        font = pygame.font.SysFont("monospace", 15)

        txt = font.render("STATISTICS", True, (255, 255, 255))
        self.screen.blit(txt, (self.width + 2, 0))
        txt = font.render("Speed", True, (255, 255, 255))
        self.screen.blit(txt, (self.width + 2, 32))
        txt = font.render("Steps", True, (255, 255, 255))
        self.screen.blit(txt, (self.width + 2, 64))
        txt = font.render("Explored", True, (255, 255, 255))
        self.screen.blit(txt, (self.width + 2, 96))
        txt = font.render("Ants", True, (255, 255, 255))
        self.screen.blit(txt, (self.width + 2, 128))
        txt = font.render("Top 3", True, (255, 255, 255))
        self.screen.blit(txt, (self.width + 2, 176))

        pygame.draw.line(self.screen, (255, 255, 255), (self.width, 0), (self.width, self.height))

    # Update stats data
    def updatestats(self):
        percent_explored = float(float(self.explored) / (self.height * self.width) * 100)

        font = pygame.font.SysFont("monospace", 15)

        txt = font.render("%i" %self.total_steps, True, (255, 255, 255))
        self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 80)))
        self.screen.blit(txt, (self.width + 2, 80))
        txt = font.render("%s" %str(round(percent_explored, 2)) + "%   ", True, (255, 255, 255))
        self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 112)))
        self.screen.blit(txt, (self.width + 2, 112))
        txt = font.render("%i" %len(self.ants), True, (255, 255, 255))
        self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 144)))
        self.screen.blit(txt, (self.width + 2, 144))

        Score1 = 0
        Score2 = 0
        Score3 = 0

        if len(self.ants) > 0:
            for i in range(len(self.ants), 0, -1):
                if self.ants_couters[i] >= self.ants_couters[Score1]:
                    Score3 = Score2
                    Score2 = Score1
                    Score1 = i
                elif self.ants_couters[i] >= self.ants_couters[Score2]:
                        Score3 = Score2
                        Score2 = i
                elif self.ants_couters[i] >= self.ants_couters[Score3]:
                            Score3 = i

            if len(self.ants) >= 1:
                txt = font.render("%i  " %self.ants_couters[Score1], True, (self.ants[Score1-1].rgb_color))
                self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 192)))
                self.screen.blit(txt, (self.width + 2, 192))
            if len(self.ants) > 1:
                txt = font.render("%i  " %self.ants_couters[Score2], True, (self.ants[Score2-1].rgb_color))
                self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 208)))
                self.screen.blit(txt, (self.width + 2, 208))
            if len(self.ants) > 2:
                txt = font.render("%i  " %self.ants_couters[Score3], True, (self.ants[Score3-1].rgb_color))
                self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 224)))
                self.screen.blit(txt, (self.width + 2, 224))

    #Update speed in stats, only when speed changes
    def updatespeed(self):
        font = pygame.font.SysFont("monospace", 15)

        txt = font.render("%ix  " %self.frame_skip, True, (255, 255, 255))
        self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 48)))
        self.screen.blit(txt, (self.width + 2, 48))
    
    def get(self, x, y):
        return self.rows[y][x]
  
class Ant(object):
    
    directions = ( (0,-1), (+1,0), (0,+1), (-1,0) )
    
    def __init__(self, grid, ant_id, x, y, color, direction):
        
        self.grid = grid
        self.ant_id = ant_id
        self.x = x
        self.y = y
        self.color = pygame.Color(color)
        self.rgb_color = globalfunctions.hex_to_rgb(color)
        self.direction = direction
        self.grid.nb_ants += 1

        self.grid.ants.append(self)
        self.grid.ants_couters.append(0)
        self.grid.colorswap(self.x, self.y, self.ant_id, self.color)

        self.starting_params = (x, y, direction, self.grid.total_steps)
        
    def move(self):
                
        self.grid.colorswap(self.x, self.y, self.ant_id, self.color)
                
        self.x = ( self.x + Ant.directions[self.direction][0] ) % self.grid.width
        self.y = ( self.y + Ant.directions[self.direction][1] ) % self.grid.height
                        
        if self.grid.get(self.x, self.y) == "X" or self.grid.get(self.x, self.y) == 0:
            self.direction = (self.direction-1) % 4
        else:
            self.direction = (self.direction+1) % 4

    def render(self, surface):
        
        grid_w, grid_h = (1,1)

class RainbowAnt(object):
    
    directions = ( (0,-1), (+1,0), (0,+1), (-1,0) )
    
    def __init__(self, grid, ant_id, x, y, color, direction):
        
        self.grid = grid
        self.ant_id = ant_id
        self.x = x
        self.y = y
        self.color = pygame.Color(color)
        self.rgb_color = globalfunctions.hex_to_rgb(color)
        self.direction = direction
        self.grid.nb_ants += 1

        self.grid.ants.append(self)
        self.grid.ants_couters.append(0)
        self.grid.colorswap(self.x, self.y, self.ant_id, self.color)
        
    def move(self):

        new_color = self.grid.colors[self.grid.total_steps / 1000 % (len(self.grid.colors)-1)]
        self.color = pygame.Color(new_color)
        self.rgb_color = globalfunctions.hex_to_rgb(new_color)
        self.grid.colorswap(self.x, self.y, self.ant_id, self.color)
        
        self.x = ( self.x + Ant.directions[self.direction][0] ) % self.grid.width
        self.y = ( self.y + Ant.directions[self.direction][1] ) % self.grid.height
        
        if self.grid.get(self.x, self.y) == "X" or self.grid.get(self.x, self.y) == 0:
            self.direction = (self.direction-1) % 4
        else:
            self.direction = (self.direction+1) % 4
        
        
    def render(self, surface):
        
        grid_w, grid_h = (1,1)
        
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

    grid = AntGrid(screen, *GRID_SIZE)
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
                        ant = Ant(grid, len(grid.ants) + 1, int(x), int(y), grid.colors[len(grid.ants) % len(grid.colors)], random.randint(0,3))

                elif event.button == 3:
                    
                    x, y = event.pos
                    
                    if x < GRID_SIZE[0]:
                        ant = RainbowAnt(grid, len(grid.ants) + 1, int(x), int(y), grid.colors[0], random.randint(0,3))

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
                            ant = Ant(grid, len(grid.ants) + 1, int(x), int(y), grid.colors[len(grid.ants) % len(grid.colors)], direction)

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