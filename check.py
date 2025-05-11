import pygame
import random
import time

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Territory Vonquest")

# Colors
PINK = (255, 182, 193)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)  # Human player color
PURPLE = (128, 0, 128)  # AI color
GREEN = (0, 255, 0)  # AI2 color (AI vs AI)
YELLOW = (255, 255, 0)  # Power-up color
RED = (255, 0, 0)  # Freeze power-up color
BLUE = (0, 0, 255)  # Bonus power-up color

# Fonts
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)

# Try to load background music, but continue if file not found
try:
    pygame.mixer.music.load("background.mp3")
    pygame.mixer.music.play(-1, 0.0)
except:
    print("Background music file not found. Game will continue without music.")

# Tile settings
TILE_SIZE = 40
SCORE_PANEL_WIDTH = 200  # Width of the score panel
GRID_WIDTH = (WIDTH - SCORE_PANEL_WIDTH) // TILE_SIZE  # Adjust grid width to account for score panel
GRID_HEIGHT = HEIGHT // TILE_SIZE

# Timer and game state variables
start_time = time.time()
game_duration = 30  # Changed to 30 seconds
player_score = 0
ai_score = 0
turn = 'player'  # 'player' or 'ai'
power_ups = []
power_up_types = {}  # Store power-up types for each position
freeze_active = False
freeze_start_time = 0
FREEZE_DURATION = 3  # 3 seconds freeze duration
game_mode = None  # 'human_vs_ai' or 'ai_vs_ai'
ai_move_timer = 0
AI_MOVE_DELAY = 0.5  # AI moves every 0.5 seconds

