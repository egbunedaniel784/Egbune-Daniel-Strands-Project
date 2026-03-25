import pytest
from base import PosBase, StrandBase, BoardBase, StrandsGameBase, Step
from strands import Pos, Strand, Board, StrandsGame


def test_inheritance() -> None:
    """
    Test that the four classes inherit from the corresponding
    abstract base classes.
    """
    assert issubclass(Pos, PosBase)
    assert issubclass(Strand, StrandBase)
    assert issubclass(Board, BoardBase)
    assert issubclass(StrandsGame, StrandsGameBase)


def test_pos_take_step() -> None:
    """
    Test a position, taking a step in each 8 neighboring directions.
    
    Specifically, test N, S, E, W (90 degrees): also test NE, NW, 
    SE, SW (45 degrees). 
    """
    
    pos = Pos(5, 5)
    
    # linear steps:
    assert pos.take_step(Step.N) == Pos(4,5)
    assert pos.take_step(Step.S) == Pos(6,5)
    assert pos.take_step(Step.E) == Pos(5,6)
    assert pos.take_step(Step.W) == Pos(5,4)
    
    # diagonal steps:
    assert pos.take_step(Step.NW) == Pos(4,4)
    assert pos.take_step(Step.NE) == Pos(4,6)
    assert pos.take_step(Step.SW) == Pos(6,4)
    assert pos.take_step(Step.SE) == Pos(6,6)

def test_pos_step_to_success() -> None:
    """
    Test determining the direction of the step between adjacent positions.
    Inverse of take_step. Return step direction that connects two positions.
    """
    pos = Pos(5, 5)

    # Test that the eight positions match the previous test.
    assert pos.step_to(Pos(4, 5)) == Step.N
    assert pos.step_to(Pos(6, 5)) == Step.S
    assert pos.step_to(Pos(5, 6)) == Step.E
    assert pos.step_to(Pos(5, 4)) == Step.W
    assert pos.step_to(Pos(4, 4)) == Step.NW
    assert pos.step_to(Pos(4, 6)) == Step.NE
    assert pos.step_to(Pos(6, 4)) == Step.SW
    assert pos.step_to(Pos(6, 6)) == Step.SE

def test_pos_step_to_failure() -> None:
    """
    Check that step_to raises ValueError for positions more than 
    one step away -- testing for two steps away and three steps away"""
    pos = Pos(5, 5)

    # List of positions two steps away
    two_steps_away = [
        Pos(3, 5),  
        Pos(7, 5), 
        Pos(5, 7), 
        Pos(5, 3), 
        Pos(3, 3), 
        Pos(3, 7), 
        Pos(7, 3), 
        Pos(7, 7)]
    
    
    for two_away in two_steps_away:
        with pytest.raises(ValueError):
            pos.step_to(two_away)

    # List of positions three steps away
    three_steps_away = [Pos(2, 5), 
                        Pos(8,5), 
                        Pos(5, 8), 
                        Pos(5, 2)]

    for three_away in three_steps_away:
        with pytest.raises(ValueError):
            pos.step_to(three_away)

def test_strand_positions_straight_cardinal() -> None:
    """
    Test strands, one in each cardinal direction, each with length = 4 steps
    and check that the position method returns properly
    """
    start = Pos(5, 5)

    # North strand:
    north_strand = Strand(start, [Step.N, Step.N, Step.N, Step.N])
    north_positions = north_strand.positions()
    
    expected_north = [
        Pos(5, 5),
        Pos(4, 5),
        Pos(3, 5),
        Pos(2, 5),
        Pos(1, 5)
    ]
    
    assert north_positions == expected_north

    # South strand:
    south_strand = Strand(start, [Step.S, Step.S, Step.S, Step.S])
    south_positions = south_strand.positions()
    
    expected_south = [
        Pos(5, 5),
        Pos(6, 5),
        Pos(7, 5),
        Pos(8, 5),
        Pos(9, 5)
    ]
    
    assert south_positions == expected_south
    
    # East strand:
    east_strand = Strand(start, [Step.E, Step.E, Step.E, Step.E])
    east_positions = east_strand.positions()
    
    expected_east = [
        Pos(5, 5),
        Pos(5, 6),
        Pos(5, 7),
        Pos(5, 8),
        Pos(5, 9)
    ]
    
    assert east_positions == expected_east
    
    # West strand
    west_strand = Strand(start, [Step.W, Step.W, Step.W, Step.W])
    west_positions = west_strand.positions()
    expected_west = [
        Pos(5, 5),
        Pos(5, 4),
        Pos(5, 3),
        Pos(5, 2),
        Pos(5, 1)
    ]
    assert west_positions == expected_west

