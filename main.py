import random
import time
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

    def set_key_value(self, key_value):
        self.__key_value = key_value

    def create_lines(self, word):
        self.__file = open("data.txt", "w")
        result = {}
        for i in range(len(word)):
            descending_number = 26
            self.__dictio = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                             'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            text = ""
            for j in range(len(self.__dictio)):
                random_number = random.randrange(0, descending_number, 1)
                text += self.__dictio[random_number]
                self.__file.write(self.__dictio[random_number])
                del self.__dictio[random_number]
                descending_number -= 1
            result[i + 1] = text
            self.__file.write("\n")
        self.__file.close()
        return result

    def read_lines(self):
        file = open("data.txt", "r")
        lines = file.readlines()
        increment_number = 1
        for line in lines:
            self.__key_value[increment_number] = line
            self.__key_value[increment_number] = line.rstrip("\n")
            increment_number += 1
        return self.__key_value

    def create_key(self, word):
        descending_number = len(word)
        list_temp = []

        for i in range(len(word)):
            list_temp.append(i + 1)

        for i in range(len(list_temp)):
            random_element = random.choice(list_temp)
            self.__list.append(random_element)
            list_temp.remove(random_element)
            descending_number -= 1
        return self.__list

    def verify_list(self):
        for item in self.__list:
            if self.__list.count(item) > 1:
                return True
        return False

    def encryption(self, word):
        result = [[]]
        for x in range(len(self.__list)):
            i = self.__list[x]
            letter = word[x]
            temp_list = []
            for j in range(len(self.__key_value[i])):
                if self.__key_value[i][j] == letter:
                    if j + 6 >= len(self.__key_value[i]):
                        a = j + 6 - len(self.__key_value[i])
                        new_letter = self.__key_value[i][a + 1 + 6]
                    else:
                        new_letter = self.__key_value[i][j + 6]
                    temp_list.append(new_letter)
            result.append(temp_list)

        return result

    def decipher(self, word, key):
        result = [[]]
        for x in range(len(key)):
            i = key[x]
            letter = word[x]
            temp_list = []
            for j in range(len(self.__key_value[i])):
                if self.__key_value[i][j] == letter:
                    temp_list.append(self.__key_value[i][j - 6])
            result.append(temp_list)
        return result


class Console:

    def __init__(self, encryption):
        self.__encryption = encryption
        self.__response = input("Voulez vous chiffrez ou dechiffrez un mot ?")

        if self.__response.lower() == "chiffrez":
            self.encryption()
        elif self.__response.lower() == "dechiffrez":
            self.decipher()

    def decipher(self):
        word = input("Donnez le mot a dechiffrer:").upper()
        key = input("Donnez la clef de dechiffrement:")

        key.replace("[", "")
        key.replace("]", "")
        key = key.split(",")
        keys = []
        for i in range(len(key)):
            keys.append(int(key[i].replace("]", "").replace("[", "").replace(" ", "")))

        decipher = self.__encryption.decipher(word, keys)
        for i in range(len(decipher)):
            for j in range(len(decipher[i])):
                print(decipher[i][j], end="")

    def encryption(self):

        result = input("Donnez un mot a chiffrer:")
        lines = self.__encryption.create_lines(result)
        self.__encryption.set_key_value(lines)
        self.__encryption.create_key(result)

        encryption = self.__encryption.encryption(result.upper())
        for i in range(len(encryption)):
            for j in range(len(encryption[i])):
                print(encryption[i][j], end="")


class View:
    def __init__(self, encryption):
        self.__encryption = encryption
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
        self.__send_button = Button(text="Envoyer les informations", command=self.decipher)
        self.__send_button.pack()

    def encryption(self):
        self.__word = self.__entry_word.get()
        self.__word = self.__word.upper()
        self.__word = self.__word.replace(" ", "")

        self.__root_info.destroy()
        self.__root_encryption = Tk()
        self.__root_encryption.title("Encryption")
        self.__root_encryption.geometry("1800x900")

        Label(text="Mot a chiffrer:" + self.__word).grid(column=0)

        self.__canvas = Canvas(self.__root_encryption, width=1000, height=900, bg="red")
        self.__canvas.grid(column=1)

        lines = self.__encryption.create_lines(self.__word)

        self.__encryption.set_key_value(lines)
        key = self.__encryption.create_key(self.__word)

        result = self.__encryption.encryption(self.__word)

        for i in range(len(self.__encryption.get_key_value())):
            for j in range(len(self.__encryption.get_key_value()[i + 1])):
                Label(self.__canvas, text=self.__encryption.get_key_value()[i + 1][j], background="red").grid(column=i,
                                                                                                              row=j)
            btn = Button(self.__canvas, text=i)
            btn.config(command=lambda a=btn: self.switch_keys(a))
            btn.grid(column=i, row=27)

        self.__root_encryption.mainloop()

    def switch_keys(self, btn):
        btn.config(state='disabled')
        print(btn["text"])

    def decipher(self):
        self.__word = self.__entry_word.get()
        self.__word = self.__word.upper()
        self.__word = self.__word.replace(" ", "")
        self.__key = self.__entry_key.get().upper()

        self.__root_info.destroy()
        self.__root_decipher = Tk()
        self.__root_decipher.title("Decipher")
        self.__root_decipher.geometry("500x300")

        self.__key.replace("[", "")
        self.__key.replace("]", "")
        key = self.__key.split(",")
        keys = []
        for i in range(len(key)):
            keys.append(int(key[i].replace("]", "").replace("[", "").replace(" ", "")))

        result = self.__encryption.decipher(self.__word, keys)

        text = Text(self.__root_decipher, width=50, height=10, wrap=WORD)
        resultFormatted = ""
        for i in range(len(result)):
            for j in range(len(result[i])):
                resultFormatted += result[i][j]

        text.insert(1.0, "Mot a déchiffrer:")
        text.insert(1.0, self.__word)
        text.insert(1.0, "Clé de déchiffrement:")
        text.insert(1.0, self.__key)
        text.insert(1.0, "Resultat:")
        text.insert(1.0, "Le mot déchiffré est : " + str(resultFormatted))

        text.pack()

        self.__root_decipher.mainloop()


encryption = Encryption()

encryption.read_lines()

# affichage = Console(encryption)

View(encryption)
