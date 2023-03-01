# Monster-Search-Demonstration
IN ORDER TO RUN THE PROGRAM IT IS NECESSARY THAT BOTH THE PATHFINDINGAI.PY AND PATHFINDINGMAP.TXT FILES ARE IN THE SAME FOLDER.

This project is a small demonstration of an algorithm that I worked hard on. The "game" is quite simple, there is a player and a monster who are both placed in a confined area, the monster will continuously chase the player until they are on top of each other where it will then stop.

 The map which the player and monster are put into can be modified by changing the values of a 0 to a 1 or vice versa in the pathfindingmap.txt file. It is imperative that no extra spaces or values be entered. Map size and generation are augmentable as defined in the first few functions.

The algorithm takes obstacles into account during its search in order to find the most efficient path to reach the player, the speed at which the monster moves can be modified by increasing or decreasing the second input to the function called on line 216.

CONTROLS:

q - Close the window

w - Up

a - Left

s - Down

d - Right