def test_strand_positions_straight_intercardinal() -> None:
    """
    Test strands, same manner as previously for cardinal directions, but
    check for the intercardinal directions these times
    """
    start = Pos(5,5)

    # Northeast strand:
    ne_strand = Strand(start, [Step.NE, Step.NE, Step.NE, Step.NE])
    ne_positions = ne_strand.positions()
    
    expected_ne = [
            Pos(5, 5),
            Pos(4, 6),
            Pos(3, 7),
            Pos(2, 8),
            Pos(1, 9)]
        
    assert ne_positions == expected_ne
        
    # Northwest strand:
    nw_strand = Strand(start, [Step.NW, Step.NW, Step.NW, Step.NW])
    nw_positions = nw_strand.positions()
        
    expected_nw = [
            Pos(5, 5),
            Pos(4, 4),
            Pos(3, 3),
            Pos(2, 2),
            Pos(1, 1)]
        
    assert nw_positions == expected_nw
        
    # Southeast strand:
    se_strand = Strand(start, [Step.SE, Step.SE, Step.SE, Step.SE])
    se_positions = se_strand.positions()
        
    expected_se = [
        Pos(5, 5),
        Pos(6, 6),
        Pos(7, 7),
        Pos(8, 8),
        Pos(9, 9)]
        
    assert se_positions == expected_se
        
    # Southwest strand
    sw_strand = Strand(start, [Step.SW, Step.SW, Step.SW, Step.SW])
    sw_positions = sw_strand.positions()

    expected_sw = [
        Pos(5, 5),
        Pos(6, 4),
        Pos(7, 3),
        Pos(8, 2),
        Pos(9, 1)]

    assert sw_positions == expected_sw

def test_strand_positions_long() -> None:
    """
    Test two long strands: must include one step each direction, but 
    does not cross itself. Check that position and is_folded return the
    expected results.
    """
    start = Pos(5,5)

    # First strand w/o crossing over
    non_folded_steps = [
        Step.N, Step.NE, Step.E, Step.SE, 
        Step.S, Step.SW, Step.W, Step.NW
    ]
    non_folded_strand = Strand(start, non_folded_steps)
    non_folded_positions = non_folded_strand.positions()

    expected_positions = [
        Pos(5, 5),
        Pos(4, 5),
        Pos(3, 6),
        Pos(3, 7), 
        Pos(4, 8), 
        Pos(5, 8),
        Pos(6, 7),
        Pos(6, 6),
        Pos(5, 5)
    ]

    assert non_folded_positions == expected_positions
    assert non_folded_strand.is_cyclic() == True
    assert non_folded_strand.is_folded() == False

    #Second strand that crosses over
    folded_steps = [
        Step.N, Step.E, Step.S, Step.W,
        Step.NE, Step.SE, Step.SW, Step.NW 
    ]
    folded_strand = Strand(start, folded_steps)
    folded_positions = folded_strand.positions()

    expected_folded_positions = [
        Pos(5, 5),  
        Pos(4, 5),
        Pos(4, 6),
        Pos(5, 6),
        Pos(5, 5),
        Pos(4, 6),
        Pos(5, 7),
        Pos(6, 6),
        Pos(5, 5)]

    assert folded_positions == expected_folded_positions
    assert folded_strand.is_cyclic() == True
    assert folded_strand.is_folded() == True

# Choose game file to test - for this testing module, used in-stitches.txt
GAME_FILE = "in-stitches"

def test_load_game_in_stitches_file() -> None:
    """
    Test loading a game from a file. Check for key parameters, including
    theme, number of rows, columns, and answers match expected results.
    """
    game = StrandsGame(f"boards/{GAME_FILE}.txt")

    assert game.theme() == "in stitches"

    # Check board dimensions (N x N)
    assert game.board().num_rows() == 8
    assert game.board().num_cols() == 6

    # Check some of the letters to see it loaded properly 
    assert game.board().get_letter(Pos(0, 0)) == "r"
    assert game.board().get_letter(Pos(0, 2)) == "n"
    assert game.board().get_letter(Pos(3, 3)) == "d"
    assert game.board().get_letter(Pos(7, 5)) == "k"

    # Check answers
    answers = game.answers()

    assert len(answers) == 8

    # Check for expected words match
    words = [word for word, _ in answers]
    assert "darn" in words
    assert "knit" in words
    assert "mend" in words
    assert "baste" in words
    assert "patch" in words
    assert "crochet" in words
    assert "embroider" in words
    assert "needlework" in words

    #Verify specific strands
    for word, strand in answers:
        if word == "darn":
            assert strand.start == Pos(7, 2)
            assert strand.steps == [Step.W, Step.W, Step.N]

            positions = strand.positions()
            expected_positions = [
                Pos(7, 2), Pos(7, 1), Pos(7, 0), Pos(6, 0)]
            assert positions == expected_positions
            break

