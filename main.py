from tkinter.ttk import *
from tkinter import *
import pyttsx3
import time
from ast import literal_eval
import random

# def updateWordExample():
#     global fc_side,words,wordExample,index_word
#     prompt = "podaj mi jakiś prosty i krótki przykład z użyciem słowa \"{}\" używając go w kontekście \"{}\" , następnie po znaku \":\" napisz przetłumaczoną wersje na polski".format(words[index_word][1],words[index_word][0])
#     response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=150)
#     text = response['choices'][0]['text']
#     print(text)
#     text_split = text.split(":")
#     print(text_split[0])
#     print(text_split[1])
#     wordExample.clear()
#     # wordExample.append(words[index_word][0])
#     # wordExample.append(words[index_word][1])
#     wordExample.append(text_split[1])
#     wordExample.append(text_split[0])

def updateWordExample():
    global fc_side,words,wordExample,index_word
    exampleLen = len(words[index_word][4])
    ran = random.randint(0,exampleLen-1)
    print(exampleLen,ran)
    wordExample.clear()
    wordExample.append(words[index_word][4][ran][0])
    wordExample.append(words[index_word][4][ran][1])



def UpArrow(event):
    global index_word,fc_side,max_rep_index,words_rep
    goodAnwser()
    if (index_rep <= len(words_rep)-1):
        if button_Text.get() == "Sprawdz":
            check_fc()
        elif button_Text.get() == "Dalej":
            next_fc()

def updateWordIndex(add):
    global words_rep,index_word,index_rep,wordExample,fc_side
    if not len(words_rep) == 0:
        index_word = words_rep[index_rep + add]

def goodAnwser():
    global index_word
    DAY = 86400
    words[index_word][2]+=1
    repCount = words[index_word][2]
    words[index_word][3] = time.time()
    print(words[index_word][3])
    if repCount == 1:
        words[index_word][3] += DAY * 0.3
    elif repCount == 2:
        words[index_word][3] += DAY * 1.9
    elif repCount == 3:
        words[index_word][3] += DAY * 3.9
    elif repCount == 4:
        words[index_word][3] += DAY * 11.9
    elif repCount == 5:
        words[index_word][3] += DAY * 34.9
    elif repCount == 6:
        words[index_word][3] += DAY * 60
    elif repCount == 7:
        words[index_word][3] += DAY * 120
    else:
        words[index_word][3] += DAY * 200
    print(time.ctime(words[index_word][3]))
    with open('words.txt', 'w',encoding='utf-8') as file_write:
        file_write.write(str(words))
def badAnwser():
    global index_word
    words[index_word][2] = 0
    with open('words.txt', 'w',encoding='utf-8') as file_write:
        file_write.write(str(words))
def checkAnwser():
    global index_word
    print(entry.get().lower())
    print(anwser_Text.get().lower())
    print(wordExample[0])
    print(words[index_word][0])
    print(words[index_word][1])
    if entry.get().lower() == anwser_Text.get().lower():
        goodAnwser()
        print("dobra odpowiedz")

def updateText():
    global fc_side,wordExample
    if not len(words_rep) == 0:
        if button_Text.get() == "Sprawdz":
            anwser_Text.set(wordExample[fc_side])
        elif button_Text.get() == "Dalej":
            fliped_fc_side = (fc_side + 1) % 2
            anwser_Text.set(wordExample[fliped_fc_side])
    else:
        anwser_Text.set("Brak fiszek na dziś")
    window.update()
def readActualWord(event):
    global fc_side
    if button_Text.get() == "Sprawdz":
        #engine.setProperty('voice', voices[fc_side].id) # po dodaniu francuskiego sie rozsypalo
        engine.setProperty('voice', voices[0].id) # ustawione na sztywno
    elif button_Text.get() == "Dalej":
        fliped_fc_side = (fc_side + 1) % 2
        #engine.setProperty('voice', voices[fliped_fc_side].id) # po dodaniu francuskiego sie rozsypalo
        engine.setProperty('voice', voices[2].id) # ustawione na sztywno
        engine.setProperty('rate', 120)
    engine.say(anwser_Text.get())
    engine.runAndWait()

def loadWords():
    with open('words.txt', encoding='utf-8') as file:
        source_words = literal_eval(file.read())
    words_rep = []
    max_rep_index = 0
    for i in range(len(source_words)):
        if source_words[i][3] <= time.time():
            max_rep_index = max(i,max_rep_index)
            words_rep.append(i)
    return source_words,words_rep,max_rep_index

