"""
Game logic for Milestone 1:
Pos, StrandFake, BoardFake, StrandsGameFake
"""

from base import PosBase, StrandBase, BoardBase, StrandsGameBase, Step

# Daniel's imeplementation of Pos for M1

class Pos(PosBase):
    def take_step(self, step: "Step") -> "PosBase":
        step_translate = {
            Step.N: (-1, 0),  # North
            Step.S: (1, 0),   # South
            Step.E: (0, 1),   # East
            Step.W: (0, -1),  # West
            Step.NE: (-1, 1), # Northeast
            Step.NW: (-1, -1),# Northwest
            Step.SE: (1, 1),  # Southeast
            Step.SW: (1, -1)}  # Southwest

        row_change, col_change = step_translate[step]
        return Pos(self.r + row_change, self.c + col_change)

    def step_to(self, other: "PosBase") -> "Step":
        coord_translate = {
            (-1, 0): Step.N,
            (1, 0): Step.S,
            (0, 1): Step.E,
            (0, -1): Step.W,
            (-1, 1): Step.NE,
            (-1, -1): Step.NW,
            (1, 1): Step.SE,
            (1, -1): Step.SW}
        coord = (other.r - self.r, other.c - self.c)

        if coord not in coord_translate:  # Check for valid steps 
            raise ValueError("Invalid Step") 
        
        return coord_translate[coord]

    def is_adjacent_to(self, other: "PosBase") -> bool:
        r_diff = abs(self.r - other.r)
        c_diff = abs(self.c - other.c)
        return r_diff <= 1 and c_diff <= 1 and (r_diff + c_diff > 0) 
############################################################

# Nicole's implementatin of StrandFake for M1

class StrandFake(StrandBase):
    """
    A strand object tracks a start position and a list of steps, where each Step is one of eight neighboring direcs.
    """

    def positions(self) -> list[PosBase]:
        """
        Compute the absolute positions represented by the strand. Positions are independent of board size.
        """
        positions_list = [self.start]
        current_position = self.start
        for step in self.steps:
            current_position = current_position.take_step(step)
            positions_list.append(current_position)
        return positions_list

    def is_cyclic(self) -> bool:
        """
        Check if any position appears multiple times in the strand
        """
        raise NotImplementedError

    def is_folded(self) -> bool:
        """
        Check if any segment of the strand crosses over another.
        """
        raise NotImplementedError
############################################################

# Sean's implementation of BoardFake for M1

class BoardFake(BoardBase):
    """
    Board implementation for the game.
    """
    
    letters: list[list[str]]
    
    def __init__(self, letters: list[list[str]]):
        """
        Constructor
        
        Inputs:
            letters (list[list[str]]): A 2D list of strings 
            representative of the board
        """
        self.letters = letters
    
    def num_rows(self) -> int:
        """
        Return the number of rows on the board based on self.letters
        
        Returns:
            int: The number of rows
        """
        return len(self.letters)
    
    def num_cols(self) -> int:
        """
        Return the number of columns on the board based on self.letters
        
        Returns:
            int: The number of columns (0 if there are no rows)
        """
        if self.num_rows() > 0:
            return len(self.letters[0])
        return 0
    
    def get_letter(self, pos: PosBase) -> str:
        """
        Return the letter at a given position on the board. Raises ValueError
        if the position is not within the bounds of the board.
        
        Inputs:
            pos (PosBase): The position on the board
            
        Returns:
            str: The letter at the position
        """

        if (pos.r < 0 or pos.r >= self.num_rows() or 
            pos.c < 0 or 
            pos.c >= self.num_cols()):
            raise ValueError(f"""Position ({pos.r}, {pos.c}) is not within 
                            the bounds of the board""")
        
        return self.letters[pos.r][pos.c]
    
    def evaluate_strand(self, strand: StrandBase) -> str:
        """
        Evaluate a strand, returning in string form the corresponding letters
        from the board. Raise ValueError if the strand's positions (if any) are
        not within the bounds of the board. 
        
        Inputs:
            strand (StrandBase): The strand to check
            
        Returns:
            str: The string the strand represents
        """
        result = ""
        for pos in strand.positions():
            result += self.get_letter(pos) # raise ValueError if out of bounds
        return result  
############################################################

