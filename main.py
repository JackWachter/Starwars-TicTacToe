import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)
WHITE = (255, 255, 255)
BUTTON_COLOR = (44, 62, 80)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Load Sounds (dummy sounds for example)
x_sound = pygame.mixer.Sound('x_sound.wav')
o_sound = pygame.mixer.Sound('o_sound.wav')

# Load Background Image (dummy image for example)
background_image = pygame.image.load('star_wars_background.jpg')

# Load Font (dummy font for example)
font = pygame.font.Font('Starjedi.ttf', 40)
font_small = pygame.font.Font('Starjedi.ttf', 20)

# Initialize Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Star Wars Tic-Tac-Toe')

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Player Names
player_X_name = input("Enter the name of player X: ")
player_O_name = input("Enter the name of player O: ")

# Button Constants
BUTTON_WIDTH, BUTTON_HEIGHT = 140, 50
PLAY_AGAIN_BUTTON_POS = (WIDTH // 2 - BUTTON_WIDTH - 20, HEIGHT // 2 + 20)
QUIT_BUTTON_POS = (WIDTH // 2 + 20, HEIGHT // 2 + 20)
PLAY_AGAIN_TEXT = "Play Again"
QUIT_TEXT = "Quit"

# Draw Lines
def draw_lines():
    screen.blit(background_image, (0, 0))
    # Horizontal
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), 15)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), 15)
    # Vertical
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), 15)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), 15)

# Animate Move
def animate_move(row, col, player):
    start_time = time.time()
    duration = 0.5  # Animation duration in seconds
    initial_scale = 0.1
    final_scale = 1.0

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break

        scale = initial_scale + (final_scale - initial_scale) * (elapsed_time / duration)
        screen.blit(background_image, (0, 0))
        draw_lines()
        draw_figures(exclude=(row, col))

        center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
        center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
        size = int(60 * scale)

        if player == 'X':
            draw_scaled_cross(center_x, center_y, size)
        elif player == 'O':
            pygame.draw.circle(screen, CIRCLE_COLOR, 
                               (center_x, center_y), size, 15)

        pygame.display.update()

    if player == 'X':
        x_sound.play()
    else:
        o_sound.play()

# Draw Scaled Cross
def draw_scaled_cross(center_x, center_y, size):
    half_size = size // 2
    pygame.draw.line(screen, CROSS_COLOR, (center_x - half_size, center_y - half_size),
                     (center_x + half_size, center_y + half_size), 15)
    pygame.draw.line(screen, CROSS_COLOR, (center_x - half_size, center_y + half_size),
                     (center_x + half_size, center_y - half_size), 15)

# Draw Figures
def draw_figures(exclude=None):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if (row, col) == exclude:
                continue
            if board[row][col] == 'X':
                draw_scaled_cross(col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                  row * SQUARE_SIZE + SQUARE_SIZE // 2, 60)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, 
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, 
                                    row * SQUARE_SIZE + SQUARE_SIZE // 2), 60, 15)

# Check Win
def check_win(player):
    # Vertical Win Check
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            animate_winning_line('vertical', col, player)
            return True

    # Horizontal Win Check
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            animate_winning_line('horizontal', row, player)
            return True

    # Ascending Diagonal Win Check
    if board[2][0] == board[1][1] == board[0][2] == player:
        animate_winning_line('asc_diagonal', None, player)
        return True

    # Descending Diagonal Win Check
    if board[0][0] == board[1][1] == board[2][2] == player:
        animate_winning_line('desc_diagonal', None, player)
        return True

    return False

# Animate Winning Line
def animate_winning_line(direction, index, player):
    start_time = time.time()
    duration = 1.0  # Animation duration in seconds
    color = CIRCLE_COLOR if player == 'O' else CROSS_COLOR

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break

        progress = elapsed_time / duration
        screen.blit(background_image, (0, 0))
        draw_lines()
        draw_figures()

        if direction == 'vertical':
            posX = index * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.line(screen, color, (posX, 15), 
                             (posX, int(HEIGHT * progress)), 15)
        elif direction == 'horizontal':
            posY = index * SQUARE_SIZE + SQUARE_SIZE // 2
            pygame.draw.line(screen, color, (15, posY), 
                             (int(WIDTH * progress), posY), 15)
        elif direction == 'asc_diagonal':
            pygame.draw.line(screen, color, (15, HEIGHT - 15), 
                             (int(WIDTH * progress), HEIGHT - int(HEIGHT * progress)), 15)
        elif direction == 'desc_diagonal':
            pygame.draw.line(screen, color, (15, 15), 
                             (int(WIDTH * progress), int(HEIGHT * progress)), 15)

        pygame.display.update()

# Reset Board
def reset_board():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = None

    start_time = time.time()
    duration = 0.5  # Animation duration in seconds

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            break

        progress = elapsed_time / duration
        screen.fill(BG_COLOR)
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col]:
                    center_x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    center_y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                    size = int(60 * (1 - progress))
                    if board[row][col] == 'X':
                        draw_scaled_cross(center_x, center_y, size)
                    elif board[row][col] == 'O':
                        pygame.draw.circle(screen, CIRCLE_COLOR, 
                                           (center_x, center_y), size, 15)
        pygame.display.update()

