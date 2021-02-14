from tkinter import *
import tkinter.font as font
import time
import pygame
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
pygame.mixer.init()
def startTime():
    global start
    global timing
    global chars
    global words
    global mistakes
    global attempts
    attempts = 0
    mistakes = 0
    chars = 0
    words = 0
    start = time.time()
    timing = True

def stopTime():
    global timing
    global done
    global charMode
    global endChar
    global endWord
    global chars
    global words
    global maxChar
    global wpm
    endChar = "{0:.3f}".format(chars / 4.79 * 2) + " WPM  "
    endWord = str(words * 2) + " WPM  "
    accuracy = "Accuracy: 100.00%"
    if attempts > 0:
        accuracy = "Accuracy: " +  "{0:.2f}".format(100 - mistakes * 100 /attempts) + "%"
    if charMode.get():
        wpm.configure(text=endChar + accuracy)
    else:
        wpm.configure(text=endWord + accuracy)
    timer.configure(text="Time up! Most misspelled character: \"" + maxChar + "\"")
    timing = False
    done = True

def updateTime():
    global root
    global timer
    global start
    global timing
    if timing:
        timer.configure(text="{0:.3f}".format(30 - time.time() + start))
    if time.time() - start >= 30 and timing:
        stopTime()
    root.after(1,updateTime)

def type(event):
    global text
    global timing
    global chars
    global words
    global charMode
    global maxx
    global maxChar
    global mistakes
    global attempts
    global wpm
    if event.char == "\b" or event.char == "":
        return
    if not timing and not done and loaded:
        startTime()
    elif done:
        return
    attempts += 1
    textBox.configure(state='normal')
    if text[0] == event.char:
        if event.char == "\b" or event.char == "":
            return
        text = text[1:]
        textBox.delete(1.0, END)
        textBox.insert(1.0, text[:30])
        textBox.tag_add("here", "1.0", "1.1")
        textBox.tag_configure("here", background = "#11FF11")
        textBox.tag_configure("here", foreground="white")
        chars += 1
        if event.char == " ":
            words += 1
    else:
        textBox.tag_add("here", "1.0", "1.1")
        textBox.tag_configure("here", background = "red")
        textBox.tag_configure("here", foreground = "white")
        try:
            sound.play()
        except:
            poo = 1
        charArr[ord(event.char)] += 1
        if charArr[ord(event.char)] > maxx:
            maxx = charArr[ord(event.char)]
            maxChar = event.char
        mistakes += 1
    textBox.configure(state='disabled')
    accuracy = "Accuracy: " + "{0:.2f}".format(100 - mistakes * 100 / attempts) + "%"
    if charMode.get():
        if time.time() - start != 0:
            wpm.configure(text="{0:.3f}".format(chars / 4.79 * 60 / (time.time() - start)) + " WPM  " + accuracy)
    else:
        if time.time() - start != 0:
            wpm.configure(text="{0:.3f}".format(words * 60 / (time.time() - start)) + " WPM  " + accuracy)

def newText():
    global text
    global textBox
    global count
    global timing
    global timer
    global done
    global title
    global loaded
    done = False
    timing = False
    loaded = False
    timer.configure(text="Start typing to start timer")
    title.configure(text="Loading...")
    root.update()
    while True:
        if count % 3 == 0:
            my_url = "https://randomincategory.toolforge.org/Computer_programming?site=en.wikipedia.org"
        elif count % 3 == 1:
            my_url = "https://randomincategory.toolforge.org/Computer_science?site=en.wikipedia.org"
        else:
            my_url = "https://randomincategory.toolforge.org/Mathematics?site=en.wikipedia.org"
        count += 1
        try:
            uClient = uReq(my_url)
        except:
            continue
        page_html = uClient.read()
        page_soup = soup(page_html, "html.parser")
        tagOpen = False
        text = ""
        nope = False
        for part in page_soup.findAll("p"):
            for char in str(part):
                if char == "<" or char == "[":
                    tagOpen = True
                    continue
                if char == ">" or char == "]":
                    tagOpen = False
                    continue
                if not tagOpen and len(text) > 1 and char != " " and char != "\n" and text[-1] == ".":
                    text += " "
                if not tagOpen and char != "\n" and not (char == " " and text[-1] == " "):
                    text += char
                if not (char.isalpha() or char.isnumeric() or char == "\n" or char in " !@#$%^&*()-=_+;./,[]{}:;<>?\\|"):
                    nope = True
                    break
        text = text[:600]
        textBox.configure(state='normal')
        textBox.delete(1.0, END)
        textBox.insert(1.0, text[:30])
        textBox.focus()
        textBox.configure(state='disabled')
        if len(text) >= 600 and "category" not in text[:100] and "outline" not in text[:100] and "Wiki" not in text[:100]:
            title.configure(text=str(page_soup.title)[7:-20], font=font.Font(size=max(20 - (len(str(page_soup.title)[7:-20]) - 25), 20), family="Microsoft Yahei UI Light"))
            loaded = True
            break

