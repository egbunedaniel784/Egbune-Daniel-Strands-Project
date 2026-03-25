import pygame
import sys
import base
import click
import os
import random
import art_gui
from ui import ArtGUIBase, ArtGUIStub, GUIStub
from strands import Pos, StrandsGame, Board, Strand

os.environ['SDL_AUDIODRIVER'] = 'dsp'


ROW_HEIGHT = 70
COL_WIDTH = 70
TEXT_AREA_WIDTH = 300



class gui:

    surface: pygame.Surface
    clock: pygame.time.Clock

    game: "StrandsGame"
    board: "Board"
    positions: list["Pos"]
    total_width: int
    total_height: int
    frame: "ArtGUIStub"

    frame_width: int
    total_frame_width: int

    display_width: int
    display_height: int

    _submission: list["Pos"]
    mode: str
    message: str

    game_started: bool
    score: int
    score_message: str
    score_sign: bool

    def __init__(self, mode: str, file_path: str, hint: int, art: "ArtGuiBase") -> None:
        
        if not mode.lower() in {"play","show"}:
            raise ValueError("Invalid game mode")

        self.mode = mode
        self.game_started = False
        self.game = StrandsGame(file_path,hint)
        self.board = self.game.board()
        self.score = 0

        self.frame = art
        self.total_frame_width = self.frame.frame_width * 2
        self.frame_width = self.frame.frame_width
        self.total_width = self.board.num_cols() * COL_WIDTH + TEXT_AREA_WIDTH + self.total_frame_width
        self.total_height = self.board.num_rows() * ROW_HEIGHT + self.total_frame_width
        self.display_width = self.board.num_cols() * COL_WIDTH + TEXT_AREA_WIDTH
        self.display_height = self.board.num_rows() * ROW_HEIGHT

        self.positions = []

        self._submission = []
        self.message = ""
        self.score_message = ""
        self.score_sign = True

        for row in range(0, self.board.num_rows()):
            for col in range(0, self.board.num_cols()):
                self.positions.append(Pos(row,col))


        pygame.init()
        #pygame.mixer.init()

        #self.click_sound = pygame.mixer.Sound("assets/click.wav")
        #self.success_sound = pygame.mixer.Sound("assets/success.wav")
        pygame.display.set_caption(self.game.theme())
        self.surface = pygame.display.set_mode((self.total_width,self.total_height))
        self.clock = pygame.time.Clock()
        self.change_score(1000,"started game")
        self.run_event_loop()
    
    def change_score(self,num: int, message: str, ) -> None:
        self.score += num
        if self.score < 0: self.score = 0
        

        start = ""
        if num < 0:
            self.score_sign = False
            color_2 = (145, 60, 60)
        else:
            self.score_sign = True
            color_2 = (60, 166, 93)
            start = "+"
        self.score_message = message + ": " + start + str(num)
    
    def render_score(self) -> None:
        msg_1 = "Current Score: " + str(self.score) + " Pts"
        font = pygame.font.Font("assets/DMSerifText-Regular.ttf", 24)
        color = (0,65,168)
        text_image = font.render(msg_1, True, color)
        self.surface.blit(text_image, self.adjust_for_frame((18,148)))

        start = ""
        if not self.score_sign:
            color_2 = (145, 60, 60)
        else:
            self.score_sign = True
            color_2 = (60, 166, 93)
            start = "+"
        text_image = font.render(self.score_message, True, color_2)
        self.surface.blit(text_image, self.adjust_for_frame((18,176)))



    def use_hint(self) -> None:
        if not self.game_started: return
        result = self.game.use_hint()
        if isinstance(result, tuple):
            self.change_score(-50,"used hint")
            pass
        else:
            self.message = result

    def submit_strand(self) -> None:
        if not self.game_started: return
        start = self._submission[0]
        steps = []
        old = start
        for num in range(1,len(self._submission)):
            steps.append(old.step_to(self._submission[num]))
            old = self._submission[num]

        strand = Strand(start,steps)
        result = self.game.submit_strand(strand)
        if isinstance(result,tuple):
            pass
            #pygame.mixer.Sound.play(self.success_sound)
            if result[1] == True:
                self.change_score(100,"correct guess")
            else:
                
                self.change_score(50,"dictionary word")
        else:
            self.message = result
            self.change_score(-25,"incorrect guess")
        self.clear_selection()

    def clear_selection(self) -> None:
        self._submission = []

    def click(self, board_location: tuple[int,int]) -> None:
        if not self.game_started: return
        #pygame.mixer.Sound.play(self.click_sound)
        p = self.board_location_to_position(board_location)
        pos = Pos(p[0],p[1])
        if pos.r < 0 or pos.r > self.board.num_rows():
            return
        if pos.c < 0 or pos.c > self.board.num_cols():
            return

        if len(self._submission) == 0:
            self._submission.append(pos)
        else:
            #check if pos was already in submission
            if pos in self._submission:
                #if it was last selected, we submit strand
                if pos == self._submission[-1:][0]:
                    self.submit_strand()
                else:     
                    #else, truncate selection, up to and including pos
                    new_submission = []
                    for current_pos in self._submission:
                        new_submission.append(current_pos)
                        if current_pos == pos:
                            break
                    self._submission = new_submission
            else:
                #it's a new pos, so we check if it's one away
                if pos.is_adjacent_to(self._submission[-1:][0]):
                    #add it to submission
                    self._submission.append(pos)
                else:
                    #clear selection
                    self.clear_selection()

    def run_event_loop(self) -> None:
        while True:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_h:
                        self.use_hint()
                    if event.key == pygame.K_RETURN and self.mode == "play":
                        self.game_started = True
                    if event.key == pygame.K_ESCAPE and self.mode == "play":
                        self.clear_selection()
                elif event.type == pygame.MOUSEBUTTONUP and self.mode == "play":
                    self.click(event.pos)
                else:
                    pass
            if self.game.game_over():
                print("Game Over! You Won!")
                print("Score:", self.score, "Pts")
                pygame.quit()
                sys.exit()
            self.draw_window()
            self.clock.tick(24)
    
    def draw_window(self) -> None:
        
        self.frame.draw_background(self.surface)
        #self.surface.fill((245, 245, 245))
        pygame.draw.rect(
            self.surface, color=(245, 245, 245), rect=(self.frame_width, 
            self.frame_width, self.display_width, self.display_height)
        )
        if self.game_started:
            self.render_text()
            self.render_board()
            self.render_score()
        else:
            self.render_title_screen()

        pygame.display.update()
    
    def render_title_screen(self) -> None:
        game_name_msg = "STRANDS"
        font = pygame.font.Font("assets/DMSerifText-Regular.ttf", 70)
        color = (0,65,168)
        text_image = font.render(game_name_msg, True, color)
        w = self.total_width // 2 - 160
        h = self.total_height // 2 - 80
        self.surface.blit(text_image, (w,h))

        press_enter_msg = "press enter to start"
        font = pygame.font.Font("assets/DMSerifText-Regular.ttf", 24)
        text_image_2 = font.render(press_enter_msg, True, color)
        w_2 = w + 45
        h_2 = self.total_height // 2 
        self.surface.blit(text_image_2, (w_2,h_2))


    def adjust_for_frame(self, pos: tuple[int,int], flip: bool = False) -> tuple[int,int]:
        if flip:
            return (pos[0] - self.frame_width, pos[1] - self.frame_width)
        else:
            return (pos[0] + self.frame_width, pos[1] + self.frame_width)


    def render_text(self) -> None:
        game_name_msg = "STRANDS!"
        font = pygame.font.Font("assets/DMSerifText-Regular.ttf", 50)
        color = (0,65,168)
        text_image = font.render(game_name_msg, True, color)
        self.surface.blit(text_image, self.adjust_for_frame((18,5)))

        num_words_found = len(self.game.found_strands())
        num_words = len(self.game.answers())
        game_progress_msg = f"Found {num_words_found}/{num_words} words!"

        font = pygame.font.Font("assets/DMSerifText-Regular.ttf", 24)
        text_image_2 = font.render(game_progress_msg, True, color)
        self.surface.blit(text_image_2, self.adjust_for_frame((18,65)))

        hint_msg = f"Hint Meter: {self.game.hint_meter()}/{self.game.hint_threshold()}"

        text_image_3 = font.render(hint_msg, True, color)
        self.surface.blit(text_image_3, self.adjust_for_frame((18,92)))

        general_msg = self.message
        text_image_4 = font.render(general_msg, True, color)
        self.surface.blit(text_image_4, self.adjust_for_frame((18,120)))

    def position_to_board_location(self,pos: tuple[int,int]) -> tuple[int, int]:
        x = TEXT_AREA_WIDTH + (pos[0] * COL_WIDTH) + round(.5*COL_WIDTH)
        y = (pos[1] * ROW_HEIGHT) + round(.5*ROW_HEIGHT)
        return self.adjust_for_frame((x,y))

    def board_location_to_position(self, location: tuple[int,int]) -> tuple[int,int]:
        location = self.adjust_for_frame(location,True)
        y = round((location[0] - TEXT_AREA_WIDTH - round(.5*COL_WIDTH)) / COL_WIDTH)
        x = round((location[1] - round(.5*ROW_HEIGHT)) / ROW_HEIGHT)
        return (x,y)

    def draw_position(self, pos: "Pos", color: tuple[int,int,int]=(0,0,0), border: int = 0) -> None:
        location = self.position_to_board_location((pos.c,pos.r))
        pygame.draw.circle(self.surface, color, center=location,radius=30, width=border)
        letter = self.board.get_letter(pos)

        font = pygame.font.Font("assets/initial.ttf", 35)
        color = (125, 175, 255)
        text_image = font.render(letter, True, color)
        self.surface.blit(text_image, (location[0]-15,location[1]-15))

    def draw_line(self, start: "Pos", end:"Pos", color: tuple[int,int,int] = (0,0,0)) -> None:
        start_loc = self.position_to_board_location((start.c,start.r))
        end_loc = self.position_to_board_location((end.c,end.r))
        pygame.draw.line(self.surface, color, start_loc,end_loc,20)

    def render_board(self) -> None:
        for pos in self.positions:
            self.draw_position(pos)
        
        color = (16, 76, 173)
        if self.mode == "play":
            found_strands = self.game.found_strands()
            #render found strands
            for strand in found_strands:
                old = strand.start
                for pos in strand.positions():
                    self.draw_line(old,pos,(16,30,145))
                    old = pos
                for pos2 in strand.positions():
                    self.draw_position(pos2,color)
            #render hint, if applicable
            hint = self.game.active_hint()
            if isinstance(hint, tuple):
                hint_word, hint_strand = self.game.answers()[hint[0]]
                for pos in hint_strand.positions():
                    self.draw_position(pos,(235, 210, 52), 4)
                if hint[1] == True:
                    start_pos = hint_strand.positions()[0]
                    end_pos = hint_strand.positions()[-1:][0]
                    self.draw_position(start_pos,(235, 210, 52))
                    self.draw_position(end_pos,(235, 210, 52))
            #render selected strand
            oldpos = None
            for pos in self._submission:
                if oldpos != None:
                    self.draw_line(oldpos,pos,(125, 175, 255))
                oldpos = pos
            for pos in self._submission:
                self.draw_position(pos)
                self.draw_position(pos,(125, 175, 255), 4)
            

        elif self.mode == "show":
            found_strands = self.game.answers()
            for word, strand in found_strands:
                old = strand.start
                for pos in strand.positions():
                    self.draw_line(old,pos,(16,30,145))
                    old = pos
                for pos2 in strand.positions():
                    self.draw_position(pos2,color)


def get_frame(name:str) -> "ArtGuiBase":
    if name == "cat1":
        return None
    elif name == "cat2":
        return art_gui.ArtGUIPlaid(25)
    elif name == "cat3":
        return art_gui.ArtGUIHoneycomb(25)
    elif name == "cat4":
        return art_gui.ArtGUIBinaryTree(25)
    elif name == "9slices":
        return art_gui.ArtGUI9Slice(25)
    else:
        return None

@click.command("Strands")
@click.option("--show",is_flag=True)
@click.option("-g","--game")
@click.option("-h","--hint",type=int, default=3)
@click.option("-a","--art")
def cmd(show, game, hint, art):
    if game: 
        game_file_path = "boards/" + game + ".txt"
    else: 
        num = random.randint(0,30)
        game_file_path = "boards/" + os.listdir("boards")[num]
        print(game_file_path)
    
    if art:
        frame = get_frame(art)
        if not frame:
            print("frame not supported")
            sys.exit()
    else:
        frame = ArtGUIStub(25)

    if show:
        mode = "show"
    else:
        mode = "play"

    gui(mode,game_file_path,hint,frame)


if __name__ == "__main__":
    cmd()


    