# ZOO

## Description
 The program makes a simulation of a nature. It prints out grid which represents world. It cointains Animals, Plants and Human, which all inherit after Organism class. Each organism makes a move each turn. The order of moves is based on initiative attribute, excpet for Human as it is controlled with arrows. If organism moves to an occoupied gird cell then fight or breed will hapen. If there are two different species on one grid cell, then one must kill the other and the winner stays on the cell. The strength attribute and overriden colision function decide on who wins. If on the grid are the same species, then they will breed. The Organism that made a move goes back to previous cell and the child is put on the closest cell to its parents. Plants don't move or breed but the sow. Human also has a special ability which can be used every couple turns. It increases strength of human to 10 and is decreased each turn by 1 until it goes back to previous value. The state of grid can be saved (in txt file) and loaded.

## Stack 
 - Python with PySide6 for GUI

## Instruction
 Run `main.py` file in main folder.
