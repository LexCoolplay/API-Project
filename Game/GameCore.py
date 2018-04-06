from downloader import Downloader
from WeaponDownloader import WeaponDownloader
from Character import Character
from Equipment import Equipment
from QuestDownloader import QuestDownloader


class Game:
    def __init__(self):
        self.Hero = None
        self.weapon_list = None
        self.character_namespace = None
        self.quests = None

    def load_data(self):
        data = Downloader('data.txt')
        weapons = WeaponDownloader('weapons.txt')
        quests = QuestDownloader('quests.txt')
        self.weapon_list = weapons.load()
        self.character_namespace = data.load()
        self.quests = quests.load()

    def save_data(self):
        data = Downloader('data.txt')
        weapons = WeaponDownloader('weapons.txt')
        weapons.save(self.weapon_list)
        data.save(self.character_namespace)

    def register(self, *args):
        try:
            name, password = args[0], args[1]
        except LookupError:
            return 'Некорректное кол-во аргументов!'
        if name in self.character_namespace.keys():
            return "This name is already exist!"
        else:
            self.character_namespace[name] = Character(name, password)
            self.save_data()
            return "Success!"

    def fight(self, *args):
        try:
            name1, name2 = args[0], args[1]
        except LookupError:
            return 'Некорректное кол-во аргументов!'
        if name1 in self.character_namespace.keys()\
                and name2 in self.character_namespace.keys():
            if self.character_namespace[name1].call_power()\
                    > self.character_namespace[name2].call_power():
                return name1, 'wins!'
            elif self.character_namespace[name2]\
                    > self.character_namespace[name1]:
                return name2, 'wins!'
            else:
                return 'Draw!'
        else:
            return "One of the warriors doesn't exist!"

    def forge(self, *args):
        try:
            name, eq_type, level_bonus, level = args[0], args[1], args[2], args[3]
        except LookupError:
            return 'Некорректное кол-во аргументов!'
        weapon = Equipment(name, eq_type, level_bonus, level)
        if weapon not in self.weapon_list:
            self.weapon_list[weapon.name] = weapon
            self.save_data()
            return "Новое оружие создано!"
        return "Успешно!", weapon

    def ask_trade(self, *args):
        if self.Hero:
            try:
                weapon = args[0]
            except LookupError:
                return 'Некорректное кол-во аргументов!'
            result = "You find:"+' '+weapon.call_info()+'.\n'
            x = input('Do you want to pick it up and drop your current weapon? Y/N ')
            if x[0] == 'Y':
                if weapon.type == 'Armor':
                    self.Hero.Armor = weapon
                elif weapon.type == 'Inhand':
                    x = input('Which hand? L/R')
                    if x[0] == 'L':
                        self.Hero.Weapon_1 = weapon
                    else:
                        self.Hero.Weapon_2 = weapon
                elif weapon.type == 'Magic':
                    self.Hero.Magic = weapon
            else:
                pass
            return result
        else:
            return 'Для выполнения этой команды необходимо войти или зарегестрироватся.'

    def log_in(self, *args):
        try:
            name = args[0]
            password = args[1]
        except LookupError:
            return 'Некорректное кол-во аргументов!'
        if name in self.character_namespace.keys() \
                and self.character_namespace[name].password == password:
            self.Hero = self.character_namespace[name]
            return "Logged in Successfully!", True
        else:
            return "No such character!", False

    def start_quest(self, *args):
        try:
            name = args[0]
        except LookupError:
            return 'Некорректное кол-во аргументов!'
        mission = self.quests[name]
        success = mission.calculate_performance(self.Hero.level)
        if not success\
           and self.Hero.level != 1:
            self.Hero.level -= 1
            return "Defeat!"
        elif type(success) == bool:
            self.Hero.level += 1
            return "Escaped!"
        else:
            self.Hero.level += 1
            self.ask_trade(self.weapon_list[success])
            return "Victory!"
