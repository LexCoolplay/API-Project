from quests import Quest


class QuestDownloader:
    def __init__(self, name):
        self.name = name
        self.dic = {}

    def load(self):
        file = open(self.name, 'r')
        for line in file:
            x = line.split()
            self.dic[x[1]] = Quest(x[0], x[1], x[1:])
        return self.dic

    def clear(self):
        self.dic.clear()
