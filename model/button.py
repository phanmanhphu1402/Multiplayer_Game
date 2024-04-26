import pygame

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click = False
    
    def draw(self, surface):
        action = False
        #Kiểm tra vị trí con trỏ
        pos = pygame.mouse.get_pos()

        #Kiểm tra con trỏ và click
        if self.rect.collidepoint(pos):
            #Nhấn chuột phải
            if pygame.mouse.get_pressed()[0] == 1 and self.click == False:
                self.click = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.click = False
        #Vẽ nút ra màn hình
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action