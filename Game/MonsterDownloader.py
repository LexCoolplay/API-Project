from Monster import Monster


class MonsterDownloader:
    def __init__(self, name):
        self.name = name
        self.monster_list = {}

    def load(self):
        file = open(self.name, 'r');
        for string in file:
            string = string.split()
            monster_name = string[0]
            level = int(string[1])
            self.monster_list[monster_name] = Monster(monster_name, level, int(string[2]), int(string[3]))
        return self.monster_list

    def clear(self):
        self.monster_list.clear()

    def save(self, new_monster_list):
        self.monster_list = new_monster_list
        file = open(self.name, 'w');
        for i in self.monster_list:
            file.write(self.monster_list[i].call_brief_data() + '\n')