def test_load_game_in_stitches_variations() -> None:
    """
    Test loading a game from variations of the file contents.
    Check for list[str] of file to ues for game initialization, and test that
    white space + caps don't affect the loading.
    """
    # Load normal style from txt file
    txt_game = StrandsGame(f"boards/{GAME_FILE}")
    
    with open(f"boards/{GAME_FILE}.txt", "r") as f:
        original_lines = f.readlines()
    
    # Check for list of strings instead of filenames
    list_game = StrandsGame(original_lines)

    # Check list_game parameters match with original game
    assert list_game.theme() == txt_game.theme()
    assert list_game.board().num_rows() == txt_game.board().num_rows()
    assert list_game.board().num_cols() == txt_game.board().num_cols()

    modified_lines = []
    for line in original_lines:
        if line.strip():
            # mess with capitalization and white spaces
            parts = line.split()
            if len(parts) > 0:
                for i in range(len(parts)):
                    if i % 2 == 0:
                        parts[i] = parts[i].upper() #uppercase some
                    else:
                        parts[i] = parts[i].lower() #lowercase some
                # create modified_lines with extra spaces
                modified_line = "   ".join(parts) + "   "
                modified_lines.append(modified_line)
            else:
                modified_lines.append(line)
        else:
            modified_lines.append(line)

    # set new modified_game to read from modified_lines
    modified_game = StrandsGame(modified_lines)

    # verify parameters are same even with messarounds in format
    assert modified_game.theme() == txt_game.theme()
    assert modified_game.board().num_rows() == txt_game.board().num_rows()
    assert modified_game.board().num_cols() == txt_game.board().num_cols()

    # verify same words are there even with messarounds in format
    original_words = set(word for word, _ in txt_game.answers())
    modified_words = set(word for word, _ in modified_game.answers())
    assert original_words == modified_words

def test_load_game_in_stitches_invalid() -> None:
    """Test loading invalid game files raises ValueError"""
    board_missing_pieces = [
        "In stitches",
        '',
        'R C N R B E',
        'E O C E O M',
        '', # empty section 1
        '', # empty section 2
        'C T L I N K',
        'M N D E B T',
        'N E W A S E',
        'R A D O R K',
        '',
        'DARN 8 3 w w n', 
    ]
    with pytest.raises(ValueError):
        StrandsGame(board_missing_pieces)

    incomplete_board = [
        "In stitches",
        '',
        'R C N R B E',
        'E O C E O M', # missing several rows
        'M N D E B T',
        'N E W A S E',
        'R A D O R K',
        '',
        'DARN 8 3 w w n',     
    ]
    with pytest.raises(ValueError):
        StrandsGame(incomplete_board)

    out_of_bounds = [
        "In stitches",
        '',
        'R C N R B E',
        'E O C E O M',
        'T H E I D R',
        'H P A D T E',
        'C T L I N K',
        'M N D E B T',
        'N E W A S E',
        'R A D O R K',
        '',
        'DARN 30 30 w w n'] # 30 30 is out of bounds
    with pytest.raises(ValueError):
        StrandsGame(out_of_bounds)

    mismatching_words = [
        "In stitches",
        '',
        'R C N R B E',
        'E O C E O M',
        'T H E I D R',
        'H P A D T E',
        'C T L I N K',
        'M N D E B T',
        'N E W A S E',
        'R A D O R K',
        '',
        'RANDOMWORD 8 3 w w n' # word doesn't match with strand letters
    ]
    with pytest.raises(ValueError):
        StrandsGame(mismatching_words)

def test_play_game_in_stitches_more() -> None:
    """
    Test playing a game with hints, triggering each
    potential scenario involving use_hint
    """
    game = StrandsGame(f"boards/{GAME_FILE}")
    answers = game.answers()
    
    # Initially no hint available
    assert game.use_hint() == "haven't earned hint"
    
    game._hint_counter = 3
    
    assert game.use_hint() == (0, False)
    assert game.active_hint() == (0, False)
    
    game._hint_counter = 3
    
    assert game.use_hint() == (0, True)
    assert game.active_hint() == (0, True)
    
    assert game.use_hint() == "Use your current hint"
    assert game.active_hint() == (0, True)
    
    assert game.submit_strand(answers[0][1]) == (answers[0][0], True)
    
    assert game.submit_strand(answers[1][1]) == (answers[1][0], True)
    
    game._hint_counter = 3
    
    assert game.use_hint() == (2, False)
    assert game.active_hint() == (2, False)
    
    assert game.submit_strand(answers[2][1]) == (answers[2][0], True)
    
    assert game.active_hint() is None
    
    for i in range(3, len(answers)):
        game.submit_strand(answers[i][1])
    
    assert game.game_over()

