import pygame
from model.character import Character


pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("Fighting")

bg_image = pygame.image.load("image/background/City of Tears.jpg").convert_alpha()

#Đặt tốc độ cập nhật frame
clock = pygame.time.Clock()
FPS = 60

#Hàm vẽ background
def draw_bg():
    scale_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(scale_bg, (0,0))

character_1 = Character(200, 310)
character_2 = Character(700, 310)

#Vòng lập game
run = True
while run:
    clock.tick(FPS)

    draw_bg()

    character_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, character_2)

    #Vẽ nhân vật
    character_1.draw(screen)
    character_2.draw(screen)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Cập nhật vẽ
    pygame.display.update()
    
pygame.quit()




































































