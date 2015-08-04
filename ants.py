import pygame, random
from pygame.locals import *

class AntGrid(object):
    
    colors = ("red","green", "blue", "yellow", "dark orange", "violet red")
    total_iterations = 0
    frame_skip = 1

    def __init__(self, screen, width, height):
        
        self.screen = screen
        self.width = width
        self.height = height        
        self.clear()
    
    def clear(self):
        
        self.rows = []
        for col_no in xrange(self.height):
            new_row = []
            self.rows.append(new_row)
            for row_no in xrange(self.width):
                new_row.append((0, 0, 0))
        self.screen.fill((0, 0, 0))
    
    # Swaps grid pixels from black to color or color to black
    def colorswap(self, x, y, color):  
        if self.rows[y][x] == (0, 0, 0):
            self.rows[y][x] = color
            self.screen.set_at((x, y), color)
        else:
            self.rows[y][x] = (0, 0, 0)
            self.screen.set_at((x, y), (0, 0, 0))

    # Stats area static labels and vertical line
    def statslabels(self):
        font = pygame.font.SysFont("monospace", 15)

        txt = font.render("STATISTICS", True, (255, 255, 255))
        self.screen.blit(txt, (self.width + 2, 0))
        txt = font.render("Speed", True, (255, 255, 255))
        self.screen.blit(txt, (self.width + 2, 32))
        txt = font.render("Iterations", True, (255, 255, 255))
        self.screen.blit(txt, (self.width + 2, 64))
        txt = font.render("Ants", True, (255, 255, 255))
        self.screen.blit(txt, (self.width + 2, 96))

        pygame.draw.line(self.screen, (255, 255, 255), (self.width, 0), (self.width, self.height))

    # Update stats data
    def updatestats(self, nb_ants):
        font = pygame.font.SysFont("monospace", 15)

        txt = font.render("%ix " %self.frame_skip, True, (255, 255, 255))
        self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 48)))
        self.screen.blit(txt, (self.width + 2, 48))
        txt = font.render("%i" %self.total_iterations, True, (255, 255, 255))
        self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 80)))
        self.screen.blit(txt, (self.width + 2, 80))
        txt = font.render("%i" %nb_ants, True, (255, 255, 255))
        self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 108)))
        self.screen.blit(txt, (self.width + 2, 108))
    
    def get(self, x, y):
        return self.rows[y][x]
  
class Ant(object):
    
    directions = ( (0,-1), (+1,0), (0,+1), (-1,0) )
    
    def __init__(self, grid, x, y, color, direction):
        
        self.grid = grid
        self.x = x
        self.y = y
        self.color = pygame.Color(color)
        self.direction = direction
        
        
    def move(self):
                
        self.grid.colorswap(self.x, self.y, self.color)
                
        self.x = ( self.x + Ant.directions[self.direction][0] ) % self.grid.width
        self.y = ( self.y + Ant.directions[self.direction][1] ) % self.grid.height        
                        
        if self.grid.get(self.x, self.y) == (0, 0, 0):
            self.direction = (self.direction-1) % 4
        else:
            self.direction = (self.direction+1) % 4

    def render(self, surface, grid_size):
        
        grid_w, grid_h = grid_size     

class RainbowAnt(object):
    
    directions = ( (0,-1), (+1,0), (0,+1), (-1,0) )
    
    def __init__(self, grid, x, y, direction):
        
        self.grid = grid
        self.x = x
        self.y = y
        self.decimal_color = 1
        self.color = pygame.Color("#000001")
        self.direction = direction
        
        
    def move(self):

        if self.decimal_color < 16777150: #<16777214
            self.decimal_color += 32
        else:
            self.decimal_color = 1

        #print self.decimal_color

        hex_color = "0x" + ("%x" % self.decimal_color).zfill(6) # pad with zeros

        self.color = pygame.Color(hex_color)
                
        self.grid.colorswap(self.x, self.y, self.color)
                
        self.x = ( self.x + Ant.directions[self.direction][0] ) % self.grid.width
        self.y = ( self.y + Ant.directions[self.direction][1] ) % self.grid.height        
                        
        if self.grid.get(self.x, self.y) == (0, 0, 0):
            self.direction = (self.direction-1) % 4
        else:
            self.direction = (self.direction+1) % 4               
        
        
    def render(self, surface, grid_size):
        
        grid_w, grid_h = grid_size        
        
def run():

    pygame.init()

    STATS_WIDTH = 120
    GRID_SIZE = (800 - STATS_WIDTH, 600)
    GRID_SQUARE_SIZE = (1, 1)

    w = GRID_SIZE[0] * GRID_SQUARE_SIZE[0] + STATS_WIDTH
    h = GRID_SIZE[1] * GRID_SQUARE_SIZE[1]
    screen = pygame.display.set_mode((w, h), 0, 32)
    
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, 22)    
    
    pygame.display.set_caption("Langton's Ants on Steroids")

    ants = []
    grid = AntGrid(screen, *GRID_SIZE)
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
                        ant = Ant(grid, int(x), int(y), grid.colors[len(ants) % len(grid.colors)], random.randint(0,3))
                        grid.colorswap(x, y, ant.color)
                        ants.append(ant)

                elif event.button == 3:
                    
                    x, y = event.pos
                    x /= GRID_SQUARE_SIZE[0]
                    y /= GRID_SQUARE_SIZE[1]
                    
                    if x < GRID_SIZE[0]:
                        ant = RainbowAnt(grid, int(x), int(y), random.randint(0,3))
                        grid.colorswap(x, y, ant.color)
                        ants.append(ant)

            if event.type == KEYDOWN:
                
                if event.key == K_SPACE:                
                    running = not running
                    
                if event.key == K_c:
                    grid.clear()
                    grid.total_iterations = 0
                    del ants[:]
                    grid.statslabels()
                    grid.updatestats(len(ants))

                # Speed setting
                if event.key == K_KP_MINUS and grid.frame_skip>1:
                    grid.frame_skip = grid.frame_skip / 4

                if event.key == K_KP_PLUS and grid.frame_skip<262144:
                    grid.frame_skip = grid.frame_skip * 4
                
        #grid.render(screen, GRID_SQUARE_SIZE)
    
        if running:
            for iteration_no in xrange(grid.frame_skip):        
                for ant in ants:
                    ant.move()
            grid.total_iterations += grid.frame_skip
            
        #txt = "%i iterations"%grid.total_iterations
        #txt_surface = font.render("Running: %i iterations"%grid.total_iterations, True, (255, 255, 255))
        #screen.blit(txt_surface, (0, 0))

        for ant in ants:
            ant.render(screen, GRID_SQUARE_SIZE)

        grid.updatestats(len(ants))

        pygame.display.update()
    
if __name__ == "__main__":
    run()
            
