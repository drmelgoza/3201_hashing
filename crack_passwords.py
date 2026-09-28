import csv
import string
import time
import random
from Crypto.Hash import SHA256
from bcrypt import checkpw, hashpw
import nltk
nltk.download('words')
from nltk.corpus import words

def crack_password(pw_hash:str, word_corpus:list[str]):
    #find the word in the wordset that returns the desired hash
    for word in word_corpus:
        #checkpw from bcrypt library
        if checkpw(word.encode("utf-8"), pw_hash.encode("utf-8")):
            return word
    return None

def get_all_passwords(filepath:str = 'user_hashes.txt'):
    #word corpus from nltk words library
    word_corpus = [word for word in words.words() if 10 >= len(word) >= 6]
    user_hashes = {}
    user_passwords = {}
    #get every hash within the hashes file
    with open(filepath) as f:
        for line in f:
            user, hashval = line.strip().split(":")
            print(f"{user}: {hashval}")
            #ensure new line chars are not included
            user_hashes[user] = hashval.replace('\n', '')

    #crack every password and write it to the temporary dictionary
    for user in user_hashes:
        password = crack_password(user_hashes[user], word_corpus)
        if password:
            user_passwords[user] = password
        else:
            user_passwords[user] = "passworderror!!!"
        print(f"Password found!: {password}")

    #write all the passwords to the file.
    with open("./user_passwords.txt", "w+") as f:
        f.write("user: password")
        for user in user_passwords:
            f.write(f"{user}: {user_passwords[user]}\n")


get_all_passwords("./user_hashes.txt")