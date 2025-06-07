import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Game window dimensions
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Game Variables
clock = pygame.time.Clock()
FPS = 60

# Load player (jetpack man) image
player_image = pygame.Surface((40, 60))
player_image.fill(RED)  # Replace with actual character image
player_rect = player_image.get_rect()
player_rect.x = 50
player_rect.y = SCREEN_HEIGHT // 2

# Movement Variables
player_speed_y = 0
GRAVITY = 0.5
UPWARD_STRENGTH = -8
DOWNWARD_STRENGTH = 8

# Obstacles
obstacle_width = 20
obstacle_height = 60
obstacle_speed = -4
obstacles = []

# Timer Variables
start_time = 0
elapsed_time = 0

# Additional Game Variables
obstacles_passed = 0  # Total obstacles passed across lives
life_obstacles_passed = 0  # Obstacles passed in the current life
lives = 3  # Player's initial life count

# Function to create obstacles
def create_obstacle():
    height = random.randint(100, SCREEN_HEIGHT - 100)
    obstacle_rect = pygame.Rect(SCREEN_WIDTH, height, obstacle_width, obstacle_height)
    obstacles.append(obstacle_rect)

# Function to draw buttons
def draw_button(text, rect, color):
    pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, BLACK)
    screen.blit(label, (rect.x + 10, rect.y + 10))

# Game States
game_state = "start"

# Button Positions
start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25, 100, 50)
restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25, 100, 50)

# Game Loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if game_state == "running":
                if event.key in [pygame.K_UP, pygame.K_k, pygame.K_SPACE]:  # Move up with UP, K, or SPACE
                    player_speed_y = UPWARD_STRENGTH
                elif event.key == pygame.K_DOWN:  # Move down
                    player_speed_y = DOWNWARD_STRENGTH
                elif event.key == pygame.K_p:  # Pause toggle
                    game_state = "paused" if game_state == "running" else "running"

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "start" and start_button_rect.collidepoint(event.pos):
                game_state = "running"
                start_time = time.time()  # Start the timer
                obstacles.clear()  # Reset obstacles
                player_rect.y = SCREEN_HEIGHT // 2  # Reset player position
                obstacles_passed = 0  # Reset total obstacles passed
                life_obstacles_passed = 0  # Reset obstacles for the current life
                lives = 3  # Reset lives
            elif game_state == "game over" and restart_button_rect.collidepoint(event.pos):
                game_state = "running"
                start_time = time.time()  # Restart the timer
                obstacles.clear()  # Reset obstacles
                player_rect.y = SCREEN_HEIGHT // 2  # Reset player position
                obstacles_passed = 0  # Reset total obstacles passed
                life_obstacles_passed = 0  # Reset obstacles for the current life
                lives = 3  # Reset lives

    # Game logic
    if game_state == "running":
        # Gravity effect (pulling down)
        player_speed_y += GRAVITY
        player_rect.y += player_speed_y

        # Keep player on the screen
        if player_rect.y < 0:
            player_rect.y = 0
        elif player_rect.y > SCREEN_HEIGHT - player_rect.height:
            player_rect.y = SCREEN_HEIGHT - player_rect.height

        # Create obstacles
        if random.randint(1, 100) > 98:  # Random chance to create obstacles
            create_obstacle()

        # Move obstacles and count passed ones
        for obstacle in obstacles[:]:
            obstacle.x += obstacle_speed
            if obstacle.x < 0:
                obstacles.remove(obstacle)
                life_obstacles_passed += 1  # Increment obstacles for the current life

        # Collision detection
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                lives -= 1  # Reduce a life on collision
                if lives <= 0:
                    print("Game Over!")
                    game_state = "game over"
                    elapsed_time = time.time() - start_time  # Capture the elapsed time
                else:
                    # Update total obstacles passed with the current life's count
                    obstacles_passed += life_obstacles_passed
                    life_obstacles_passed = 0  # Reset for the new life
                    player_rect.y = SCREEN_HEIGHT // 2  # Reset player position
                obstacles.remove(obstacle)  # Remove obstacle on collision

    # Drawing
    screen.fill(BLACK)  # Background color

    if game_state == "start":
        draw_button("Start", start_button_rect, GREEN)
    elif game_state == "running":
        screen.blit(player_image, player_rect)

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(screen, WHITE, obstacle)

        # Display the running time, obstacles passed, and lives left
        elapsed_time = time.time() - start_time
        time_label = font.render(f"Time: {int(elapsed_time)}s", True, WHITE)
        obstacles_label = font.render(f"Obstacles Passed: {obstacles_passed + life_obstacles_passed}", True, WHITE)
        lives_label = font.render(f"Lives: {lives}", True, WHITE)
        
        screen.blit(time_label, (10, 10))
        screen.blit(obstacles_label, (10, 40))
        screen.blit(lives_label, (10, 70))

    elif game_state == "paused":
        pause_label = font.render("Paused - Press 'P' to Resume", True, WHITE)
        screen.blit(pause_label, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))

    elif game_state == "game over":
        draw_button("Restart", restart_button_rect, GREEN)
        game_over_label = font.render(f"Game Over! Time: {int(elapsed_time)}s", True, WHITE)
        screen.blit(game_over_label, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))
        obstacles_label = font.render(f"Total Obstacles Passed: {obstacles_passed + life_obstacles_passed}", True, WHITE)
        screen.blit(obstacles_label, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60))

    # Update screen
    pygame.display.flip()

    # Frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()