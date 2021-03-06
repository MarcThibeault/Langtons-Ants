import pygame, random, csv, datetime, re
import tkinter
from pygame.locals import *
from tkinter import filedialog
import globalfunctions

#All classes

#The grid in which the simulation takes place
class AntGrid(object):

	colors = ["#000000", "#FF0000", "#444444", "#FFFF00", "#00FF00", "#00FFFF",  "#0000FF", "#9900FF"]
	mode = 1
	scheme = ""
	modenames = ["Free4All", "Langton", "Turk-Propp"]
	total_steps = 0
	frame_skip = 1
	nb_ants = 0
	rainbow = False
	ants = []
	ants_couters = []
	loadlist = []

	def __init__(self, screen, width, height):

		self.screen = screen
		self.width = width
		self.height = height
		self.clear()

	#setmode takes care of the starting params for each mode
	#It also creates the starting ant for non-Free4All modes
	def setmode(self, mode, scheme):

		self.mode = mode
		self.scheme = scheme

		self.clear()

		if self.mode == 1 or self.mode == 2:
			#Langton mode // Turk-Propp mode starting ant
			ant = ClassicAnt(self, len(self.ants) + 1, self.width // 2, self.height // 2, 0)
		elif self.mode == 0:
			#Free4All mode
			self.rainbow = False

	# Reset the simulation
	def clear(self):

		del self.ants[:]
		self.ants_couters = []
		self.ants_couters.append(0)
		self.rows = []
		for col_no in range(self.height):
			new_row = []
			self.rows.append(new_row)
			for row_no in range(self.width):
				new_row.append("X")
		self.screen.fill((0, 0, 0))
		del self.loadlist[:]
		self.total_steps = 0
		self.frame_skip = 1
		self.nb_ants = 0

		self.statslabels()
		self.updatespeed()
		self.updatestats()

	#Saving the simulation's ants and params in a CSV file
	def save(self):

		now = datetime.datetime.now()
		with open(now.strftime("save/[" + str(self.mode) + "-" + self.scheme + "](" + str(len(self.ants)) + ") " "%Y-%m-%d %H.%M.%S") + '.csv', 'wb') as csvfile:
			csv_writer = csv.writer(csvfile)
			for ant in self.ants:
				csv_writer.writerow(ant.starting_params)

	#Loading a simulation from a CSV file
	def load(self, csv_path):

		#Retrieving mode and scheme
		match = re.search(r"^.*?\[[^\d]*(\d+)[^\d]*\-.*$", csv_path)
		newmode = int(match.group(1))
		match = re.search(r"\-([RL]*)\]", csv_path)
		newscheme = match.group(1)

		self.setmode(newmode, newscheme)
		self.clear()
		running = False

		with open(csv_path, 'rb') as csvfile:
			csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			self.loadlist = list(csv_reader)
			self.loadlist.sort(key=lambda x: int(x[3]))

		for row in self.loadlist:
			#Loading only ants that are due to appear at step 0
			if row[3] == '0':
				x = int(row[0])
				y = int(row[1])
				direction = int(row[2])
				if self.mode == 1:
					#Langton Mode
					ant = ClassicAnt(self, len(self.ants) + 1, int(x), int(y), direction)
				elif self.mode == 2:
					#Turk-Propp Mode
					ant = ClassicAnt(self, len(self.ants) + 1, int(x), int(y), direction)
				elif self.mode == 0:
					#Free4All Mode
					ant = Free4AllAnt(self, len(self.ants) + 1, int(x), int(y), 1 + len(self.ants) % (len(self.colors) - 1), direction)

		#Removing previously loaded ants from the load list
		for row in self.loadlist[:]:
			if row[3] == '0':
				self.loadlist.remove(row)


	# Increments the color of a pixel
	# For Classic ants
	def incrementcolor(self, x, y):

		if self.rows[y][x] == "X":
			self.rows[y][x] = 0

		self.rows[y][x] = (self.rows[y][x] + 1)  % len(self.scheme)
		self.screen.set_at((x, y), pygame.Color(self.colors[self.rows[y][x] % len(self.colors)]))

	# Swaps grid pixels from black to color or from color to black
	# For Free4All ants
	def colorswap(self, x, y, ant_id, color_id):

		if self.rows[y][x] == "X":
			self.rows[y][x] = ant_id
			self.screen.set_at((x, y), pygame.Color(self.colors[color_id]))
			self.ants_couters[ant_id] += 1
		elif self.rows[y][x] == 0:
			self.rows[y][x] = ant_id
			self.screen.set_at((x, y), pygame.Color(self.colors[color_id]))
			self.ants_couters[ant_id] += 1
		else:
			self.ants_couters[self.rows[y][x]] -= 1
			self.rows[y][x] = 0
			self.screen.set_at((x, y), (0, 0, 0))

	# Stats area static labels and vertical line
	def statslabels(self):

		font = pygame.font.SysFont("monospace", 15)

		txt = font.render("MODE", True, (255, 255, 255))
		self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 0)))
		self.screen.blit(txt, (self.width + 2, 0))
		txt = font.render("%s" %self.modenames[self.mode], True, (255, 255, 255))
		self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 16)))
		self.screen.blit(txt, (self.width + 2, 16))

		font = pygame.font.SysFont("monospace", 13)
		txt = font.render("%s                " %self.scheme, True, (255, 255, 255))
		self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 32)))
		self.screen.blit(txt, (self.width + 2, 32))

		font = pygame.font.SysFont("monospace", 15)
		txt = font.render("Speed", True, (255, 255, 255))
		self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 64)))
		self.screen.blit(txt, (self.width + 2, 64))
		txt = font.render("Steps", True, (255, 255, 255))
		self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 96)))
		self.screen.blit(txt, (self.width + 2, 96))
		txt = font.render("Ants", True, (255, 255, 255))
		self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 128)))
		self.screen.blit(txt, (self.width + 2, 128))

		if self.mode == 0:
			txt = font.render("SCORES", True, (255, 255, 255))
			self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 208)))
			self.screen.blit(txt, (self.width + 2, 208))

		pygame.draw.line(self.screen, (255, 255, 255), (self.width, 0), (self.width, self.height))

	# Update stats data
	def updatestats(self):

		font = pygame.font.SysFont("monospace", 15)

		txt = font.render("%s" %'{:,}'.format(self.total_steps).replace(',', ' '), True, (255, 255, 255))
		self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 112)))
		self.screen.blit(txt, (self.width + 2, 112))
		txt = font.render("%i" %len(self.ants), True, (255, 255, 255))
		self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 144)))
		self.screen.blit(txt, (self.width + 2, 144))

		if self.mode == 0:
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
					self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 224)))
					self.screen.blit(txt, (self.width + 2, 224))
				if len(self.ants) > 1:
					txt = font.render("%i  " %self.ants_couters[Score2], True, (self.ants[Score2-1].rgb_color))
					self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 240)))
					self.screen.blit(txt, (self.width + 2, 240))
				if len(self.ants) > 2:
					txt = font.render("%i  " %self.ants_couters[Score3], True, (self.ants[Score3-1].rgb_color))
					self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 256)))
					self.screen.blit(txt, (self.width + 2, 256))

	#Update speed in stats, only when speed changes
	def updatespeed(self):

		font = pygame.font.SysFont("monospace", 15)

		txt = font.render("%ix  " %self.frame_skip, True, (255, 255, 255))
		self.screen.fill((0,0,0), rect=txt.get_rect(topleft=(self.width + 2, 80)))
		self.screen.blit(txt, (self.width + 2, 80))

	def get(self, x, y):

		return self.rows[y][x]

