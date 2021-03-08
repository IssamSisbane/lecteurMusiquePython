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

#Fenetre Principale
root = Tk()
root.title("Lecteur Audio")
root.geometry("500x450")

#tableau qui contient la musique qui peut etre jouer
musics = []

#on initialise mixer de pygame
pygame.mixer.init()

'''
Fait une recherche sur youtube avec le titre entrée par l'utilisateur puis recupère le lien du premier résultat dans la page de youtube.
Appelle la fonction telechargerMusic avec ce lien.

'''
def rechercherMusic():

    url = "https://www.youtube.com/results?search_query="+e2.get()
    print("url = "+url)

    # on recupère la code source de la page depuis l'url
    browser = webdriver.Chrome()
    browser.get(url)


    # on recupère seulement les liens
    elems = browser.find_elements_by_tag_name('a')

    liens = []

    # On recupère tous les liens des videos de la page
    for elem in elems:
        href = elem.get_attribute('href')
        if(href != None) and (href != "https://www.youtube.com/"):
            liens.append(href)
            

    print("liens = "+liens[0])

    browser.quit()

    # On choisit le premier lien de la page qui correspond au premier resultat de la requête
    telechargerMusic(liens[0])

'''
Telecharge la vidéo dont le lien est donnée par RechercheMusic ou donnée par l'entrée e1.
Converti ensuite la vidéo en .mp4 puis en .mp3

'''
def telechargerMusic(url = "rien"):

    # Si le lien entré n'a pas été crée grâce à la fonction rechercherMusic 
    # cela signifie que le lien entré est un lien direct vers la vidéo, 
    # on recupère ainsi directement ce que l'utilisateur à écrit dans l'entrée 1

    if(url == "rien"):
        url = e1.get()

    # On recupère les infos de la vidéo
    video = YouTube(url)

    # A chaque nouvelle recherche on remet la page à 0
    for widget in frame2.winfo_children():
        widget.destroy()

    print("\nLe titre de cette video est : "+video.title)
    print("\nLa chaine est : "+video.author)
    print('\nCette video a ',video.views," vues")

    # On recupère la vidéo dans la meilleure qualité
    streams = video.streams.filter(progressive = True).order_by('resolution').desc()
    for stream in streams:
        print(stream)

    # On telecharge la vidéo
    streams[0].download("Web_Scrpijng/videos/")

    print("\nvideo telechargéé !!!")

    # On met la vidéo dans le format mp4 pour le convertir juste après
    video1 =  moviepy.editor.VideoFileClip("Web_Scrpijng/videos/"+video.title.replace('.','')+".mp4")

    print(video.title)

    # On crée le nouveau fichier audio .mp3 qui contient la musique
    audio = video1.audio
    audio.write_audiofile('Web_Scrpijng/audios/'+video.title+".mp3")

    print("\naudio converti !!!")

    # La nouvelle musique recherché remplace l'ancienne
    if musics :
        musics.pop(0)
    musics.append("C:/Users/snipi/OneDrive/Documents/Python/Web_Scrpijng/audios/"+video.title+".mp3")

    # On met à jour le titre de la musique dans le label
    label = Label(frame2, text=musics[0].replace('C:/Users/snipi/OneDrive/Documents/Python/Web_Scrpijng/audios/','').replace('.mp3',''), bg="gray")
    label.pack()

"""
Ouvre une music dans le dossier audios selon son titre 
"""
def openMusic():

    # On remet à 0 la frame
    for widget in frame2.winfo_children():
        widget.destroy()
    
    # La nouvelle musique recherché remplace l'ancienne
    if musics :
        musics.pop(0)
    filename = filedialog.askopenfilename(initialdir="C:\\Users\snipi\OneDrive\Documents\Python\Web_Scrpijng\audios", title="Select File", filetypes=[("music","*.mp3")])
    musics.append(filename)
   
    print(filename)

    # On met à jour le titre de la musique dans le label
    label = Label(frame2, text=musics[0].replace('C:/Users/snipi/OneDrive/Documents/Python/Web_Scrpijng/audios/','').replace('.mp3',''), bg="gray")
    label.pack()

    return filename

'''
Lance la musique en première position dans la liste music[]
'''
def play():
    pygame.mixer.music.load(musics[0])
    pygame.mixer.music.play()

    get_time()

'''
Stop la musique en cours de lecture
'''
def stop():
    pygame.mixer.music.stop()

global paused
paused = False

'''
Permet de mettre en pause et de reprendre la musique
'''
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.pause()
        paused = False
    else:
        pygame.mixer.music.unpause()
        paused = True

'''
Permet de recupèrer le temps ecoulée depuis le debut de la lecture de la musqiue
'''
def get_time():

    # On recupère la durée que l'on met en seconde
    current_time = pygame.mixer.music.get_pos() / 1000

    # On converti en minutes et secondes
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    # On met à jour l'affichage
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


