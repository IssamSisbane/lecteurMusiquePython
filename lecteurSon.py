'''
from playsound import playsound
import time
playsound('audios/Pop Smoke - Hawk Em (Official Audio).mp3', True)
time.sleep(10)
playsound(False)
'''

from tkinter import *
from tkinter import filedialog, Text
import pygame
import time
from pytube import YouTube
from pytube import Playlist
import moviepy.editor
import os
import requests
import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
from mutagen.mp3 import MP3



wd = os.getcwd()
print("working directory is ", wd)

filePath = __file__
print("This script file path is ", filePath)

#Main screen
root = Tk()
root.title("Lecteur Audio")
root.geometry("500x450")

#tableau qui contient la music qui peut etre jouer
musics = []

#on initialise mixer de pygame
pygame.mixer.init()

def rechercherMusic():

    url = "https://www.youtube.com/results?search_query="+e2.get()
    print("url = "+url)
    browser = webdriver.Chrome()
    browser.get(url)

    elems = browser.find_elements_by_tag_name('a')

    liens = []

    for elem in elems:
        href = elem.get_attribute('href')
        if(href != None) and (href != "https://www.youtube.com/"):
            liens.append(href)
            

    print("liens = "+liens[0])

    browser.quit()

    telechargerMusic(liens[0])


def telechargerMusic(url = "rien"):

    if(url == "rien"):
        url = e1.get()

    video = YouTube(url)

    for widget in frame2.winfo_children():
        widget.destroy()

    print("\nLe titre de cette video est : "+video.title)
    print("\nLa chaine est : "+video.author)
    print('\nCette video a ',video.views," vues")

    streams = video.streams.filter(progressive = True).order_by('resolution').desc()
    for stream in streams:
        print(stream)

    streams[0].download("Web_Scrpijng/videos/")

    print("\nvideo telechargéé !!!")

    video1 =  moviepy.editor.VideoFileClip("Web_Scrpijng/videos/"+video.title.replace('.','')+".mp4")

    print(video.title)

    audio = video1.audio

    audio.write_audiofile('Web_Scrpijng/audios/'+video.title+".mp3")

    print("\naudio converti !!!")

    if musics :
        musics.pop(0)
    musics.append("C:/Users/snipi/OneDrive/Documents/Python/Web_Scrpijng/audios/"+video.title+".mp3")
    label = Label(frame2, text=musics[0].replace('C:/Users/snipi/OneDrive/Documents/Python/Web_Scrpijng/audios/','').replace('.mp3',''), bg="gray")
    label.pack()

def openMusic():

    
    for widget in frame2.winfo_children():
        widget.destroy()
    
    if musics :
        musics.pop(0)
    filename = filedialog.askopenfilename(initialdir="C:\\Users\snipi\OneDrive\Documents\Python\Web_Scrpijng\audios", title="Select File", filetypes=[("music","*.mp3")])
    musics.append(filename)
    '''
    song_box.insert(END, filename)
    '''
    print(filename)
    label = Label(frame2, text=musics[0].replace('C:/Users/snipi/OneDrive/Documents/Python/Web_Scrpijng/audios/','').replace('.mp3',''), bg="gray")
    label.pack()
    return filename

def play():
    pygame.mixer.music.load(musics[0])
    pygame.mixer.music.play()

    get_time()

def stop():
    pygame.mixer.music.stop()

global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.pause()
        paused = False
    else:
        pygame.mixer.music.unpause()
        paused = True

def get_time():
    current_time = pygame.mixer.music.get_pos() / 1000
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    status_bar.config(text=converted_current_time)
    status_bar.after(1000, get_time)




# Canvas
canvas = Canvas(root, height=700, width=700, bg="orange")
canvas.pack()



# Fenetres
frame = Frame(root, bg="white")
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)


frame2 = Frame(root, bg="blue")
frame2.place(relwidth=1, relheight=0.1, relx=0.0, rely=0.0)

'''
# Playlist Box
song_box = Listbox(canvas, bg="black", fg="green", width=60)
song_box.pack()
'''

# Labels
label2 = Label(frame, text = "Enter url du son a telecharger")
label2.pack()


# Entrées
e1 = Entry(frame)
e1.pack()

e2 = Entry(frame)


# Boutons
telecharger = Button(frame, text="Telcharger",command=telechargerMusic)
telecharger.pack()

telecharger2 = Button(frame, text="Telcharger2",command=rechercherMusic)
e2.pack()
telecharger2.pack()

openFile = Button(frame, text="Open File", padx = 10, pady=5, fg="grey", bg="#263D42",command=openMusic)
openFile.pack()

my_button = Button(frame, text="Play Song", command=play)
my_button.pack()

my_button2 = Button(frame, text="Stop", command=stop)
my_button2.pack()

my_button3 = Button(frame, text="Pause", command=lambda: pause(paused))
my_button3.pack()

my_button5 = Button(frame, text="Pos", command=get_time)
my_button5.pack()

# Status Bar
status_bar = Label(frame, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


#loop de la fenetre
root.mainloop()


