# This code is modified from: https://github.com/nikolockenvitz/2048/blob/master/2048.py
from tkinter import *
from tkinter import messagebox
from math import log2
from env import game

KEYS_UP = ["Up"]
KEYS_RIGHT = ["Right"]
KEYS_DOWN = ["Down"]
KEYS_LEFT = ["Left"]


BG = "#776e65"
BG_END_OF_GAME = "#edc22e"
FONT_FIELD = ["Consolas", "18", "bold"]
FONT_TEXT = ["Consolas", "16"]
FONT_2048 = ["Consolas", "64"]
FG_2048 = "#50d1f5"

DEFAULT_DESIGN = [[0, "#000000", "#aa9898"],  # -
                  [1, "#776e65", "#eee4da"],  # 2
                  [2, "#776e65", "#ede0c8"],  # 4
                  [3, "#f9f6f2", "#f2b179"],  # 8
                  [4, "#f9f6f2", "#f59563"],  # 16
                  [5, "#f9f6f2", "#f67c5f"],  # 32
                  [6, "#f9f6f2", "#f65e3b"],  # 64
                  [7, "#f9f6f2", "#edcf72"],  # 128
                  [8, "#f9f6f2", "#edcc61"],  # 256
                  [9, "#f9f6f2", "#edc850"],  # 512
                  [10, "#f9f6f2", "#edc53f"],  # 1024
                  [11, "#f9f6f2", "#edc22e"],  # 2048
                  [12, "#ffffff", "#50d1f5"],  # 4096
                  [13, "#ffffff", "#7070ee"],  # 8192
                  [14, "#ffffff", "#4040ee"],  # 16384
                  [15, "#ffffff", "#484e4d"],  # 32768
                  [16, "#ffffff", "#403635"],  # 65536
                  [17, "#ffffff", "#201818"]]  # 131072

DEFAULT_WIDTH_WINDOW = 740

GRID_COLUMNS = 37
GRID_ROWS = 25
GRID_UNIT = 20