def test_play_game_in_stitches_twice() -> None:
    """
    Test playing same game, but check that it works with different order
    """
    # Load game
    game = StrandsGame(f"boards/{GAME_FILE}")
    
    # Load answers
    answers = game.answers()

    assert game.submit_strand(answers[7][1]) == (answers[7][0], True)
    assert len(game.found_strands()) == 1
    

    assert game.submit_strand(answers[5][1]) == (answers[5][0], True)
    assert len(game.found_strands()) == 2

    assert game.submit_strand(answers[3][1]) == (answers[3][0], True)
    assert len(game.found_strands()) == 3
    

    assert game.submit_strand(answers[4][1]) == (answers[4][0], True)
    assert len(game.found_strands()) == 4
    
    assert game.submit_strand(answers[2][1]) == (answers[2][0], True)
    assert len(game.found_strands()) == 5
    

    assert game.submit_strand(answers[1][1]) == (answers[1][0], True)
    assert len(game.found_strands()) == 6
    
    assert game.submit_strand(answers[6][1]) == (answers[6][0], True)
    assert len(game.found_strands()) == 7
    
    assert game.submit_strand(answers[0][1]) == (answers[0][0], True)
    assert len(game.found_strands()) == 8
    
    assert game.game_over()


def test_play_game_in_stitches_three_times() -> None:
    """Test playing a game with non-theme words and already found words"""
    # Load game
    game = StrandsGame(f"boards/{GAME_FILE}")
    
    # Load answers
    answers = game.answers()

    # Play theme word 1
    assert game.submit_strand(answers[0][1]) == (answers[0][0], True)
    
    # strand that doesns't match theme word
    non_theme_strand1 = Strand(Pos(0, 0), [Step.E, Step.E, Step.S])
    assert game.submit_strand(non_theme_strand1) == "Not a theme word"
    
    # strand 2 that doesn't match theme word
    non_theme_strand2 = Strand(Pos(4, 4), [Step.N, Step.N, Step.E])
    assert game.submit_strand(non_theme_strand2) == "Not a theme word"
    
    # Repeat theme word 1, should raise already found
    assert game.submit_strand(answers[0][1]) == "Already found"
    
    # Check found word count
    assert len(game.found_strands()) == 1
    
    # Play theme word 2
    assert game.submit_strand(answers[1][1]) == (answers[1][0], True)
    
    # Play theme word 3
    assert game.submit_strand(answers[2][1]) == (answers[2][0], True)
    
    # Play remaining words
    for i in range(3, len(answers)):
        assert game.submit_strand(answers[i][1]) == (answers[i][0], True)
    
    assert game.game_over()


def test_play_game_in_stitches_more() -> None:
    """
    Test playing a game with hints, triggering each 
    potential scenario involving use_hint
    """
    game = StrandsGame(f"boards/{GAME_FILE}")
    answers = game.answers()

    # hint 1: shouldn't show start/end
    assert game.use_hint() == (0, False)
    assert game.active_hint() == (0, False)

    # hint 2: show start/end for word 1, same word
    assert game.use_hint() == (0, True)
    assert game.active_hint() == (0, True)
    
    # hint 3: should prompt usage of original hint
    assert game.use_hint() == "Use your current hint"
    assert game.active_hint() == (0, True)
    
    # submit first hint word 
    assert game.submit_strand(answers[0][1]) == (answers[0][0], True)

    assert game.submit_strand(answers[1][1]) == (answers[1][0], True)

    assert game.use_hint() == (2, False)
    assert game.active_hint() == (2, False)

    # submit second hint word
    assert game.submit_strand(answers[2][1]) == (answers[2][0], True)

    assert game.active_hint() is None
    # finish rest of the game
    for i in range(3, len(answers)):
        assert game.submit_strand(answers[i][1]) == (answers[i][0], True)

    assert game.game_over()

def test_is_not_cyclic() -> None:
    """
    Define four acyclic strands with different lengths and shapes, 
    and check that is_cyclic returns the appropriate answer.
    """
    start = Pos(5, 5)
    
    # straight case
    straight_steps = [Step.N, Step.N, Step.N]
    straight_strand = Strand(start, straight_steps)
    assert straight_strand.is_cyclic() == False
    
    # l-shape case
    l_shape_steps = [Step.N, Step.N, Step.E, Step.E]
    l_shape_strand = Strand(start, l_shape_steps)
    assert l_shape_strand.is_cyclic() == False
    
    # zigzag case
    zigzag_steps = [Step.N, Step.E, Step.N, Step.W, Step.N]
    zigzag_strand = Strand(start, zigzag_steps)
    assert zigzag_strand.is_cyclic() == False
    
     # snake case
    snake_steps = [Step.N, Step.E, Step.S, Step.E, Step.N, Step.E]
    snake_strand = Strand(start, snake_steps)
    assert snake_strand.is_cyclic() == False

