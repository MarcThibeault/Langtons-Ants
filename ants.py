import pygame, random
from pygame.locals import *

class AntGrid(object):
    
    colors = ("red","green", "blue", "yellow")

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

    # Right statistics zone
    def updatestats(self):
        pygame.draw.line(self.screen, (255, 255, 255), (self.width, 0), (self.width, self.height))
        
        font = pygame.font.SysFont("monospace", 15)
        txt = font.render("STATISTICS", True, (255, 255, 255))
        self.screen.blit(txt, (691, 0))
    
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

    STATS_WIDTH = 110
    GRID_SIZE = (800 - STATS_WIDTH, 600)
    GRID_SQUARE_SIZE = (1, 1)
    frame_skip = 1

    w = GRID_SIZE[0] * GRID_SQUARE_SIZE[0] + STATS_WIDTH
    h = GRID_SIZE[1] * GRID_SQUARE_SIZE[1]
    screen = pygame.display.set_mode((w, h), 0, 32)
    
    default_font = pygame.font.get_default_font()
    font = pygame.font.SysFont(default_font, 22)    
    
    pygame.display.set_caption("Langton's Ants on Steroids")

    ants = []
    grid = AntGrid(screen, *GRID_SIZE)
    running = False
    
    total_iterations = 0
    
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
                        ant = Ant(grid, int(x), int(y), grid.colors[random.randint(0,len(grid.colors)-1)], random.randint(0,3))
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
                    total_iterations = 0
                    del ants[:]

                # Speed setting
                if event.key == K_KP_MINUS and frame_skip>1:
                    frame_skip = frame_skip / 4

                if event.key == K_KP_PLUS and frame_skip<262144:
                    frame_skip = frame_skip * 4
                
        #grid.render(screen, GRID_SQUARE_SIZE)
    
        if running:
            for iteration_no in xrange(frame_skip):        
                for ant in ants:
                    ant.move()
            total_iterations += frame_skip
            
        #txt = "%i iterations"%total_iterations
        #txt_surface = font.render("Running: %i iterations"%total_iterations, True, (255, 255, 255))
        #screen.blit(txt_surface, (0, 0))

        for ant in ants:
            ant.render(screen, GRID_SQUARE_SIZE)

        grid.updatestats()

        pygame.display.update()
    
if __name__ == "__main__":
    run()
            
