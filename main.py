import pygame
from model.character import Character


pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("Fighting")

bg_image = pygame.image.load("image/background/City of Tears.jpg").convert_alpha()

#Đặt kích thước nhân vật
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#Tải sprite nhân vật
warrior_sheet = pygame.image.load("image\characters\warrior\Sprites\warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("image\characters\wizard\Sprites\wizard.png").convert_alpha()

#Đặt số bước của mỗi hoạt ảnh
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#Đặt tốc độ cập nhật frame
clock = pygame.time.Clock()
FPS = 60

#Màu
RED = (255, 0 ,0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

#Hàm vẽ background
def draw_bg():
    scale_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(scale_bg, (0,0))

#Hàm vẽ thanh máu
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

#Tạo nhân vật
character_1 = Character(200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
character_2 = Character(700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)

#Vòng lập game
run = True
while run:
    clock.tick(FPS)

    draw_bg()

    #Hiện thanh máu nhân vật
    draw_health_bar(character_1.health,20, 20)
    draw_health_bar(character_2.health,580, 20)

    character_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, character_2)

    #Cập nhật nhân vật
    character_1.update()
    character_2.update()

    # #Vẽ nhân vật
    character_1.draw(screen)
    character_2.draw(screen)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Cập nhật vẽ
    pygame.display.update()
    
pygame.quit()




































































