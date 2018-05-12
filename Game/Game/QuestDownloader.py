from quests import Quest


class QuestDownloader:
    def __init__(self, name):
        self.name = name
        self.dic = {}

    def load(self):
        file = open(self.name, 'r')
        for line in file:
            x = line.split()
            self.dic[x[1]] = Quest(x[0], x[1])
        return self.dic

    def clear(self):
        self.dic.clear()

    def save(self, dic2):
        self.dic = dic2
        file = open(self.name, 'w')
        for i in self.dic:
            file.write(self.dic[i].call_brief_data() + '\n')
