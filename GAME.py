import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
PLAYER_COLOR = (0, 128, 255)
BACKGROUND_COLOR = (0, 0, 0)
FPS = 60
PLAYER_SPEED = 5

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Top-Down Movement Game')

# Player attributes
player_x = SCREEN_WIDTH // 2
player_y = SCREEN_HEIGHT // 2

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get keys pressed
    keys = pygame.key.get_pressed()

    # Movement logic
    if keys[pygame.K_LEFT]:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player_y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player_y += PLAYER_SPEED

    # Boundaries check (to keep player within the screen)
    player_x = max(0, min(SCREEN_WIDTH - PLAYER_SIZE, player_x))
    player_y = max(0, min(SCREEN_HEIGHT - PLAYER_SIZE, player_y))

    # Fill screen with background color
    screen.fill(BACKGROUND_COLOR)

    # Draw the player (a rectangle for simplicity)
    pygame.draw.rect(screen, PLAYER_COLOR, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
