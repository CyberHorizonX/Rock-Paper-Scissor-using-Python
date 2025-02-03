# Rock-Paper-Scissors Game Documentation

This documentation provides a comprehensive overview of the Rock-Paper-Scissors game implemented in Python using the `curses` library for terminal handling and user interaction. The game allows a player to compete against a computer in a series of rounds.

## Table of Contents

1. [Overview](#overview)
2. [Imports](#imports)
3. [Global Variables](#global-variables)
4. [Functions](#functions)
   - [play_sound](#play_sound)
   - [point](#point)
   - [countdown_timer](#countdown_timer)
   - [display_choice](#display_choice)
   - [play_again](#play_again)
   - [title_screen](#title_screen)
   - [get_input](#get_input)
   - [main](#main)
5. [Execution](#execution)

## Overview

The Rock-Paper-Scissors game allows the player to choose one of three options: Rock (`r`), Paper (`p`), or Scissors (`s`). The computer randomly selects one of these options as well. The game consists of three rounds, and the player with the most wins at the end of the rounds is declared the winner. The game also includes sound effects for winning, losing, and drawing, as well as a countdown timer for the player's turn. At the end of the game, players have the option to play again or exit.

## Imports

```python
import time
import random
import curses
from threading import Thread, Event
import os
```

- `time`: Provides time-related functions, such as sleeping for a specified duration.
- `random`: Used to generate random choices for the computer's turn.
- `curses`: For creating text user interfaces in the terminal.
- `Thread` and `Event` from `threading`: For handling concurrent input while the countdown timer is running.
- `os`: Used to check the operating system for sound playback.

## Global Variables

```python
choices_art = { ... }
player_stats = {"wins": 0, "losses": 0, "draws": 0}
```

- `choices_art`: A dictionary containing the ASCII art representations of Rock, Paper, and Scissors.
- `player_stats`: A dictionary to keep track of the player's wins, losses, and draws.

## Functions

### play_sound

```python
def play_sound(frequency=500, duration=200):
```

Plays a sound using the system's beep functionality. This function is platform-dependent:
- On Windows, it uses the `winsound` module to generate a beep sound.
- On non-Windows platforms, the function does nothing but can be extended to use another sound library.

#### Parameters:
- `frequency`: The frequency of the beep sound (default is 500 Hz).
- `duration`: Duration of the beep in milliseconds (default is 200 ms).

---

### point

```python
def point(you, com):
```

Determines the outcome of a round based on the player's choice and the computer's choice.

#### Parameters:
- `you`: The player's choice (`'r'`, `'p'`, or `'s'`).
- `com`: The computer's choice (`'r'`, `'p'`, or `'s'`).

#### Returns:
- `-1`: If the round is a draw.
- `1`: If the player wins.
- `0`: If the computer wins.

---

### countdown_timer

```python
def countdown_timer(stdscr, timeout=5):
```

Displays a countdown timer on the terminal for the player's turn.

#### Parameters:
- `stdscr`: The standard screen object for drawing in the terminal.
- `timeout`: The number of seconds for the countdown (default is 5 seconds).

---

### display_choice

```python
def display_choice(stdscr, choice, row, label, color_pair):
```

Displays the player's or computer's choice along with the corresponding ASCII art.

#### Parameters:
- `stdscr`: The standard screen object.
- `choice`: The choice to display (`'r'`, `'p'`, or `'s'`).
- `row`: The starting row for displaying the choice.
- `label`: The label to show above the choice.
- `color_pair`: The color pair to use for text formatting.

---

### play_again

```python
def play_again(stdscr):
```

Prompts the player to decide if they want to play another game.

#### Parameters:
- `stdscr`: The standard screen object.

#### Returns:
- `True`: If the player chooses to play again.
- `False`: If the player chooses not to play again.

---

### title_screen

```python
def title_screen(stdscr):
```

Displays the welcome screen and instructions for the game.

#### Parameters:
- `stdscr`: The standard screen object.

---

### get_input

```python
def get_input(stdscr, event):
```

Handles input from the player, allowing it to be processed in a separate thread.

#### Parameters:
- `stdscr`: The standard screen object.
- `event`: An event object used to signal when input is received.

#### Returns:
- The key pressed by the player or `'timeout'` if no key was pressed within the allowed time.

---

### main

```python
def main(stdscr):
```

The main function that initializes the game, manages the game loop, and coordinates the gameplay.

#### Parameters:
- `stdscr`: The standard screen object.

- Initializes color schemes for visual feedback.
- Calls `title_screen` to display the welcome message.
- Manages the game loop for three rounds, handling player inputs, game logic, score tracking, and sound effects.
- Displays the final results and prompts the player to play again.

---

## Execution

To run the game, execute the script in a terminal that supports `curses`. The entry point of the game is defined in the `if __name__ == "__main__":` block, which calls `curses.wrapper(main)` to start the game safely within the `curses` environment.

```python
if __name__ == "__main__":
    curses.wrapper(main)
```

This setup ensures that the terminal is properly initialized and restored after the game ends.
