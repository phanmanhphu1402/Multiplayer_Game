class Game:
    def __init__(self, id):
        self.id = id
        self.ready = False
        self.p1Went = False
        self.p2Went = False
        self.guessing = False
        self.betting = False
        self.playerTurn = 0
        self.winner = 0
        self.messagesList = []
        self.cardsList = [1,2,3,4,5,6,7,8,9,10,
                          11,12,13,14,15,16,17,18,
                          19,20,21,22,23,24,25,26,
                          27,28,29,30,31,32,33,34,
                          35,36,37,38,39,40,41,42,
                          43,44,45,46,47,48,49,50,
                          51,52,53,54]
        self.guess = None
        self.card = [None, None]
        self.score = [10, 10]
        self.bet = [1, 1]

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.p1Went and self.p2Went and self.guessing and self.betting

    def check_player_win(self):
        if self.guess == "High":
            if self.card[0] < self.card[1]:
                self.winner = 0
            else:
                self.winner = 1
        elif self.guess == "Low":
            if self.card[0] > self.card[1]:
                self.winner = 0
            else:
                self.winner = 1
        return self.winner
    
    def check_win(self):
        if self.check_player_win() == 0:
            self.score[0] += self.bet[1]
            self.score[1] -= self.bet[1]
            self.winner = 0
        elif self.check_player_win() == 1:
            self.score[1] += self.bet[1]
            self.score[0] -= self.bet[1]
            self.winner = 1
        return self.winner
    
    # def changeTurn(self):
    #     if(self.playerTurn == 0):
    #         self.playerTurn = 1
    #     else:
    #         self.playerTurn = 0
    
    def resetGame(self):
        self.playerTurn = 0
        self.ready = True
        self.winner = 0
        self.p1Went = False
        self.p2Went = False
        self.guessing = False
        self.betting = False
        self.bet = [1, 1]
        if len(self.cardsList) <= 2:
            self.cardsList = [1,2,3,4,5,6,7,8,9,10,
                          11,12,13,14,15,16,17,18,
                          19,20,21,22,23,24,25,26,
                          27,28,29,30,31,32,33,34,
                          35,36,37,38,39,40,41,42,
                          43,44,45,46,47,48,49,50,
                          51,52,53,54]

    def changerRouse(self):
        self.score[0] , self.score[1] = self.score[1], self.score[0]
        print(self.score)