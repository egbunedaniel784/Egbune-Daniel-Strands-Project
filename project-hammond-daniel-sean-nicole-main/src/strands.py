from base import PosBase, StrandBase, BoardBase, StrandsGameBase, Step


class Pos(PosBase):
    def __hash__(self):
        return hash((self.r, self.c))
    
    def __eq__(self, other):
        if not isinstance(other, Pos):
            return False
        return self.r == other.r and self.c == other.c
    
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


class Strand(StrandBase):
    """
    Strand implementation for the game.
    """
    def __eq__(self, other):
        if not isinstance(other, StrandBase):
            return False
        return self.start == other.start and self.steps == other.steps
 
    def positions(self) -> list[PosBase]:
        """
        Compute the absolute positions represented by the strand. These 
        positions are independent of any particular board size. That is, 
        the resulting positions assume a board of infinite size 
        in all directions.
        """
        positions_list = [self.start]
        current_position = self.start
        for step in self.steps:
            current_position = current_position.take_step(step)
            positions_list.append(current_position)
        return positions_list
    
    def is_cyclic(self) -> bool:
        """
        Decide whether or not the strand is cyclic. That is, check whether or
        not any position appears multiple times in the strand.
        """
        positions = self.positions()

        if len(positions) > 1 and positions[-1] == positions[0]:
            return True
        
        marked = set()
        for pos in positions[:-1]:
            if pos in marked:
                return True
            marked.add(pos)
        return False
    
    def is_folded(self) -> bool:
        """
        Decide whether or not the strand is folded. That is, check whether or 
        not any connection in the strand crosses over another connection in 
        the strand.
        """
        positions = self.positions()
    
        if len(positions) < 4:
            return False
            
        visited = set()
        for i, pos in enumerate(positions[:-1]):
            if pos in visited:
                return True
            visited.add(pos)

        for i in range(len(positions) - 1):
            for j in range(i + 2, len(positions) - 1):
                # Get points that define edges
                if j == i + 1:
                    continue
                
                p1 = positions[i]
                p2 = positions[i + 1]
                p3 = positions[j]
                p4 = positions[j + 1]
                
                # Check if edges cross
                if self._check_edges_crossing(p1, p2, p3, p4):
                    return True
        
        return False

    def _check_edges_crossing(self, p1, p2, p3, p4) -> bool:
        """
        Helper function for is_folded: check if edge p1 - p2 crosses edge
        p3 - p4. Essentially, check if edges make an X: edges cross if both
        edges are diagonal, go in opposite directions, and share a center 
        point. 
        """
        
        # Diagonal check:
        edge1_is_diagonal = (p1.r != p2.r) and (p1.c != p2.c)
        edge2_is_diagonal = (p3.r != p4.r) and (p3.c != p4.c)
        
        if not (edge1_is_diagonal and edge2_is_diagonal):
            return False
        
        # Centers check:
        edge1_center_r = (p1.r + p2.r) / 2
        edge1_center_c = (p1.c + p2.c) / 2
        edge2_center_r = (p3.r + p4.r) / 2
        edge2_center_c = (p3.c + p4.c) / 2
        
        # Centers must match for diagonal crossing
        if edge1_center_r != edge2_center_r or edge1_center_c != edge2_center_c:
            return False
        
        # Opposite direction diagonals check:
        edge1_same_sign = ((p2.r - p1.r) > 0) == ((p2.c - p1.c) > 0)
        edge2_same_sign = ((p4.r - p3.r) > 0) == ((p4.c - p3.c) > 0)
        
        # Return T or F for same sign
        return edge1_same_sign != edge2_same_sign

class Board(BoardBase):
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
        if not letters or len(letters) == 0:
            raise ValueError("Board cannot be empty.")
        
        if not letters[0] or len(letters[0]) == 0:
            raise ValueError("Board must have at least one column.")
        
        expected_cols = len(letters[0])
        for i, row in enumerate(letters):
            if len(row) != expected_cols:
                raise ValueError(f"Board must have a rectangular shape. "
                                 f"Row {i} has {len(row)} columns, expected {expected_cols}")
        
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
            raise ValueError(f"Position ({pos.r}, {pos.c}) is not within "
                            f"the bounds of the board")
        
        return self.letters[pos.r][pos.c]
    
    def evaluate_strand(self, strand: StrandBase) -> str:
        """
        Evaluate a strand, returning the string of
        corresponding letters from the board.

        Raises ValueError if any of the strand's positions
        are not within the bounds of the board.
        """
        result = ""
        for pos in strand.positions():
            result += self.get_letter(pos) # raise ValueError if out of bounds
        return result   