# Player positions
player_pos = [GRID_WIDTH // 4, GRID_HEIGHT // 2]  # Start on the left side
ai_pos = [(GRID_WIDTH * 3) // 4, GRID_HEIGHT // 2]  # Start on the right side

# Initialize board (2D grid)
board = [['' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Power-up types
POWER_UPS = ['freeze', 'bonus']

def get_valid_moves(pos):
    moves = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_x = pos[0] + dx
        new_y = pos[1] + dy
        # Strict boundary checking - ensure we're at least 1 tile away from the edges
        if 1 <= new_x < GRID_WIDTH - 1 and 1 <= new_y < GRID_HEIGHT - 1:
            # Check if the move is not blocked by the other player
            if (new_x != ai_pos[0] or new_y != ai_pos[1]) and (new_x != player_pos[0] or new_y != player_pos[1]):
                moves.append((new_x, new_y))
    return moves

def evaluate_position(pos, is_ai=True):
    score = 0
    # Check the tile at the position
    if board[pos[1]][pos[0]] == 'player' and is_ai:
        score += 3  # Higher score for capturing player tiles
    elif board[pos[1]][pos[0]] == 'ai' and not is_ai:
        score += 3  # Higher score for capturing AI tiles
    elif board[pos[1]][pos[0]] == '':
        score += 1  # Basic score for empty tiles
    
    # Check for power-ups
    if (pos[1], pos[0]) in power_ups:
        power_type = power_up_types[(pos[1], pos[0])]
        if power_type == 'bonus':
            score += 2  # Bonus power-up is good
        elif power_type == 'freeze':
            score -= 2  # Avoid freeze power-ups
    
    # Check surrounding tiles for strategic value
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_x = pos[0] + dx
        new_y = pos[1] + dy
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
            if is_ai and board[new_y][new_x] == 'player':
                score += 1  # Bonus for being near player tiles
            elif not is_ai and board[new_y][new_x] == 'ai':
                score += 1  # Bonus for being near AI tiles
    
    return score

def minimax(pos, depth, alpha, beta, is_ai=True):
    if depth == 0:
        return evaluate_position(pos, is_ai)
    
    valid_moves = get_valid_moves(pos)
    if not valid_moves:
        return evaluate_position(pos, is_ai)
    
    if is_ai:
        max_eval = float('-inf')
        for move in valid_moves:
            # Simulate move
            new_x, new_y = move
            old_board = [row[:] for row in board]
            old_ai_score = ai_score
            old_player_score = player_score
            
            # Make move
            if board[new_y][new_x] != 'ai':
                if board[new_y][new_x] == 'player':
                    player_score -= 1
                board[new_y][new_x] = 'ai'
                ai_score += 1
            
            # Recursive evaluation
            eval = minimax([new_x, new_y], depth - 1, alpha, beta, False)
            
            # Restore state
            board = [row[:] for row in old_board]
            ai_score = old_ai_score
            player_score = old_player_score
            
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in valid_moves:
            # Simulate move
            new_x, new_y = move
            old_board = [row[:] for row in board]
            old_ai_score = ai_score
            old_player_score = player_score
            
            # Make move
            if board[new_y][new_x] != 'player':
                if board[new_y][new_x] == 'ai':
                    ai_score -= 1
                board[new_y][new_x] = 'player'
                player_score += 1
            
            # Recursive evaluation
            eval = minimax([new_x, new_y], depth - 1, alpha, beta, True)
            
            # Restore state
            board = [row[:] for row in old_board]
            ai_score = old_ai_score
            player_score = old_player_score
            
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(pos, is_ai=True, depth=2):  # Reduced depth to 2 for better performance
    best_score = float('-inf') if is_ai else float('inf')
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
    
    valid_moves = get_valid_moves(pos)
    if not valid_moves:
        return None
    
    for move in valid_moves:
        # Simulate move
        new_x, new_y = move
        old_board = [row[:] for row in board]
        old_ai_score = ai_score
        old_player_score = player_score
        
        # Make move
        if is_ai:
            if board[new_y][new_x] != 'ai':
                if board[new_y][new_x] == 'player':
                    player_score -= 1
                board[new_y][new_x] = 'ai'
                ai_score += 1
        else:
            if board[new_y][new_x] != 'player':
                if board[new_y][new_x] == 'ai':
                    ai_score -= 1
                board[new_y][new_x] = 'player'
                player_score += 1
        
        # Evaluate move
        score = minimax([new_x, new_y], depth - 1, alpha, beta, not is_ai)
        
        # Restore state
        board = [row[:] for row in old_board]
        ai_score = old_ai_score
        player_score = old_player_score
        
        if is_ai:
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)
        else:
            if score < best_score:
                best_score = score
                best_move = move
            beta = min(beta, best_score)
    
    return best_move

def move_ai():
    global ai_pos, ai_score, player_score
    if not freeze_active:
        try:
            best_move = get_best_move(ai_pos, True, 2)  # Reduced depth to 2
            if best_move:
                new_x, new_y = best_move
                # Update position and capture tile
                ai_pos = [new_x, new_y]
                if board[new_y][new_x] != 'ai':
                    if board[new_y][new_x] == 'player':
                        player_score -= 1  # Deduct from player's score
                    board[new_y][new_x] = 'ai'
                    ai_score += 1
                # Check for power-up
                if (new_y, new_x) in power_ups:
                    handle_power_up(new_y, new_x)
        except Exception as e:
            print(f"Error in AI move: {e}")
            # Fallback to simple movement if minimax fails
            valid_moves = get_valid_moves(ai_pos)
            if valid_moves:
                new_x, new_y = random.choice(valid_moves)
                ai_pos = [new_x, new_y]
                if board[new_y][new_x] != 'ai':
                    if board[new_y][new_x] == 'player':
                        player_score -= 1
                    board[new_y][new_x] = 'ai'
                    ai_score += 1

def move_player_ai():
    global player_pos, player_score, ai_score
    if not freeze_active:
        try:
            best_move = get_best_move(player_pos, False, 2)  # Reduced depth to 2
            if best_move:
                new_x, new_y = best_move
                # Update position and capture tile
                player_pos = [new_x, new_y]
                if board[new_y][new_x] != 'player':
                    if board[new_y][new_x] == 'ai':
                        ai_score -= 1  # Deduct from AI's score
                    board[new_y][new_x] = 'player'
                    player_score += 1
                # Check for power-up
                if (new_y, new_x) in power_ups:
                    handle_power_up(new_y, new_x)
        except Exception as e:
            print(f"Error in player AI move: {e}")
            # Fallback to simple movement if minimax fails
            valid_moves = get_valid_moves(player_pos)
            if valid_moves:
                new_x, new_y = random.choice(valid_moves)
                player_pos = [new_x, new_y]
                if board[new_y][new_x] != 'player':
                    if board[new_y][new_x] == 'ai':
                        ai_score -= 1
                    board[new_y][new_x] = 'player'
                    player_score += 1

def move_player(dx, dy):
    global player_pos, player_score, ai_score
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    
    # Strict boundary checking - ensure we're at least 1 tile away from the edges
    if (1 <= new_x < GRID_WIDTH - 1 and 1 <= new_y < GRID_HEIGHT - 1 and 
        (new_x != ai_pos[0] or new_y != ai_pos[1])):
        player_pos = [new_x, new_y]
        # Check if there's a power-up at the new position
        if (new_y, new_x) in power_ups:
            handle_power_up(new_y, new_x)
        # Update score and capture tile
        if board[new_y][new_x] != 'player':
            if board[new_y][new_x] == 'ai':
                ai_score -= 1  # Deduct from AI's score
            board[new_y][new_x] = 'player'
            player_score += 1

def handle_power_up(row, col):
    global freeze_active, freeze_start_time, player_score, ai_score
    if (row, col) in power_ups:
        power_type = power_up_types[(row, col)]
        if power_type == 'freeze':
            freeze_active = True
            freeze_start_time = time.time()
            power_ups.remove((row, col))
            del power_up_types[(row, col)]
        elif power_type == 'bonus':
            if turn == 'player':
                player_score += 5
            else:
                ai_score += 5
            power_ups.remove((row, col))
            del power_up_types[(row, col)]

def draw_power_up(surface, x, y, power_type):
    center_x = x * TILE_SIZE + TILE_SIZE // 2
    center_y = y * TILE_SIZE + TILE_SIZE // 2
    if power_type == 'freeze':
        pygame.draw.circle(surface, RED, (center_x, center_y), TILE_SIZE // 3)
        pygame.draw.line(surface, WHITE, (center_x - 5, center_y), (center_x + 5, center_y), 2)
        pygame.draw.line(surface, WHITE, (center_x, center_y - 5), (center_x, center_y + 5), 2)
    else:  # bonus
        pygame.draw.rect(surface, BLUE, (center_x - TILE_SIZE // 3, center_y - TILE_SIZE // 3, 
                                       TILE_SIZE // 1.5, TILE_SIZE // 1.5))
        pygame.draw.line(surface, WHITE, (center_x - 5, center_y), (center_x + 5, center_y), 2)

def draw_grid():
    # Draw the grid background and captured tiles
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            # Draw walls
            if row == 0 or row == GRID_HEIGHT - 1 or col == 0 or col == GRID_WIDTH - 1:
                pygame.draw.rect(screen, (100, 100, 100), rect)  # Dark gray for walls
                # Draw a thicker border for walls
                pygame.draw.rect(screen, (50, 50, 50), rect, 3)  # Darker border for walls
            elif board[row][col] == 'player':
                pygame.draw.rect(screen, BLACK, rect)
            elif board[row][col] == 'ai':
                pygame.draw.rect(screen, PURPLE, rect)
            else:
                pygame.draw.rect(screen, PINK, rect)
            # Only draw white border for non-wall tiles
            if not (row == 0 or row == GRID_HEIGHT - 1 or col == 0 or col == GRID_WIDTH - 1):
                pygame.draw.rect(screen, WHITE, rect, 2)

    # Draw the player
    player_rect = pygame.Rect(player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, BLACK, player_rect)
    center_x = player_pos[0] * TILE_SIZE + TILE_SIZE // 2
    center_y = player_pos[1] * TILE_SIZE + TILE_SIZE // 2
    pygame.draw.circle(screen, WHITE, (center_x, center_y), TILE_SIZE // 4)

    # Draw the AI
    ai_rect = pygame.Rect(ai_pos[0] * TILE_SIZE, ai_pos[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, PURPLE, ai_rect)
    center_x = ai_pos[0] * TILE_SIZE + TILE_SIZE // 2
    center_y = ai_pos[1] * TILE_SIZE + TILE_SIZE // 2
    pygame.draw.line(screen, WHITE, (center_x - 10, center_y - 10), (center_x + 10, center_y + 10), 2)
    pygame.draw.line(screen, WHITE, (center_x + 10, center_y - 10), (center_x - 10, center_y + 10), 2)

    # Draw power-ups
    for pos in power_ups:
        draw_power_up(screen, pos[1], pos[0], power_up_types[pos])

def draw_scores():
    # Draw score panel
    score_panel = pygame.Rect(WIDTH - 200, 0, 200, HEIGHT)
    pygame.draw.rect(screen, (50, 50, 50), score_panel)
    
    # Draw scores
    player_text = font.render(f"Player: {player_score}", True, WHITE)
    ai_text = font.render(f"AI: {ai_score}", True, WHITE)
    screen.blit(player_text, (WIDTH - 180, 20))
    screen.blit(ai_text, (WIDTH - 180, 60))

    # Draw power-up legend
    legend_text = font.render("Power-ups:", True, WHITE)
    screen.blit(legend_text, (WIDTH - 180, 120))
    
    # Draw freeze power-up example
    pygame.draw.circle(screen, RED, (WIDTH - 160, 170), 10)
    freeze_text = small_font.render("Freeze", True, WHITE)
    screen.blit(freeze_text, (WIDTH - 140, 165))
    
    # Draw bonus power-up example
    pygame.draw.rect(screen, BLUE, (WIDTH - 170, 190, 20, 20))
    bonus_text = small_font.render("Bonus", True, WHITE)
    screen.blit(bonus_text, (WIDTH - 140, 195))

    # Draw controls
    controls_text = font.render("Controls:", True, WHITE)
    screen.blit(controls_text, (WIDTH - 180, 250))
    w_text = small_font.render("W - Move Up", True, WHITE)
    a_text = small_font.render("A - Move Left", True, WHITE)
    s_text = small_font.render("S - Move Down", True, WHITE)
    d_text = small_font.render("D - Move Right", True, WHITE)
    screen.blit(w_text, (WIDTH - 180, 290))
    screen.blit(a_text, (WIDTH - 180, 320))
    screen.blit(s_text, (WIDTH - 180, 350))
    screen.blit(d_text, (WIDTH - 180, 380))

def display_scoreboard():
    screen.fill(PINK)
    
    # Draw title
    title_font = pygame.font.SysFont(None, 60)
    title_text = title_font.render("Game Over!", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))
    
    # Draw scores
    score_font = pygame.font.SysFont(None, 50)
    player_text = score_font.render(f"Player Score: {player_score}", True, BLACK)
    ai_text = score_font.render(f"AI Score: {ai_score}", True, PURPLE)
    
    screen.blit(player_text, (WIDTH // 2 - player_text.get_width() // 2, 250))
    screen.blit(ai_text, (WIDTH // 2 - ai_text.get_width() // 2, 320))
    
    # Draw winner
    winner_font = pygame.font.SysFont(None, 45)
    if player_score > ai_score:
        winner_text = winner_font.render("Player Wins!", True, BLACK)
    elif ai_score > player_score:
        winner_text = winner_font.render("AI Wins!", True, PURPLE)
    else:
        winner_text = winner_font.render("It's a Tie!", True, WHITE)
    
    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, 400))
    
    pygame.display.flip()
    time.sleep(5)  # Display scoreboard for 5 seconds

def display_menu():
    global game_mode
    while True:
        screen.fill(PINK)
        pygame.draw.rect(screen, WHITE, pygame.Rect(WIDTH // 4, HEIGHT // 3, WIDTH // 2, 50))
        pygame.draw.rect(screen, WHITE, pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, 50))

        menu_text1 = font.render("Human vs AI", True, BLACK)
        menu_text2 = font.render("AI vs AI", True, BLACK)
        
        screen.blit(menu_text1, (WIDTH // 2 - menu_text1.get_width() // 2, HEIGHT // 3 + 10))
        screen.blit(menu_text2, (WIDTH // 2 - menu_text2.get_width() // 2, HEIGHT // 2 + 10))
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Check if the click is within the bounds of the buttons
                if WIDTH // 4 <= pos[0] <= WIDTH // 4 + WIDTH // 2:
                    if HEIGHT // 3 <= pos[1] <= HEIGHT // 3 + 50:
                        game_mode = 'human_vs_ai'
                        return
                    if HEIGHT // 2 <= pos[1] <= HEIGHT // 2 + 50:
                        game_mode = 'ai_vs_ai'
                        return

def game_over(board):
    return all(board[row][col] != '' for row in range(GRID_HEIGHT) for col in range(GRID_WIDTH))

def main():
    global start_time, power_ups, power_up_types, freeze_active, freeze_start_time
    global game_mode, turn, board, player_score, ai_score, ai_move_timer
    
    display_menu()  # Show the menu to select game mode

    running = True
    board = [['' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    player_score = 0
    ai_score = 0
    turn = 'player'  # human starts
    power_ups = []
    power_up_types = {}
    freeze_active = False
    freeze_start_time = 0
    ai_move_timer = 0
    player_pos = [GRID_WIDTH // 4, GRID_HEIGHT // 2]  # Reset player position
    ai_pos = [(GRID_WIDTH * 3) // 4, GRID_HEIGHT // 2]  # Reset AI position

    # Initialize starting positions
    board[player_pos[1]][player_pos[0]] = 'player'
    board[ai_pos[1]][ai_pos[0]] = 'ai'
    player_score = 1
    ai_score = 1

    start_time = time.time()
    clock = pygame.time.Clock()  # Add clock for consistent frame rate

    while running:
        screen.fill(PINK)
        current_time = time.time()
        elapsed_time = current_time - start_time
        remaining_time = max(0, game_duration - elapsed_time)

        # Check freeze duration
        if freeze_active and current_time - freeze_start_time >= FREEZE_DURATION:
            freeze_active = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if game_mode == 'human_vs_ai' and event.type == pygame.KEYDOWN and not freeze_active:
                if event.key == pygame.K_w:  # Up
                    move_player(0, -1)
                elif event.key == pygame.K_s:  # Down
                    move_player(0, 1)
                elif event.key == pygame.K_a:  # Left
                    move_player(-1, 0)
                elif event.key == pygame.K_d:  # Right
                    move_player(1, 0)

        # AI movement with timer
        if current_time - ai_move_timer >= AI_MOVE_DELAY:
            if game_mode == 'ai_vs_ai':
                # In AI vs AI mode, both players are AI
                if turn == 'player':
                    move_player_ai()
                    turn = 'ai'
                else:
                    move_ai()
                    turn = 'player'
            elif game_mode == 'human_vs_ai':
                # In human vs AI mode, only AI moves
                move_ai()
            ai_move_timer = current_time

        draw_grid()
        draw_scores()

        # Draw remaining time
        time_text = font.render(f"Time: {int(remaining_time)}s", True, WHITE)
        screen.blit(time_text, (WIDTH - 180, 420))

        # Spawn power-ups
        if random.random() < 0.01 and len(power_ups) < 5:
            row = random.randint(0, GRID_HEIGHT - 1)
            col = random.randint(0, GRID_WIDTH - 1)
            if board[row][col] == '' and (row, col) not in power_ups:
                power_ups.append((row, col))
                power_up_types[(row, col)] = random.choice(POWER_UPS)

        if remaining_time <= 0 or game_over(board):
            display_scoreboard()
            break
        
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

if __name__ == "__main__":
    main()
    pygame.quit()
