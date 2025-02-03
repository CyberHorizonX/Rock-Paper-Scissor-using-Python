import time
import random
import curses
from threading import Thread, Event
import os

choices_art = {
    "r": ["    _______", "---'   ____)", "      (_____)", "      (_____)", "      (____)", "---.__(___)"],
    "p": ["     _______", "---'    ____)____", "           ______)", "          _______)", "         _______)", "---.__________)"],
    "s": ["    _______", "---'   ____)____", "          ______)", "       __________)", "      (____)", "---.__(___)"]
}

player_stats = {"wins": 0, "losses": 0, "draws": 0}

def play_sound(frequency=500, duration=200):
    # Cross-platform solution (no actual sound here, but could use a package like `pygame` or `playsound`)
    if os.name == 'nt':  # Windows
        import winsound
        winsound.Beep(frequency, duration)
    else:
        # Placeholder for non-Windows platforms
        pass

def point(you, com):
    if you == com:
        return -1
    if (you == 'r' and com == 's') or (you == 'p' and com == 'r') or (you == 's' and com == 'p'):
        return 1
    return 0

def countdown_timer(stdscr, timeout=5):
    for i in range(timeout, 0, -1):
        stdscr.addstr(5, 10, f"Time left: {i}s", curses.A_BOLD)
        stdscr.refresh()
        time.sleep(1)
    stdscr.addstr(5, 10, " " * 20)
    stdscr.refresh()

def display_choice(stdscr, choice, row, label, color_pair):
    stdscr.addstr(row, 5, label, curses.A_BOLD | color_pair)
    for i, line in enumerate(choices_art[choice]):
        stdscr.addstr(row + i + 1, 5, line, color_pair)
    stdscr.refresh()
    time.sleep(1.5)

def play_again(stdscr):
    stdscr.addstr(12, 10, "Play again? (y/n): ", curses.A_BOLD | curses.color_pair(3))
    stdscr.refresh()
    choice = stdscr.getkey().strip().lower()
    return choice == 'y'

def title_screen(stdscr):
    stdscr.clear()
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.addstr(5, 10, "⚡ WELCOME TO ROCK-PAPER-SCISSORS ⚡", curses.A_BOLD | curses.color_pair(4))
    stdscr.addstr(7, 10, "Rock - r | Paper - p | Scissors - s | Quit - q", curses.A_BOLD)
    stdscr.addstr(9, 10, "Press any key to start...", curses.A_BOLD | curses.color_pair(3))
    stdscr.addstr(11, 10, "Let's Begin!", curses.A_BOLD | curses.color_pair(4))
    stdscr.refresh()
    stdscr.getch()

def get_input(stdscr, event):
    try:
        key = stdscr.getkey().strip().lower()
        event.set()
        return key
    except:
        event.set()
        return 'timeout'

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    title_screen(stdscr)
    
    while True:
        stdscr.clear()
        stdscr.refresh()
        player_score, computer_score = 0, 0
        
        for i in range(1, 4):
            stdscr.clear()
            stdscr.addstr(2, 10, f"Round {i}", curses.A_BOLD | curses.color_pair(4))
            stdscr.refresh()
            
            countdown_timer(stdscr, 3)
            
            stdscr.addstr(6, 5, "Your turn (5s to choose): ", curses.A_BOLD)
            stdscr.refresh()
            
            event = Event()
            input_thread = Thread(target=get_input, args=(stdscr, event))
            input_thread.start()
            input_thread.join(5)  # Wait for 5 seconds for input
            
            if not event.is_set():
                stdscr.addstr(7, 5, "Timeout! You lose this round.", curses.A_BOLD | curses.color_pair(2))
                computer_score += 1
                stdscr.refresh()
                time.sleep(1.5)
                continue
            
            # Fix: Capture the return value of get_input()
            you = get_input(stdscr, event)
            
            if you == 'q':
                return
            elif you not in ['p', 'r', 's']:
                stdscr.addstr(7, 5, "Invalid choice! You lose this round.", curses.A_BOLD | curses.color_pair(2))
                computer_score += 1
                stdscr.refresh()
                time.sleep(1.5)
                continue
            
            com = random.choice(['p', 'r', 's'])
            
            stdscr.clear()
            display_choice(stdscr, you, 5, "You chose:", curses.color_pair(1))
            display_choice(stdscr, com, 15, "Computer chose:", curses.color_pair(2))
            
            result = point(you, com)
            if result == 1:
                player_score += 1
                player_stats["wins"] += 1
                play_sound(700, 300)
            elif result == -1:
                player_stats["draws"] += 1
                play_sound(500, 300)
            else:
                computer_score += 1
                player_stats["losses"] += 1
                play_sound(300, 300)
            
            stdscr.addstr(22, 5, f"Round {i} Score: Your Score = {player_score} | Computer Score = {computer_score}", curses.A_BOLD | curses.color_pair(3))
            stdscr.refresh()
            time.sleep(2)
        
        stdscr.clear()
        stdscr.addstr(5, 10, f"Final Score: Your Score = {player_score} | Computer Score = {computer_score}", curses.A_BOLD | curses.color_pair(3))
        
        if player_score > computer_score:
            stdscr.addstr(7, 10, "🎉 You Won! 🎉", curses.A_BOLD | curses.color_pair(1))
        elif player_score == computer_score:
            stdscr.addstr(7, 10, "🤝 Match DRAW 🤝", curses.A_BOLD | curses.color_pair(3))
        else:
            stdscr.addstr(7, 10, "😢 You Lose 😢", curses.A_BOLD | curses.color_pair(2))
        
        stdscr.addstr(9, 10, f"Wins: {player_stats['wins']} | Losses: {player_stats['losses']} | Draws: {player_stats['draws']}", curses.A_BOLD | curses.color_pair(4))
        stdscr.refresh()
        time.sleep(3)
        
        # Fix: Ensure play_again prompt is visible
        stdscr.clear()
        if not play_again(stdscr):
            break


if __name__ == "__main__":
    curses.wrapper(main)