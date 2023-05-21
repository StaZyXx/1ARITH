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

    def set_key_value(self, key_value):
        self.__key_value = key_value

    def get_list(self):
        return self.__list

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
        self.__root_info = Tk()
        self.__root_info.title("Page des infos")
        self.__root_info.geometry("500x300")
        self.__root_info.configure(bg="black")
        self.__label = Label(text="Mot à chiffrer/déchiffrer :", fg="red", bg="black")
        self.__label.pack(pady=10)
        self.__entry_word = Entry(self.__root_info, fg="red", bg="black")
        self.__entry_word.pack(pady=10)
        self.__send_button = Button(text="Valider", fg="red", bg="black", command=self.encryption)
        self.__send_button.pack()

        self.__root_info.mainloop()

    def encryption(self):
        self.__word = self.__entry_word.get()
        self.__word = self.__word.upper()
        self.__word = self.__word.replace(" ", "")

        self.__root_info.destroy()
        self.__root_encryption = Tk()
        self.__root_encryption.title("Encryption")
        self.__root_encryption.geometry("700x900")
        self.__root_encryption.configure(bg="black")

        self.__frame = Frame(self.__root_encryption, width=1000, height=900, bg="black")
        self.__frame.pack(anchor="center")

        lines = self.__encryption.create_lines(self.__word)

        self.__encryption.set_key_value(lines)

        self.update_encryption_with_button()

        self.__root_encryption.mainloop()

    def switch_keys(self, btn):
        btn.config(state='disabled')
        self.__encryption.get_list().append(btn["text"])
        if len(self.__encryption.get_list()) == len(self.__encryption.get_key_value()):
            self.init_last_page()

    def init_last_page(self):
        self.__root_encryption.destroy()
        self.__root_last_page = Tk()
        self.__root_last_page.title("Last Page")
        self.__root_last_page.geometry("700x900")
        self.__root_last_page.configure(bg="black")

        self.__frame = Frame(self.__root_last_page, width=1000, height=900, bg="black")
        self.__frame.pack(anchor="center")

        for i in range(len(self.__encryption.get_key_value())):
            arrow_up = Button(self.__frame, text="⬆", fg="red", bg="black")
            arrow_up.config(command=lambda a=i: self.pop_key_value(a + 1))
            arrow_up.grid(column=i, row=27)
            arrow_down = Button(self.__frame, text="⬇", fg="red", bg="black")
            arrow_down.config(command=lambda a=i: self.remove_key_value(a + 1))
            arrow_down.grid(column=i, row=28)

        clearText = Label(self.__frame, text="⬅ Clear", fg="red", bg="black")
        clearText.grid(column=len(self.__encryption.get_key_value()), row=10)

        cipherText = Label(self.__frame, text="⬅ Cipher", fg="red", bg="black")
        cipherText.grid(column=len(self.__encryption.get_key_value()), row=16)

        self.update_encryption()

        self.__root_last_page.mainloop()

    def update_encryption_with_button(self):
        for i in range(len(self.__encryption.get_key_value())):
            for j in range(len(self.__encryption.get_key_value()[i + 1])):
                Label(self.__frame, text=self.__encryption.get_key_value()[i + 1][j], background="black",
                      fg="red").grid(column=i,
                                     row=j)
            btn = Button(self.__frame, text=i + 1)
            btn.config(fg="red", bg="black", command=lambda a=btn: self.switch_keys(a))
            btn.grid(column=i, row=27)

    def update_encryption(self):
        if len(self.__encryption.get_list()) == len(self.__encryption.get_key_value()):
            for i in range(len(self.__encryption.get_list())):
                a = int(self.__encryption.get_list()[i])
                for j in range(len(self.__encryption.get_key_value()[a])):
                    Label(self.__frame, text=self.__encryption.get_key_value()[a][j], background="black",
                          fg="red").grid(
                        column=i,
                        row=j)
        else:
            for i in range(len(self.__encryption.get_key_value())):
                for j in range(len(self.__encryption.get_key_value()[i + 1])):
                    Label(self.__frame, text=self.__encryption.get_key_value()[i + 1][j], background="black",
                          fg="red").grid(
                        column=i,
                        row=j)

    def pop_key_value(self, index):
        result = self.__encryption.get_key_value()[index]

        t = result[0]
        self.__encryption.get_key_value()[index] = result[1:]
        self.__encryption.get_key_value()[index] += t

        self.update_encryption()

    def remove_key_value(self, index):
        result = self.__encryption.get_key_value()[index]

        t = result[len(result) - 1]
        self.__encryption.get_key_value()[index] = result[:len(result) - 1]
        self.__encryption.get_key_value()[index] = t + self.__encryption.get_key_value()[index]

        self.update_encryption()


encryption = Encryption()

encryption.read_lines()

# affichage = Console(encryption)

View(encryption)
