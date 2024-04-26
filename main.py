import pygame
from pygame import mixer
from model.character import Character
from model.button import Button


pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

pygame.display.set_caption("Fighting")

bg_image = pygame.image.load("image/background/City of Tears.jpg").convert_alpha()

#Tải ảnh chiến thắng
victory_img = pygame.image.load("image/icons/victory.png").convert_alpha()

#Đặt kích thước nhân vật
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#Tải nhạc và âm thanh
pygame.mixer.music.load("audio\music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)

sword_fx = pygame.mixer.Sound("audio\sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("audio\magic.wav")
magic_fx.set_volume(0.75)

#Tải sprite nhân vật
warrior_sheet = pygame.image.load("image\characters\warrior\Sprites\warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("image\characters\wizard\Sprites\wizard.png").convert_alpha()

#Đặt số bước của mỗi hoạt ảnh
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#Cài đặt Font chữ
count_font = pygame.font.Font("fonts/turok.ttf", 80)
score_font = pygame.font.Font("fonts/turok.ttf", 30)

#Hàm vẽ chữ
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


#Đặt tốc độ cập nhật frame
clock = pygame.time.Clock()
FPS = 60

#Màu
RED = (255, 0 ,0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

#Chỉnh giá trị của game
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 2000

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
character_1 = Character(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
character_2 = Character(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)


#Tạo nút bấm
start_image = pygame.image.load("image/button/start_btn.png").convert_alpha()
exit_image = pygame.image.load("image/button/exit_btn.png").convert_alpha()
start_button = Button(100, 200, start_image, 0.5)
exit_button = Button(450, 200, exit_image, 0.5)

#Vòng lập game
run = True
while run:
    clock.tick(FPS)

    draw_bg()
    if start_button.draw(screen) == True:
        print("Start")
    if exit_button.draw(screen) == True:
        run = False
    

    #Hiện thanh máu nhân vật
    draw_health_bar(character_1.health,20, 20)
    draw_health_bar(character_2.health,580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P1: " + str(score[1]), score_font, RED, 580, 60)

    #Cập nhật đếm ngược
    if intro_count <= 0:
        character_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, character_2, round_over)
        character_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, character_1, round_over)
    else:
        #Hiển thị đếm ngược
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        if(pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

    #Cập nhật nhân vật
    character_1.update()
    character_2.update()

    # #Vẽ nhân vật
    character_1.draw(screen)
    character_2.draw(screen)

    #Kiểm tra xem người chơi đã bị đánh bại chưa
    if round_over == False:
        if character_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif character_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            character_1 = Character(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            character_2 = Character(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #Cập nhật vẽ
    pygame.display.update()
    
pygame.quit()




































































