# Dots-boxes-Team_S-Y
    members- Saurabh and Yash Raythatha

# Game description
Dots and Boxes is a classic pencil-and-paper game played by two players. Here's how it works:
    1- Setting Up: Start by drawing a grid of dots. The size of the grid can vary, but a common grid is 5x5 or 6x6 dots.
    2- Gameplay: Players take turns connecting two adjacent dots with a line. If a player completes the fourth side of a 1x1 square, they "capture" that square by writing their initial inside it and get an extra turn.
    3- Goal: The goal of the game is to capture more squares than your opponent. The game ends when all dots are connected and all possible squares are captured.
    4- Winning: The player with the most captured squares at the end of the game wins.

## Features

- Interactive graphical user interface.
- Adjustable AI difficulty through Monte Carlo Tree Search.
- Customizable settings for different levels of gameplay challenge.

# Installation

To run this game, you will need Python and Pygame installed on your system.

- Python 3.6 or higher
- Pygame

You can install Pygame using pip:
pip install pygame

# Configuration
Adjust the AI's difficulty by changing the BRAIN_POWER value in the Game.py file:

-0.1 for Beginner
-0.4 for Intermediate
-1.0 for Hard
-2.0 for Pro

# How to run the Game:-
- go to terminal 
- run python game.py
- scores will be generated in the terminal when the game is terminated.

# Project files 

DBNode.py - a class for a Dots and Boxes Node used in MCTS

DotsAndBoxes.py - a class for a game of Dots and Boxes.

Game.py - driver for game intended for AI vs Human. Note that at the start of the file, BRAIN_POWER can be adjusted to change the time given to the computer to think. 0.4 is default value. It is simply a multiplier for the number of rollouts used in a game.

MCTS.py - Driver for the Monte Carlo Tree Search Algorithm. Contains all relevant functions to execute the algorithm with a game of Dots and Boxes.

fonts - fonts for the game.

README.md - Description of the project.