# Hammond's Implementation of StrandsGameFake for M1
class StrandsGameFake(StrandsGameBase):
    _theme: str
    _board: BoardFake
    _answers: list[tuple[str, StrandBase]]
    _found_strands: list[StrandBase]
    _game_over: bool
    _hint_threshold: int
    _hint_counter: int
    _current_hint_index: int | None  
    _show_hint_letters: bool  
    
    def __init__(self, game_text_data:str | list[str], hint_threshold:int = 3):
        """
        Initialize game from text data.
        
        Args: 
            game_text_data: Path to game file
            hint_threshold: Number of incorrect submissions before hint is open
        
        """
        if isinstance(game_text_data, str):
            with open(game_text_data, "r") as file:
                lines = file.readlines()
        else:
            lines = game_text_data

        # strip quotes if necessary, parse theme
        self._theme = lines[0].strip()
    
        # Parse board
        text_for_board = []
        i = 1
        while i < len(lines) and not lines[i].strip():
            i += 1
        # Read the lines on the board until you hit empty line
        while i < len(lines) and lines[i].strip():
            # Convert each line to list of characters, delete whitespaces
            board_line = lines[i].strip().lower()
            # Remove in-line whitespaces
            board_line = ''.join(board_line.split())
            # Convert to list of characters
            board_chars = []
            for char in board_line:
                board_chars.append(char)
            text_for_board.append(board_chars)
            i += 1
        self._board = BoardFake(text_for_board)
        
        print(self._board.num_rows())
        print(self._board.num_cols())
        # Skip empty lines after board
        while i < len(lines) and not lines[i].strip():
            i += 1
        
        self._answers = []
        
        while i < len(lines):
            line = lines[i].strip()
            if not line:  # Skip empty lines
                i += 1
                continue
            
            parts = line.split()
            if len(parts) < 4:  # Need word, row, col, and one step
                i += 1
                continue
            
            try:
                word_to_find = parts[0].lower()
                row = int(parts[1]) - 1
                col = int(parts[2]) - 1
                
                steps = []
                for step_str in parts[3:]:
                    # Handle step strings
                    steps.append(Step[step_str.upper()])
                    
                start_position = Pos(row, col)
                strand = StrandFake(start_position, steps)
                self._answers.append((word_to_find, strand))
            except (ValueError, KeyError, IndexError):
                # Skip if invalid
                print("Error with answers!")
                pass
                
            i += 1
        
        # Initialize game state
        self._found_strands = []
        self._hint_threshold = hint_threshold
        self._hint_counter = 0
        self._current_hint_index = None
        self._show_hint_letters = False      

    def theme(self) -> str:
        return self._theme        
    
    def board(self) -> BoardBase:
        return self._board
    
    def answers(self) -> list[tuple[str, StrandBase]]:
        return self._answers
    
    def found_strands(self) -> list[StrandBase]:
        return self._found_strands
    
    def game_over(self) -> bool:
        return len(self._found_strands) == len(self._answers)
    
    def hint_threshold(self) -> int:
        return self._hint_threshold
    
    def hint_meter(self) -> int:
        return self._hint_counter
    
    def active_hint(self) -> None | tuple[int, bool]:
        if self._current_hint_index is None:
            return None
        return (self._current_hint_index, self._show_hint_letters)
    
    def submit_strand(self, strand: StrandBase) -> tuple[str, bool] | str:
        """Submit a strand for evaluation."""
        for i, val in enumerate(self._answers):
            word = val[0]
            answer = val[1]
            # Check if the strands match by comparing their positions
            if strand.positions() == answer.positions():
                for found in self._found_strands:
                    if found.positions() == strand.positions():
                        return "Already found"
                    
                self._found_strands.append(strand)    

                if self._current_hint_index == i:
                    self._current_hint_index = None
                    self._show_hint_letters = False

                return (word, True)    
        return "Not a theme word"

    def use_hint(self) -> tuple[int, bool] | str:
        if self._show_hint_letters:
            return "Use your current hint"
        
        for i, val in enumerate(self._answers):
            answer = val[1]
            found = False
            
            for found_strand in self._found_strands:
                if found_strand.start.r == answer.start.r and found_strand.start.c == answer.start.c:
                    found = True
                    break
            
            if not found:
                if self._current_hint_index is None:
                    self._current_hint_index = i
                    self._show_hint_letters = False
                    return (i, False)
                else:
                    self._show_hint_letters = True
                    return (i, True)
        
        return "No hint yet"
######################################################################################################################## 