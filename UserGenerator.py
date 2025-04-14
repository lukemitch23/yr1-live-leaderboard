import random
import os

class user_gen:
    def __init__ (self, filePathAdj, filePathNoun):
        self.noun = None
        self.adj = None
        self.num = None
        self.filePathAdj = filePathAdj
        self.filePathNoun = filePathNoun
    
    def get_noun(self):
        with open(self.filePathNoun, 'r') as file:
            lines = file.readlines()
        file.close()
        random_line = random.choice(lines).strip()
        self.noun = random_line
    
    def get_adj(self):
        with open(self.filePathAdj, 'r') as file:
            lines = file.readlines()
        file.close()
        random_line = random.choice(lines).strip()
        self.adj = random_line
    
    def get_num(self):
        random_integer = random.randint(1, 99)
        self.num = random_integer
    
    def get_name(self):
        self.code = self.adj[0] + self.noun[0] + str(self.num)
        self.name = self.adj + " " + self.noun + str(self.num)
        name = [self.name, self.code]
        return name

    def check_user(self):
        with open('generated.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                if self.name in line:
                    return False
        file.close()
        with open('generated.txt', 'a') as file:
            file.write(self.name + '\n')
        file.close()
        return True


def generate():
    print(os.getcwd())
    userName = user_gen('adjectives.txt', 'animals.txt')
    generated = False
    while generated == False:
        userName.get_noun()
        userName.get_adj()
        userName.get_num()
        nameGenerated = userName.get_name()
        generated = userName.check_user()
    return nameGenerated