class StrandsGame(StrandsGameBase):
    _theme: str
    _board: Board
    _answers: list[tuple[str, StrandBase]]
    _found_strands: list[StrandBase]
    _found_dictionary: list[str]
    _dictionary: set
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

        #validity checks

        if not isinstance(hint_threshold, int):
            raise TypeError("hint threshold must be int")

        if isinstance(game_text_data, str):
            try:
                with open(game_text_data, "r") as file:
                    lines = file.readlines()
            except FileNotFoundError:
                try:
                    with open(game_text_data, "r") as file:
                        lines = file.readlines()
                except FileNotFoundError:
                    with open(f"{game_text_data}.txt", "r") as file:
                        lines = file.readlines()
        elif isinstance(game_text_data, list):
            lines = game_text_data  # Accept list directly
        else:
            raise ValueError("Must pass path as string or list of strings")

        if lines[0] == "\n": 
            raise ValueError("Invalid Theme")
        if lines[1] != "\n": 
            raise ValueError("Expected Blank Line")

        # strip quotes if necessary, parse theme
        theme_line = lines[0].strip()
        
        self._theme = theme_line

        letters = {a for a in "abcdefghijklmnopqrstuvwxyz"}

        # Parse board and check board validity
        text_for_board = []
        i = 2
        len_board = 0
        while i < len(lines):
            line = lines[i].strip()

            if not line:
                break

            line_chars = [char for char in line if char != " "]

            if i == 2:
                len_board = len(line_chars)
            else:
                if len(line_chars) != len_board and len(line_chars) != 0:
                    raise ValueError("board needs to be rectangular")

            if len(line) == 0:
                break

            final_line = []
            for letter in line_chars:
                if not letter.lower() in letters:
                    raise ValueError("invalid character in board")
                final_line.append(letter.lower())
            
            text_for_board.append(final_line)
            i += 1

        self._board = Board(text_for_board)

        i += 1 #we are now at the index where the answers should start

        answers = []
        while i < len(lines):
            line = lines[i]
            if line.strip() == "": #for empty lines
                break
            
            parts = line.lower().split()
            if len(parts) < 5:
                raise ValueError("Missing information in strand")
            
            word = ""
            row = 0
            col = 0
            steps = []
            for index, val in enumerate(parts):
                if index == 0:
                    for letter in val:
                        if not letter in letters: raise ValueError("Answer must contain letters")
                    if len(val) < 3:
                        raise ValueError("answer must have atleast 3 letters")
                    word = val
                elif index == 1:
                    #we have a row
                    row = int(val) - 1
                    if row < 0 or row >= self._board.num_rows(): 
                        raise ValueError("Invalid row coordinate")
                elif index == 2:
                    #we have col
                    col = int(val) - 1
                    if col < 0 or col >= self._board.num_cols(): 
                        raise ValueError("Invalid col coordinate")
                else:
                    #we have a step
                    for current_step in Step:
                        if current_step.value == val:
                            steps.append(current_step)
            i += 1

            #construct strand from word
            pos = Pos(row,col)
            strand = Strand(pos,steps)

            if strand.is_folded():
                raise ValueError("No folds allowed in strands")    
            answers.append((word,strand))
        self._answers = answers
        #check that every space is taken up by letters, no crossing words
        #and no spaces have more than 1 letter
        mock_board = [[0 for i2 in range(self._board.num_cols())] for i in range(self._board.num_rows())]

        for word, strand in self._answers:
            for pos in strand.positions():
                r = pos.r
                c = pos.c
                mock_board[r][c] += 1

        for row in mock_board:
            for num in row:
                if num > 1:
                    raise ValueError("Positions repeated in board")
                if num < 1:
                    raise ValueError("Board position empty")
        
        # Initialize game state
        self._dictionary = set()
        
        with open("assets/web2.txt") as dict_file:
            dict_lines = dict_file.readlines()
            for word in dict_lines:
                self._dictionary.add(word.strip())

        self._found_strands = []
        self._found_dictionary = []
        self._hint_threshold = hint_threshold
        self._game_over = False
        self._hint_counter = 0
        self._current_hint_index = None
        self._show_hint_letters = False      

    def theme(self) -> str:
        if isinstance(self._theme, str):
            words = self._theme.split()
            return ' '.join(words)
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
        if len(self._board.evaluate_strand(strand)) < 4:
            is_answer = False
            for _, answer_strand in self._answers:
                if strand == answer_strand:
                    is_answer = True

            if not is_answer:
                return "Too short"

        for i, val in enumerate(self._answers):
            word = val[0]
            answer = val[1]
            if answer == strand:
                for found in self._found_strands:
                    if found == strand:
                        return "Already found"
                    
                self._found_strands.append(strand)    

                if self._current_hint_index == i:
                    self._current_hint_index = None
                    self._show_hint_letters = False
                return (word, True)

        strand_word = self._board.evaluate_strand(strand)
        if strand_word in self._dictionary:
            if not strand_word in self._found_dictionary:
                self._found_dictionary.append(strand_word)
                self._hint_counter += 1
                return (strand_word,False)
            else:
                return "Already found"
           
        
        return "Not a theme word"

    def use_hint(self) -> tuple[int, bool] | str:
        if self._show_hint_letters:
            return "Use your current hint"
        
        if self._hint_counter < self._hint_threshold:
            return "haven't earned hint"

        for i, val in enumerate(self._answers):
            answer = val[1]
            found = False
            
            for found_strand in self._found_strands:
                if found_strand == answer:
                    found = True
                    break
            
            if not found:
                if self._current_hint_index is None:
                    self._current_hint_index = i
                    self._show_hint_letters = False
                    self._hint_counter -= self._hint_threshold
                    return (i, False)
                else:
                    self._show_hint_letters = True
                    self._hint_counter -= self._hint_threshold
                    return (i, True)
        
        return "No hint yet"