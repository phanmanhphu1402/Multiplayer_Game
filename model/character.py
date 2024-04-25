class Character():
    def __init__(self, name, health, damage, image, skill):
        self.name = name
        self.health = health
        self.damage = damage
        self.image = image
        self.skill = skill

    def attack(self, target):
        target.health -= self.damage

    def isDead(self):
        if(self.health<=0):
            return True
        return False
    
    