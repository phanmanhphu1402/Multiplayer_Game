import pygame


class Attribute():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.click = False

    def draw(self, surface):
        # Vẽ nút ra màn hình
        surface.blit(self.image, (self.rect.x, self.rect.y))