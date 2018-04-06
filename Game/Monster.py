import copy


class Monster:
    def __init__(self, name, level, hp, damage):
        self.hp = hp
        self.damage = damage
        self.level = int(level)
        self.name = name
        self.Hero = None
        self.differ = True

    def call_level(self):
        return self.level

    def call_info(self):
        x = "Monster "+str(self.name)+' '+str(self.level)+'LVL'
        return x

    def copy(self):
        return copy.deepcopy(self)

    def call_brief_data(self):
        x = self.name+' '+str(self.level)+'LVL'
        return ' '.join(x)

    def generate_monster(self,level):
        self.Hero = self.copy()
        if self.level >= level*3:
            self.Hero.name = "Miserable "+self.Hero.name
        elif self.level >= level*2:
            self.Hero.name = "Weak "+self.Hero.name
        elif level*2 > self.level > int(level*0.5):
            pass
        elif self.level < level//2:
            self.Hero.name = "Strong "+self.Hero.name
        elif self.level < level//3:
            self.Hero.name = "Dreadful "+self.Hero.name
        self.Hero.level = level
        self.Hero.hp = int(self.hp*(level/self.level))
        self.Hero.damage = int(self.damage * (level / self.level))
        self.Hero.name = self.Hero.name.capitalize()
        return self.Hero


