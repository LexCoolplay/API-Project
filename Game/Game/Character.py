from WeaponDownloader import WeaponDownloader


class Character:
    def __init__(self, name, password, level=1, armor='Chest', weapon1='Fist', weapon2='Fist', magic='Nothing'):
        weapons_raw_data = WeaponDownloader("weapons.txt")
        self.weapon_list = weapons_raw_data.load()
        self.Armor = self.weapon_list[armor]
        self.Weapon_1 = self.weapon_list[weapon1]
        self.Weapon_2 = self.weapon_list[weapon2]
        self.level = int(level)
        self.Magic = self.weapon_list[magic]
        self.name = name
        self.password = password

    def call_level(self):
        return self.level

    def call_power(self):
        return self.Armor.call_level_bonus()\
               + self.Magic.call_level_bonus()\
               + self.Weapon_1.call_level_bonus()\
               + self.Weapon_2.call_level_bonus()

    def call_info(self):
        result = "Character "+str(self.call_level())+'LVL '\
          + ':\n'+self.Armor.call_info()\
          + self.Weapon_1.call_info()\
          + self.Weapon_2.call_info()\
          + self.Magic.call_info()
        return result

    def call_brief_data(self):
        result = [self.name,
                  self.password,
                  str(self.level),
                  str(self.Armor.name),
                  str(self.Weapon_1.name),
                  str(self.Weapon_2.name),
                  str(self.Magic.name)]
        return ' '.join(result)
