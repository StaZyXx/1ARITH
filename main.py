import random
from tkinter import *


class Encryption:

    def __init__(self):
        self.__file = None
        self.__dictio = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                         'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        self.__key_value = {}
        self.__list = []

    def get_key_value(self):
        return self.__key_value

    def create_lines(self, word):
        pass

    def read_lines(self):
        file = open("data.txt", "r")
        lines = file.readlines()
        print(lines)
        increment_number = 1
        for line in lines:
            print("line", increment_number, ":", line)
            self.__key_value[increment_number] = line
            self.__key_value[increment_number] = line.rstrip("\n")
            increment_number += 1

    def create_key(self, word):
        descending_number = len(word)
        list_temp = []

        for i in range(len(word)):
            list_temp.append(i)

        for i in range(len(list_temp)):
            random_element = random.choice(list_temp)
            self.__list.append(random_element)
            list_temp.remove(random_element)
            descending_number -= 1

    def verify_list(self):
        for item in self.__list:
            if self.__list.count(item) > 1:
                return True
        return False

    def encryption(self, word):
        result = [[]]
        print(self.__key_value)
        for x in range(len(self.__list)):
            i = self.__list[x]
            letter = word[x]
            for j in range(len(self.__key_value[i])):
                if self.__key_value[i][j] == letter:
                    if j + 6 >= len(self.__key_value[i]):
                        a = j + 6 - len(self.__key_value[i])
                        new_letter = self.__key_value[i][a + 1 + 6]
                    else:
                        new_letter = self.__key_value[i][j + 6]
                    result[x][j] = new_letter
        return result

    def decipher(self, word, key):
        result = [[]]
        for x in range(len(key)):
            i = key[x]
            letter = word[x]
            for j in range(len(self.__key_value[i])):
                if self.__key_value[i][j] == letter:
                    result[x][j] = self.__key_value[i][j - 6]
        return result

class Console(Encryption):

    def __init__(self):
        super().__init__()
        self.__response = input("Voulez vous chiffrez ou dechiffrez un mot ?")

        if self.__response.lower() == "chiffrez":
            self.encryption()
        elif self.__response.lower() == "dechiffrez":
            self.decipher()

    def create_lines(self, word):
        self.__file = open("data.txt", "w")
        for i in range(len(word)):
            descending_number = 26
            self.__dictio = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                             'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            for j in range(len(self.__dictio)):
                random_number = random.randrange(0, descending_number, 1)
                self.__file.write(self.__dictio[random_number])
                del self.__dictio[random_number]
                descending_number -= 1
            self.__file.write("\n")

    def decipher(self):
        word = input("Donnez le mot a dechiffrer:")
        key = input("Donnez la clef de dechiffrement:")

        key.replace("[", "")
        key.replace("]", "")
        key = key.split(",")
        keys = []
        for i in range(len(key)):
            keys.append(int(key[i]))

        decipher = super().decipher(word, keys)
        for i in range(len(decipher)):
            for j in range(len(decipher[i])):
                print(decipher[i][j], end="")
            print("")

    def encryption(self):

        result = input("Donnez un mot a chiffrer:")
        self.create_lines(result)
        super().read_lines()
        super().create_key(result)
        super().verify_list()

        encryption = super().encryption(result)
        for i in range(len(encryption)):
            for j in range(len(encryption[i])):
                print(encryption[i][j], end="")
            print("")

class View(Encryption):
    def __init__(self):
        self.__encryption = super().__init__()
        self.__root = Tk()
        self.__button1 = Button(text="Encryption", command=self.info_encryption)
        self.__button1.config(width=30, height=5, bg="red")
        self.__button1.pack()
        self.__button2 = Button(text="Decipher", command=self.info_decipher)
        self.__button2.config(width=30, height=5, bg="blue")
        self.__button2.pack()

        self.__root.mainloop()

    def info_encryption(self):
        self.__root.destroy()
        self.__root_info = Tk()
        self.__root_info.title("Page des infos")
        self.__root_info.geometry("500x300")
        self.__label = Label(text="Entrez le mot a chiffrer:")
        self.__label.pack()
        self.__entry_word = Entry(self.__root_info, width=50, borderwidth=2)
        self.__entry_word.pack()
        self.__send_button = Button(text="Envoyer les informations", command=self.encryption)
        self.__send_button.pack()

    def info_decipher(self):
        self.__root.destroy()
        self.__root_info = Tk()
        self.__root_info.title("Page des infos")
        self.__root_info.geometry("500x300")
        self.__label1 = Label(text="Entrez le mot a déchiffrer:")
        self.__label1.pack()
        self.__entry_word = Entry(self.__root_info, width=50, borderwidth=2)
        self.__entry_word.pack()
        self.__label2 = Label(text="Entrez la clé de déchiffrement:")
        self.__label2.pack()
        self.__entry_key = Entry(self.__root_info, width=50, borderwidth=2)
        self.__entry_key.pack()
        self.__label3 = Label(text="Mettez ici votre cylindre:")
        self.__label3.pack()
        self.__entry_data = Entry(self.__root_info, width=50)
        self.__entry_data.pack()
        self.__send_button = Button(text="Envoyer les informations", command=self.decipher)
        self.__send_button.pack()

    def encryption(self):
        self.__word = self.__entry_word.get()
        self.__word = self.__word.upper()
        self.__word = self.__word.replace(" ", "")

        self.__root_info.destroy()
        self.__root_encryption = Tk()
        self.__root_encryption.title("Encryption")
        self.__root_encryption.geometry("500x300")

        self.__root_encryption.mainloop()

    def decipher(self):
        self.__word = self.__entry_word.get()
        self.__word = self.__word.upper()
        self.__word = self.__word.replace(" ", "")
        self.__key = self.__entry_key.get()
        self.__dict = self.__entry_data.get()


        if len(self.__dict) == 0 or len(self.__dict) % 26 != 0:
            self.__entry_data.config(bg="red")
        else:
            self.__root_info.destroy()
            self.__root_decipher = Tk()
            self.__root_decipher.title("Decipher")
            self.__root_decipher.geometry("500x300")
            super().decipher(self.__word, self.__key)

            self.__root_decipher.mainloop()


affichage = Console()


#View()