# Langtons-Ants on Steriods
By Marc Thibeault & Josaphat Comeau

Made using Python + pygame. 
### How to run
* Run ants.py with Python from command prompt
* Requires Python 2.7 + pygame 1.9

As of January 2016 it has 3 modes as explained below. 
#Modes and Controls
Each mode has a few specific controls as follows.
### 1. Classic Langton Mode
* Press 1 for Classic Langton Mode: One ant using the LR movement scheme. There's not much more to it. 
 * Press space bar to start / pause the simulation
 * Press + / - to adjust speed
 * Press C to reset the simulation

### 2. Turk-Propp Mode
* Press 2 for Turk-Propp Mode: One ant using a custom movement scheme type by the user. 
* Using the L and R keys, input movement scheme. Exemple: RRLL. Must be at least 2 characters long. 
 * Press space bar to start / pause the simulation
 * Press + / - to adjust speed
 * Press C to reset the simulation

### 3. Free4All mode
* Press 0 for Free4All mode in which you add your ants manually in the simulation. Ants use the LR scheme and each of them has a color. 
 * Left click to create ants
 * Left click to create rainbow ants (!)
 * Press space bar to start
 * Press S to save your starting ant positions to a CSV file. 
 * Press D to load a previously saved CSV file. 
 * Press C to reset the simulation
