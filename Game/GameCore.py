from CharacterDownloader import Downloader
from WeaponDownloader import WeaponDownloader
from Character import Character
from Equipment import Equipment
from QuestDownloader import QuestDownloader
from MonsterDownloader import MonsterDownloader
import random
from telegram.ext import ConversationHandler
import requests


def stop(bot, update):
    return ConversationHandler.END


def begin_quest(bot, update):
    return 1

class Game:
    def __init__(self):
        self.weapon_list = None
        self.character_namespace = None
        self.quests = None
        self.monsters = None

    def load_data(self):
        # Загружает словари персонажей, квестов, монстров и оружия
        data = Downloader('data.txt')
        weapons = WeaponDownloader('weapons.txt')
        quests = QuestDownloader('quests.txt')
        monsters = MonsterDownloader('monsters.txt')
        self.weapon_list = weapons.load()
        self.character_namespace = data.load()
        self.quests = quests.load()
        self.monsters = monsters.load()

    def save_data(self):
        # Сохраняет только оружие и персонажей
        data = Downloader('data.txt')
        weapons = WeaponDownloader('weapons.txt')
        weapons.save(self.weapon_list)
        data.save(self.character_namespace)

    def register(self, user_data, *args):
        # Регистрирует нового персонажа
        #  и добавляет его в словарь
        try:
            name, password = args[0], args[1]
        except LookupError:
            return 'Invalid number of arguments!'
        if name in self.character_namespace.keys():
            return "This name is already taken!"
        else:
            self.character_namespace[name] = Character(name, password)
            self.save_data()
            return "Success!"

    def forge(self, user_data, *args):
        # Функция позволяет создать новое
        # оружие и добавить его в словарь
        try:
            name, eq_type, level_bonus, level = args[0], args[1], args[2], args[3]
        except LookupError:
            return 'Invalid number of arguments!'
        weapon = Equipment(name, eq_type, level_bonus, level)
        if weapon not in self.weapon_list:
            self.weapon_list[weapon.name] = weapon
            self.save_data()
            return "New weapon created!"
        return "Success!", weapon

    def log_in(self, user_data, *args):
        # Функция входа
        try:
            name = args[0]
            password = args[1]
        except LookupError:
            return 'Invalid number of arguments!'
        if name in self.character_namespace.keys() \
                and self.character_namespace[name].password == password:
            user_data['hero'] = self.character_namespace[name]
            return "Logged in successfully", True
        else:
            return "Invalid login or password!", False

    def start_quest(self, bot, job):
        # Начинает квест
        user_data = job.context['user_data']
        update = job.context['update']
        try:
            hero = user_data['hero']
        except KeyError:
            update.message.reply_text("Register or login to execute this operation.")
            user_data['result'] = ConversationHandler.END
        else:
            mission = user_data['mission']
            # После проверки входных данных,
            # получаем случайного монстра из
            # всех возможных существ в этом
            # подземелье.
            monster = self.monsters[random.choice(mission.monster_pool)]
            print(monster)
            monster = monster.generate_monster(hero.level)
            print(monster)
            success, log = self.challenge_monster(user_data, monster)
            update.message.reply_text(log)
            if not success\
               and hero.level != 1:
                hero.level -= 1
                update.message.reply_text("Defeat!")
                user_data['hero'] = hero
                user_data['result'] = ConversationHandler.END
            else:
                hero.level += 1
                user_data['weapon'] = self.weapon_list[mission.calculate_loot()]
                update.message.reply_text("Victory!")
                # После победы даём персонажу часть экипировки.
                weapon = user_data['weapon']
                update.message.reply_text(
                    "You found weapon: \n" +
                    weapon.call_info() +
                    "Do you want to take it instead of yours?"
                )
                user_data['hero'] = hero
                user_data['result'] = 1
        user_data['mission'] = None

    def summon_monster(self, name, level):
        return self.monsters[name].generate_monster(level)

    @staticmethod
    def challenge_monster(user_data, *args):
        # Функция сражения с монстром
        print('da')
        try:
            monster = args[0]
        except LookupError:
            return 'Invalid number of arguments!'
        fl = random.choice([True, False])
        hero = user_data['hero']
        past_hp_monster = monster.hp
        print('2')
        past_hp_hero = hero.get_hp()
        result = ''
        while True:
            print(result)
            if past_hp_monster <= 0:
                result += "Victory!\n"
                user_data['hero'] = hero
                return [True, result]

            elif past_hp_hero <= 0:
                result += "Defeat!\n"
                user_data['hero'] = hero
                return [False, result]

            elif fl:
                    damage = int(int(hero.get_damage()) + random.randint(-hero.differ, hero.differ))
                    past_hp_monster -= damage
                    result += hero.name + ' hit ' + monster.name + ' with ' + str(damage) + ' damage!\n'
                    result += hero.name + " : " + str(past_hp_hero) + '\n'
                    result += monster.name+' : ' + str(past_hp_monster) + '\n'

                    fl = False

            elif not fl:
                    damage = monster.damage
                    result += monster.name + ' hit ' + hero.name + ' with ' + str(damage) + ' damage!\n'
                    past_hp_hero -= damage
                    result += hero.name + " : " + str(past_hp_hero) + '\n'
                    result += monster.name+' : ' + str(past_hp_monster) + '\n'

                    fl = True

    def ask_trade_telegram_conversation_question_first_response(self, bot, update, user_data):
        weapon = user_data['weapon']
        hero = user_data['hero']
        answer = update.message.text
        if answer == 'Y':
            if weapon.type == 'Armor':
                hero.Armor = weapon
                user_data['hero'] = hero
                self.save_data()
            elif weapon.type == 'Inhand':
                update.message.reply_text('Which hand? L/R')
                return 2
            elif weapon.type == 'Magic':
                hero.Magic = weapon
                user_data['hero'] = hero
                self.save_data()
            user_data['weapon'] = None
            return ConversationHandler.END
        else:
            return ConversationHandler.END

    def ask_trade_telegram_conversation_question_second_response(self, bot, update, user_data):
        weapon = user_data['weapon']
        hero = user_data['hero']
        answer = update.message.text
        if answer == 'L':
            hero.Weapon_1 = weapon
        else:
            hero.Weapon_2 = weapon
        update.message.reply_text('Success!')
        user_data['hero'] = hero
        self.save_data()
        user_data['weapon'] = None
        return ConversationHandler.END

    @staticmethod
    def get_character_info(user_data, *args):
        hero = user_data['hero']
        return hero.call_info()

    def show_pic(self, bot, update, job_queue, chat_data, user_data, args):
        print('da')
        delay = 2
        try:
            user_data['mission'] = self.quests[args[0]]
        except LookupError:
            update.message.reply_text("Invalid argument number.")
        else:
            job = job_queue.run_once(self.start_quest, delay, context={'update': update, 'user_data': user_data})
            chat_data['job'] = job
            bot.sendPhoto(update.message.chat.id, download_picture(args[0]))
            return 1

def download_picture(name_of_the_pic):
    response_array = requests.get("https://yandex.ru/images/search?text={}&format=soap"
                                  .format(name_of_the_pic+'+fantasy')).text.split("img_href")
    element_of_array = response_array[1][3:]
    img_adr = ""
    i = 0
    while True:
        if element_of_array[i] == '"':
            break
        img_adr += element_of_array[i]
        i += 1
    return img_adr