def modeChange(mode):
    global charMode
    global endChar
    global endWord
    global wpm
    global mistakes
    global attempts
    accuracy = "Accuracy: 100.00%"
    if attempts > 0:
        accuracy = "Accuracy: " +  "{0:.2f}".format(100 - mistakes * 100/attempts) + "%"
    charMode = mode
    if done:
        if charMode.get():
            wpm.configure(text=endChar)
        else:
            wpm.configure(text=endWord)
        return
    if mode:
        wpm.configure(text="{0:.3f}".format(chars / 4.79 * 60 / (time.time() - start)) + " WPM  " + accuracy)
    else:
        wpm.configure(text="{0:.3f}".format(words * 60 / (time.time() - start)) + " WPM  " + accuracy)

def soundChange():
    global sound
    global soundMode
    if soundMode:
        sound = pygame.mixer.Sound("pop.wav")
        soundMode = False
    else:
        sound = pygame.mixer.Sound("wrong.wav")
        soundMode = True


attempts = 0
mistakes = 0
charArr = [0] * 128
maxx = 0
maxChar = "None! Amazing!"
loaded = False
root = Tk()
charMode = BooleanVar()
soundMode = False
sound = pygame.mixer.Sound("pop.wav")
endChar = ""
endWord = ""
heading = ""
chars = 0
words = 0
timing = False
done = False
start = 0
count = 0
text = ""
root.configure(bg="#ffabff")
root.title("Typing Test")
root.geometry("500x400")
root.resizable(False,False)
myFont = font.Font(size=30, family = "Microsoft Yahei UI Light")
topFrame = Frame(root, bg="#ffabff")
topFrame.pack()
title = Label(topFrame, text="Typing Test", pady=20, font=myFont, bg="#ffabff")
title.pack()
myFont = font.Font(size=15, family = "Microsoft Yahei UI Light")
timer = Label(topFrame, text="Start typing to start timer", font=myFont, bg="#ffabff")
timer.pack()
wpm = Label(topFrame, text="", pady=10, font=myFont, bg="#ffabff")
wpm.pack()
modeChange(charMode)
textBox = Text(topFrame, font=myFont, height=1, width=30)
textBox.bind("<Key>", type)
textBox.pack()
textBox.configure(state='disabled')
searchButton = Button(topFrame, text="New wiki!", padx=20, pady=10, font=myFont, command=newText)
searchButton.pack(pady=20)
toppyFrame = Frame(topFrame, bg="#ffabff")
toppyFrame.pack()
myFont = font.Font(size=10, family = "Microsoft Yahei UI Light")
Radiobutton(toppyFrame, text="Actual WPM", font=myFont, bg="#ffabff", variable=charMode, value=False, command=lambda: modeChange(charMode)).grid(row=0, column=0)
Radiobutton(toppyFrame, text="Calculated WPM", font=myFont, bg="#ffabff", variable=charMode, value=True, command=lambda: modeChange(charMode)).grid(row=0, column=1)
Radiobutton(toppyFrame, text="Scary DUN Sound :O", font=myFont, bg="#ffabff", value=False, command=lambda: soundChange()).grid(row=1, column=1)
Radiobutton(toppyFrame, text="Pop Sound :D", font=myFont, bg="#ffabff",  value=True, command=lambda: soundChange()).grid(row=1, column=0)

newText()
updateTime()
root.mainloop()
