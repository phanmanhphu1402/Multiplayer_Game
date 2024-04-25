import pygame

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("Fighting")

bg_image = pygame.image.load("image/background/City of Tears.jpg").convert_alpha()

#Hàm vẽ background
def draw_bg():
    scale_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH,SCREEN_HEIGHT))
    screen.blit(scale_bg, (0,0))
    


#Vòng lập game
run = True
while run:

    draw_bg()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Cập nhật vẽ
    pygame.display.update()
    
pygame.quit()




































































