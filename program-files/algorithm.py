import itertools
import subprocess

lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
special = "`~!@#$%^&№€*()_+,./\<>?|-="
chars = ""
guess = ""

def combinations(l):
        return itertools.product(l,repeat=length)

password = str(input("Enter a password: "))
length = len(password)

for c in password:
    if (c in lowercase) and (lowercase not in chars):
        chars+=lowercase
    elif (c in uppercase) and (uppercase not in chars):
        chars+=uppercase
    elif (c in digits) and (digits not in chars):
        chars+=digits
    elif (c in special) and (special not in chars):
        chars+=special
charsList = list(chars)

file = open("passlist.txt","r")
for word in file:
    if word.rstrip("\n") == password:
        guess = word.rstrip("\n")
        break
file.close()

if guess!=password:
    for comb in combinations(charsList):
        guess = "".join(comb)
        if guess == password:
            break
print("Password is: ",guess)

process = subprocess.Popen(["important_info.txt"], shell=True)
process.wait()