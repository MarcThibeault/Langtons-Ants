import pygame, random
from pygame.locals import *

#Global Functions
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

class AntGrid(object):
    
    colors = ("#FF0000", "#FF5000", "#FFFF00", "#00FF00", "#00FFFF",  "#0000FF", "#9900FF", "#FFFFFF")
    total_steps = 0
    frame_skip = 1
    explored = 0
    nb_ants = 0
    ants_couters = []

    def __init__(self, screen, width, height):
        
        self.screen = screen
        self.width = width
        self.height = height        
        self.clear()
    
    def clear(self):
        
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
        self.nb_ants = 0
    
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
    def updatestats(self, nb_ants):
        percent_explored = float(float(self.explored) / (self.height * self.width) * 100)

        font = pygame.font.SysFont("monospace", 15)

        txt = font.render("%i" %self.total_steps, True, (255, 255, 255))
        self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 80)))
        self.screen.blit(txt, (self.width + 2, 80))
        txt = font.render("%s" %str(round(percent_explored, 2)) + "%", True, (255, 255, 255))
        self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 112)))
        self.screen.blit(txt, (self.width + 2, 112))
        txt = font.render("%i" %nb_ants, True, (255, 255, 255))
        self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 144)))
        self.screen.blit(txt, (self.width + 2, 144))

        Score1 = 0
        Score2 = 0
        Score3 = 0

        if nb_ants > 0:
            for i in range(1, nb_ants + 1):
                if self.ants_couters[i] >= self.ants_couters[Score1]:
                    Score3 = Score2
                    Score2 = Score1
                    Score1 = i
                else:
                    if self.ants_couters[i] >= self.ants_couters[Score2]:
                        Score3 = Score2
                        Score2 = i
                    else:
                        if self.ants_couters[i] >= self.ants_couters[Score3]:
                            Score3 = i

            txt = font.render("%i  " %self.ants_couters[Score1], True, (hex_to_rgb(self.colors[Score1 % len(self.colors) - 1])))
            self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 192)))
            self.screen.blit(txt, (self.width + 2, 192))
            txt = font.render("%i  " %self.ants_couters[Score2], True, (hex_to_rgb(self.colors[Score2 % len(self.colors) - 1])))
            self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 208)))
            self.screen.blit(txt, (self.width + 2, 208))
            txt = font.render("%i  " %self.ants_couters[Score3], True, (hex_to_rgb(self.colors[Score3 % len(self.colors) - 1])))
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
        self.direction = direction
        self.grid.nb_ants += 1
        
        
    def move(self):
                
        self.grid.colorswap(self.x, self.y, self.ant_id, self.color)
                
        self.x = ( self.x + Ant.directions[self.direction][0] ) % self.grid.width
        self.y = ( self.y + Ant.directions[self.direction][1] ) % self.grid.height        
                        
        if self.grid.get(self.x, self.y) == "X" or self.grid.get(self.x, self.y) == 0:
            self.direction = (self.direction-1) % 4
        else:
            self.direction = (self.direction+1) % 4

    def render(self, surface, grid_size):
        
        grid_w, grid_h = grid_size     

class RainbowAnt(object):
    
    directions = ( (0,-1), (+1,0), (0,+1), (-1,0) )
    
    def __init__(self, grid, ant_id, x, y, color, direction):
        
        self.grid = grid
        self.ant_id = ant_id
        self.x = x
        self.y = y
        self.decimal_color = 1
        self.color = pygame.Color(color)
        self.direction = direction
        self.grid.nb_ants += 1
        
        
    def move(self):

        self.color = pygame.Color(self.grid.colors[self.grid.total_steps / 1000 % (len(self.grid.colors)-1)])
        self.grid.colorswap(self.x, self.y, self.ant_id, self.color)
                
        self.x = ( self.x + Ant.directions[self.direction][0] ) % self.grid.width
        self.y = ( self.y + Ant.directions[self.direction][1] ) % self.grid.height        
                        
        if self.grid.get(self.x, self.y) == "X" or self.grid.get(self.x, self.y) == 0:
            self.direction = (self.direction-1) % 4
        else:
            self.direction = (self.direction+1) % 4
        
        
    def render(self, surface, grid_size):
        
        grid_w, grid_h = grid_size        
        
def run():

    pygame.init()

    STATS_WIDTH = 100
    GRID_SIZE = (900 - STATS_WIDTH, 600)
    GRID_SQUARE_SIZE = (1, 1)

    w = GRID_SIZE[0] * GRID_SQUARE_SIZE[0] + STATS_WIDTH
    h = GRID_SIZE[1] * GRID_SQUARE_SIZE[1]
    screen = pygame.display.set_mode((w, h), 0, 32)
    
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, 22)    
    
    pygame.display.set_caption("Langton's Ants on Steroids")

    ants = []
    grid = AntGrid(screen, *GRID_SIZE)
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
                    x /= GRID_SQUARE_SIZE[0]
                    y /= GRID_SQUARE_SIZE[1]
                    
                    if x < GRID_SIZE[0]:
                        ant = Ant(grid, len(ants) + 1, int(x), int(y), grid.colors[len(ants) % len(grid.colors)], random.randint(0,3))
                        ants.append(ant)
                        grid.ants_couters.append(0)
                        grid.colorswap(x, y, ant.ant_id, ant.color)

                elif event.button == 3:
                    
                    x, y = event.pos
                    x /= GRID_SQUARE_SIZE[0]
                    y /= GRID_SQUARE_SIZE[1]
                    
                    if x < GRID_SIZE[0]:
                        ant = RainbowAnt(grid, len(ants) + 1, int(x), int(y), grid.colors[0], random.randint(0,3))
                        ants.append(ant)
                        grid.ants_couters.append(0)
                        grid.colorswap(x, y, ant.ant_id, ant.color)

            if event.type == KEYDOWN:
                
                if event.key == K_SPACE:                
                    running = not running
                    
                if event.key == K_c:
                    grid.clear()
                    grid.total_steps = 0
                    del ants[:]
                    grid.statslabels()
                    grid.updatestats(len(ants))
                    grid.updatespeed()
                    running = False

                # Speed setting
                if event.key == K_KP_MINUS and grid.frame_skip>1:
                    grid.frame_skip = grid.frame_skip / 4
                    grid.updatespeed()

                if event.key == K_KP_PLUS and grid.frame_skip<262144:
                    grid.frame_skip = grid.frame_skip * 4
                    grid.updatespeed()
                
        #grid.render(screen, GRID_SQUARE_SIZE)
    
        if running:
            for step_no in xrange(grid.frame_skip):        
                for ant in ants:
                    ant.move()
            grid.total_steps += grid.frame_skip

        for ant in ants:
            ant.render(screen, GRID_SQUARE_SIZE)

        grid.updatestats(len(ants))

        pygame.display.update()
        grid.updatespeed()
    
if __name__ == "__main__":
    run()