import random

import pygame
from network import Network
from game import Game
from button import Button
from attribute import Attribute
import pickle
import sys

pygame.init()

# Kich co man hinh va chatbox
WIDTH_SCREEN = 700
HEIGHT_SCREEN = 700
ChatBox = 200

win = pygame.display.set_mode((WIDTH_SCREEN + ChatBox, HEIGHT_SCREEN))

pygame.display.set_caption("Guessing Game")

font = pygame.font.SysFont("arial", 20)
fontCard = pygame.font.SysFont("arial", 40)

LINE_WIDTH = 15

# Mau
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (245, 88, 88)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Chat box object
chatbox = pygame.Rect(WIDTH_SCREEN, 0, ChatBox, HEIGHT_SCREEN)
input_box = pygame.Rect(WIDTH_SCREEN + 10, HEIGHT_SCREEN - 50, 120, 40)
send_message_button = pygame.Rect(WIDTH_SCREEN + 140, HEIGHT_SCREEN - 50, 60, 40)

# Game button
draw_button = pygame.Rect(20, 50, 100, 40)
high_button = pygame.Rect(20, 100, 100, 40)
low_button = pygame.Rect(20, 150, 100, 40)


# Game card
border_card_1 = pygame.Rect(300 - 2, 50 - 2, 100 + 4, 160 + 4)
border_card_2 = pygame.Rect(520 - 2, 50 - 2, 100 + 4, 160 + 4)
game_card_1 = pygame.Rect(300, 50, 100, 160)
game_card_2 = pygame.Rect(520, 50, 100, 160)

# Card Attri
heart = pygame.image.load("image/heart.png").convert_alpha()
spades = pygame.image.load("image/spades.png").convert_alpha()


ListMessage = []
StartMessage = []
input_text = ''

players = ["Dealer", "Player"]
game = Game(0)

