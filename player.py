import os
import pygame
from tkinter import Tk, Label, Button, filedialog

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("400x200")

        self.track_label = Label(self.root, text="No Track Playing", font=("Helvetica", 12))
        self.track_label.pack(pady=10)

        self.play_button = Button(self.root, text="Play", command=self.play_music)
        self.play_button.pack(pady=10)

        self.pause_button = Button(self.root, text="Pause", command=self.pause_music)
        self.pause_button.pack(pady=10)

        self.stop_button = Button(self.root, text="Stop", command=self.stop_music)
        self.stop_button.pack(pady=10)

        self.select_button = Button(self.root, text="Select Song", command=self.select_music)
        self.select_button.pack(pady=10)

        self.music_file = ""
        self.playing = False

    def play_music(self):
        if self.music_file:
            pygame.mixer.init()
            pygame.mixer.music.load(self.music_file)
            pygame.mixer.music.play()
            self.track_label.config(text="Now Playing: " + os.path.basename(self.music_file))
            self.playing = True

    def pause_music(self):
        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False

    def stop_music(self):
        if self.playing:
            pygame.mixer.music.stop()
            self.track_label.config(text="No Track Playing")
            self.playing = False

    def select_music(self):
        self.music_file = filedialog.askopenfilename(defaultextension=".mp3",
                                                       filetypes=[("MP3 files", "*.mp3"),
                                                                  ("WAV files", "*.wav"),
                                                                  ("All files", "*.*")])

if __name__ == "__main__":
    root = Tk()
    music_player = MusicPlayer(root)
    root.mainloop()