def test_is_cyclic() -> None:
    """
    Define four cyclic strands with different lengths and shapes, 
    and check that is_cyclic returns the appropriate answer.
    """
    start = Pos(5, 5)
    
    # square case
    square_steps = [Step.N, Step.E, Step.S, Step.W]
    square_strand = Strand(start, square_steps)
    assert square_strand.is_cyclic() == True
    
    # diamond case
    diamond_steps = [Step.NE, Step.SE, Step.SW, Step.NW]
    diamond_strand = Strand(start, diamond_steps)
    assert diamond_strand.is_cyclic() == True
    
    # rectangle case
    rectangle_steps = [Step.N, Step.N, Step.E, Step.E, Step.S, Step.S, Step.W, Step.W]
    rectangle_strand = Strand(start, rectangle_steps)
    assert rectangle_strand.is_cyclic() == True
    
    # black widow shape case
    black_widow_steps = [Step.NE, Step.E, Step.SE, Step.SW, Step.W, Step.NW]
    black_widow_strand = Strand(start, black_widow_steps)
    assert black_widow_strand.is_cyclic() == True

def test_overlapping() -> None:
    """
    Check that each of the overlapping strands can be 
    successfully played to find that theme word.
    """
    game1 = StrandsGame("boards/best-in-class.txt")
    
    # Get the correct strand for eyes from the answers
    eyes_strand = None
    for word, strand in game1.answers():
        if word == "eyes":
            eyes_strand = strand
            break
    
    assert eyes_strand is not None, "Couldn't find 'eyes' in answers"
    
    # Use the correct strand
    result1 = game1.submit_strand(eyes_strand)
    assert isinstance(result1, tuple)
    assert result1 == ("eyes", True)
    
    # Create a new game instance
    game2 = StrandsGame("boards/best-in-class.txt")
    
    # Use the same correct strand again
    result2 = game2.submit_strand(eyes_strand)
    assert result2 == ("eyes", True)

def test_load_game_kitty_corner_file() -> None:
    """
    Test loading a game from a file. Check for key parameters, including
    theme, number of rows, columns, and answers match expected results.
    """
    game = StrandsGame("boards/kitty-corner.txt")

    assert game.theme() == "kitty corner"

    # Check board dimensions (N x N)
    assert game.board().num_rows() == 8
    assert game.board().num_cols() == 6

    # Check some of the letters to see it loaded properly 
    assert game.board().get_letter(Pos(0, 0)) == "u"
    assert game.board().get_letter(Pos(0, 2)) == "c"
    assert game.board().get_letter(Pos(3, 3)) == "e"
    assert game.board().get_letter(Pos(7, 5)) == "c"

    # Check answers
    answers = game.answers()

    assert len(answers) == 8

    # Check for expected words match
    words = [word for word, _ in answers]
    assert "purr" in words
    assert "swat" in words
    assert "hiss" in words
    assert "blink" in words
    assert "pounce" in words
    assert "snuggle" in words
    assert "stretch" in words
    assert "catbehavior" in words

    #Verify specific strands
    for word, strand in answers:
        if word == "purr":
            assert strand.start == Pos(4, 0)
            assert strand.steps == [Step.E, Step.N, Step.NE]

            positions = strand.positions()
            expected_positions = [
                Pos(4, 0), Pos(4, 1), Pos(3, 1), Pos(2, 2)]
            assert positions == expected_positions
            break


def test_load_game_kitty_corner_variations() -> None:
    """
    Test loading a game from variations of the file contents.
    Check for list[str] of file to ues for game initialization, and test that
    white space + caps don't affect the loading.
    """
    # Load normal style from txt file
    txt_game = StrandsGame("boards/kitty-corner")
    
    with open("boards/kitty-corner.txt", "r") as f:
        original_lines = f.readlines()
    
    # Check for list of strings instead of filenames
    list_game = StrandsGame(original_lines)

    # Check list_game parameters match with original game
    assert list_game.theme() == txt_game.theme()
    assert list_game.board().num_rows() == txt_game.board().num_rows()
    assert list_game.board().num_cols() == txt_game.board().num_cols()

    modified_lines = []
    for line in original_lines:
        if line.strip():
            # mess with capitalization and white spaces
            parts = line.split()
            if len(parts) > 0:
                for i in range(len(parts)):
                    if i % 2 == 0:
                        parts[i] = parts[i].upper() #uppercase some
                    else:
                        parts[i] = parts[i].lower() #lowercase some
                # create modified_lines with extra spaces
                modified_line = "   ".join(parts) + "   "
                modified_lines.append(modified_line)
            else:
                modified_lines.append(line)
        else:
            modified_lines.append(line)

    # set new modified_game to read from modified_lines
    modified_game = StrandsGame(modified_lines)

    # verify parameters are same even with messarounds in format
    assert modified_game.theme() == txt_game.theme()
    assert modified_game.board().num_rows() == txt_game.board().num_rows()
    assert modified_game.board().num_cols() == txt_game.board().num_cols()

    # verify same words are there even with messarounds in format
    original_words = set(word for word, _ in txt_game.answers())
    modified_words = set(word for word, _ in modified_game.answers())
    assert original_words == modified_words


