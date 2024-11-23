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
player_x = SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT - 20
player_speed = 10

# Lanes
LANE_WIDTH = SCREEN_WIDTH // 3
lanes = [LANE_WIDTH // 2, SCREEN_WIDTH // 2, SCREEN_WIDTH - LANE_WIDTH // 2]

# Obstacle properties
OBSTACLE_RADIUS = 20
obstacle_speed = 5
obstacle_interval = 1.5  # Interval in seconds for spawning obstacles

# Font for displaying score
font = pygame.font.Font(None, 36)

# Game variables
score = 0
obstacles = []
last_oxygen_time = time.time()
game_speed = 1

# Spawn a new obstacle
def spawn_obstacle():
    lane = random.choice(lanes)
    obstacle_type = random.choice(["oxygen", "carbon_dioxide"])
    return {"x": lane, "y": -OBSTACLE_RADIUS, "type": obstacle_type}

# Draw the player
def draw_player(x, y):
    screen.blit(player_sprite, (x, y))

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

# Game loop
running = True
last_obstacle_time = time.time()

while running:
    screen.blit(space_bg, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_WIDTH:
        player_x += player_speed

    # Ensure the player stays in the closest lane
    player_lane = min(lanes, key=lambda lane: abs(player_x + PLAYER_WIDTH // 2 - lane))
    player_x = player_lane - PLAYER_WIDTH // 2

    # Spawn new obstacles periodically
    if time.time() - last_obstacle_time > obstacle_interval / game_speed:
        obstacles.append(spawn_obstacle())
        last_obstacle_time = time.time()

    # Update obstacles
    for obstacle in obstacles[:]:
        obstacle["y"] += obstacle_speed * game_speed

        # Check for collision with the player
        if (
            abs(player_x + PLAYER_WIDTH // 2 - obstacle["x"]) < OBSTACLE_RADIUS and
            abs(player_y + PLAYER_HEIGHT // 2 - obstacle["y"]) < OBSTACLE_RADIUS
        ):
            if obstacle["type"] == "carbon_dioxide":
                game_over_screen("You touched carbon dioxide!")
            elif obstacle["type"] == "oxygen":
                score += 1
            