def debug():
    global fc_side, index_word, max_rep_index,words_rep,fc_side_check,wordExample,words
    print(wordExample[0])
    print(wordExample[1])
    print(words[index_word][0])
    print(words[index_word][1])
    engine.say(words[index_word][1])
    engine.runAndWait()

def check_fc():
    button_Text.set("Dalej")
    updateText()
    readActualWord(None)
    checkAnwser()

def next_fc():
    global index_word,words_rep,max_rep_index,index_rep
    if (index_rep >= len(words_rep)-1):
        next_Round()
    else:
        index_rep += 1
        index_word = words_rep[index_rep]
    updateWordExample()
    button_Text.set("Sprawdz")
    updateText()
    entry.delete(0, END)
    progressBarUpdate()
def next_Round():
    init()
    updateText()

def fc_side_change():
    global fc_side
    if (flip.get() == 1):
        fc_side=0
    else:
        fc_side=1
    print(fc_side)
    updateText()
    entry.delete(0, END)

def progressBarUpdate():
    global index_rep,words_rep
    if not len(words_rep) == 0:
        bar['value'] = (index_rep / len(words_rep)) * 100
    else:
        bar['value'] = 0
    stat.set(str(index_rep) + "/" + str(len(words_rep)))
    window.update_idletasks()

def anwser():
    global index_word,fc_side,max_rep_index,words_rep
    if (index_rep <= len(words_rep)-1):
        if button_Text.get() == "Sprawdz":
            check_fc()
        elif button_Text.get() == "Dalej":
            if not entry.get().lower() == anwser_Text.get().lower():
                badAnwser()
                print("zla odpowiedz")
            next_fc()


def init():
    global words,words_rep,index_word,max_rep_index,index_rep
    words = loadWords()[0]
    words_rep = loadWords()[1]
    max_rep_index = loadWords()[2]
    index_word = 0
    index_rep = 0
    updateWordIndex(0)
    updateWordExample()
    # tu musze zrobić update wordExample



engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 150)
window =Tk()
window.geometry('800x600')

# Variables
button_Text = StringVar()
anwser_Text = StringVar()
flip = IntVar()
stat = StringVar()
wordExample = []
fc_side = 1


# set init variable

index_rep = 0
words = loadWords()[0]
words_rep = loadWords()[1]
print("len words_rep {}".format(len(words_rep)))
max_rep_index = loadWords()[2]
index_word = 0
updateWordIndex(0)
button_Text.set("Sprawdz")
updateWordExample()
updateText()
stat.set("0/" + str(len(words_rep)))

#adding frames
top_frame = Frame(window,width=800,height=50,bg="#f5f5f5")
top_frame.place(x=0,y=0)

middle_frame = Frame(window,width=800,height=470,bg="white")
middle_frame.place(x=0,y=50)

bottom_frame = Frame(window,width=800,height=80,bg="#f5f5f5")
bottom_frame.place(x=0,y=50+470)

#top_frame content

bar = Progressbar(top_frame,orient=HORIZONTAL, length=100)
bar.pack(side=RIGHT)

stat_Label = Label(top_frame,textvariable=stat)
stat_Label.pack(side=RIGHT)

text_Label = Label(middle_frame, textvariable= anwser_Text,pady=50,fg="black")
text_Label.pack(side=TOP)


entry = Entry(middle_frame,font=("Arial",20),fg="black",bg="#f5f5f5",width=40)
entry.pack(side=LEFT)


check_button = Button(middle_frame, textvariable= button_Text,width=10,command=anwser)
check_button.pack(side=RIGHT)

read_button = Button(middle_frame, text="Read",width=10,command=lambda : readActualWord(None))
read_button.pack(side=LEFT)


debug_button = Button(middle_frame, text="d",command=debug)
debug_button.pack(side=RIGHT)

#bottom_frame content

fc_side_check = Checkbutton(bottom_frame,text="ustaw 0",variable=flip, command=fc_side_change)
fc_side_check.pack()
fc_side_check.select()
fc_side_change()





#binds
window.bind("<Return>",lambda event: check_button.invoke())
# window.bind("<r>",readActualWord)
window.bind("<Up>",UpArrow)


#
window.mainloop()