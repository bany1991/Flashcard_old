from tkinter.ttk import *
from tkinter import *
from ast import literal_eval

def saveWords():
    global source_words
    with open('words.txt', 'w',encoding='utf-8') as file_write:
        file_write.write(str(source_words))

def loadWords():
    with open('words.txt', encoding='utf-8') as file:
        source_words = literal_eval(file.read())
        return source_words
def addExample():
    global source_words
    index = wordsList.curselection()[0]
    newExample = (str(entryFirst.get()),str(entrySecond.get()))
    for word in source_words[index]:
        if isinstance(word,list):
            word.append(newExample)
    updateExamples()
    saveWords()
    entryFirst.delete(0,END)
    entrySecond.delete(0,END)
def addWord():
    global source_words
    newWord = [str(entryFirst.get()),str(entrySecond.get()),0,0,[]]
    source_words.append(newWord)
    updateWords()
    saveWords()
    entryFirst.delete(0,END)
    entrySecond.delete(0,END)
def updateWords():
    global source_words
    wordsList.delete(0,END)
    for i in range(len(source_words)):
        wordsList.insert(END, "{} : {}".format(source_words[i][0], source_words[i][1]))
def updateExamples():
    global source_words,examplesList
    index = wordsList.curselection()[0]
    examplesList.delete(0,END)
    for i in range(len(source_words[index][4])):
        examplesList.insert(END,source_words[index][4][i][0])
        examplesList.insert(END, source_words[index][4][i][1])
        examplesList.insert(END, "-----------------")

        # examplesList.insert("{} : {}".format(source_words[index][4][i][0],source_words[index][4][i][1]))
source_words = []
source_words = loadWords()


window =Tk()
window.geometry('1000x600')

selected = StringVar()

#adding frames
top_frame = Frame(window,width=800,height=50,bg="#f5f5f5")
top_frame.place(x=0,y=0)

middle_frame = Frame(window,width=800,height=470,bg="white")
middle_frame.place(x=150,y=50)

bottom_frame = Frame(window,width=800,height=100,bg="#f5f5f5")
bottom_frame.place(x=150,y=300)

wordsList = Listbox(middle_frame,font=("Arial",10),width=40)
wordsList.place(x=0,y=0)

examplesList = Listbox(middle_frame,font=("Arial",10),width=100)
examplesList.place(x=250, y=0)


entryFirst = Entry(bottom_frame,font=("Arial",15),fg="black",bg="white",width=40)
entryFirst.pack(side=TOP)
entrySecond = Entry(bottom_frame,font=("Arial",15),fg="black",bg="white",width=40)
entrySecond.pack(side=TOP)

addButton = Button(bottom_frame,text="dodaj przykład",command=addExample)
addButton.pack(side=BOTTOM)

addWordButton = Button(bottom_frame,text="dodaj słowo",command=addWord)
addWordButton.pack(side=BOTTOM)

updateWords()


wordsList.bind('<<ListboxSelect>>',lambda event: updateExamples())



window.mainloop()