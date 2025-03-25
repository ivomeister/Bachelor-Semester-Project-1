import PySimpleGUI as sg
import time
import itertools
import subprocess
import threading


lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"
special = "`~!@#$%^&№€*()_+,./\<>?|-="
chars = ""
guess = ""
charsList = list(chars)

password_found = False



def isValid(string, s1, s2, s3 ,s4):
    for c in string:
        if c not in s1 and c not in s2 and c not in s3 and c not in s4:
            return False
    return True

def createCharsList(string, s1, s2, s3, s4, res):
    for c in string:
        if (c in s1) and (s1 not in res):
            res+=s1
        elif (c in s2) and (s2 not in res):
            res+=s2
        elif (c in s3) and (s3 not in res):
            res+=s3
        elif (c in s4) and (s4 not in res):
            res+=s4
    return res

def combinations(l,p):
        return itertools.product(l,repeat=len(p))

def guessPassword1(p):
    file = open("passlist.txt","r")
    for word in file:
        if word.rstrip("\n") == p:
            file.close()
            return True
        else:
            continue
    file.close()
    return False
        
def guessPassword2(g,p):
    global password_found
    if g!=p:
        for comb in combinations(charsList,p):
            g = "".join(comb)
            if g == p:
                password_found = True
                return True
    return False
    
def timeInt():
    return round(time.time() * 100)


if __name__ == '__main__':

    passWindowLayout = [
        [sg.Text("Enter a password:", pad=((0,0),(15,30)),font=("Helvetica",15))],
        [sg.Input(size=(50,1), pad=((0,0),(0,20)), enable_events=True, key="INPUT")],
        [sg.Button("OK", size=(10,2), pad=(10,30), font=("Helvetica",15)), sg.Button("Exit", size=(10,2), pad=(10,30), font=("Helvetica",15))]
    ]

    attemptWindowLayout = [
        [sg.Text(size=(20,1), pad=((0,0),(30,0)), font=("Helvetica",30), justification="center", key="TIMER")],
        [sg.Text("Target: 05:00:00", font=("Helvetica",15), pad=(0,30), key="TARGET")],
        [sg.Text(size=(20,2), font=("Helvetica",25), justification="center", key="OUTPUT")],
        [sg.Button("Run", size=(20,5), pad=((0,0),(0,5)), font=("Helvetica",20), key="ACTION")],
        [sg.Button("Quit", size=(20,5), pad=(5), font=("Helvetica",20) )]
    ]

    passWindow = sg.Window("Password-cracking simulation", passWindowLayout, size = (600,240), element_justification="c")
    attemptWindow = sg.Window("Password-cracking simulation", attemptWindowLayout, size=(720,720), element_justification="c")
    

    while True:
        passWindowEvent, passWindowValues = passWindow.read()

        password = passWindow["INPUT"].get()
        
        if " " in password:
            passWindow["INPUT"].update(password[:-1])

        if passWindowEvent in (sg.WIN_CLOSED, "Exit"):
            break

        if passWindowEvent == "OK":
            if len(password)!=0 and isValid(password, lowercase, uppercase, digits, special):
                charsList = list(createCharsList(password, lowercase, uppercase, digits, special, chars))
                length = len(password)
                passWindow.close()

                currentTime, pausedTime, startTime, paused, thread_running = 0, 0, 0, True, False
                while True:
                    attemptWindowEvent, attemptWindowValues = attemptWindow.read(timeout=10)

                    if attemptWindowEvent in (sg.WIN_CLOSED, "Quit"):
                        break

                    if not paused:
                        if attemptWindow["TIMER"].get() > attemptWindow["TARGET"].get()[8:]:
                            paused = True
                            pausedTime = timeInt()
                            attemptWindow["ACTION"].update("Reset")
                            attemptWindow["OUTPUT"].update("FAILURE", text_color = "red")
                        if guess != password:
                            if guessPassword1(password):
                                paused = True
                                pausedTime = timeInt()
                                attemptWindow["ACTION"].update("Reset")
                                attemptWindow["OUTPUT"].update("SUCCESS", text_color = "lightgreen")
                                process = subprocess.Popen(["important_info.txt"], shell=True)
                                process.wait()
                            else:
                                if not thread_running:
                                    threading.Thread(target = guessPassword2, args=[guess,password]).start()
                                    thread_running = True
                            if password_found:
                                paused = True
                                pausedTime = timeInt()
                                attemptWindow["ACTION"].update("Reset")
                                attemptWindow["OUTPUT"].update("SUCCESS", text_color = "lightgreen")
                                process = subprocess.Popen(["important_info.txt"], shell=True)
                                process.wait()
                                guess = ""
                        else:
                            currentTime = timeInt() - startTime

                    if attemptWindowEvent == "ACTION":
                        if pausedTime != 0:
                            currentTime, pausedTime, startTime, paused = 0, 0, 0, True
                            attemptWindow["ACTION"].update("Run")
                            attemptWindow["OUTPUT"].update("")
                        else:
                            if not paused:
                                pausedTime = timeInt()
                                attemptWindow["ACTION"].update("Reset")
                                attemptWindow["OUTPUT"].update("TERMINATED", text_color = "yellow")
                            else:
                                startTime = startTime + timeInt() - pausedTime
                                attemptWindow["ACTION"].update("Stop")
                                attemptWindow["OUTPUT"].update("")

                            paused = not paused
                    
                    attemptWindow["TIMER"].update("{:02d}:{:02d}:{:02d}".format((currentTime // 100) // 60, (currentTime // 100) % 60, (currentTime % 100)))

                attemptWindow.close()
            else:
                sg.popup_ok("Invalid password. Please try again.")
    passWindow.close()