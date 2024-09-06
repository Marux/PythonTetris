import pygame
import random

# Configuración de la ventana de juego
WIDTH, HEIGHT = 300, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Definir las piezas (tetriminos)
TETRIMINOS = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]]
]

class Tetris:
    def __init__(self):
        pygame.init()
        self.width = WIDTH
        self.height = HEIGHT
        self.window = WINDOW
        self.clock = pygame.time.Clock()
        self.fall_speed = 1
        self.placed_pieces = set()
        self.board = [[0 for _ in range(self.width // 30)] for _ in range(self.height // 30)]
        self.current_piece = self.new_piece()
        self.running = True
        self.game_over = False

    def new_piece(self):
        piece = {
            'piece': random.choice(TETRIMINOS),
            'x': self.width // 2 // 30 * 30,
            'y': 0,
            'rotation': 0,
            'static': False
        }
        if self.has_collision(piece['piece'], piece['x'], piece['y']):
            self.game_over = True
        return piece

    def rotate_piece(self, piece):
        return [[piece[y][x] for y in range(len(piece))] for x in range(len(piece[0]) - 1, -1, -1)]

    def draw_piece(self, piece, x, y):
        for row in range(len(piece)):
            for col in range(len(piece[row])):
                if piece[row][col]:
                    pygame.draw.rect(self.window, WHITE, (x + col * 30, y + row * 30, 30, 30))

    def has_collision(self, piece, x, y):
        for row in range(len(piece)):
            for col in range(len(piece[row])):
                if piece[row][col]:
                    if x + col * 30 < 0 or x + col * 30 >= self.width or y + row * 30 >= self.height or self.board[(y // 30) + row][(x // 30) + col]:
                        return True
        return False

    def has_landed(self, piece, x, y):
        for row in range(len(piece)):
            for col in range(len(piece[row])):
                if piece[row][col]:
                    if y + row * 30 >= self.height - 30 or self.board[(y // 30) + row + 1][(x // 30) + col]:
                        return True
        return False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if not self.current_piece['static']:
            if keys[pygame.K_LEFT] and not self.has_collision(self.current_piece['piece'], self.current_piece['x'] - 30, self.current_piece['y']):
                self.current_piece['x'] -= 30
            if keys[pygame.K_RIGHT] and not self.has_collision(self.current_piece['piece'], self.current_piece['x'] + 30, self.current_piece['y']):
                self.current_piece['x'] += 30
            if keys[pygame.K_DOWN]:
                self.current_piece['y'] += 30
            if keys[pygame.K_UP]:
                new_rotated_piece = self.rotate_piece(self.current_piece['piece'])
                if not self.has_collision(new_rotated_piece, self.current_piece['x'], self.current_piece['y']):
                    self.current_piece['piece'] = new_rotated_piece

    def update(self):
        if not self.current_piece['static'] and (self.has_landed(self.current_piece['piece'], self.current_piece['x'], self.current_piece['y']) or self.has_collision(self.current_piece['piece'], self.current_piece['x'], self.current_piece['y'])):
            for row in range(len(self.current_piece['piece'])):
                for col in range(len(self.current_piece['piece'][row])):
                    if self.current_piece['piece'][row][col]:
                        board_row = (self.current_piece['y'] // 30) + row
                        board_col = (self.current_piece['x'] // 30) + col
                        if 0 <= board_row < len(self.board) and 0 <= board_col < len(self.board[0]):
                            self.board[board_row][board_col] = 1
            self.clear_lines()
            self.current_piece = self.new_piece()
            if self.has_collision(self.current_piece['piece'], self.current_piece['x'], self.current_piece['y']):
                self.placed_pieces = set()

        if not self.current_piece['static']:
            self.current_piece['y'] += self.fall_speed * 30

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = len(self.board) - len(new_board)
        self.board = [[0 for _ in range(self.width // 30)] for _ in range(lines_cleared)] + new_board

    def draw(self):
        self.window.fill(BLACK)
        self.draw_piece(self.current_piece['piece'], self.current_piece['x'], self.current_piece['y'])
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col]:
                    pygame.draw.rect(self.window, WHITE, (col * 30, row * 30, 30, 30))
        if self.game_over:
            font = pygame.font.SysFont('Arial', 30)
            text_surface = font.render('Game Over', True, RED)
            self.window.blit(text_surface, (self.width // 4, self.height // 2))
        pygame.display.update()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if not self.game_over:
                self.handle_input()
                self.update()
            self.draw()
            self.clock.tick(5)

        pygame.quit()

if __name__ == "__main__":
    game = Tetris()
    game.run()