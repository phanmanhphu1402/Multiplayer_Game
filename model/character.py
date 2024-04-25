import pygame

class Character():
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0

    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx, self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            print("Hit")

        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

    def move(self, screen_width, screen_height, surface, target):
        toc_do = 10
        trong_luc = 2
        dx = 0
        dy = 0

        #nút nhấn
        key = pygame.key.get_pressed()

        #Chỉ có thể thực hiện các hành động khác khi ngừng tấn công
        if self.attacking == False:

            #di chuyển
            if key[pygame.K_a]:
                dx = -toc_do
            if key[pygame.K_d]:
                dx = toc_do
            
            #Nhảy
            if key[pygame.K_w] and self.jump == False:
                self.vel_y = -30
                self.jump = True
            
            #Tấn công
            if key[pygame.K_r] or key[pygame.K_t]:
                self.attack(surface, target)
                #Định hình đòn đánh
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 2

        #Áp dụng trọng lực
        self.vel_y += trong_luc
        dy += self.vel_y

        #Giới hạn di chuyển nhân vật
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        #cập nhật vị trí nhân vật
        self.rect.x += dx
        self.rect.y += dy
    
    