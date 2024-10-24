import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up screen dimensions (1600x1200)
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top-Down Game - 1600x1200 Resolution")

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors (RGB values)
WHITE = (255, 255, 255)
BLUE = (0, 128, 255)
GREEN = (0, 255, 0)

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Player's size (50x50 pixels)
        self.image.fill(BLUE)                  # Blue color for the player
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # Start position at the center of the screen
        self.speed = 5

    def update(self, keys):
        # Movement controls
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Prevent the player from moving off the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define an Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))  # Obstacle size
        self.image.fill(GREEN)  # Green color for obstacles
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Main game loop
def main():
    # Create player object and add it to a sprite group
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Create obstacles (scaling for larger screen)
    obstacles = pygame.sprite.Group()
    obstacle1 = Obstacle(300, 200, 150, 400)  # Example obstacle, scaled up
    obstacle2 = Obstacle(800, 700, 300, 100)  # Another obstacle, scaled up
    obstacles.add(obstacle1, obstacle2)

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get keys pressed
        keys = pygame.key.get_pressed()

        # Update the player
        player.update(keys)

        # Fill the screen with a solid color (white background)
        screen.fill(WHITE)

        # Draw all sprites (player)
        all_sprites.draw(screen)

        # Draw obstacles
        obstacles.draw(screen)

        # Update the display
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
