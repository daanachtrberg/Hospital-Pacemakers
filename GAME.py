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
background_image = pygame.image.load("Map.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale to fit the screen

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Colors (RGB values)
BLUE = (0, 128, 255)
SKYBLUE = (135, 206, 235)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
HOVER_COLOR = (200, 200, 200)

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        """Initialize the Player sprite.

        Args:
            spawn_x (int): The x-coordinate for the player's starting position.
            spawn_y (int): The y-coordinate for the player's starting position.
        """
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (spawn_x, spawn_y)
        self.speed = 7

    def update(self, keys, walls):
        """Update the player's position based on input and collisions with walls.

        Args:
            keys (list): The current state of all keyboard keys.
            walls (list): A list of wall rectangles for collision detection.
        """
        original_rect = self.rect.copy()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        self.rect.clamp_ip(screen.get_rect())
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect = original_rect
                break

# Define an Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y):
        """Initialize the Enemy sprite.

        Args:
            spawn_x (int): The x-coordinate for the enemy's starting position.
            spawn_y (int): The y-coordinate for the enemy's starting position.
        """
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = spawn_x
        self.rect.y = spawn_y
        self.speed = random.uniform(3, 4)
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]

    def update(self, walls):
        """Update the enemy's position based on its direction and handle wall collisions.

        Args:
            walls (list): A list of wall rectangles for collision detection.
        """
        original_rect = self.rect.copy()
        self.rect.x += self.speed * self.direction[0]
        self.rect.y += self.speed * self.direction[1]
        for wall in walls:
            if self.rect.colliderect(wall):
                self.rect = original_rect
                self.direction[0] *= -1
                self.direction[1] *= -1
                break
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction[0] *= -1
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.direction[1] *= -1

# Define a Point class for collectibles
class Point(pygame.sprite.Sprite):
    def __init__(self):
        """Initialize the Point sprite (collectible).

        The point's position is set to a random location on initialization.
        """
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        """Respawn the point at a random location on the screen."""
        self.rect.x = random.randint(0, SCREEN_WIDTH - 8)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 8)

# Define a NeutralNPC class with a timer
class NeutralNPC(pygame.sprite.Sprite):
    def __init__(self, walls):
        """Initialize the NeutralNPC sprite.

        Args:
            walls (list): A list of wall rectangles for collision detection.
        """
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.respawn(walls)
        self.spawn_time = pygame.time.get_ticks()

    def respawn(self, walls):
        """Respawn the NPC at a random location on the screen, ensuring it does not overlap with walls.

        Args:
            walls (list): A list of wall rectangles for collision detection.
        """
        while True:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
            if not any(self.rect.colliderect(wall) for wall in walls):
                break
        self.spawn_time = pygame.time.get_ticks()  # Reset the timer on respawn

    def update(self):
        """Update the NPC's state based on the elapsed time.

        The NPC changes color based on how long it has been alive and despawns after 10 seconds.
        """
        elapsed_time = (pygame.time.get_ticks() - self.spawn_time) / 1000  # Time in seconds
        if elapsed_time >= 10:
            self.kill()  # Despawn the NPC after 10 seconds
        elif elapsed_time >= 9:
            self.image.fill(RED)
        elif elapsed_time >= 6:
            self.image.fill(ORANGE)
        elif elapsed_time >= 3:
            self.image.fill(YELLOW)
        else:
            self.image.fill(GREEN)

def find_spawn_point(enemies, walls):
    """Find a valid spawn point for the player.

    Args:
        enemies (Group): A group of enemy sprites.
        walls (list): A list of wall rectangles for collision detection.

    Returns:
        tuple: The x and y coordinates of the spawn point.
    """
    while True:
        spawn_x = random.randint(0, SCREEN_WIDTH - 30)
        spawn_y = random.randint(0, SCREEN_HEIGHT - 30)
        player_rect = pygame.Rect(spawn_x, spawn_y, 30, 30)

        # Ensure the spawn point is not too close to walls or enemies
        if (not any(player_rect.colliderect(enemy.rect) for enemy in enemies) and
            not any(player_rect.colliderect(wall) for wall in walls) and
            all(not wall.colliderect(player_rect.inflate(30, 30)) for wall in walls)):  # Check if player is far enough from walls
            return spawn_x, spawn_y

def find_enemy_spawn_point(enemies, walls):
    """Find a valid spawn point for an enemy.

    Args:
        enemies (Group): A group of enemy sprites.
        walls (list): A list of wall rectangles for collision detection.

    Returns:
        tuple: The x and y coordinates of the enemy spawn point.
    """
    while True:
        spawn_x = random.randint(0, SCREEN_WIDTH - 30)
        spawn_y = random.randint(0, SCREEN_HEIGHT - 30)
        enemy_rect = pygame.Rect(spawn_x, spawn_y, 30, 30)

        # Ensure the spawn point is not too close to walls or other enemies
        if (not any(enemy_rect.colliderect(other_enemy.rect) for other_enemy in enemies) and
            not any(enemy_rect.colliderect(wall) for wall in walls) and
            all(not wall.colliderect(enemy_rect.inflate(30, 30)) for wall in walls)):  # Check if enemy is far enough from walls
            return spawn_x, spawn_y

