import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up screen dimensions (1600x1200)
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top-Down Game with Moving Enemies and Points")

# Load background image
background_image = pygame.image.load("Map.png")  # Replace with your image file
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
        self.image = pygame.Surface((50, 50))  # Player's size
        self.image.fill(BLUE)                  # Blue color for the player
        self.rect = self.image.get_rect()
        self.rect.center = (spawn_x, spawn_y)  # Set the spawn position
        self.speed = 5

    def update(self, keys):
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

# Define an Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))  # Enemy size
        self.image.fill(RED)                    # Red color for enemies
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 50)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 50)
        self.speed = random.uniform(0.5, 2)     # Slower random speed for movement
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]  # Random initial direction

    def update(self):
        # Move the enemy in both x and y directions
        self.rect.x += self.speed * self.direction[0]
        self.rect.y += self.speed * self.direction[1]

        # Reverse direction if enemy hits the screen edge
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction[0] *= -1  # Reverse horizontal direction
            self.rect.x += self.speed * self.direction[0]  # Adjust position to stay in bounds

        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.direction[1] *= -1  # Reverse vertical direction
            self.rect.y += self.speed * self.direction[1]  # Adjust position to stay in bounds

# Define a Point class for collectibles
class Point(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))  # Point size
        self.image.fill(YELLOW)                 # Yellow color for points
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 10)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 10)

# Function to find a spawn point for the player
def find_spawn_point(enemies):
    while True:
        spawn_x = random.randint(0, SCREEN_WIDTH - 50)
        spawn_y = random.randint(0, SCREEN_HEIGHT - 50)
        player_rect = pygame.Rect(spawn_x, spawn_y, 50, 50)  # Player's hitbox
        # Check if the spawn point collides with any enemy
        if not any(player_rect.colliderect(enemy.rect) for enemy in enemies):
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
    enemies = pygame.sprite.Group()
    for i in range(5):  # Create 5 enemies
        enemy = Enemy()
        enemies.add(enemy)

    # Find a spawn point for the player
    spawn_x, spawn_y = find_spawn_point(enemies)
    player = Player(spawn_x, spawn_y)

    # Create points
    points = pygame.sprite.Group()
    total_points_collected = 0  # Total points collected
    spawn_timer = 0  # Timer for point respawn

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    score = 0  # Initialize score
    font = pygame.font.Font(None, 36)  # Font for displaying score

    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get keys pressed
        keys = pygame.key.get_pressed()

        # Update the player and enemies
        player.update(keys)
        enemies.update()

        # Check for collisions with enemies
        if pygame.sprite.spritecollideany(player, enemies):
            display_game_over()  # Show game over message
            spawn_x, spawn_y = find_spawn_point(enemies)  # Find a new spawn point
            player.rect.center = (spawn_x, spawn_y)  # Reset player position

        # Check for collisions with points
        collected_points = pygame.sprite.spritecollide(player, points, True)  # Collect points and remove them
        score += len(collected_points)  # Increase score by the number of collected points
        total_points_collected += len(collected_points)  # Update total points collected

        # Fill the screen with the background image
        screen.blit(background_image, (0, 0))  # Draw the background image

        # Draw all sprites (player, enemies, and points)
        all_sprites.draw(screen)
        enemies.draw(screen)
        points.draw(screen)

        # Respawn points at a normal pace
        spawn_timer += 1
        if spawn_timer > 60:  # Respawn every 60 frames (1 second)
            if len(points) < 10:  # Limit to 10 points on the screen at once
                point = Point()
                points.add(point)
            spawn_timer = 0  # Reset spawn timer

        # Display the score and total points collected
        score_text = font.render(f"Score: {score}", True, WHITE)
        total_points_text = font.render(f"Total Points: {total_points_collected}", True, WHITE)
        screen.blit(score_text, (10, 10))  # Display score at the top left
        screen.blit(total_points_text, (10, 50))  # Display total points below the score

        # Update the display
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
