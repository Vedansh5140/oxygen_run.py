import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Background image
try:
    space_bg = pygame.image.load("space_bg.jpg")
    space_bg = pygame.transform.scale(space_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
except pygame.error:
    print("Error: 'space_bg.jpg' file is missing or not in the correct directory.")
    sys.exit()

# Load player sprite
try:
    player_sprite = pygame.image.load("player_sprite.png")  # Replace with your human sprite image
    player_sprite = pygame.transform.scale(player_sprite, (40, 60))
except pygame.error:
    print("Error: 'player_sprite.png' file is missing or not in the correct directory.")
    sys.exit()

# Player properties
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 20
current_lane_index = 1  # Start in the middle lane
lanes = [SCREEN_WIDTH // 6, SCREEN_WIDTH // 2, 5 * SCREEN_WIDTH // 6]  # Three lanes
player_x = lanes[current_lane_index]

# Obstacle properties
OBSTACLE_RADIUS = 20
obstacle_speed = 5
obstacle_interval = 1.5  # Interval in seconds for spawning obstacles

# Font for displaying text
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# Game variables
score = 0
obstacles = []
oxygen_timer_active = False  # Timer starts only after collecting the first oxygen
last_oxygen_time = 0  # Tracks the last oxygen collected time
game_speed = 1

# Countdown before the game starts
def show_countdown():
    for countdown in range(3, 0, -1):
        screen.fill((0, 0, 0))  # Clear the screen
        text = large_font.render(str(countdown), True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)  # Pause for 1 second
    screen.fill((0, 0, 0))  # Clear the screen
    text = large_font.render("Go!", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    time.sleep(1)

# Spawn a new obstacle
def spawn_obstacle():
    lane = random.choice(lanes)
    obstacle_type = random.choice(["oxygen", "carbon_dioxide"])
    return {"x": lane, "y": -OBSTACLE_RADIUS, "type": obstacle_type}

# Draw the player
def draw_player(x, y):
    screen.blit(player_sprite, (x - PLAYER_WIDTH // 2, y))

# Draw obstacles
def draw_obstacle(obstacle):
    color = BLUE if obstacle["type"] == "oxygen" else RED
    pygame.draw.circle(screen, color, (obstacle["x"], obstacle["y"]), OBSTACLE_RADIUS)

# Game over screen
def game_over_screen(reason):
    screen.fill((0, 0, 0))
    game_over_text = font.render("GAME OVER", True, WHITE)
    reason_text = font.render(reason, True, WHITE)
    final_score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
    screen.blit(reason_text, (SCREEN_WIDTH // 2 - reason_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# Show the countdown before starting
show_countdown()

# Game loop
running = True
last_obstacle_time = time.time()

while running:
    screen.blit(space_bg, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and current_lane_index > 0:
                current_lane_index -= 1  # Move to the left lane
            if event.key == pygame.K_RIGHT and current_lane_index < 2:
                current_lane_index += 1  # Move to the right lane

    # Update player position based on the lane
    player_x = lanes[current_lane_index]

    # Spawn new obstacles periodically
    if time.time() - last_obstacle_time > obstacle_interval / game_speed:
        obstacles.append(spawn_obstacle())
        last_obstacle_time = time.time()

    # Update obstacles
    for obstacle in obstacles[:]:
        obstacle["y"] += obstacle_speed * game_speed

        # Check for collision with the player
        if (
            abs(player_x - obstacle["x"]) < OBSTACLE_RADIUS + PLAYER_WIDTH // 2 and
            abs(player_y + PLAYER_HEIGHT // 2 - obstacle["y"]) < OBSTACLE_RADIUS
        ):
            if obstacle["type"] == "carbon_dioxide":
                game_over_screen("You touched carbon dioxide!")
            elif obstacle["type"] == "oxygen":
                score += 1
                last_oxygen_time = time.time()
                oxygen_timer_active = True  # Enable oxygen timer after collecting the first oxygen
                obstacles.remove(obstacle)

        # Remove obstacles that go off-screen
        if obstacle["y"] > SCREEN_HEIGHT:
            obstacles.remove(obstacle)

    # Check for oxygen timer only after collecting the first oxygen
    if oxygen_timer_active and time.time() - last_oxygen_time > 5:
        game_over_screen("You ran out of oxygen!")

    # Increase game speed progressively
    game_speed = 1 + score // 5
    obstacle_speed = 5 + score // 10

    # Draw player and obstacles
    draw_player(player_x, player_y)
    for obstacle in obstacles:
        draw_obstacle(obstacle)

    # Display score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update the screen
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
