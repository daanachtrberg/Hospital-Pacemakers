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
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (spawn_x, spawn_y)
        self.speed = 7

    def update(self, keys, walls):
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
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 30)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 30)
        self.speed = random.uniform(3, 4)
        self.direction = [random.choice([-1, 1]), random.choice([-1, 1])]

    def update(self, walls):
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
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        self.rect.x = random.randint(0, SCREEN_WIDTH - 8)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - 8)

# Define a NeutralNPC class with a timer
class NeutralNPC(pygame.sprite.Sprite):
    def __init__(self, walls):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.respawn(walls)
        self.spawn_time = pygame.time.get_ticks()

    def respawn(self, walls):
        while True:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
            if not any(self.rect.colliderect(wall) for wall in walls):
                break
        self.spawn_time = pygame.time.get_ticks()  # Reset the timer on respawn

    def update(self):
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
    while True:
        spawn_x = random.randint(0, SCREEN_WIDTH - 30)
        spawn_y = random.randint(0, SCREEN_HEIGHT - 30)
        player_rect = pygame.Rect(spawn_x, spawn_y, 30, 30)
        if not any(player_rect.colliderect(enemy.rect) for enemy in enemies) and not any(player_rect.colliderect(wall) for wall in walls):
            return spawn_x, spawn_y

def display_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("You Died", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

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
                return
        title_animation_offset += title_animation_direction
        if title_animation_offset > 10 or title_animation_offset < -10:
            title_animation_direction *= -1
        mouse_pos = pygame.mouse.get_pos()
        if start_rect.collidepoint(mouse_pos):
            start_text = start_font.render("Start Game", True, HOVER_COLOR)
        else:
            start_text = start_font.render("Start Game", True, WHITE)
        screen.blit(background_image, (0, 0))
        screen.blit(title_text, (title_rect.x, title_rect.y + title_animation_offset))
        screen.blit(start_text, start_rect)
        pygame.display.update()
        clock.tick(FPS)

def draw_scoreboard(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Main game loop
def main():
    walls = [
        pygame.Rect(340, 245, 230, 10),
        pygame.Rect(620, 245, 90, 10),
        pygame.Rect(680, 245, 7, 95),
        pygame.Rect(680, 340, 50, 4),
        pygame.Rect(650, 330, 35, 4),
        pygame.Rect(565, 330, 30, 4),
        pygame.Rect(959, 245, 10, 175),
        pygame.Rect(760, 245, 200, 10),
        pygame.Rect(810, 340, 5, 80),
        pygame.Rect(780, 340, 180, 5),
        pygame.Rect(810, 460, 5, 30),
        pygame.Rect(959, 458, 10, 34),
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

    global all_sprites, enemies, points, neutral_npcs
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    points = pygame.sprite.Group()
    neutral_npcs = pygame.sprite.Group()

    spawn_x, spawn_y = find_spawn_point(enemies, walls)
    player = Player(spawn_x, spawn_y)
    all_sprites.add(player)

    for _ in range(5):
        enemy = Enemy()
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
    game_over = False

    while True:
        screen.fill(BLACK)  # Clear the screen at the start of each frame
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

            if pygame.sprite.spritecollideany(player, enemies):
                print("Collision with enemy!")
                game_over = True

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

            screen.blit(background_image, (0, 0))
            all_sprites.draw(screen)
            draw_scoreboard(score)

        else:
            display_game_over()
            return

        pygame.display.update()
        clock.tick(FPS)

display_title_screen()
main()