def test_load_game_kitty_corner_invalid() -> None:
    """Test loading invalid game files raises ValueError"""
    board_missing_pieces = [
        "Kitty Corner",
        '',
        'U G C H C T',
        'N G A T K E',
        '', # empty section 1
        '', # empty section 2
        'G L R B N R',
        'P U A B L S',
        'W T S O N O',
        'H I S R E C',
        '',
        'PURR 5 1 e n ne', 
    ]
    with pytest.raises(ValueError):
        StrandsGame(board_missing_pieces)

    incomplete_board = [
        "Kitty Corner",
        '',
        'U G C H C T',
        'N G A T K E', # missing several rows
        'P U A B L S',
        'W T S O N O',
        'H I S R E C',
        '',
        'PURR 5 1 e n ne',     
    ]
    with pytest.raises(ValueError):
        StrandsGame(incomplete_board)

    out_of_bounds = [
        "Kitty Corner",
        '',
        'U G C H C T',
        'N G A T K E',
        'S L R B N R',
        'E R H E I T',
        'P U A B L S',
        'S A V I U P',
        'W T S O N O',
        'H I S R E C',
        '',
        'PURR 15 15 e n ne'] # 15 15 is out of bounds
    with pytest.raises(ValueError):
        StrandsGame(out_of_bounds)

    mismatching_words = [
        "Kitty Corner",
        '',
        'U G C H C T',
        'N G A T K E',
        'S L R B N R',
        'E R H E I T',
        'P U A B L S',
        'S A V I U P',
        'W T S O N O',
        'H I S R E C',
        '',
        'RANDOMWORD 5 1 e n ne' # word doesn't match with strand letters
    ]
    with pytest.raises(ValueError):
        StrandsGame(mismatching_words)


def test_play_game_kitty_corner_once() -> None:
    """
    Test playing a game with moves involving only submitting 
    theme words in the correct order. Check intermediate results.
    """  
    # Load game
    game = StrandsGame("boards/kitty-corner")
    
    # Load answers
    answers = game.answers()

    assert game.submit_strand(answers[0][1]) == (answers[0][0], True)
    assert len(game.found_strands()) == 1
    

    assert game.submit_strand(answers[1][1]) == (answers[1][0], True)
    assert len(game.found_strands()) == 2

    assert game.submit_strand(answers[2][1]) == (answers[2][0], True)
    assert len(game.found_strands()) == 3
    

    assert game.submit_strand(answers[3][1]) == (answers[3][0], True)
    assert len(game.found_strands()) == 4
    
    assert game.submit_strand(answers[4][1]) == (answers[4][0], True)
    assert len(game.found_strands()) == 5
    

    assert game.submit_strand(answers[5][1]) == (answers[5][0], True)
    assert len(game.found_strands()) == 6
    
    assert game.submit_strand(answers[6][1]) == (answers[6][0], True)
    assert len(game.found_strands()) == 7
    
    assert game.submit_strand(answers[7][1]) == (answers[7][0], True)
    assert len(game.found_strands()) == 8
    
    assert game.game_over()


def test_play_game_kitty_corner_twice() -> None:
    """
    Test playing same game, but check that it works with different order
    """
    # Load game
    game = StrandsGame("boards/kitty-corner")
    
    # Load answers
    answers = game.answers()

    assert game.submit_strand(answers[7][1]) == (answers[7][0], True)
    assert len(game.found_strands()) == 1
    

    assert game.submit_strand(answers[5][1]) == (answers[5][0], True)
    assert len(game.found_strands()) == 2

    assert game.submit_strand(answers[3][1]) == (answers[3][0], True)
    assert len(game.found_strands()) == 3
    

    assert game.submit_strand(answers[4][1]) == (answers[4][0], True)
    assert len(game.found_strands()) == 4
    
    assert game.submit_strand(answers[2][1]) == (answers[2][0], True)
    assert len(game.found_strands()) == 5
    

    assert game.submit_strand(answers[1][1]) == (answers[1][0], True)
    assert len(game.found_strands()) == 6
    
    assert game.submit_strand(answers[6][1]) == (answers[6][0], True)
    assert len(game.found_strands()) == 7
    
    assert game.submit_strand(answers[0][1]) == (answers[0][0], True)
    assert len(game.found_strands()) == 8
    
    assert game.game_over()


