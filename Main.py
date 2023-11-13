import pygame
import random


# Configuración de la ventana de juego
WIDTH, HEIGHT = 300, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Definir las piezas (tetriminos)
tetriminos = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]]
]

# Función para rotar una pieza
def rotate_piece(piece):
    return [[piece[y][x] for y in range(len(piece))] for x in range(len(piece[0]) - 1, -1, -1)]

# Función para dibujar una pieza
def draw_piece(piece, x, y):
    for row in range(len(piece)):
        for col in range(len(piece[row])):
            if piece[row][col]:
                pygame.draw.rect(WINDOW, WHITE, (x + col * 30, y + row * 30, 30, 30))

# Función para verificar colisiones
def has_collision(piece, x, y, placed_pieces):
    for row in range(len(piece)):
        for col in range(len(piece[row])):
            if piece[row][col]:
                if x + col * 30 < 0 or x + col * 30 >= WIDTH or y + row * 30 >= HEIGHT or (x + col * 30, y + row * 30) in placed_pieces:
                    return True
    return False

# Función para crear una nueva pieza
def new_piece():
    return {
        'piece': random.choice(tetriminos),
        'x': WIDTH // 2,
        'y': 0,
        'rotation': 0,
        'static': False
    }

# Función para verificar si una pieza ha alcanzado el suelo
def has_landed(piece, x, y, placed_pieces):
    for row in range(len(piece)):
        for col in range(len(piece[row])):
            if piece[row][col]:
                if y + row * 30 >= HEIGHT - 30 or (x + col * 30, y + (row + 1) * 30) in placed_pieces:
                    return True
    return False

# Lógica del juego
def main():
    pygame.init()
    clock = pygame.time.Clock()
    current_piece = new_piece()
    fall_speed = 1  # Velocidad de caída inicial
    placed_pieces = set()  # Conjunto para registrar las celdas ocupadas

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if not current_piece['static']:
            if keys[pygame.K_LEFT] and not has_collision(current_piece['piece'], current_piece['x'] - 30, current_piece['y'], placed_pieces):
                current_piece['x'] -= 30
            if keys[pygame.K_RIGHT] and not has_collision(current_piece['piece'], current_piece['x'] + 30, current_piece['y'], placed_pieces):
                current_piece['x'] += 30
            if keys[pygame.K_DOWN]:
                current_piece['y'] += 30
            if keys[pygame.K_UP]:
                # Solo rota si la pieza no está estática
                new_rotated_piece = rotate_piece(current_piece['piece'])
                if not has_collision(new_rotated_piece, current_piece['x'], current_piece['y'], placed_pieces):
                    current_piece['piece'] = new_rotated_piece

        # Verificar si la pieza ha alcanzado el suelo
        if not current_piece['static'] and (has_landed(current_piece['piece'], current_piece['x'], current_piece['y'], placed_pieces) or has_collision(current_piece['piece'], current_piece['x'], current_piece['y'], placed_pieces)):
            # Fija la pieza en su posición actual y agrega sus coordenadas al conjunto
            for row in range(len(current_piece['piece'])):
                for col in range(len(current_piece['piece'][row])):
                    if current_piece['piece'][row][col]:
                        placed_pieces.add((current_piece['x'] + col * 30, current_piece['y'] + row * 30))
            # Obtener una nueva pieza aleatoria
            current_piece = new_piece()
            # Reinicia el conjunto de celdas ocupadas si es necesario
            if has_collision(current_piece['piece'], current_piece['x'], current_piece['y'], placed_pieces):
                placed_pieces = set()

        # Actualizar la posición vertical de la pieza (caída automática)
        if not current_piece['static']:
            current_piece['y'] += fall_speed * 30

        WINDOW.fill(BLACK)
        draw_piece(current_piece['piece'], current_piece['x'], current_piece['y'])
        # Dibuja las piezas colocadas
        for px, py in placed_pieces:
            pygame.draw.rect(WINDOW, WHITE, (px, py, 30, 30))
        pygame.display.update()
        clock.tick(5)

if __name__ == "__main__":
    main()
