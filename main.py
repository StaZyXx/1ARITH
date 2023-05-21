import random
from tkinter import *
from typing import IO


class Encryption:

    def __init__(self):
        self.__file: IO = None
        # The dictionary is used to create the lines
        self.__dictio: list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                               'S',
                               'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        # This list used for cylinder
        self.__cylinder: dict = {}
        # This list is used for the key
        self.__keys: list = []

    def get_cylinder(self):
        return self.__cylinder

    def set_cylinder(self, key_value):
        self.__cylinder = key_value

    def get_keys(self):
        return self.__keys

    def create_cylinder(self, word):
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

    # This function is used to read the lines of the file
    def read_cylinder(self):
        file = open("data.txt", "r")
        lines = file.readlines()
        increment_number = 1
        for line in lines:
            self.__cylinder[increment_number] = line
            self.__cylinder[increment_number] = line.rstrip("\n")
            increment_number += 1
        return self.__cylinder

    # This function is used to create the key
    def create_key(self, word):
        descending_number = len(word)
        list_temp = []

        for i in range(len(word)):
            list_temp.append(i + 1)

        for i in range(len(list_temp)):
            random_element = random.choice(list_temp)
            self.__keys.append(random_element)
            list_temp.remove(random_element)
            descending_number -= 1
        return self.__keys

    # This function is used to encrypt the word
    def encryption(self, word):
        result = [[]]
        for x in range(len(self.__keys)):
            i = self.__keys[x]
            letter = word[x]
            temp_list = []
            for j in range(len(self.__cylinder[i])):
                if self.__cylinder[i][j] == letter:
                    if j + 6 >= len(self.__cylinder[i]):
                        a = j + 6 - len(self.__cylinder[i])
                        new_letter = self.__cylinder[i][a + 1 + 6]
                    else:
                        new_letter = self.__cylinder[i][j + 6]
                    temp_list.append(new_letter)
            result.append(temp_list)

        return result

    # This function is used to decipher the word
    def decipher(self, word, key):
        result = [[]]
        for x in range(len(key)):
            i = key[x]
            letter = word[x]
            temp_list = []
            for j in range(len(self.__cylinder[i])):
                if self.__cylinder[i][j] == letter:
                    temp_list.append(self.__cylinder[i][j - 6])
            result.append(temp_list)
        return result


class Console:

    def __init__(self, encryption):
        self.__encryption = encryption
        self.__response = input("Voulez vous chiffrer ou dechiffrer un mot ?")

        if self.__response.lower() == "chiffrer":
            self.encryption()
        elif self.__response.lower() == "dechiffrer":
            self.decipher()
        else:
            print("Veuillez choisir entre chiffrer ou dechiffrer")

    # This function is used to decipher the word by console input
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

    # This function is used to encrypt the word by console input
    def encryption(self):

        result = input("Donnez un mot a chiffrer:")
        lines = self.__encryption.create_cylinder(result)
        self.__encryption.set_cylinder(lines)
        key = self.__encryption.create_key(result)

        resultEncryption = self.__encryption.encryption(result.upper())
        for i in range(len(resultEncryption)):
            for j in range(len(resultEncryption[i])):
                print(resultEncryption[i][j], end="")
        print("\n", key, end="")