class UI:
    """
    Class UI
    This class implements the frontend using tkinter.
    """
    def __init__(self):

        # set keys
        self.keys = [KEYS_UP, KEYS_RIGHT,
                     KEYS_DOWN, KEYS_LEFT]

        # set colours for tiles: [ [exponent, fg, bg], ... ]
        self.colours = DEFAULT_DESIGN

        # colours and fonts
        self.bg = BG
        self.bgEndOfGame = BG_END_OF_GAME
        self.fontFields = FONT_FIELD
        self.fontText = FONT_TEXT
        self.font2048 = FONT_2048
        self.fg2048 = FG_2048

        # create a game instance
        self.game = game.Game()

        # create window
        self.root = Tk()
        self.root.config(bg=self.bg)
        self.root.title("2048")

        # init grid
        self.unit = GRID_UNIT
        self.width = 0
        self.height = 0

        # get coefficient for fonts (dependency between font size and grid unit)
        self.coefficientFontFields = int(self.fontFields[1]) / self.unit
        self.coefficientFontText = int(self.fontText[1]) / self.unit
        self.coefficientFont2048 = int(self.font2048[1]) / self.unit

        # initialize window
        self.create_ui_elements()
        self.set_window_size()
        self.show()

        # bindings
        self.root.bind("<Enter>", self.adjust_window_to_current_width)
        self.root.bind("<Configure>", self.adjust_window_to_current_state)
        self.root.bind("<Key>", self.key_pressed)

        # call function to close gracefully
        self.root.protocol("WM_DELETE_WINDOW", self.root_destroy)

    def destroy(self):
        self.root.destroy()

    def adjust_window_to_current_state(self, event=None):
        """
        When state of window changes (normal <-> zoomed) the content has to
        be adjusted. Either default width or maximum width.
        """
        # zoomed to normal
        if((self.unit == self.root.winfo_screenheight()//GRID_ROWS-2 or
            self.unit == self.root.winfo_screenwidth()//GRID_COLUMNS) and
           self.root.state() == "normal"):
            width = DEFAULT_WIDTH_WINDOW
            self.set_window_size(width)
        # normal to zoomed
        if(not (self.unit == self.root.winfo_screenheight()//GRID_ROWS-2 or
                self.unit == self.root.winfo_screenwidth()//GRID_COLUMNS) and
           self.root.state() == "zoomed"):
            width = self.root.winfo_screenwidth()
            self.set_window_size(width)

    def adjust_window_to_current_width(self, event=None):
        """
        After the user changed the window size, the window will be resized
        to new width (which includes size of content). The size of the
        window will not really change but the size of content.
        """
        width = self.root.winfo_width()
        self.set_window_size(width)

    def set_window_size(self, width=DEFAULT_WIDTH_WINDOW):
        """
        This function resizes the window. Depending on parameter "width" the
        size of a unit (in grid) is calculated. One unit should be at least
        5 pixels (which is actually very small, but must not be larger than
        possible. That means a maximum value for one unit is calculated
        depending on screen size and grid size. (Also some space for task bar
        should be available)
        When maximum unit size is reached the window will automatically switch
        to full screen (zoomed state).
        When window size has to be changed, also all elements in UI have to be
        adjusted.
        """
        # calculate unit, width and height
        self.unit = min(max(5, width // GRID_COLUMNS),
                        self.root.winfo_screenheight()//GRID_ROWS-2,
                        self.root.winfo_screenwidth()//GRID_COLUMNS)
        width = GRID_COLUMNS * self.unit
        height = GRID_ROWS * self.unit

        # set state of window (zoomed/normal)
        if(self.unit == self.root.winfo_screenheight()//GRID_ROWS-2 or
           self.unit == self.root.winfo_screenwidth()//GRID_COLUMNS):
            # max value -> full screen / zoomed
            self.root.state("zoomed")
        else:
            self.root.state("normal")

        # update window (also UI-elements if changed)
        if width != self.width or height != self.height:
            size = str(width) + "x" + str(height)
            self.root.geometry(size)
            self.width = width
            self.height = height
            self.hide_ui_elements()
            self.show_ui_elements()

    def label_field(self):
        """
        Factory method to create a field/tile containing the numbers.
        """
        return Label(self.root,
                     text="",
                     anchor=CENTER,
                     font=self.fontFields)

    def label_text(self, text=""):
        """
        Factory method to create a text label.
        """
        return Label(self.root,
                     text=text,
                     bg=self.bg,
                     font=self.fontText,
                     fg="#ffffff")

    def update_font_size(self):
        """
        This function updates all font sizes (depending on new size of grid unit)
        and labels.
        """
        self.fontFields[1] = int(self.coefficientFontFields * self.unit)
        self.fontText[1] = int(self.coefficientFontText * self.unit)
        self.font2048[1] = int(self.coefficientFont2048 * self.unit)

        for label in self.listLabels:
            label.config(font=self.fontText)

        self.label2048.config(font=self.font2048)

        for fields in self.field:
            for field in fields:
                field.config(font=self.fontFields)

    def show_ui_elements(self):
        """
        Labels and number fields are placed at their posiiton depending on grid.
        Afterwards fonts and content will be updated.
        """
        for i in range(4):
            self.listLabels[i].place(x=26 * self.unit,
                                     y=(6*i+1)*self.unit,
                                     width=9*self.unit,
                                     height=5*self.unit)

        for y in range(4):
            for x in range(4):
                self.field[y][x].place(x=6*self.unit*x+self.unit,
                                       y=6*self.unit*y+self.unit,
                                       width=5*self.unit,
                                       height=5*self.unit)

        self.update_font_size()
        self.show()

    def hide_ui_elements(self):
        """
        During resize old labels and fields have to be removed.
        """
        for label in self.listLabels:
            label.place_forget()

        for fields in self.field:
            for field in fields:
                field.place_forget()

    def create_ui_elements(self):
        """
        This function creates all number fields and labels and sets up general
        settings for these (text, fonts, colours, bindings).
        """
        self.labelScore = self.label_text()
        self.labelHighScore = self.label_text()

        self.label2048 = Label(self.root,
                               text="2048",
                               bg=self.bg,
                               font=self.font2048,
                               fg=self.fg2048)

        self.labelNewGame = self.label_text("New Game")
        self.labelNewGame.config(relief=RIDGE)
        self.labelNewGame.bind("<Button-1>", self.new_game)

        self.listLabels = [self.labelScore,
                           self.labelHighScore,
                           self.label2048,
                           self.labelNewGame]

        self.field00 = self.label_field()
        self.field01 = self.label_field()
        self.field02 = self.label_field()
        self.field03 = self.label_field()

        self.field10 = self.label_field()
        self.field11 = self.label_field()
        self.field12 = self.label_field()
        self.field13 = self.label_field()

        self.field20 = self.label_field()
        self.field21 = self.label_field()
        self.field22 = self.label_field()
        self.field23 = self.label_field()

        self.field30 = self.label_field()
        self.field31 = self.label_field()
        self.field32 = self.label_field()
        self.field33 = self.label_field()

        self.field = [[self.field00, self.field01, self.field02, self.field03],
                      [self.field10, self.field11, self.field12, self.field13],
                      [self.field20, self.field21, self.field22, self.field23],
                      [self.field30, self.field31, self.field32, self.field33]]

        self.show_ui_elements()

    def confirm_action(self, msgboxHeading, msgboxText):
        """
        Critical actions need to be confirmed. This functions creates a
        message box to ask the user whether he is sure to continue.
        This will only happen if game is not finished, otherwise the action
        can continue (because a finished game is not supposed to be critical).
        """
        if not self.game.is_finished():
            # game is not finished yet
            answer = messagebox.askyesno(msgboxHeading,
                                         msgboxText)
            return answer

        # return True per default when game is finished
        return True

    def root_destroy(self, event=None):
        """
        This functions closes the window gracefully when confirmed again.
        """
        if self.confirm_action("Quit?", "Do you really want to quit?"):
            # self.game.writeHighScore()
            self.root.destroy()

    def new_game(self, event=None):
        """
        After confirming this action, old game will be saved and a new game
        will be created. Afterwards UI has to be updated.
        """
        if self.confirm_action("New Game?",
                               "Do you really want to start a new game?"):
            # self.game.writeHighScore()
            self.game.new_game()
            self.show()

    def key_pressed(self, event):
        """
        When a key is pressed, it will check whether pressed key should
        trigger a move.
        Also some additional keys for resize etc. can be processed here.
        """
        for direction in range(4):
            if event.keysym in self.keys[direction]:
                self.game.move(direction)
                self.show()
                return

    def get_colours(self, number):
        """
        This functions returns a list [exponent, fg, bg] for passed number.
        """
        if number <= 0:
            number = 1
        ix = int(log2(number))
        return self.colours[ix]

    def show(self):
        """
        This function updates content and appearence of fields.
        Also current score and highscore are shown. Depending on current game
        status (finished or not) the background colour is adjusted.
        """
        for y in range(4):
            for x in range(4):
                current_number = self.game.field[y][x]
                colours = self.get_colours(current_number)
                self.field[y][x].config(fg=colours[1], bg=colours[2])
                if current_number:
                    self.field[y][x]["text"] = current_number
                else:
                    self.field[y][x]["text"] = ""

        self.labelScore["text"] = "Score:\n" + str(self.game.score)

        is_finished = self.game.is_finished()
        if is_finished:
            for element in [self.root] + self.listLabels:
                element.config(bg=self.bgEndOfGame)
        else:
            for element in [self.root] + self.listLabels:
                element.config(bg=self.bg)

        self.root.update()


if __name__ == "__main__":
    gui = UI()
    gui.root.mainloop()
