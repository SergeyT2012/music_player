import json
import random
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter.constants import *
import os
import os.path
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from mutagen.flac import FLAC
from mutagen.m4a import M4A
from PIL import Image, ImageTk
import io
import pygame

_location = os.path.dirname(__file__)

import music_player_support

_bgcolor = '#d9d9d9'
_fgcolor = '#000000'
_tabfg1 = 'black' 
_tabfg2 = 'white' 
_bgmode = 'light' 
_tabbg1 = '#d9d9d9' 
_tabbg2 = 'gray40' 

_style_code_ran = 0
def _style_code():
    global _style_code_ran
    if _style_code_ran: return        
    try: music_player_support.root.tk.call('source',
                os.path.join(_location, 'themes', 'default.tcl'))
    except: pass
    style = ttk.Style()
    style.theme_use('default')
    style.configure('.', font = "TkDefaultFont")
    if sys.platform == "win32":
       style.theme_use('winnative')    
    _style_code_ran = 1

class Toplevel1:
    def __init__(self, top=None):
        
        pygame.mixer.init()
        self.current_index = -1
        self.is_paused = False

        top.protocol("WM_DELETE_WINDOW", self.save_and_exit)

        top.geometry("660x502+789+275")
        top.minsize(640, 480)
        top.maxsize(1905, 1050)
        top.resizable(1,  1)
        top.title("Toplevel 0")
        top.configure(background="#bababa")
        top.configure(highlightbackground="#bababa")
        top.configure(highlightcolor="#bababa")

        self.top = top

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        _style_code()
        self.TLabel2 = ttk.Label(self.top)
        self.TLabel2.place(relx=0.348, rely=0.251, height=34, width=400)
        self.TLabel2.configure(background="#bababa")
        self.TLabel2.configure(font="-family {song ti} -size 12")
        self.TLabel2.configure(relief="flat")
        self.TLabel2.configure(text='''ArtistName''')
        self.TLabel2.configure(compound='left')

        self.TLabel1 = ttk.Label(self.top)
        self.TLabel1.place(relx=0.348, rely=0.042, height=66, width=400)
        self.TLabel1.configure(background="#bababa")
        self.TLabel1.configure(font="-family {song ti} -size 20")
        self.TLabel1.configure(borderwidth="0")
        self.TLabel1.configure(relief="flat")
        self.TLabel1.configure(text='''TrackName''')
        self.TLabel1.configure(compound='left')

        self.placeholder_image = Image.open("/home/star/workspace/github/SergeyT2012/music_player/Images/placeholder.png")
        self.placeholder_image = self.placeholder_image.resize((149, 141))
        self.placeholder_photo = ImageTk.PhotoImage(self.placeholder_image)

        self.Label1 = tk.Label(self.top)
        self.Label1.place(relx=0.076, rely=0.042, height=141, width=149)
        self.Label1.configure(activebackground="#d9d9d9")
        self.Label1.configure(anchor='w')
        self.Label1.configure(compound='left')
        self.Label1.configure(font="-family {gothic} -size 9")
        self.Label1.configure(image=self.placeholder_photo)
        self.Label1.image = self.placeholder_photo

        self.Button2 = tk.Button(self.top)
        self.Button2.place(relx=0.242, rely=0.396, height=25, width=70)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(font="-family {gothic} -size 9")
        self.Button2.configure(text='''Previous''', command=self.play_previous_song)

        self.Button3 = tk.Button(self.top)
        self.Button3.place(relx=0.545, rely=0.396, height=25, width=70)
        self.Button3.configure(activebackground="#d9d9d9")
        self.Button3.configure(font="-family {gothic} -size 9")
        self.Button3.configure(text='''Next''', command=self.play_next_song)

        self.Button4 = tk.Button(self.top)
        self.Button4.place(relx=0.394, rely=0.438, height=25, width=60)
        self.Button4.configure(activebackground="#d9d9d9")
        self.Button4.configure(font="-family {gothic} -size 9")
        self.Button4.configure(text='''Shuffle''', command=self.shuffle)

        self.Button1 = tk.Button(self.top)
        self.Button1.place(relx=0.348, rely=0.396, height=25, width=130)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(font="-family {gothic} -size 9")
        self.Button1.configure(text='''Play/Pause''', command=self.play_pause)

        self.Button7 = tk.Button(self.top)
        self.Button7.place(relx=0.803, rely=0.578, height=45, width=130)
        self.Button7.configure(activebackground="#d9d9d9")
        self.Button7.configure(font="-family {gothic} -size 9")
        self.Button7.configure(text='''Add folder''', command=self.load_music_from_folder)

        self.Button5 = tk.Button(self.top)
        self.Button5.place(relx=0.803, rely=0.5, height=45, width=60)
        self.Button5.configure(activebackground="#d9d9d9")
        self.Button5.configure(font="-family {gothic} -size 9")
        self.Button5.configure(text='''Add song''', command=self.load_music)

        self.Button6 = tk.Button(self.top)
        self.Button6.place(relx=0.894, rely=0.5, height=45, width=70)
        self.Button6.configure(activebackground="#d9d9d9")
        self.Button6.configure(font="-family {gothic} -size 9")
        self.Button6.configure(text='''Del. song''', command=self.delete_song_from_library)

        self.Button8 = tk.Button(self.top)
        self.Button8.place(relx=0.803, rely=0.657, height=35, width=60)
        self.Button8.configure(activebackground="#d9d9d9")
        self.Button8.configure(font="-family {gothic} -size 9")
        self.Button8.configure(text='''+ Vol.''', command=self.add_volume)

        self.Button9 = tk.Button(self.top)
        self.Button9.place(relx=0.894, rely=0.657, height=35, width=70)
        self.Button9.configure(activebackground="#d9d9d9")
        self.Button9.configure(font="-family {gothic} -size 9")
        self.Button9.configure(text='''- Vol.''', command=self.decrease_volume)

        self.Button10 = tk.Button(self.top)
        self.Button10.place(relx=0.803, rely=0.717, height=145, width=130)
        self.Button10.configure(activebackground="#d9d9d9")
        self.Button10.configure(command=self.save_and_exit)
        self.Button10.configure(font="-family {gothic} -size 9")
        self.Button10.configure(text='''Exit''')

        self.TSeparator1 = ttk.Separator(self.top)
        self.TSeparator1.place(relx=0.348, rely=0.207,  relwidth=0.438)

        self.Progressvar1 = tk.DoubleVar()
        self.Progressbar1 = ttk.Progressbar(self.top, variable=self.Progressvar1)
        self.Progressbar1.place(relx=0.106, rely=0.355, relwidth=0.697
                , relheight=0.0, height=19)
        self.Progressbar1.configure(length="460",)

        self.Scrolledtreeview1 = ScrolledTreeView(self.top)
        self.Scrolledtreeview1.place(relx=0.0, rely=0.498, relheight=0.508
                , relwidth=0.803)
        self.Scrolledtreeview1.configure(columns=("Col1", "Col2", "Col3"))

        self.Scrolledtreeview1.heading("#0",text="Track")
        self.Scrolledtreeview1.heading("#0",anchor="center")
        self.Scrolledtreeview1.column("#0",width="256")
        self.Scrolledtreeview1.column("#0",minwidth="20")
        self.Scrolledtreeview1.column("#0",stretch="1")
        self.Scrolledtreeview1.column("#0",anchor="w")
        self.Scrolledtreeview1.heading("Col1",text="Artist")
        self.Scrolledtreeview1.heading("Col1",anchor="center")
        self.Scrolledtreeview1.column("Col1",width="257")
        self.Scrolledtreeview1.column("Col1",minwidth="20")
        self.Scrolledtreeview1.column("Col1",stretch="1")
        self.Scrolledtreeview1.column("Col1",anchor="w")
        self.Scrolledtreeview1.heading("Col2",text="Album")
        self.Scrolledtreeview1.heading("Col2",anchor="center")
        self.Scrolledtreeview1.column("Col2",width="257")
        self.Scrolledtreeview1.column("Col2",minwidth="20")
        self.Scrolledtreeview1.column("Col2",stretch="1")
        self.Scrolledtreeview1.column("Col2",anchor="w")
        self.Scrolledtreeview1.heading("Col3",text="Year")
        self.Scrolledtreeview1.heading("Col3",anchor="center")
        self.Scrolledtreeview1.column("Col3",width="257")
        self.Scrolledtreeview1.column("Col3",minwidth="20")
        self.Scrolledtreeview1.column("Col3",stretch="1")
        self.Scrolledtreeview1.column("Col3",anchor="w")
        self.Scrolledtreeview1.bind("<Double-1>", self.on_track_double_click)

        self.playlist = []
        self.load_previous_session()

    def popup1(self, event, *args, **kwargs):
        self.Popupmenu1 = tk.Menu(self.top, tearoff=0)
        self.Popupmenu1.configure(background=_bgcolor)
        self.Popupmenu1.configure(foreground=_fgcolor)
        self.Popupmenu1.configure(font="-family {gothic} -size 9")
        self.Popupmenu1.post(event.x_root, event.y_root)

    def popup2(self, event, *args, **kwargs):
        self.Popupmenu3 = tk.Menu(self.top, tearoff=0)
        self.Popupmenu3.configure(background=_bgcolor)
        self.Popupmenu3.configure(foreground=_fgcolor)
        self.Popupmenu3.configure(font="-family {gothic} -size 9")
        self.Popupmenu3.post(event.x_root, event.y_root)
    
    def load_music_from_folder(self):
        folder_selected = filedialog.askdirectory(title="Select Music Folder")
        if not folder_selected:
            return

        supported_formats = (".mp3", ".wav", ".flac", ".ogg")

        for root, dirs, files in os.walk(folder_selected):
            for file in files:
                if file.lower().endswith(supported_formats):
                    file_path = os.path.join(root, file)
                    title, artist, album, year = self.extract_metadata(file_path)
                    print(f"Loaded: {title} - Artist: {artist}")
                    item_id = self.Scrolledtreeview1.insert("", "end", text=title, values=(artist, album, year, file_path))
                    self.playlist.append({"title": title, "artist": artist, "album": album, "year": year, "file_path": file_path, "item_id": item_id})
    
    def save_and_exit(self):
        session_data = {
            "current_index": self.current_index,
            "playlist": [
                {
                    key: track[key] for key in ("title", "artist", "album", "year", "file_path")
                }
                for track in self.playlist
            ]
        }

        try:
            with open("session.json", "w") as f:
                json.dump(session_data, f, indent=4)
            print("Session saved.")
        except Exception as e:
            print(f"Error saving session: {e}")

        self.top.destroy()

    def load_previous_session(self):
        try:
            with open("session.json", "r") as f:
                session_data = json.load(f)
                self.current_index = session_data.get("current_index", -1)
                playlist = session_data.get("playlist", [])

                for track in playlist:
                    title = track["title"]
                    artist = track["artist"]
                    album = track["album"]
                    year = track["year"]
                    file_path = track["file_path"]

                    if os.path.exists(file_path):
                        item_id = self.Scrolledtreeview1.insert("", "end", text=title, values=(artist, album, year, file_path))
                        track["item_id"] = item_id
                        self.playlist.append(track)

                if self.current_index != -1 and len(self.playlist) > self.current_index:
                    current_track = self.playlist[self.current_index]
                    self.TLabel1.configure(text=current_track["title"])
                    self.TLabel2.configure(text=f"{current_track['artist']}\n{current_track['album']} - {current_track['year']}")
                    artwork = self.get_album_art(current_track["file_path"])
                    self.Label1.configure(image=artwork if artwork else self.placeholder_photo)
                    self.Label1.image = artwork if artwork else self.placeholder_photo
                    self.Scrolledtreeview1.focus(current_track["item_id"])
                    self.Scrolledtreeview1.selection_set(current_track["item_id"])
        except Exception as e:
            print(f"No session to load or error reading session: {e}")
        
    def load_music(self):
        file_path = filedialog.askopenfilename(
        title="Select Music File",
        filetypes=[("Audio Files", "*.mp3 *.wav *.flac *.ogg")]
        )
        
        if not file_path:
            return    
       
        if any(file_path == track["file_path"] for track in self.playlist):
            messagebox.showerror("Song already in playlist", "Song already in playlist!")
            return
        
        title, artist, album, year = self.extract_metadata(file_path)

        messagebox.showinfo("Loaded", f"Loaded: {title} - Artist: {artist}")
        item_id = self.Scrolledtreeview1.insert("", "end", text=title, values=(artist, file_path, year, album))
        self.playlist.append({"title" : title,"artist" : artist,"album" : album,"year" : year,"file_path" : file_path,"item_id" : item_id})
        
    def extract_metadata(self, file_path):
        try:
            audio = File(file_path, easy=True)
            title = audio.get("title", [os.path.basename(file_path)])[0]
            artist = audio.get("artist", ["Unknown Artist"])[0]
            album = audio.get("album", ["Unknown Album"])[0]
            year = audio.get("date", ["Unknown Year"])[0]

            return title, artist, album, year
        except Exception as e:
            print(f"Metadata error: {e}")
            return os.path.basename(file_path), "Unknown Artist", "Unknow Album", "Unknown Year"
        
    def get_album_art(self, file_path):
        
        try:
            if file_path.lower().endswith(".mp3"):
                audio = MP3(file_path, ID3=ID3)
                for tag in audio.tags.values():
                    if isinstance(tag, APIC):
                        image_data = tag.data
                        image = Image.open(io.BytesIO(image_data))
                        image = image.resize((150, 150))
                        return ImageTk.PhotoImage(image)
            
            elif file_path.lower().endswith(".flac"):
                audio = FLAC(file_path)
                if audio.pictures:
                    pic = audio.pictures[0]
                    image_data = pic.data
                    image = Image.open(io.BytesIO(image_data))
                    image = image.resize((150, 150))
                    return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"Could not extract artwork: {e}")
        return None
    
    def shuffle(self):  
        if not self.playlist:
            messagebox.showinfo("Shuffle", "Playlist is empty.")
            return
        
        random.shuffle(self.playlist)

        for item in self.Scrolledtreeview1.get_children():
            self.Scrolledtreeview1.delete(item)

        for track in self.playlist:
            item_id = self.Scrolledtreeview1.insert(
                "", "end",
                text=track["title"],
                values=(track["artist"], track["album"], track["year"], track["file_path"])
            )
            track["item_id"] = item_id
        

        self.current_index = 0
        item = self.playlist[self.current_index]
        title = item["title"]
        artist = item["artist"]
        album = item["album"]
        year = item["year"]
        file_path = item["file_path"]
        item_id = item["item_id"]

        self.current_index = 0
        self.TLabel1.configure(text=title)
        self.TLabel2.configure(text=f"{artist}\n{album} - {year}")
        artwork = self.get_album_art(file_path)
        self.Label1.configure(image=artwork if artwork else self.placeholder_photo)
        self.Label1.image = artwork if artwork else self.placeholder_photo
        self.play_audio(file_path)
        self.Scrolledtreeview1.focus(item_id)
        self.Scrolledtreeview1.selection_set(item_id)
        

    def check_music_end(self):
        if not pygame.mixer.music.get_busy() and not self.is_paused:
            self.play_next_track()
        else:
            self.top.after(1000, self.check_music_end)

    def delete_song_from_library(self):
        selected_item = self.Scrolledtreeview1.focus()
        if not selected_item:
            return

        item = self.Scrolledtreeview1.item(selected_item)
        title = item["text"]

        confirm = messagebox.askyesno("Delete Song", f"Are you sure you want to delete '{title}'?")
        if confirm:
            self.Scrolledtreeview1.delete(selected_item)
            if selected_item == self.playlist[self.current_index]["item_id"]:
                pygame.mixer.music.stop()
                self.playlist.remove(self.playlist[self.current_index])
            
    def get_track_length(self, file_path):
        
        global total_duration
        try:
            audio = File(file_path)
            if audio and hasattr(audio.info, 'length'):
                total_duration = int(audio.info.length)
            else:
                return "Unknown"
        except Exception as e:
            print(f"Error getting track length: {e}")
            return "Unknown"
    
    def on_track_double_click(self, event):
        
        global total_duration
        selected_item = self.Scrolledtreeview1.focus()
        
        if not selected_item:
            return
        
        item = self.Scrolledtreeview1.item(selected_item)
        title = item["text"]
        artist = item["values"][0]
        album = item["values"][1]  
        year = item["values"][2]
        file_path = item["values"][3]

        for index, track in enumerate(self.playlist):
            if track["file_path"] == file_path:
                self.current_index = index
                break
        else:
            self.current_index = -1 
            print("Track not found in playlist")
            return
                
        self.TLabel1.configure(text=title)
        self.TLabel2.configure(text=f"{artist}\n{album} - {year}")
        
        artwork = self.get_album_art(file_path)
        if artwork:
            self.Label1.configure(image=artwork)
            self.Label1.image = artwork
        else:
            self.Label1.configure(image=self.placeholder_photo)
        self.play_audio(file_path)
    
    def progressbar(self): 
        
        if self.current_track_duration > 0:
            current_time = pygame.mixer.music.get_pos() / 1000  # Convert ms to seconds
            progress = (current_time / self.current_track_duration) * 100
            progress = min(progress, 100)
            self.Progressvar1.set(progress)
        self.top.after(500, self.progressbar)
    
    def play_audio(self, file_path):
        
        pygame.mixer.music.set_volume(0.25)
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.top.after(1000, self.check_music_end)
            audio = File(file_path)
            self.current_track_duration = audio.info.length if audio and hasattr(audio.info, 'length') else 0
            self.progressbar()
        except Exception as e:
            pass

        
    def play_pause(self):
        
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True
        else:
            pygame.mixer.music.unpause()
            self.is_paused = False

    def play_next_track(self):
        
        if self.current_index + 1 < len(self.playlist):
            self.current_index += 1
            self.Scrolledtreeview1.focus(self.playlist[self.current_index]["item_id"])
            item = self.playlist[self.current_index]
            title = item["title"]
            artist = item["artist"]
            album = item["album"]
            year = item["year"]
            file_path = item["file_path"]
            item_id = item["item_id"]
            self.TLabel1.configure(text=title)
            self.TLabel2.configure(text=f"{artist}\n{album} - {year}")
            artwork = self.get_album_art(file_path)
            self.Label1.configure(image=artwork if artwork else self.placeholder_photo)
            self.Label1.image = artwork if artwork else None
            self.Scrolledtreeview1.selection_set(item_id)
            self.play_audio(file_path)
        else:
            print("Reached end of playlist.")
    
    def play_next_song(self):
        try:
            if self.current_index < len(self.playlist) - 1:
                self.current_index += 1
                item = self.playlist[self.current_index]
                title = item["title"]
                artist = item["artist"]
                album = item["album"]
                year = item["year"]
                file_path = item["file_path"]
                item_id = item["item_id"]
                self.TLabel1.configure(text=title)
                self.TLabel2.configure(text=f"{artist}\n{album} - {year}")
                artwork = self.get_album_art(file_path)
                if artwork:
                    self.Label1.configure(image=artwork)
                    self.Label1.image = artwork
                else:
                    self.Label1.configure(image=self.placeholder_photo)
                self.play_audio(file_path)
                self.Scrolledtreeview1.focus(item_id)
                self.Scrolledtreeview1.selection_set(item_id)
        except IndexError:
            messagebox.showerror("End of the playlist.", "End of the playlist.")
    
    def play_previous_song(self):
        if self.current_index > 0:
            self.current_index -= 1
            item = self.playlist[self.current_index]
            title = item["title"]
            artist = item["artist"]
            album = item["album"]
            year = item["year"]
            file_path = item["file_path"]
            item_id = item["item_id"]
            self.TLabel1.configure(text=title)
            self.TLabel2.configure(text=f"{artist}\n{album} - {year}")
            artwork = self.get_album_art(file_path)
            if artwork:
                self.Label1.configure(image=artwork)
                self.Label1.image = artwork
            else:
                self.Label1.configure(image=self.placeholder_photo)
            self.play_audio(file_path)
            self.Scrolledtreeview1.focus(item_id)
            self.Scrolledtreeview1.selection_set(item_id)
        else:
            messagebox.showerror("Already at the beginning of the playlist.", "Already at the beginning of the playlist.")
    
    def add_volume(self):
        current_volume = pygame.mixer.music.get_volume()
        if current_volume < 1.0:
            new_volume = min(current_volume + 0.1, 1.0)
            pygame.mixer.music.set_volume(new_volume)
        else:
            messagebox.showinfo("Volume", "Already at max volume!")
    
    def decrease_volume(self):
        
        current_volume = pygame.mixer.music.get_volume()
        if current_volume > 0.0:
            new_volume = max(current_volume - 0.1, 0.0)
            pygame.mixer.music.set_volume(new_volume)
        else:
            messagebox.showinfo("Volume", "Already at min volume!")

class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledTreeView(AutoScroll, ttk.Treeview):
    '''A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')
def start_up():
    music_player_support.main()

if __name__ == '__main__':
    music_player_support.main()