# This class is used to create the GUI of the program and to interact with the user
class View:
    def __init__(self, encryption):
        self.__root_info = None
        self.__cypher = None
        self.__main_page = None
        self.__encryption = encryption
        self.init_main_page()

    # This function is used to initialize the main page
    def init_main_page(self):
        self.__main_page = Tk()
        self.__main_page.title("Chiffrage | Déchiffrage")
        self.__main_page.geometry("500x300")
        self.__main_page.config(bg="black", takefocus=True)
        Button(self.__main_page, text="Chiffrer", command=lambda: self.init_encryption_page(False), width=20, height=5,
               background="red", fg="black", activebackground="#C5272a", anchor="center").pack(pady=20)
        Button(self.__main_page, text="Déchiffrer", command=lambda: self.init_encryption_page(True), width=20, height=5,
               background="red", fg="black", activebackground="#C5272a", anchor="center").pack(pady=10)
        self.__main_page.mainloop()

    # This function is used to initialize the encryption page
    def init_encryption_page(self, is_cypher):
        self.__cypher = not is_cypher
        self.__main_page.destroy()
        self.__root_info = Tk()
        self.__root_info.title("Page des infos")
        self.__root_info.geometry("500x300")
        self.__root_info.configure(bg="black")
        if is_cypher:
            self.__label = Label(text="Mot à déchiffrer :", height=4, fg="red", bg="black")
        else:
            self.__label = Label(text="Mot à chiffrer :", height=4, fg="red", bg="black")
        self.__label.pack(pady=10)
        self.__entry_word = Entry(self.__root_info, fg="black", bg="red")
        self.__entry_word.pack(pady=10)
        self.__send_button = Button(text="Valider", fg="red", bg="black", command=lambda: self.encryption(is_cypher))
        self.__send_button.pack()

        self.__root_info.mainloop()

    # This function is used to create key buttons
    def encryption(self, bool):
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
        if bool:
            self.__encryption.read_cylinder()
        else:
            lines = self.__encryption.create_cylinder(self.__word)
            self.__encryption.set_cylinder(lines)

        self.update_encryption_with_button()

        self.__root_encryption.mainloop()

    def switch_keys(self, btn):
        btn.config(state='disabled')
        self.__encryption.get_keys().append(btn["text"])

        if len(self.__encryption.get_keys()) == len(self.__encryption.get_cylinder()):
            self.init_last_page()

    # This function is used to update the encryption page with the key buttons
    def init_last_page(self):
        self.__root_encryption.destroy()
        self.__root_last_page = Tk()
        self.__root_last_page.title("Last Page")
        self.__root_last_page.geometry("700x900")
        self.__root_last_page.configure(bg="black")

        self.__frame = Frame(self.__root_last_page, width=1000, height=900, bg="black")
        self.__frame.pack(anchor="center")

        for i in range(len(self.__encryption.get_cylinder())):
            arrow_up = Button(self.__frame, text="⬆", fg="red", bg="black")
            arrow_up.config(command=lambda a=self.__encryption.get_keys()[i]: self.pop_key_value(True, a))
            arrow_up.grid(column=i, row=27)
            arrow_down = Button(self.__frame, text="⬇", fg="red", bg="black")
            arrow_down.config(command=lambda a=self.__encryption.get_keys()[i]: self.remove_key_value(True, a))
            arrow_down.grid(column=i, row=28)

        clearText = Label(self.__frame, text="⬅ Clear", fg="red", bg="black")
        clearText.grid(column=len(self.__encryption.get_cylinder()), row=10)

        cipherText = Label(self.__frame, text="⬅ Cipher", fg="red", bg="black")
        cipherText.grid(column=len(self.__encryption.get_cylinder()), row=16)

        self.sort_key_value()
        self.update_encryption()

        self.__root_last_page.mainloop()

    # This function is used to sort key by input
    def sort_key_value(self):
        for i in range(len(self.__encryption.get_cylinder())):
            while not self.check_good_letter_at_index(self.__encryption.get_keys()[i],
                                                      self.__word[i]):
                self.pop_key_value(False, self.__encryption.get_keys()[i])

    # This function is used to check if cypher key is on the right place or decrypt key is on the right place
    def check_good_letter_at_index(self, index, letter):
        if self.__cypher:
            return self.__encryption.get_cylinder()[index][10] == letter
        else:
            return self.__encryption.get_cylinder()[index][16] == letter

    # This function is used to update the encryption page with the key buttons
    def update_encryption_with_button(self):
        for i in range(len(self.__encryption.get_cylinder())):
            for j in range(len(self.__encryption.get_cylinder()[i + 1])):
                Label(self.__frame, text=self.__encryption.get_cylinder()[i + 1][j], background="black",
                      fg="red").grid(column=i,
                                     row=j)
            btn = Button(self.__frame, text=i + 1)
            btn.config(fg="red", bg="black", command=lambda btnCloned=btn: self.switch_keys(btnCloned))
            btn.grid(column=i, row=27)

    # This function is used to update all the encryption page
    def update_encryption(self):
        if len(self.__encryption.get_keys()) == len(self.__encryption.get_cylinder()):
            for i in range(len(self.__encryption.get_keys())):
                key = int(self.__encryption.get_keys()[i])
                for j in range(len(self.__encryption.get_cylinder()[key])):
                    Label(self.__frame, text=self.__encryption.get_cylinder()[key][j], background="black",
                          fg="red").grid(
                        column=i,
                        row=j)
        else:
            for i in range(len(self.__encryption.get_cylinder())):
                for j in range(len(self.__encryption.get_cylinder()[i + 1])):
                    Label(self.__frame, text=self.__encryption.get_cylinder()[i + 1][j], background="black",
                          fg="red").grid(
                        column=i,
                        row=j)

    # This function is used to pop the first letter of the key
    def pop_key_value(self, update, index):
        result = self.__encryption.get_cylinder()[index]
        first_letter = result[0]

        self.__encryption.get_cylinder()[index] = result[1:]
        self.__encryption.get_cylinder()[index] += first_letter

        if update:
            self.update_encryption()

    # This function is used to remove the last letter of the key
    def remove_key_value(self, update, index):
        result = self.__encryption.get_cylinder()[index]

        last_letter = result[len(result) - 1]
        self.__encryption.get_cylinder()[index] = result[:len(result) - 1]
        self.__encryption.get_cylinder()[index] = last_letter + self.__encryption.get_cylinder()[index]

        if update:
            self.update_encryption()


encryption = Encryption()

# Console(encryption)

View(encryption)
