import random
from LootGenerator import Treasure


class Quest:
    def __init__(self, level, name, monster_pool):
        self.level = level
        self.name = name
        self.monster_pool = monster_pool

    def calculate_loot(self):
        loot = Treasure()
        result = random.randint(1, 100)
        if result < 94:
            return random.choice(loot.get_pool(int(self.level)))
        else:
            if(loot.get_pool(int(self.level)+1)):
                return random.choice(loot.get_pool(int(self.level)+1))
            else:
                return random.choice(loot.get_pool(int(self.level)))

    @staticmethod
    def calculate_loss():
        return False

    def call_info(self):
        x = "Quest in "+self.name\
          + '. Recommended level: '+self.level+'.'
        return x

    def call_brief_data(self):
        x = self.level+' '+self.name
        return x
