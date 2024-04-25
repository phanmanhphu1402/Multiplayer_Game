import pygame

class Character():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0: đứng yên, 1: chạy, 2: nhảy, 3: tấn công1, 4: tấn công2, 5: tấn công, 6: chết
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        #extract hình từ sprite sheet
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface( x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list


    def attack(self, target):
        if self.attack_cooldown == 0:
            #Thực hiện tấn công
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 10
                target.hit = True

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    #Xử lý cập nhật hoạt ảnh
    def update(self):
        #Kiểm tra hành đôn gj mà người chơi đang thực hiện
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.hit == True:
            self.update_action(5)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)


        animation_cooldown = 50
        #Cập nhật hình ảnh
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        #Kiểm tra hoạt ảnh đã hết hay chưa
        if self.frame_index >= len(self.animation_list[self.action]):
            #Nếu nhân vật đã chết thì kết thúc hoạt ảnh
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                #Kiểm tra đòn tấn công đã được thực hiện chưa
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                #Kiểm tra xem nhân vật bị nhận đòn tấn công
                if self.action == 5:
                    self.hit = False
                    #Nếu người chơi đang ở giữa 1 đòn đánh, thì không được thực hiện đòn tấn công
                    self.attacking = False
                    self.attack_cooldown = 20

    def update_action(self, new_action):
        #Kiểm tra xem hành động mới khác không ?
        if new_action != self.action:
            self.action = new_action
            #Cập nhật cài đặt hành động
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def move(self, screen_width, screen_height, target, round_over):
        toc_do = 10
        trong_luc = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        #nút nhấn
        key = pygame.key.get_pressed()

        #Chỉ có thể thực hiện các hành động khác khi ngừng tấn công
        if self.attacking == False and self.alive == True and round_over == False:
            if self.player == 1:
            #di chuyển
                if key[pygame.K_a]:
                    dx = -toc_do
                    self.running = True
                if key[pygame.K_d]:
                    dx = toc_do
                    self.running = True

                #Nhảy
                if key[pygame.K_w] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                
                #Tấn công
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    #Định hình đòn đánh
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2



            if self.player == 2:
            #di chuyển
                if key[pygame.K_LEFT]:
                    dx = -toc_do
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = toc_do
                    self.running = True

                #Nhảy
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True
                
                #Tấn công
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    #Định hình đòn đánh
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
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

        #Điều chỉnh nhân vật mặt đối mặt
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #Áp dụng khoảng trễ tấn công
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        #cập nhật vị trí nhân vật
        self.rect.x += dx
        self.rect.y += dy
    
    





































