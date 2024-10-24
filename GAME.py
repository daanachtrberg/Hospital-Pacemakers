import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up screen dimensions (1000x800)
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top-Down Game with Moving Enemies and Points")

# Load background image (make sure to have the correct path)
# Replace with your image file
background_image = pygame.image.load("Map.png")  
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to fit the screen

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors (RGB values)
BLUE = (0, 128, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # Player's size
        self.image.fill(BLUE)                  # Blue color for the player
        self.rect = self.image.get_rect()
        self.rect.center = (spawn_x, spawn_y)  # Set the spawn position
        self.speed = 5

    def update(self, keys, walls):
        # Store the original position
        original_rect = self.rect.copy()

        # Move the player based on key presses
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Prevent moving off the screen
        self.rect.clamp_ip(screen.get_rect())  # Clamp the player's rect within the screen boundaries

        # Prevent moving through walls
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect = original_rect  # Revert to original position if collision occurs
                break  # Exit the loop if a collision is detected

# Define an Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # Enemy size
        self.image.fill(RED)                    # Red color for enemies
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 30)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 30)
        self.speed = random.uniform(0.5, 1.5)     # Slower random speed for movement
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]  # Random initial direction

    def update(self, walls):
        # Save the original position
        original_rect = self.rect.copy()

        # Move the enemy in both x and y directions
        self.rect.x += self.speed * self.direction[0]
        self.rect.y += self.speed * self.direction[1]

        # Check for collision with all walls
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect = original_rect  # Revert to original position
                self.direction[0] *= -1  # Reverse direction on x-axis
                self.direction[1] *= -1  # Reverse direction on y-axis
                break  # Exit the loop if a collision is detected

        # Reverse direction if enemy hits the screen edge
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction[0] *= -1  # Reverse horizontal direction

        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.direction[1] *= -1  # Reverse vertical direction

# Define a Point class for collectibles
class Point(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((8, 8))  # Point size
        self.image.fill(YELLOW)                 # Yellow color for points
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 8)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 8)

# Function to find a spawn point for the player
def find_spawn_point(enemies, walls):
    while True:
        spawn_x = random.randint(0, SCREEN_WIDTH - 30)
        spawn_y = random.randint(0, SCREEN_HEIGHT - 30)
        player_rect = pygame.Rect(spawn_x, spawn_y, 30, 30)  # Player's hitbox
        # Check if the spawn point collides with any enemy or walls
        if not any(player_rect.colliderect(enemy.rect) for enemy in enemies) and not any(player_rect.colliderect(wall) for wall in walls):
            return spawn_x, spawn_y

# Function to display the "You died" message
def display_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("You Died", True, WHITE)  # Change text color to white
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds before restarting

# Main game loop
def main():
    walls = [
        pygame.Rect(30, 240, 10, 170),  # Wall 1
        pygame.Rect(30, 240, 50, 10),  # Wall 2
        pygame.Rect(140, 240, 130, 10),           # Wall 3 (Horizontal)
        pygame.Rect(190, 240, 10, 150),  # Wall 1
        pygame.Rect(700, 0, 10, 200),  # Wall 2
        pygame.Rect(500, 300, 200, 10),           # Wall 3 (Horizontal)
        pygame.Rect(300, 0, 10, 200),  # Wall 1
        pygame.Rect(700, 0, 10, 200),  # Wall 2
        pygame.Rect(500, 300, 200, 10),           # Wall 3 (Horizontal)
    ]

    enemies = pygame.sprite.Group()
    for i in range(5):  # Create 5 enemies
        enemy = Enemy()
        enemies.add(enemy)

    # Find a spawn point for the player
    spawn_x, spawn_y = find_spawn_point(enemies, walls)
    player = Player(spawn_x, spawn_y)

    # Create points
    points = pygame.sprite.Group()
    total_points_collected = 0

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.blit(background_image, (0, 0))  # Use the background image

        # Draw all walls
        for wall in walls:
            pygame.draw.rect(screen, WHITE, wall)  # Draw all walls

        # Update and draw player and enemies
        keys = pygame.key.get_pressed()
        player.update(keys, walls)
        screen.blit(player.image, player.rect)

        enemies.update(walls)
        enemies.draw(screen)

        # Check for collisions with enemies
        if pygame.sprite.spritecollideany(player, enemies):
            display_game_over()
            main()  # Restart the game after death

        # Check for points collection
        if len(points) < 10:  # Limit the number of points to 10
            new_point = Point()
            points.add(new_point)

        # Draw points
        for point in points:
            screen.blit(point.image, point.rect)

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

# Run the game
if __name__ == "__main__":
    main()