#Classic ant moving and evolving according to the AntGrid's moving scheme
class ClassicAnt(object):

	directions = ((0,-1), (+1,0), (0,+1), (-1,0))

	def __init__(self, grid, ant_id, x, y, direction):

		self.grid = grid
		self.ant_id = ant_id
		self.x = x
		self.y = y
		self.direction = direction
		self.grid.nb_ants += 1

		self.grid.ants.append(self)
		self.grid.ants_couters.append(0)

		self.starting_params = (x, y, direction, self.grid.total_steps)

	def move(self):

		if self.grid.rows[self.y][self.x] == "X":
			if self.grid.scheme[0] == "L":
				self.direction = (self.direction-1) % 4
			elif self.grid.scheme[0] == "R":
				self.direction = (self.direction+1) % 4
		else:
			if self.grid.scheme[self.grid.rows[self.y][self.x]] == "L":
				self.direction = (self.direction-1) % 4
			elif self.grid.scheme[self.grid.rows[self.y][self.x]] == "R":
				self.direction = (self.direction+1) % 4

		self.grid.incrementcolor(self.x, self.y)

		self.x = ( self.x + self.directions[self.direction][0] ) % self.grid.width
		self.y = ( self.y + self.directions[self.direction][1] ) % self.grid.height

#Ant considering only 2 colors: Black or not black
class Free4AllAnt(object):

	directions = ((0,-1), (+1,0), (0,+1), (-1,0))

	def __init__(self, grid, ant_id, x, y, color_id, direction):

		self.grid = grid
		self.ant_id = ant_id
		self.color_id = color_id
		self.x = x
		self.y = y
		self.color = pygame.Color(self.grid.colors[color_id])
		self.rgb_color = globalfunctions.hex_to_rgb(self.grid.colors[self.color_id])
		self.direction = direction
		self.grid.nb_ants += 1

		self.grid.ants.append(self)
		self.grid.ants_couters.append(0)
		self.grid.colorswap(self.x, self.y, self.ant_id, self.color_id)

		self.starting_params = (x, y, direction, self.grid.total_steps)

	def move(self):

		self.grid.colorswap(self.x, self.y, self.ant_id, self.color_id)

		self.x = ( self.x + self.directions[self.direction][0] ) % self.grid.width
		self.y = ( self.y + self.directions[self.direction][1] ) % self.grid.height

		if self.grid.get(self.x, self.y) == "X" or self.grid.get(self.x, self.y) == 0:
			self.direction = (self.direction-1) % 4
		else:
			self.direction = (self.direction+1) % 4

