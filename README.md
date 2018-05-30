# Langtons-Ants Simulator
By Marc Thibeault & Josaphat Comeau

Looking for the best Lanton's Ants Simulator out there? You just found it.

Made with Python and Pygame, this simulator is basically the Langton Ant fan's wet dream.

You can run classic Langton simulations using the RL movement scheme, or more advanced ones using custom moving schemes as imagined by Greg Turk and Jim Propp. You can also run a Free for All simulation in which infinite chaos is very likely to ensue.

Simulations can be saved and loaded for infinite tests and replays.

It's undergoing constant development, so new exciting and interesting features are being implemented every now and then.

###Screenshots
[Click here for screenshots](https://www.dropbox.com/sh/hlra0uyvo84o3kz/AADYIAuVAB63eimGCZBkFEKsa?dl=0 "Langton's Ants Simulator Screenshots | Dropbox")

###Requirements
* Install [Python 3.6](https://www.python.org/downloads/)
* Install [Pygame 1.9](http://pygame.org/download.shtml)

### How to run
* Run ants.py with Python from command prompt

Modes and controls are explained below, as well as how to save and load simulations.
##Modes
### 1. Classic Langton Mode
* Press 1 for Classic Langton Mode: One ant using the RL movement scheme. You can add your own ants at anytime by left clicking in the simulation.

### 2. Turk-Propp Mode
* Press 2 for Turk-Propp Mode: One ant using a custom movement scheme typed by the user. You can add your own ants at anytime by left clicking in the simulation.
* Using the L, R and Backspace  keys, input movement scheme. Exemple: RRLL. Must be at least 2 characters long.
* Clearing the simulation doesn't clear the moving scheme. You can modify it as long as you didn't start a new simulation.

### 0. Free4All mode
* Press 0 for Free4All mode in which you add your ants manually in the simulation. Ants use the RL scheme and each of them has a color and score. You can add new ants at anytime by left clicking in the simulation.

 ## Controls
* Press 1-2-0 keys to select mode
* In Turk-Propp Mode, press R, L, Backspace to input your moving scheme before starting the simulation.
* Press space bar to start / pause the simulation
* Left click the simulation to add new ants
* Press + / - to adjust speed
* Press S to save the simulation to a CSV file (See naming convetion below)
* Press D to load a previously saved CSV file
* Press C to clear the simulation
* Press F11 to toggle fullscreen/windowed mode
* Press Escape to quit the simulator

## Saving and Loading Simulations
At any time you can save a simulation by pressing the S key or load a saved simulation pressing the D key. Saved simulations are located in the /save folder. Here's the naming convention for the saves:

`[MODE-SCHEME](#ANTS) DATE TIME.csv`

`Exemple: [0-RL](7) 2016-02-07 21.31.28.csv` (That's a Langton Mode simulation using the RL scheme with 7 ants)

When loading a simulation, the program will automatically switch to the proper mode and will load all ants as expected. To be clear, ants that were there at the beginning of the simulation will load at first, then all the ants that were created while the simulation was running are going to automatically show up at the expected time and location.

Have fun!