# AI Move using Minimax Algorithm (dummy implementation for example)
def ai_move():
    # Dummy AI move for example
    available_moves = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] is None]
    if available_moves:
        row, col = random.choice(available_moves)
        board[row][col] = 'O'
        animate_move(row, col, 'O')

# Display Player Turn
def display_player_turn(player):
    player_turn_text = f"{player_X_name if player == 'X' else player_O_name}'s Turn"
    text_surface = font_small.render(player_turn_text, True, WHITE)
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT - 40))

# Display Winner
def display_winner(winner):
    winner_text = f"{player_X_name if winner == 'X' else player_O_name} Wins!"
    text_surface = font.render(winner_text, True, WHITE)
    screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - text_surface.get_height() // 2))
    
    # Draw Play Again and Quit Buttons
    pygame.draw.rect(screen, BUTTON_COLOR, (PLAY_AGAIN_BUTTON_POS, (BUTTON_WIDTH, BUTTON_HEIGHT)))
    pygame.draw.rect(screen, BUTTON_COLOR, (QUIT_BUTTON_POS, (BUTTON_WIDTH, BUTTON_HEIGHT)))
    
    play_again_text_surface = font_small.render(PLAY_AGAIN_TEXT, True, BUTTON_TEXT_COLOR)
    quit_text_surface = font_small.render(QUIT_TEXT, True, BUTTON_TEXT_COLOR)
    
    screen.blit(play_again_text_surface, (PLAY_AGAIN_BUTTON_POS[0] + BUTTON_WIDTH // 2 - play_again_text_surface.get_width() // 2,
                                         PLAY_AGAIN_BUTTON_POS[1] + BUTTON_HEIGHT // 2 - play_again_text_surface.get_height() // 2))
    
    screen.blit(quit_text_surface, (QUIT_BUTTON_POS[0] + BUTTON_WIDTH // 2 - quit_text_surface.get_width() // 2,
                                    QUIT_BUTTON_POS[1] + BUTTON_HEIGHT // 2 - quit_text_surface.get_height() // 2))
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if PLAY_AGAIN_BUTTON_POS[0] <= mouse_x <= PLAY_AGAIN_BUTTON_POS[0] + BUTTON_WIDTH and \
                   PLAY_AGAIN_BUTTON_POS[1] <= mouse_y <= PLAY_AGAIN_BUTTON_POS[1] + BUTTON_HEIGHT:
                    reset_board()
                    return 'play_again'
                elif QUIT_BUTTON_POS[0] <= mouse_x <= QUIT_BUTTON_POS[0] + BUTTON_WIDTH and \
                     QUIT_BUTTON_POS[1] <= mouse_y <= QUIT_BUTTON_POS[1] + BUTTON_HEIGHT:
                    pygame.quit()
                    sys.exit()

# Main Loop
player = 'X'
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if board[clicked_row][clicked_col] is None:
                board[clicked_row][clicked_col] = player
                animate_move(clicked_row, clicked_col, player)
                if check_win(player):
                    game_over = True
                    result = display_winner(player)
                    if result == 'play_again':
                        player = 'X'
                        game_over = False
                else:
                    player = 'O' if player == 'X' else 'X'
                    if player == 'O' and not game_over:
                        ai_move()
                        if check_win('O'):
                            game_over = True
                            display_winner('O')
                        else:
                            player = 'X'

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_board()
                player = 'X'
                game_over = False

    screen.blit(background_image, (0, 0))
    draw_lines()
    draw_figures()
    if not game_over:
        display_player_turn(player)
    pygame.display.update()
