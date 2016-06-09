# tron-curses
Final project for CSE 190: Robotics.

## Code Overview

`constants.py` contains various constant configuration values that are used throughout the program.

`controllers.py` contains implementations for two ways to control the bike: via AI (MDP) or keyboard keys.

`game.py` contains the main game logic, which is a thread with a run loop controlled by states.

`game_exceptions.py` contains a game-related exception that can be thrown.

`graphics.py` contains the graphical interface of the game, supported by the curses library.

`mdp_bot.py` contains our implementation of an AI player that uses MDP to guide its movements.

`player.py` contains a representation of the Player object and state.

`tron` is the game executable, handling command line arguments and starting the game.
