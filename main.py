import random
from tkinter import *
import pandas
import time
from pathlib import Path

from numpy.ma.core import append

BACKGROUND_COLOR = "#B1DDC6"
toggle = 0
lang = "English"
fr_word =[]
en_word =[]
pinyin_number=[]

# -------French------
def dictionary_of_words():
    global lang
    global en_word, fr_word,pinyin_number,flip_timer_flip

    data = pandas.read_csv("./data/chinese.csv")
    fr_list = data.Simplified.to_list()
    fr_word = random.choice(fr_list)
    fr_number = fr_list.index(fr_word)
    en_list = data.Meaning.to_list()
    pinyin = data.Pinyin.to_list()
    en_word = en_list[fr_number]
    pinyin_number =pinyin[fr_number]


    # title_id=canvas.create_text(400, 150, text="French", font=("Arial", 40, "italic"))
    canvas.itemconfig(fr_front, image=card_back)
    canvas.itemconfig(title_id, text="Chinese",fill="white")
    canvas.itemconfig(word_id, text=fr_word,fill="white")
    canvas.itemconfig(pinyin_id,text="")
    flip_timer_flip=window.after(6000,func=flip_cards)


def flip_cards():
    global en_word
    global pinyin_number,flip_timer_dict
    canvas.itemconfig(fr_front, image=card_front)
    canvas.itemconfig(title_id, text="English",fill="black")
    canvas.itemconfig(word_id, text=en_word,fill="black")
    canvas.itemconfig(pinyin_id,text=pinyin_number)
    flip_timer_dict=window.after(6000,func=dictionary_of_words)


def remove_word():
    global fr_word
    global en_word,flip_timer_dict,flip_timer_flip
    originalList = pandas.read_csv("./data/chinese.csv")
    fr_list = originalList.Simplified.to_list()
    en_list = originalList.Meaning.to_list()
    pn_list = originalList.Pinyin.to_list()
    # window.after_cancel(flip_timer_flip)
    try:
        store = pandas.read_csv("learned_words.csv")
        print(store)
        words_delete_fr=store.Simplified.to_list()
        print(words_delete_fr)
        words_delete_en=store.Meaning.to_list()
        print(fr_word)
        words_delete_pn=store.Pinyin.to_list()
        words_delete_fr.remove(fr_word)
        words_delete_en.remove(en_word)
        words_delete_pn.remove(pinyin_number)
        df = pandas.DataFrame({"Simplified": words_delete_fr,"Pinyin":words_delete_pn,"Meaning":words_delete_en})
        # print(f"{df} try block")
        df.to_csv("learned_words.csv", index=False,mode="w")


    except FileNotFoundError:
        #path = Path("./data/learned_words.csv")
        df=pandas.DataFrame({"Simplified": fr_list, "Pinyin": pn_list, "Meaning": en_list})
        df.to_csv("learned_words.csv",index=False)


def add_word():
    global fr_word
    global en_word,pinyin_number
    store = pandas.read_csv("./data/chinese.csv")
    try:
        store = pandas.read_csv("learned_words.csv")
        df = pandas.DataFrame({"Simplified":[fr_word],"Pinyin":[pinyin_number],"Meaning":[en_word]})
        df.to_csv("learned_words.csv",mode="a",index=False,header=False)

    except FileNotFoundError:
        # path = Path("./data/learned_words.csv")
        df = pandas.DataFrame({"Simplified":[fr_word],"Pinyin":[pinyin_number],"Meaning": [en_word]})
        print(df)
        df.to_csv("learned_words.csv",mode="w",index=False)






# def next_card():
#         global toggle
#         global lang
#         lang="French"
#         canvas.itemconfig(fr_front,image=card_back)
#         canvas.itemconfig(title_id, text="French")
#         canvas.itemconfig(word_id, text=fr_word)
#         window.after(3000, flip_cards)


#-------UI SETUP----
window = Tk()
window.title("Flashy")
window.config(padx=50,pady=50,background=BACKGROUND_COLOR)
flip_timer_dict = window.after(6000,dictionary_of_words)
is_on=True
#Flash Card
canvas = Canvas(height=526,width=800,background=BACKGROUND_COLOR,highlightthickness=0)
card_front = PhotoImage(file="./images/card_front.png")
fr_front=canvas.create_image(400,275, image = card_front)
card_back = PhotoImage(file="./images/card_back.png")








title_id=canvas.create_text(400,150,font=("Arial",40,"italic") )
word_id=canvas.create_text(400,263,font=("Arial",60,"bold"))
pinyin_id= canvas.create_text(400,400,font=("Arial",60,"bold"))
canvas.grid(column=0,row=0,columnspan=2,rowspan=2)

#Labels
# title_label=Label(text="Title",font=("Arial",40,"italic"),background="white")
# title_label.grid(column=0,row=0,columnspan=2)
#
# translation_label=Label(text="Translation",font=("Arial",60,"bold"),background="white")
# translation_label.grid(column=0,row=1,columnspan=2)

#buttons
right_button_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_button_img,command= remove_word,highlightthickness=0)
right_button.grid(column=1,row=2)

wrong_button_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_button_img,command=add_word,highlightthickness=0)
wrong_button.grid(column=0,row=2)





window.mainloop()

