import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Game settings
FPS = 30
GRAVITY = 0.5
BIRD_JUMP = -6
PIPE_SPEED = 4
PIPE_GAP = 150

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird - Red Bird")

# Clock
clock = pygame.time.Clock()

# Load assets
font = pygame.font.Font(None, 36)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.width = 30
        self.height = 30
        self.velocity = 0

    def draw(self):
        pygame.draw.ellipse(screen, RED, (self.x, self.y, self.width, self.height))

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def jump(self):
        self.velocity = BIRD_JUMP

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.top = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
        self.bottom = self.top + PIPE_GAP
        self.width = 50

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top))
        pygame.draw.rect(screen, GREEN, (self.x, self.bottom, self.width, SCREEN_HEIGHT - self.bottom))

    def update(self):
        self.x -= PIPE_SPEED

# Main game loop
def main():
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + i * 200) for i in range(3)]
    score = 0
    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        # Update bird and pipes
        bird.update()
        for pipe in pipes:
            pipe.update()

            # Reset pipe when it goes off screen
            if pipe.x + pipe.width < 0:
                pipe.x = SCREEN_WIDTH
                pipe.top = random.randint(50, SCREEN_HEIGHT - PIPE_GAP - 50)
                pipe.bottom = pipe.top + PIPE_GAP
                score += 1

            # Collision detection
            if (
                bird.x + bird.width > pipe.x and bird.x < pipe.x + pipe.width and
                (bird.y < pipe.top or bird.y + bird.height > pipe.bottom)
            ) or bird.y + bird.height > SCREEN_HEIGHT or bird.y < 0:
                game_over(score)

        # Draw bird and pipes
        bird.draw()
        for pipe in pipes:
            pipe.draw()

        # Draw score
        draw_text(f"Score: {score}", font, BLACK, screen, SCREEN_WIDTH // 2, 50)

        # Update display and clock
        pygame.display.flip()
        clock.tick(FPS)

def game_over(score):
    screen.fill(WHITE)
    draw_text("Game Over!", font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
    draw_text(f"Final Score: {score}", font, BLACK, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
    pygame.display.update()
    pygame.time.wait(3000)  # Wait for 3 seconds
    main()

# Run the game
if __name__ == "__main__":
    main()
