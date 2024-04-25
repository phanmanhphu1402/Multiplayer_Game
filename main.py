import pygame
import sys
from model.platform import *

# Khởi tạo Pygame
pygame.init()

# Cài đặt màn hình và kích thước
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 750
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fighting Game")
# Các màu sắc
player_image = pygame.image.load("image\character2.png")
player_width, player_height = player_image.get_size()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

platforms = [Platform(200, SCREEN_HEIGHT - 50, 400, 20),  # Vật thể 1
             Platform(50, SCREEN_HEIGHT - 150, 200, 20), # Vật thể 2
             Platform(600, SCREEN_HEIGHT - 250, 200, 20)]# Vật thể 3
# Các người chơi
player1_pos = [SCREEN_WIDTH-player_width, SCREEN_HEIGHT-player_height]

# Vận tốc di chuyển
player_speed = 10
jumping = False
jump_count = 16

def check_collision(player_rect):
    for platform in platforms:
        if player_rect.colliderect(platform.rect):
            return True
    return False

def jump():
    global player1_pos, jumping, jump_count
    if not jumping:
        jumping = True
        jump_count = 16
# Vòng lặp trò chơi
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                jump()
    
    # Di chuyển người chơi
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        player1_pos[0] += player_speed
    if keys[pygame.K_a]:
        player1_pos[0] -= player_speed
    if jumping:
        if jump_count >= -14:
            neg = 1
            if jump_count < 0:
                neg = -1
            player1_pos[1] -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            jumping = False

    # Giới hạn di chuyển của người chơi
    player1_pos[0] = max(0, min(SCREEN_WIDTH - player_width, player1_pos[0]))
    player1_pos[1] = max(0, min(SCREEN_HEIGHT - player_height, player1_pos[1]))

    # Xóa màn hình và vẽ lại
    player_rect = pygame.Rect(player1_pos[0], player1_pos[1], player_width, player_height)
    if check_collision(player_rect):
        jumping = False
        jump_count = 0
        player1_pos[1] = platforms[0].rect.top - player_height

    # Xóa màn hình và vẽ lại
    screen.fill(WHITE)
    for platform in platforms:
        pygame.draw.rect(screen, BLACK, platform.rect)
    screen.blit(player_image, player1_pos)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Kết thúc Pygame
pygame.quit()
sys.exit()