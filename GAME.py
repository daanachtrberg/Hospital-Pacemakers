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
HOVER_COLOR = (200, 200, 200)

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

def display_title_screen():
    title_font = pygame.font.Font(None, 72)
    start_font = pygame.font.Font(None, 48)

    title_text = title_font.render("Game Title", True, WHITE)
    start_text = start_font.render("Start Game", True, WHITE)

    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    title_animation_offset = 0
    title_animation_direction = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return  # Exit the title screen

        # Animate title text
        title_animation_offset += title_animation_direction
        if title_animation_offset > 10 or title_animation_offset < -10:
            title_animation_direction *= -1

        # Check for hover effect
        mouse_pos = pygame.mouse.get_pos()
        if start_rect.collidepoint(mouse_pos):
            start_text = start_font.render("Start Game", True, HOVER_COLOR)
        else:
            start_text = start_font.render("Start Game", True, WHITE)

        screen.blit(background_image, (0, 0))  # Draw the background image
        screen.blit(title_text, (title_rect.x, title_rect.y + title_animation_offset))
        screen.blit(start_text, start_rect)
        pygame.display.update()
        clock.tick(FPS)

def draw_scoreboard(score):
    font = pygame.font.Font(None, 36)  # Create a font object for the scoreboard
    score_text = font.render(f"Score: {score}", True, WHITE)  # Render the score text
    screen.blit(score_text, (10, 10))  # Draw the score text at the top-left corner

def display_title_screen():
    title_font = pygame.font.Font(None, 72)
    start_font = pygame.font.Font(None, 48)

    title_text = title_font.render("Game Title", True, WHITE)
    start_text = start_font.render("Start Game", True, WHITE)

    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    title_animation_offset = 0
    title_animation_direction = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return  # Exit the title screen

        # Animate title text
        title_animation_offset += title_animation_direction
        if title_animation_offset > 10 or title_animation_offset < -10:
            title_animation_direction *= -1

        # Check for hover effect
        mouse_pos = pygame.mouse.get_pos()
        if start_rect.collidepoint(mouse_pos):
            start_text = start_font.render("Start Game", True, HOVER_COLOR)
        else:
            start_text = start_font.render("Start Game", True, WHITE)

        screen.blit(background_image, (0, 0))  # Draw the background image
        screen.blit(title_text, (title_rect.x, title_rect.y + title_animation_offset))
        screen.blit(start_text, start_rect)
        pygame.display.update()
        clock.tick(FPS)

# Main game loop
def main():
    walls = [
        pygame.Rect(340, 245, 230, 10),  # Wall 1
        pygame.Rect(620, 245, 90, 10),   # Wall 2
        pygame.Rect(680, 245, 7, 95), # Wall 3 (Horizontal)
        pygame.Rect(680, 340, 50, 4), # Wall 4
        pygame.Rect(650, 330, 35, 4),   # Wall 5
        pygame.Rect(565, 330, 30, 4), # Wall 6 (Horizontal)
        pygame.Rect(959, 245, 10, 175),   # Wall 2
        pygame.Rect(760, 245, 200, 10), # Wall 3 (Horizontal)
        pygame.Rect(810, 340, 5, 80), # Wall 4
        pygame.Rect(780, 340, 180, 5), # Wall 6 (Horizontal)
        pygame.Rect(810, 460, 5, 30), # Wall 4
        pygame.Rect(959, 458, 10, 34), # Wall 4
        pygame.Rect(540, 483, 420, 10),
        pygame.Rect(30, 240, 10, 170),
        pygame.Rect(560, 330, 10, 160),
        pygame.Rect(30, 240, 50, 10),
        pygame.Rect(135, 243, 130, 10),
        pygame.Rect(190, 240, 10, 150),
        pygame.Rect(30, 480, 438, 10),
        pygame.Rect(30, 460, 10, 30),
        pygame.Rect(30, 365, 60, 10),
        pygame.Rect(140, 365, 60, 10)
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

    display_title_screen()

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.blit(background_image, (0, 0))  # Use the background image

        # Draw all walls
        # for wall in walls:
        #     pygame.draw.rect(screen, WHITE, wall)  # Draw all walls

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

        # Check for collisions with points
        collected_points = pygame.sprite.spritecollide(player, points, True)  # True to remove the collected points
        total_points_collected += len(collected_points)  # Update the score

        # Draw points
        for point in points:
            screen.blit(point.image, point.rect)

        # Draw the scoreboard
        draw_scoreboard(total_points_collected)  # Call the scoreboard drawing function

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

# Run the game
if __name__ == "__main__":
    main()


