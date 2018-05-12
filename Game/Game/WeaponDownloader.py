from Equipment import Equipment


class WeaponDownloader:
    def __init__(self, name):
        self.name = name
        self.weapon_list = dict()

    def load(self):
        if not self.weapon_list:
            file = open(self.name, 'r')
            for string in file:
                x = string.split()
                self.weapon_list[x[0]] = Equipment(str(x[0]),
                                                   str(x[1]),
                                                   int(x[2]),
                                                   int(x[3]))
        return self.weapon_list

    def clear(self):
        self.weapon_list = []

    def save(self, arr2):
        self.weapon_list = arr2
        file = open(self.name, 'w')
        for i in self.weapon_list:
            file.write(self.weapon_list[i].call_brief() + '\n')