#Free4All ant that changes color every 1000 steps
class RainbowAnt(object):

	directions = ((0,-1), (+1,0), (0,+1), (-1,0))

	def __init__(self, grid, ant_id, x, y, color_id, direction):

		self.grid = grid
		self.ant_id = ant_id
		self.color_id = color_id
		self.x = x
		self.y = y
		self.color = pygame.Color(self.grid.colors[color_id])
		self.rgb_color = globalfunctions.hex_to_rgb(self.grid.colors[color_id])
		self.direction = direction
		self.grid.nb_ants += 1
		self.grid.rainbow = True

		self.grid.ants.append(self)
		self.grid.ants_couters.append(0)
		self.grid.colorswap(self.x, self.y, self.ant_id, self.color_id)

		self.starting_params = (x, y, direction, self.grid.total_steps)

	def move(self):

		new_color_id = 1 + self.grid.total_steps / 1000 % (len(self.grid.colors) - 1)
		new_color = self.grid.colors[new_color_id]
		self.color = pygame.Color(new_color)
		self.rgb_color = globalfunctions.hex_to_rgb(new_color)
		self.grid.colorswap(self.x, self.y, self.ant_id, new_color_id)

		self.x = ( self.x + self.directions[self.direction][0] ) % self.grid.width
		self.y = ( self.y + self.directions[self.direction][1] ) % self.grid.height

		if self.grid.get(self.x, self.y) == "X" or self.grid.get(self.x, self.y) == 0:
			self.direction = (self.direction-1) % 4
		else:
			self.direction = (self.direction+1) % 4
