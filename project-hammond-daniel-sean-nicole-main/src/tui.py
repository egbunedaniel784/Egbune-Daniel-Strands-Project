"""
Theses links are what helped me do this code and also for me to look back on just in case I forget
https://docs.python.org/3/library/termios.html
https://www.geeksforgeeks.org/python-sys-module/
https://www.youtube.com/watch?v=oHZjjcxgY6U&ab_channel=LukeMay

"""

from base import StrandsGameBase, Step
from strands import StrandsGame, Strand, Pos
from art_tui import ArtTUIPolkaDots
from art_tui import ArtTUIWrappers
import sys
import termios
import tty
import click
import random
import os

class TUI:
    def __init__(self, mode: str, game_file: str, hint_threshold: int = 3, art_frame: str = None):
        self.game: StrandsGameBase = StrandsGame(game_file, hint_threshold)
        
        supported_frames = ["cat0", "cat1", "wrappers"]
        if art_frame:
            try:
                if art_frame == "cat1":
                    
                    self.art = ArtTUIPolkaDots(frame_width=2, interior_width=20)
                elif art_frame == "wrappers" or art_frame == "cat0":
                    
                    self.art = ArtTUIWrappers(num_wrappers=2, interior_width=20, height=8)
                else:
                    print(f"Art frame '{art_frame}' is not supported in TUI. TUI only Supports: {', '.join(supported_frames)}")
                    sys.exit(1)
            except ImportError:
                
                sys.exit(1)
        else:
            
            self.art = ArtTUIPolkaDots(frame_width=2, interior_width=20) # This just make the thing look better cause the default is not vering good looking. ArtTUD looks so bad D:::::
        
        self.letter_color = "\033[94m"  # Blue for found strands
        self.current_color = "\033[93m"  # Yellow for current selection
        self.hint_color = "\033[92m"    # Green for hints
        self.cursor_color = "\033[91m"  # Red for cursor
        self.rest_of_the_board = "\033[0m"  # Reset color
        
        self.mode = mode
        self.cursor_pos = Pos(0, 0)  # this tracks the cursor position
        self.strand_on_currently = None   # this track current selection
        self.current_positions = []  # this track the positions in current selection
        self.last_message = ""  # Store the last result message
        
        if mode == "show":
            self.show_all_answers()
            self.run_show_mode()
        else:
            self.run_play_mode()
    
    def show_all_answers(self) -> None:
        for word, strand in self.game.answers():
            self.game.submit_strand(strand)
    
    def run_show_mode(self) -> None:
        while True:
            print("\033[H\033[2J\033[3J", end="", flush=True)
            self.show_board()
            key = self.get_key()
            if key == 'q':
                break
    
    def run_play_mode(self) -> None:
        while True:
            print("\033[H\033[2J\033[3J", end="", flush=True)
            self.show_board()
            key = self.get_key()
            self.handle_key(key)
    
    def handle_key(self, key: str) -> None:
        if key == 'q':
            sys.exit(0)
        if len(self.game.found_strands()) == len(self.game.answers()):
            return
        elif key == 'h':
            result = self.game.use_hint()
            if isinstance(result, tuple):
                self.last_message = f"Hint shown for word: {self.game.answers()[result[0]][0]}"
            else:
                self.last_message = str(result)
        elif key == '\x1b':
            self.clear_current_selection()
        elif key == '\r' or key == '\n':
            if self.strand_on_currently:
                self.submit_current_strand()
            else:
                self.start_current_selection()
        elif key in ['w', 'a', 's', 'd', 'i', 'j', 'k', 'l']:
            self.move_cursor(key)
    
    def move_cursor(self, key: str) -> None:
        step_map = {
            'w': Step.N,  # Up
            'a': Step.W,  # Left
            's': Step.S,  # Down
            'd': Step.E,  # Right
            'i': Step.NW, # Northwest
            'j': Step.SW, # Southwest
            'k': Step.SE, # Southeast
            'l': Step.NE  # Northeast
        }
        
        if key in step_map:
            new_pos = self.cursor_pos.take_step(step_map[key])
            if (0 <= new_pos.r < self.game.board().num_rows() and 
                0 <= new_pos.c < self.game.board().num_cols()):
                self.cursor_pos = new_pos
                if self.strand_on_currently:
                    self.extend_current_selection(step_map[key])
    
    def is_valid_position(self, pos: Pos) -> bool:
        return (0 <= pos.r < self.game.board().num_rows() and 
                0 <= pos.c < self.game.board().num_cols())
    
    def start_current_selection(self) -> None:
        self.strand_on_currently = Strand(self.cursor_pos, [])
        self.current_positions = [self.cursor_pos]
    
    def extend_current_selection(self, step: Step) -> None:
        if not self.strand_on_currently:
            return
        
        new_pos = self.cursor_pos
        if not self.is_valid_position(new_pos):
            return
        
        if new_pos in self.current_positions:
            idx = self.current_positions.index(new_pos)
            self.current_positions = self.current_positions[:idx+1]
            steps = []
            for i in range(len(self.current_positions)-1):
                try:
                    step = self.current_positions[i].step_to(self.current_positions[i+1])
                    steps.append(step)
                except ValueError:
                    continue
            self.strand_on_currently = Strand(self.current_positions[0], steps)
        else:
            self.current_positions.append(new_pos)
            if len(self.current_positions) > 1:
                step = self.current_positions[-2].step_to(self.current_positions[-1])
                self.strand_on_currently.steps.append(step)
    
    def clear_current_selection(self) -> None:
        self.strand_on_currently = None
        self.current_positions = []
    
    def submit_current_strand(self) -> None:
        if self.strand_on_currently:
            result = self.game.submit_strand(self.strand_on_currently)
            if isinstance(result, tuple) and result[1]:
                self.last_message = f"Word found: {result[0]}"
            elif result == "Too short":
                self.last_message = "\033[91mToo short(3-4 min)\033[0m"
            elif result == "Not a theme word":
                self.last_message = "\033[91mNot a theme word! \033[0m"
            elif result == "Already found":
                self.last_message = "\033[93mAlready found!    \033[0m"
            else:
                self.last_message = f"\033[91m{result}\033[0m"
            self.clear_current_selection()
    
    def show_board(self) -> None:
        self.art.print_top_edge()
        board = self.game.board()
        cell_width = 3  
        row_width = board.num_cols() * cell_width + (board.num_cols() - 1) * 3  
        total_width = max(20, row_width)
        if self.last_message:
            message_content_width = self.art.interior_width - 2 # Subtract 2 for the left and right vertical borders

            # Top of the message box
            self.art.print_left_bar()
            print(f"\033[96m╔{'═' * message_content_width}╗\033[0m", end="")
            self.art.print_right_bar()

            # Message line
            self.art.print_left_bar()
            print(f"\033[96m║{self.last_message.center(message_content_width)}║\033[0m", end="")
            self.art.print_right_bar()

            # Bottom of the message box
            self.art.print_left_bar()
            print(f"\033[96m╚{'═' * message_content_width}╝\033[0m", end="")
            self.art.print_right_bar()
        
        self.art.print_left_bar()
        theme_text = f"Theme: {self.game.theme()}"
        box_width = total_width
        print(f"\033[91m{'═' * box_width}\033[0m")
        print(f"\033[91m{theme_text.center(box_width)} \033[0m")
        print(f"\033[91m{'═' * box_width}\033[0m")
        self.art.print_right_bar()
        found_positions = set()
        for strand in self.game.found_strands():
            found_positions.update((pos.r, pos.c) for pos in strand.positions())
        current_positions = set()
        if self.strand_on_currently:
            current_positions.update((pos.r, pos.c) for pos in self.strand_on_currently.positions())
        hint_positions = set()
        hint = self.game.active_hint()
        if hint:
            index, show_letters = hint
            word, strand = self.game.answers()[index]
            if show_letters:
                positions = strand.positions()
                hint_positions.add((positions[0].r, positions[0].c))
                hint_positions.add((positions[-1].r, positions[-1].c))
            else:
                hint_positions.update((pos.r, pos.c) for pos in strand.positions())
        for row in range(board.num_rows()):
            self.art.print_left_bar()
            for col in range(board.num_cols()):
                pos = Pos(row, col)
                letter = board.get_letter(pos)
                if (row, col) == (self.cursor_pos.r, self.cursor_pos.c):
                    print(f"{self.cursor_color}{letter}{self.rest_of_the_board}  ", end="")
                elif (row, col) in hint_positions:
                    print(f"{self.hint_color}{letter}{self.rest_of_the_board}  ", end="")
                elif (row, col) in current_positions:
                    print(f"{self.current_color}{letter}{self.rest_of_the_board}  ", end="")
                elif (row, col) in found_positions:
                    print(f"{self.letter_color}{letter}{self.rest_of_the_board}  ", end="")
                else:
                    print(f"{letter}  ", end="")
                if col < board.num_cols() - 1:
                    if self.should_draw_connection(row, col, row, col + 1):
                        print(" ━ ", end="")
                    else:
                        print("   ", end="")
            print(" " * (total_width - row_width), end="")
            self.art.print_right_bar()
            if row < board.num_rows() - 1:
                self.art.print_left_bar()
                for col in range(board.num_cols()):
                   
                    if col < board.num_cols() - 1:
                        
                        if self.should_draw_connection(row, col, row + 1, col + 1):
                            print("  ╲", end="")
                        else:
                            print("   ", end="")
                        #
                        if self.should_draw_connection(row, col + 1, row + 1, col):
                            print("╱  ", end="")
                        else:
                            print("   ", end="")
                    else:
                        print("   ", end="")
                print(" " * (total_width - row_width), end="")
                self.art.print_right_bar()
                self.art.print_left_bar()
                for col in range(board.num_cols()):
                    if self.should_draw_connection(row, col, row + 1, col):
                        print("┃  ", end="")
                    else:
                        print("   ", end="")
                    if col < board.num_cols() - 1:
                        print("   ", end="")
                print(" " * (total_width - row_width), end="")
                self.art.print_right_bar()
                if row < board.num_rows() - 1:
                    self.art.print_left_bar()

                    self.art.print_right_bar()
                    print()
        self.art.print_bottom_edge()
        stats = f"\033[1;94mFound: {len(self.game.found_strands())}/{len(self.game.answers())} words\033[0m"
        if self.strand_on_currently:
            selection_length = len(self.strand_on_currently.positions())
            letters = [board.get_letter(pos) for pos in self.strand_on_currently.positions()]
            letter_sequence = "-".join(letters)
            stats += f" | Current Selection: {selection_length} letters ({letter_sequence})"
        print(stats.ljust(total_width))
        if self.last_message:
            print(self.last_message.ljust(total_width))
        if len(self.game.found_strands()) == len(self.game.answers()):
            self.words(False)
        self.words(True)

    def words(self, bool: bool) -> None:
        if bool:
            print("\nHow to Play:")
            print("1. Move cursor using WASD (up (W), down(S), left (A), right (D),) or IJKL (northwest (I), southwest (J), southeast (K), northeast (L))")
            print("2. Press Enter to start selecting letters")
            print("3. Move to adjacent letters to extend selection")
            print("4. Press Enter again to submit your word")
            print("5. Press Esc to cancel selection")
            print("\nOther Controls:")
            print("h: Get hint")
            print("q: Quit game")
        else:
            # Simple rainbow celebration
            colors = ["\033[91m", "\033[93m", "\033[92m", "\033[96m", "\033[94m", "\033[95m"]
            reset = "\033[0m"
            
            print("\n")
            print(f"{colors[0]}╔════════════════════════════════════════════════════════════╗{reset}")
            print(f"{colors[1]}║                                                            ║{reset}")
            print(f"{colors[2]}║                  GOOD JOB! YOU DID IT!                     ║{reset}")
            print(f"{colors[3]}║                                                            ║{reset}")
            print(f"{colors[4]}╚════════════════════════════════════════════════════════════╝{reset}")
            print(f"{colors[5]}\nYou found all the words! Congratulations! 🎉{reset}")

    def should_draw_connection(self, r1: int, c1: int, r2: int, c2: int) -> bool:
        pos1 = Pos(r1, c1)
        pos2 = Pos(r2, c2)
        
        for strand in self.game.found_strands():
            positions = strand.positions()
            for i in range(len(positions)-1):
                if (positions[i] == pos1 and positions[i+1] == pos2) or \
                   (positions[i] == pos2 and positions[i+1] == pos1):
                    return True
        
        if self.strand_on_currently:
            positions = self.strand_on_currently.positions()
            for i in range(len(positions)-1):
                if (positions[i] == pos1 and positions[i+1] == pos2) or \
                   (positions[i] == pos2 and positions[i+1] == pos1):
                    return True
        
        return False
    
    def get_key(self) -> str:
        fd = sys.stdin.fileno()
        setting = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            letter = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, setting)
        return letter

@click.command()
@click.option('--show', is_flag=True, help='Show all answers instead of playing')
@click.option('-g', '--game', help='Game file to load (without .txt extension)')
@click.option('-h', '--hint', 'hint_threshold', default=3, help='Hint threshold')
@click.option('-a', '--art', 'art_frame', help='Art frame to use')
def main(show: bool, game: str, hint_threshold: int, art_frame: str):
    """Play Strands in the terminal."""
    mode = "show" if show else "play"
    
    if game:
        game_file = f"boards/{game}.txt"
    else:
        # Select a random game file
        game_files = [f for f in os.listdir("boards") if f.endswith(".txt")]
        if not game_files:
            click.echo("No game files found in boards/ directory")
            sys.exit(1)
        game_file = f"boards/{random.choice(game_files)}"
    
    if not os.path.exists(game_file):
        click.echo(f"Game file {game_file} not found")
        sys.exit(1)
    
    tui = TUI(mode, game_file, hint_threshold, art_frame)

if __name__ == "__main__":
    main()
