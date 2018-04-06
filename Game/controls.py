from GameCore import Game


class Controller:
    def __init__(self):
        self.cycle = Game()

    def start(self):
        name = None
        self.cycle.load_data()
        while True:
            line = input()

            if line.startswith('/newchar')\
                    and len(line.split()) == 2:
                x = line.split()
                self.cycle.register(x[1])

            elif line.startswith('/newchar')\
                    and len(line.split()) != 2:
                print("Usage: /newchar <name of your new character>")

            elif line.startswith("/fight")\
                    and len(line.split()) == 3:
                x = line.split()
                self.cycle.fight(x[1], x[2])

            elif line.startswith('/fight')\
                    and len(line.split()) != 3:
                print("Usage: /fight <name of first warrior> <name of second warrior>")

            elif line.startswith('/endgame'):
                break

            elif line.startswith('/login')\
                    and len(line.split()) == 2:
                x = line.split()
                if self.cycle.log_in(x[1]):
                    name = x[1]

            elif line.startswith('/login')\
                    and len(line.split()) != 2:
                print("Usage: /login <name of your character>")

            elif line.startswith('/forge')\
                    and len(line.split()) > 4:
                x = line.split()
                self.cycle.forge(x[1], x[2], x[3], x[4])

            elif line.startswith('/forge')\
                    and len(line.split()) < 4:
                print("Usage: /forge <bonus> <level> <type>")

            elif line.startswith('/find')\
                    and len(line.split()) == 2:
                x = line.split()
                self.cycle.ask_trade(self.cycle.weapon_list[x[1]])

            elif line.startswith('/info'):
                print(self.cycle.Hero.call_info())

            elif line.startswith('/quest')\
                    and len(line.split()) == 2:
                x = line.split()
                if x[1] in self.cycle.quests.keys():
                    self.cycle.start_quest(x[1])

            elif line.startswith('/quest_list'):
                for i in self.cycle.quests.keys():
                    print(self.cycle.quests[i].call_info())

        if name:
            self.cycle.character_namespace[name] = self.cycle.Hero
            print("Saved Successfully")
        self.cycle.save_data()

controls = Controller()
temp = input()

controls.start()
