from Character import Character


class Downloader:
    def __init__(self, name):
        self.name = name
        self.char_list = {}

    def load(self):
        file = open(self.name, 'r')
        for string in file:
            string = string.split()
            character_name = string[0]
            password = string[1]
            level,\
                armor,\
                weapon1,\
                weapon2,\
                magic =\
                str(string[2]),\
                str(string[3]),\
                str(string[4]),\
                str(string[5]),\
                str(string[6])
            self.char_list[character_name] = Character(character_name, password, level, armor, weapon1, weapon2, magic)
        return self.char_list

    def clear(self):
        self.char_list.clear()

    def save(self, new_char_dict):
        self.char_list = new_char_dict
        file = open(self.name, 'w')
        for i in self.char_list:
            file.write(self.char_list[i].call_brief_data() + '\n')
