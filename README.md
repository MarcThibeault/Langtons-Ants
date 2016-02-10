# Langtons-Ants on Steriods
By Marc Thibeault & Josaphat Comeau

Made using Python + pygame. 
###Requirements
* Python 2.7
* Pygame 1.9

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
* Press S to save your starting ant positions to a CSV file (See naming convetion below)
* Press D to load a previously saved CSV file
* Press C to clear the simulation

## Saving and Loading Simulations
At any time you can save a simulation by pressing the S key or load a saved simulation pressing the D key. Saved simulations are located in the /save folder. Here's the naming convention for the saves:

`[MODE-SCHEME](#ANTS) DATE TIME.csv`

`Exemple: [0-RL](7) 2016-02-07 21.31.28.csv` (That's a Langton Mode simulation using the RL scheme with 7 ants)

When loading a simulation, the program will automatically switch to the proper mode and will load all ants as expected. To be clear, ants that were there at the beginning of the simulation will load at first, then all the ants that were created while the simulation was running are going to automatically show up at the expected time and location. 

Have fun! 