def display_game_over():
    """Display the 'GAME OVER' message and wait before exiting the game."""
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def display_title_screen():
    """Display the title screen with animations and handle user input to start the game."""
    title_font = pygame.font.Font(None, 72)
    start_font = pygame.font.Font(None, 48)
    subtitle_font = pygame.font.Font(None, 36)  # Font for the subtitle

    title_text = title_font.render("Pacemaker Panic", True, BLUE)
    start_text = start_font.render("Start Game", True, WHITE)
    subtitle_text = subtitle_font.render("Collect 3 screws and save the patients before they flatline!", True, SKYBLUE)  # Subtitle text

    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))  # Positioning the start text
    subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))  # Positioning the subtitle above the start text

    title_animation_offset = 0
    title_animation_direction = 1
    subtitle_animation_offset = 0
    subtitle_animation_direction = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return

        title_animation_offset += title_animation_direction
        subtitle_animation_offset += subtitle_animation_direction

        if title_animation_offset > 10 or title_animation_offset < -10:
            title_animation_direction *= -1

        if subtitle_animation_offset > 5 or subtitle_animation_offset < -5:  # Adjust subtitle animation limits
            subtitle_animation_direction *= -1

        mouse_pos = pygame.mouse.get_pos()
        if start_rect.collidepoint(mouse_pos):
            start_text = start_font.render("Start Game", True, HOVER_COLOR)
        else:
            start_text = start_font.render("Start Game", True, WHITE)

        screen.blit(background_image, (0, 0))
        screen.blit(title_text, (title_rect.x, title_rect.y + title_animation_offset))
        screen.blit(subtitle_text, (subtitle_rect.x, subtitle_rect.y + subtitle_animation_offset))  # Draw the subtitle above the start text
        screen.blit(start_text, start_rect)  # Draw the start text below the subtitle

        pygame.display.update()
        clock.tick(FPS)

def draw_scoreboard(score, npc_interactions):
    """Draws the scoreboard which keeps track of points"""
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, YELLOW)
    interactions_text = font.render(f"NPC Interactions: {npc_interactions}", True, YELLOW)
    screen.blit(score_text, (10, 10))
    screen.blit(interactions_text, (10, 40))

def main():
    """The main game loop that initializes the game and handles game logic."""
    walls = [
        pygame.Rect(340, 245, 230, 10),  
        pygame.Rect(620, 245, 90, 10),   
        pygame.Rect(680, 245, 7, 95), 
        pygame.Rect(680, 340, 50, 4), 
        pygame.Rect(650, 330, 35, 4),   
        pygame.Rect(565, 330, 30, 4), 
        pygame.Rect(959, 245, 10, 170),   
        pygame.Rect(770, 245, 190, 10), 
        pygame.Rect(810, 340, 5, 75), 
        pygame.Rect(780, 340, 180, 5), 
        pygame.Rect(810, 465, 5, 25), 
        pygame.Rect(959, 463, 10, 29), 
        pygame.Rect(540, 483, 420, 10),
        pygame.Rect(30, 240, 10, 165),
        pygame.Rect(560, 330, 10, 160),
        pygame.Rect(30, 240, 50, 10),
        pygame.Rect(135, 243, 130, 10),
        pygame.Rect(190, 240, 10, 150),
        pygame.Rect(30, 480, 438, 10),
        pygame.Rect(30, 465, 10, 25),
        pygame.Rect(30, 365, 60, 10),
        pygame.Rect(140, 365, 60, 10)
    ]

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    points = pygame.sprite.Group()
    neutral_npcs = pygame.sprite.Group()

    spawn_x, spawn_y = find_spawn_point(enemies, walls)
    player = Player(spawn_x, spawn_y)
    all_sprites.add(player)

    # Start with one enemy
    enemy_spawn_x, enemy_spawn_y = find_enemy_spawn_point(enemies, walls)
    enemy = Enemy(enemy_spawn_x, enemy_spawn_y)
    enemies.add(enemy)
    all_sprites.add(enemy)

    for _ in range(10):
        point = Point()
        points.add(point)
        all_sprites.add(point)

    neutral_npc = NeutralNPC(walls)
    neutral_npcs.add(neutral_npc)
    all_sprites.add(neutral_npc)

    score = 0
    npc_interactions = 0  # Counter for NPC interactions
    game_over = False
    game_start_time = pygame.time.get_ticks()  # Track game start time

    while True:
        screen.fill(BLACK)  # Clear the screen at the start of each frame
        
        # Set the wall color to white
        WALL_COLOR = (255, 255, 255)

        # Draw the walls
        for wall in walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            keys = pygame.key.get_pressed()
            player.update(keys, walls)

            for enemy in enemies:
                enemy.update(walls)

            # Update Neutral NPCs
            for neutral_npc in neutral_npcs:
                neutral_npc.update()

            # Check if NPC is still alive, if not game over
            if len(neutral_npcs) == 0:
                print("The NPC has despawned!")
                game_over = True

            # Check collision with enemies only if more than 2 seconds have passed
            elapsed_time = (pygame.time.get_ticks() - game_start_time) / 1000  # Time in seconds
            if elapsed_time >= 2 and pygame.sprite.spritecollideany(player, enemies):
                print("Collision with enemy!")
                game_over = True

            # Collect points
            collected_points = pygame.sprite.spritecollide(player, points, True)
            for _ in collected_points:
                point = Point()
                points.add(point)
                all_sprites.add(point)

            score += len(collected_points)

            # Check collision with neutral NPC
            if score >= 3 and pygame.sprite.spritecollideany(player, neutral_npcs):
                neutral_npc.respawn(walls)
                score -= 3
                npc_interactions += 1  # Increment the NPC interactions counter
                
                # Add a new enemy each time an NPC is interacted with
                enemy_spawn_x, enemy_spawn_y = find_enemy_spawn_point(enemies, walls)
                new_enemy = Enemy(enemy_spawn_x, enemy_spawn_y)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            screen.blit(background_image, (0, 0))
            all_sprites.draw(screen)
            draw_scoreboard(score, npc_interactions)  # Update the scoreboard display

        else:
            display_game_over()
            return

        pygame.display.update()
        clock.tick(FPS)


        if game_over:
            display_game_over()
            break

    pygame.quit()

if __name__ == "__main__":
    display_title_screen()
    main()