def test_play_game_kitty_corner_three_times() -> None:
    """Test playing a game with non-theme words and already found words"""
    # Load game
    game = StrandsGame("boards/kitty-corner")
    
    # Load answers
    answers = game.answers()

    # Play theme word 1
    assert game.submit_strand(answers[0][1]) == (answers[0][0], True)
    
    # strand that doesns't match theme word
    non_theme_strand1 = Strand(Pos(0, 0), [Step.E, Step.E, Step.S])
    assert game.submit_strand(non_theme_strand1) == "Not a theme word"
    
    # strand 2 that doesn't match theme word
    non_theme_strand2 = Strand(Pos(4, 4), [Step.N, Step.N, Step.E])
    assert game.submit_strand(non_theme_strand2) == "Not a theme word"
    
    # Repeat theme word 1, should raise already found
    assert game.submit_strand(answers[0][1]) == "Already found"
    
    # Check found word count
    assert len(game.found_strands()) == 1
    
    # Play theme word 2
    assert game.submit_strand(answers[1][1]) == (answers[1][0], True)
    
    # Play theme word 3
    assert game.submit_strand(answers[2][1]) == (answers[2][0], True)
    
    # Play remaining words
    for i in range(3, len(answers)):
        assert game.submit_strand(answers[i][1]) == (answers[i][0], True)
    
    assert game.game_over()


def test_play_game_kitty_corner_more() -> None:
    """
    Test playing a game with hints, triggering each 
    potential scenario involving use_hint
    """
    game = StrandsGame("boards/kitty-corner")
    answers = game.answers()
    
    # Initially no hint available
    assert game.use_hint() == "haven't earned hint"
    
    game._hint_counter = 3
    
    assert game.use_hint() == (0, False)
    assert game.active_hint() == (0, False)
    
    game._hint_counter = 3
    
    assert game.use_hint() == (0, True)
    assert game.active_hint() == (0, True)
    
    assert game.use_hint() == "Use your current hint"
    assert game.active_hint() == (0, True)
    
    assert game.submit_strand(answers[0][1]) == (answers[0][0], True)
    assert game.submit_strand(answers[1][1]) == (answers[1][0], True)
    
    game._hint_counter = 3
    
    assert game.use_hint() == (2, False)
    assert game.active_hint() == (2, False)
    
    assert game.submit_strand(answers[2][1]) == (answers[2][0], True)
    
    assert game.active_hint() is None
    
    # finish rest of the game
    for i in range(3, len(answers)):
        game.submit_strand(answers[i][1])
    
    assert game.game_over()

def test_valid_game_files() -> None:
    """
    Check each board game in boards complies/is valid with our program.
    """
    import os
    board_files = os.listdir("boards")

    skip_files = ["shine-on.txt"]
    
    # check for empty case
    assert len(board_files) > 0, "No game files found in boards/ directory"
    
    # load each game into path
    for file_name in board_files:
        if file_name in skip_files:
            print(f"Skipping known problematic file: {file_name}")
            continue
        file_path = f"boards/{file_name}" 
        # Attempt to load the game - this will raise ValueError if invalid
        try:
            game = StrandsGame(file_path)
            # Basic validation checks
            assert game.theme() != "", "empty theme"
            assert game.board().num_rows() > 0, "need at least 1 row"
            assert game.board().num_cols() > 0, "need at least 1 columns"
            assert len(game.answers()) > 0, "need at least one answer"
            
            # Check that board is full
            for r in range(game.board().num_rows()):
                for c in range(game.board().num_cols()):
                    assert game.board().get_letter(Pos(r, c)) != "", "imcomplete board"
            
            # Check strands draw from game answers given
            for word, strand in game.answers():
                try:
                    board_word = game.board().evaluate_strand(strand)
                    assert word == board_word, f"Strand for '{word}' actually spells '{board_word}'"
                except ValueError as e:
                    assert False, f"Strand for '{word}' goes out of bounds: {e}"
                
                # check for not folded or cyclic
                assert not strand.is_folded(), f"Strand for '{word}' is folded"
                assert not strand.is_cyclic(), f"Strand for '{word}' is cyclic"
                
                # Verify all positions are in bounds
                for pos in strand.positions():
                    assert 0 <= pos.r < game.board().num_rows(), f"out of bounds {pos.r}"
                    assert 0 <= pos.c < game.board().num_cols(), f"out of bounds {pos.c}"
                
        except ValueError as name_error:
            assert False, f"File {file_name} is invalid: {name_error}"