btns = [Button("ONLINE MODE", WIDTH_SCREEN // 2 - 150, 50, RED, 250, 80),
        Button("OFFLINE MODE", WIDTH_SCREEN // 2 - 150, 150, RED, 250, 80),
        Button("TUTORIAL", WIDTH_SCREEN // 2 - 150, 250, RED, 250, 80),
        Button("EXIT", WIDTH_SCREEN // 2 - 150, 350, BLACK, 250, 80)]

btns_dealer = [Button("Draw", 20, 50, BLACK, 100, 40),
        Button("High", 20, 100, BLACK, 100, 40),
        Button("Low", 20, 150, BLACK, 100, 40)]

btns_player = [Button("Draw", 20, 50, BLACK, 100, 40),
            Button("1", 20, 100, BLACK, 40, 40),
            Button("2", 20, 150, BLACK, 40, 40),
            Button("3", 20, 200, BLACK, 40, 40),
            Button("4", 80, 100, BLACK, 40, 40),
            Button("5", 80, 150, BLACK, 40, 40),
            Button("6", 80, 200, BLACK, 40, 40)]

btn_back = Button("BACK", WIDTH_SCREEN // 2 - (100/2), 600, BLACK, 100, 40)

def draw_game_table(player):
    if player == "Dealer":
        for btn in btns_dealer:
            btn.draw(win)
    if player == "Player":
        for btn in btns_player:
            btn.draw(win)

def draw_card1(card_value, game_card, border):
    color = BLACK
    pygame.draw.rect(win, BLACK, border)
    pygame.draw.rect(win, WHITE, game_card)
    if card_value >= 27:
        color = RED
        heartAttribute = Attribute(275 + (100 // 2), 200 // 2, heart, 1)
        heartAttribute.draw(win)
    else:
        color = BLACK
        spadesAttribute = Attribute(280 + (100 // 2), 200 // 2, spades, 1)
        spadesAttribute.draw(win)
    value = font.render(str(card_value), True, color)
    win.blit(value, (310, 60))
    win.blit(value, (380 - 10, 190 - 10))

def draw_card2(card_value, game_card, border):
    color = BLACK
    pygame.draw.rect(win, BLACK, border)
    pygame.draw.rect(win, WHITE, game_card)
    if card_value >= 27:
        color = RED
        heartAttribute = Attribute(495 + (100 // 2), 200 // 2, heart, 1)
        heartAttribute.draw(win)
    else:
        color = BLACK
        spadesAttribute = Attribute(500 + (100 // 2), 200 // 2, spades, 1)
        spadesAttribute.draw(win)
    value = font.render(str(card_value), True, color)
    win.blit(value, (530, 60))
    win.blit(value, (600 - 10, 190 - 10))

def draw_chat_box():
    pygame.draw.rect(win, WHITE, chatbox)
    pygame.draw.rect(win, WHITE, input_box, 0)
    pygame.draw.rect(win, BLACK, input_box, 1)
    pygame.draw.rect(win, BLACK, send_message_button, 1)
    global game
    playerTurn_surface = font.render("CHAT BOX", True, BLACK)
    win.blit(playerTurn_surface, (WIDTH_SCREEN + 10, 10))

    # Ve tin nhan
    if len(StartMessage) > 0:
        for i, message in enumerate(StartMessage):
            text_surface = font.render(message, True, BLACK)
            win.blit(text_surface, (WIDTH_SCREEN + 10, 30 + i * 24))
    else:
        for i, message in enumerate(ListMessage):
            text_surface = font.render(message, True, BLACK)
            win.blit(text_surface, (WIDTH_SCREEN + 10, 30 + i * 24))

    # Ve input chat box
    input_surface = font.render(input_text, True, BLACK)
    win.blit(input_surface, (input_box.x + 5, input_box.y + 10))

    # Ve nut gui
    send_text = font.render("Send", True, BLACK)
    win.blit(send_text, (send_message_button.x + 10, send_message_button.y + 10))



def redrawWindow(win, game, player):
    win.fill(RED)

    if not (game.connected()):
        waiting_screen("Waiting For Player.... If dont have player exit in 20s")
    else:
        draw_game_table(player)
        draw_chat_box()
        if game.p1Went:
            # cardP1 = font.render("CARD1: "+ str(game.card[0]), True, WHITE)
            # win.blit(cardP1, (200, 50))
            cardP1 = font.render("CARD1: ", True, WHITE)
            win.blit(cardP1, (200, 50))
            draw_card1(game.card[0], game_card_1, border_card_1)
        if game.guessing:
            guessResult = font.render("DEALER GUESS: " + str(game.guess), True, WHITE)
            win.blit(guessResult, (200, 300))
        if game.p2Went:
            cardP2 = font.render("CARD2: ", True, WHITE)
            win.blit(cardP2, (420, 50))
            draw_card2(game.card[1], game_card_2, border_card_2)
        if game.betting:
            betting = font.render("PLAYER BETTING: " + str(game.bet[1]), True, WHITE)
            win.blit(betting, (420, 300))
        # if player == "Dealer":
        dealerScore = font.render("DEALER SCORE: " + str(game.score[0]), True, WHITE)
        win.blit(dealerScore, (50, 600))
        # if player == "Player":
        playerScore = font.render("PLAYER SCORE: " + str(game.score[1]), True, WHITE)
        win.blit(playerScore, (250, 600))
    pygame.display.update()


def waiting_screen(text):
    # pygame.draw.rect(win, BLACK, (WIDTH_SCREEN // 2, HEIGHT_SCREEN // 2 - 50, WIDTH_SCREEN, 100))
    font = pygame.font.Font(None, 36)
    text = font.render(text, True, WHITE)
    win.blit(text, (WIDTH_SCREEN // 2 - text.get_width() // 2 + 100, 0 + text.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(2000)


# Online Mode
def Online():
    win = pygame.display.set_mode((WIDTH_SCREEN + ChatBox, WIDTH_SCREEN))
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = n.getP()
    global ListMessage
    global StartMessage
    global input_text
    global game
    StartMessage = ["You are : " + player]

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
            ListMessage = game.messagesList

            #Neu co ng choi chat
            if len(ListMessage) > 0:
                StartMessage = []

        except:
            run = False
            print("Couldn't get game")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if send_message_button.collidepoint(event.pos):
                    # Them tin nhan vao list
                    ListMessage.append(player + " : " + input_text)
                    # Gui tin nhan vao game message
                    input_text = ""
                    game.messages = ListMessage
                    game = n.send(game)
                pos = pygame.mouse.get_pos()
                if player == "Player":
                    btns_play = btns_player
                if player == "Dealer":
                    btns_play = btns_dealer
                for btn in btns_play:
                    if btn.click(pos) and game.connected():
                        if btn.text == "Draw" and player == "Dealer" or btn.text == "Draw" and player == "Player" and game.betting == True:
                            if player == "Dealer" and game.p1Went == False:
                                drawn_number = random.choice(game.cardsList)
                                # Remove the drawn number from the list
                                game.cardsList.remove(drawn_number)
                                print(drawn_number)
                                game.card[0] = drawn_number
                                game.p1Went = True
                                game = n.send(game)
                            if player == "Player" and game.p2Went == False and game.guessing == True and game.betting:
                                drawn_number = random.choice(game.cardsList)
                                # Remove the drawn number from the list
                                game.cardsList.remove(drawn_number)
                                print(drawn_number)
                                game.card[1] = drawn_number
                                game.p2Went = True
                                game = n.send(game)
                        if btn.text == "High" or btn.text == "Low":
                            if player == "Dealer" and game.p1Went == True:
                                game.guess = btn.text
                                print(btn.text)
                                game.guessing = True
                                game = n.send(game)
                        else:
                            if player == "Player" and btn.text == "Draw":
                                pass
                            elif player == "Player" and game.betting == False and game.p1Went and game.guessing:
                                game.bet[1] = int(btn.text)
                                game.betting = True
                                game = n.send(game)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Xóa ký tự cuối cùng
                elif event.key == pygame.K_RETURN:
                    # Them tin nhan vao List tin nhan
                    ListMessage.append(player + " : " + input_text)
                    # Gui vao list message cuar game
                    input_text = ""
                    game.messages = ListMessage
                    game = n.send(game)
                else:
                    input_text += event.unicode
        # check player win
        if game.bothWent():
            print(game.score)
            redrawWindow(win, game, player)
            game.check_win()
            game = n.send(game)
            waiting_screen(players[game.winner] + " Win!")
            print(game.score)
            if player == "Player":
                player = "Dealer"
            else:
                player = "Player"
            # game.changerRouse()
            game = n.send("reset")
        redrawWindow(win, game, player)

def Offline():
    win = pygame.display.set_mode((WIDTH_SCREEN, WIDTH_SCREEN))
    run = True
    clock = pygame.time.Clock()
    game = Game(0)
    player = "Player"
    while run:
        win.fill(RED)
        choice = ["High", "Low"]
        if not game.p1Went:
            game.card[0] = random.choice(game.cardsList)
            game.cardsList.remove(game.card[0])
            game.p1Went = True
        if not game.guessing:
            game.guess = random.choice(choice)
            game.guessing = True
        if game.p1Went:
            cardP1 = font.render("CARD1: ", True, WHITE)
            win.blit(cardP1, (200, 50))
            draw_card1(game.card[0], game_card_1, border_card_1)
        if game.guessing:
            guessResult = font.render("DEALER GUESS: "+ str(game.guess), True, WHITE)
            win.blit(guessResult, (200, 300))
        playerScore = font.render("PLAYER SCORE: " + str(game.score[1]), True, WHITE)
        win.blit(playerScore, (50, 500))
        dealerScore = font.render("BOT SCORE: " + str(game.score[0]), True, WHITE)
        win.blit(dealerScore, (250, 500))
        draw_game_table(player)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns_player:
                    if btn.click(pos):
                        if btn.text == "Draw" and game.betting == True and game.p2Went == False:
                            game.card[1] = random.choice(game.cardsList)
                            game.p2Went = True
                        if not game.betting and btn.text != "Draw":
                            game.bet[1] = int(btn.text)
                            game.betting = True
        if game.p2Went:
            # cardP2 = font.render("CARD2: "+ str(game.card[1]), True, WHITE)
            # win.blit(cardP2, (200, 150))
            cardP2 = font.render("CARD2: ", True, WHITE)
            win.blit(cardP2, (420, 50))
            draw_card2(game.card[1], game_card_2, border_card_2)
        if game.betting:
            betting = font.render("PLAYER BETTING: "+ str(game.bet[1]), True, WHITE)
            win.blit(betting, (420, 300))
        if game.bothWent():
            game.check_win()
            if game.check_win() == 0:
                waiting_screen("BOT WIN")
            else:
                waiting_screen("PLAYER WIN")

            game.resetGame()

        pygame.display.update()


def Tutorial():
    win = pygame.display.set_mode((WIDTH_SCREEN, WIDTH_SCREEN))
    run = True
    lawList = ["Law 1: Dealer always go first",
               "Law 2: Dealer has to Draw first and make a Guess",
               "Law 3: After Dealer has done his/her move Player can go",
               "Law 4: Player can bet from 1-6 score",
               "Law 5: Player has to bet before draw a number",
               "Law 6: Dealer betting base on Player bet",
               "Law 7: If Dealer Guess the card Player draw is correct Dealer win else Dealer lose",
               "Law 8: If Check who win and score will be plus/minus base on bet result"]

    while run:
        win.fill(RED)
        btn_back.draw(win)
        lineSpace = 40
        for law in lawList:
            text = font.render(law, True, WHITE)
            win.blit(text, (50, lineSpace))
            lineSpace += 40
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btn_back.click(pos):
                    run = False
        pygame.display.update()


def menu():
    win = pygame.display.set_mode((WIDTH_SCREEN, WIDTH_SCREEN))
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill(WHITE)
        for btn in btns:
            btn.draw(win)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos):
                        run = False
                        if btn.text == "ONLINE MODE":
                            Online()
                        if btn.text == "OFFLINE MODE":
                            Offline()
                        if btn.text == "TUTORIAL":
                            Tutorial()
                        if btn.text == "EXIT":
                            pygame.quit()


while True:
    menu()
