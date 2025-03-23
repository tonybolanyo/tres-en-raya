import pygame as pg

pg.init()

WINDOW_SIZE = (490, 550)
C_BACKGROUND = (20, 20, 20)
C_TEXT = (255, 255, 100)
FPS = 60

BOARD_SIZE = 450
BOARD_MARGIN = 20

CELL_SIZE = 150
CELL_PADDING = 50
LINE_WIDTH = 5
C_LINES = (150, 150, 150)

CROSS = 'X'
CROSS_LINE = 12
C_CROSS = (200, 100, 0)

CIRCLE = 'O'
CIRCLE_LINE = 8
C_CIRCLE = (0, 0, 200)

class TicTacToe:

    def __init__(self):
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        pg.display.set_caption('Tres en Raya')
        self.clock = pg.time.Clock()
        self.font = pg.font.Font(None, 60)

        self.background_color = C_BACKGROUND
        self.line_color = C_LINES
        self.x_color = C_CROSS
        self.o_color = C_CIRCLE

        self.reset()        

    def draw_board(self):
        self.screen.fill(self.background_color)
        for i in range(1, 3):
            distance = i * CELL_SIZE + BOARD_MARGIN
            pg.draw.line(
                self.screen, self.line_color,
                (distance, BOARD_MARGIN),
                (distance, BOARD_SIZE + BOARD_MARGIN),
                LINE_WIDTH)
            pg.draw.line(
                self.screen, self.line_color,
                (BOARD_MARGIN, distance),
                (BOARD_SIZE + BOARD_MARGIN, distance),
                LINE_WIDTH)
        
        for i in range(3):      # fila
            for j in range(3):  # columna
                index = i * 3 + j
                y = BOARD_MARGIN + BOARD_SIZE - i * CELL_SIZE - CELL_SIZE // 2
                if self.board[index] == CROSS:
                    x = BOARD_MARGIN + j * CELL_SIZE + CELL_SIZE // 2
                    left = x - CELL_PADDING
                    right = x + CELL_PADDING
                    top = y - CELL_PADDING
                    bottom = y + CELL_PADDING
                    pg.draw.line(
                        self.screen, self.x_color,
                        (left, top), (right, bottom),
                        CROSS_LINE)
                    pg.draw.line(
                        self.screen, self.x_color,
                        (right, top), (left, bottom),
                        CROSS_LINE)
                elif self.board[index] == CIRCLE:
                    x = BOARD_MARGIN + j * CELL_SIZE + CELL_SIZE // 2
                    pg.draw.circle(
                        self.screen, self.o_color,
                        (x, y), CELL_PADDING, CIRCLE_LINE)

    def make_move(self, position):
        if self.board[position] == '' and not self.game_over:
            self.board[position] = self.current_player
            self.check_winner()
            if self.current_player == CROSS:
                self.current_player = CIRCLE
            else:
                self.current_player = CROSS

    def check_winner(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontales
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Verticales
            [0, 4, 8], [2, 4, 6]              # Diagonales
        ]
        
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != '':
                self.winner = self.board[combo[0]]
                self.game_over = True
                return
        
        if '' not in self.board:
            self.game_over = True

    def reset(self):
        self.board = ['' for _ in range(9)]
        self.current_player = CROSS
        self.winner = None
        self.game_over = False

    def draw_status(self):
        if self.game_over:
            if self.winner:
              text = f'¡{self.winner} gana!'
            else:
              text = '¡Empate!'
        else:
            text = f'Turno para {self.current_player}'

        text_surface = self.font.render(text, True, C_TEXT, C_BACKGROUND)
        board_size = BOARD_SIZE + BOARD_MARGIN * 2
        x = WINDOW_SIZE[0] // 2
        y = WINDOW_SIZE[1] - CELL_PADDING // 2
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def play(self):
        playing = True

        while playing:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    playing = False
                if event.type == pg.KEYDOWN:
                    code = event.unicode
                    if event.key == pg.K_ESCAPE:
                        playing = False
                    if event.key == pg.K_r:
                        game.reset()
                    if code in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        number = int(code) - 1
                        position = number
                        game.make_move(position)
                if event.type == pg.MOUSEBUTTONDOWN and not game.game_over:
                    x, y = event.pos
                    if x < BOARD_SIZE and y < BOARD_SIZE:
                        col = x // CELL_SIZE
                        row = (BOARD_SIZE - y) // CELL_SIZE
                        position = row * 3 + col
                        game.make_move(position)

            game.draw_board()
            game.draw_status()
            pg.display.flip()
        
        pg.quit()

if __name__ == "__main__":
    game = TicTacToe()
    game.play()