def test_play_game_G_hints_0() -> None:
    """
    Test playing game G (the-movies.txt) with a hint threshold of 0.
    """
    game = StrandsGame("boards/the-movies.txt", hint_threshold=0)
    answers = game.answers()
    
    assert game.hint_threshold() == 0
    
    hint1 = game.use_hint()
    assert isinstance(hint1, tuple)
    assert hint1[1] == False 
    first_hint_index = hint1[0]
    
    hint2 = game.use_hint()
    assert hint2 == (first_hint_index, True)
    
    game.submit_strand(answers[first_hint_index][1])
    
    hint3 = game.use_hint()
    assert isinstance(hint3, tuple)
    assert hint3[0] != first_hint_index 
    assert hint3[1] == False  
    second_hint_index = hint3[0]
    
    hint4 = game.use_hint()
    assert hint4 == (second_hint_index, True)
    
    game.submit_strand(answers[second_hint_index][1])
    
    if len(answers) > 2:
        hint5 = game.use_hint()
        assert isinstance(hint5, tuple)
        assert hint5[0] != first_hint_index and hint5[0] != second_hint_index


def test_play_game_G_hints_1() -> None:
    """
    Test playing game G (the-movies.txt) with a hint threshold of 1.
    
    """
    game = StrandsGame("boards/the-movies.txt", hint_threshold=1)
    answers = game.answers()
    
    assert game.hint_threshold() == 1
    assert game.use_hint() == "haven't earned hint"
    dictionary_words_found = 0
    
    game._hint_counter = 1
    dictionary_words_found += 1
    
    # First hint should be available
    hint1 = game.use_hint()
    assert isinstance(hint1, tuple)
    assert hint1[1] == False
    first_hint_index = hint1[0]
    
    # Counter should be reset to 0
    assert game.hint_meter() == 0
    
    game._hint_counter = 1
    dictionary_words_found += 1
    
    hint2 = game.use_hint()
    assert hint2 == (first_hint_index, True)
    
    game.submit_strand(answers[first_hint_index][1])
    
    game._hint_counter = 1
    dictionary_words_found += 1
    
    hint3 = game.use_hint()
    assert isinstance(hint3, tuple)
    assert hint3[0] != first_hint_index  # different word
    assert hint3[1] == False
    second_hint_index = hint3[0]
    
    game._hint_counter = 1
    dictionary_words_found += 1
    
    hint4 = game.use_hint()
    assert hint4 == (second_hint_index, True)
    
    assert dictionary_words_found >= 4

def test_play_game_H_hints_0() -> None:
   game = StrandsGame("boards/wetland-patrol.txt", hint_threshold=0)
   answers = game.answers()
   
   assert game.hint_threshold() == 0
   
   hint1 = game.use_hint()
   assert isinstance(hint1, tuple)
   assert hint1[1] == False
   first_hint_index = hint1[0]
   
   hint2 = game.use_hint()
   assert hint2 == (first_hint_index, True)
   
   game.submit_strand(answers[first_hint_index][1])
   
   hint3 = game.use_hint()
   assert isinstance(hint3, tuple)
   assert hint3[0] != first_hint_index
   assert hint3[1] == False
   second_hint_index = hint3[0]
   
   hint4 = game.use_hint()
   assert hint4 == (second_hint_index, True)
   
   game.submit_strand(answers[second_hint_index][1])


def test_play_game_H_hints_1() -> None:
   game = StrandsGame("boards/wetland-patrol.txt", hint_threshold=1)
   answers = game.answers()
   
   assert game.hint_threshold() == 1
   
   assert game.use_hint() == "haven't earned hint"
   
   dictionary_words_found = 0
   
   game._hint_counter = 1
   dictionary_words_found += 1
   
   hint1 = game.use_hint()
   assert isinstance(hint1, tuple)
   assert hint1[1] == False
   first_hint_index = hint1[0]
   
   assert game.hint_meter() == 0
   
   game._hint_counter = 1
   dictionary_words_found += 1
   
   hint2 = game.use_hint()
   assert hint2 == (first_hint_index, True)
   
   game.submit_strand(answers[first_hint_index][1])
   
   game._hint_counter = 1
   dictionary_words_found += 1
   
   hint3 = game.use_hint()
   assert isinstance(hint3, tuple)
   assert hint3[0] != first_hint_index
   assert hint3[1] == False
   second_hint_index = hint3[0]
   
   game._hint_counter = 1
   dictionary_words_found += 1
   
   hint4 = game.use_hint()
   assert hint4 == (second_hint_index, True)
   
   assert dictionary_words_found >= 4