class Equipment:
    def __init__(self, name, eq_type, level_bonus, level):
        self.name = name
        self.level_bonus = level_bonus
        self.level = level
        self.type = eq_type

    def call_level_bonus(self):
        return self.level_bonus

    def call_level(self):
        return self.level

    def call_type(self):
        return self.type

    def call_info(self):
        x = self.call_type() + ' '\
            + 'level ' + str(self.call_level())\
            + ' bonus ' + str(self.call_level_bonus())\
            + ' '+self.name + ' ' + '\n'
        return x

    def call_brief(self):
        x = self.name+' '\
            + self.type+' '\
            + str(self.level_bonus)\
            + ' '+str(self.level)
        return x
