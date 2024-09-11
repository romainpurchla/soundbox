import os
import tkinter as tk
from tkinter import messagebox
from soundsbox import mixer

# Dossier contenant les fichiers sons
SOUNDS_DIR = "./sounds/"

# Initialisation de pygame mixer pour jouer les sons
mixer.init()

# Fonction pour jouer un son
def play_sound(sound_file):
    try:
        mixer.music.load(sound_file)
        mixer.music.play()
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de lire le fichier : {sound_file}\n{e}")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Lecteur de Sons")

# Liste les fichiers audio dans le répertoire "sounds"
sounds = [f for f in os.listdir(SOUNDS_DIR) if f.endswith('.mp3') or f.endswith('.wav')]

# Crée un bouton pour chaque son
for sound in sounds:
    button = tk.Button(root, text=sound, command=lambda s=sound: play_sound(os.path.join(SOUNDS_DIR, s)))
    button.pack(pady=10)

# Lancer la boucle principale
root.mainloop()