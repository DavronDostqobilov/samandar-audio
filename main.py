import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import PyPDF2
import pyttsx3
import threading
import speech_recognition as sr
import os
import asyncio
import edge_tts
import tempfile
import pygame
import time
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import pythoncom
import shutil

# Dictionary to map Uzbek word numbers to indices
UZBEK_NUMBERS = {
    "bir": 1, "birinchi": 1,
    "ikki": 2, "ikkinchi": 2,
    "uch": 3, "uchinchi": 3,
    "to'rt": 4, "to'rtinchi": 4,
    "besh": 5, "beshinchi": 5,
    "olti": 6, "oltinchi": 6,
    "yetti": 7, "yettinchi": 7,
    "sakkiz": 8, "sakkizinchi": 8,
    "to'qqiz": 9, "to'qqizinchi": 9,
    "o'n": 10, "o'ninchi": 10
}

class VoiceLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Library & Reader")
        self.root.geometry("900x700")
        self.root.configure(bg="#f8f9fa")

        # Paths (EXE compatible)
        import sys
        if getattr(sys, 'frozen', False):
            self.base_path = os.path.dirname(sys.executable)
        else:
            self.base_path = os.path.dirname(os.path.abspath(__file__))
            
        self.audiobooks_path = os.path.join(self.base_path, "audiobooks")
        self.music_path = os.path.join(self.base_path, "music")
        
        for p in [self.audiobooks_path, self.music_path]:
            if not os.path.exists(p):
                os.makedirs(p)

        # State
        self.is_speaking = False
        self.is_listening = True
        self.current_category = None # "audiobooks" or "music"
        self.current_items = []
        self.recognizer = sr.Recognizer()
        
        # Audio
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # GUI
        self.setup_ui()
        
        # Start background listening
        threading.Thread(target=self.listen_for_commands, daemon=True).start()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#1e272e", height=80)
        header.pack(fill=tk.X)
        tk.Label(header, text="DIGITAL AUDIO LIBRARY", fg="#d2dae2", bg="#1e272e", font=("Segoe UI", 20, "bold")).pack(pady=20)

        # Main Container
        container = tk.Frame(self.root, bg="#f8f9fa")
        container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)

        # Left Panel (Navigation & Upload)
        left_panel = tk.Frame(container, bg="#ffffff", bd=1, relief=tk.RIDGE, width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20), pady=10)
        left_panel.pack_propagate(False)

        tk.Label(left_panel, text="Bo'limlar", font=("Segoe UI", 12, "bold"), bg="#ffffff").pack(pady=15)

        # Category Buttons
        tk.Button(left_panel, text="📚 Kitoblar", command=lambda: self.enter_category("audiobooks"), 
                  bg="#3498db", fg="white", font=("Segoe UI", 10), bd=0, height=2).pack(fill=tk.X, padx=15, pady=5)
        
        tk.Button(left_panel, text="🎵 Musiqalar", command=lambda: self.enter_category("music"), 
                  bg="#9b59b6", fg="white", font=("Segoe UI", 10), bd=0, height=2).pack(fill=tk.X, padx=15, pady=5)

        ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, padx=15, pady=20)

        tk.Label(left_panel, text="Fayl Yuklash", font=("Segoe UI", 10, "bold"), bg="#ffffff").pack(pady=5)
        
        tk.Button(left_panel, text="+ Kitob yuklash", command=lambda: self.upload_file("audiobooks"), 
                  bg="#2ecc71", fg="white", font=("Segoe UI", 9), bd=0, height=1).pack(fill=tk.X, padx=25, pady=5)
        
        tk.Button(left_panel, text="+ Musiqa yuklash", command=lambda: self.upload_file("music"), 
                  bg="#27ae60", fg="white", font=("Segoe UI", 9), bd=0, height=1).pack(fill=tk.X, padx=25, pady=5)

        # Right Panel (List Area)
        right_panel = tk.Frame(container, bg="#f8f9fa")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.list_label = tk.Label(right_panel, text="Ro'yxatni ko'rish uchun bo'limni tanlang", font=("Segoe UI", 14), bg="#f8f9fa", fg="#485460")
        self.list_label.pack(pady=(0, 10), anchor=tk.W)

        # Styled Listbox
        list_frame = tk.Frame(right_panel, bg="white", bd=1, relief=tk.FLAT)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.items_listbox = tk.Listbox(list_frame, font=("Segoe UI", 11), bd=0, highlightthickness=0, 
                                        selectbackground="#dfe6e9", selectforeground="#2d3436", yscrollcommand=scrollbar.set)
        self.items_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.config(command=self.items_listbox.yview)

        # Status
        self.status_bar = tk.Label(self.root, text="Ovozli buyruq kutilmoqda: 'Kitoblar', 'Musiqalar', '1', '2'...", 
                                   bd=0, anchor=tk.W, bg="#dfe6e9", padx=10, pady=5, font=("Segoe UI", 9, "italic"))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def upload_file(self, category):
        if category == "audiobooks":
            filetypes = [("Documents & Audio", "*.pdf *.txt *.mp3 *.wav")]
        else:
            filetypes = [("Audio Files", "*.mp3 *.wav")]
            
        files = filedialog.askopenfilenames(title=f"{'Kitob' if category == 'audiobooks' else 'Musiqa'} yuklang", filetypes=filetypes)
        
        if files:
            target_dir = self.audiobooks_path if category == "audiobooks" else self.music_path
            for f in files:
                try:
                    shutil.copy(f, target_dir)
                except Exception as e:
                    messagebox.showerror("Xato", f"Faylni yuklashda xatolik: {e}")
            
            self.enter_category(category) # Refresh
            self.announce("Fayl yuklandi")

    async def speak_uz(self, text):
        """Async function to speak using edge-tts"""
        try:
            fd, temp_path = tempfile.mkstemp(suffix=".mp3")
            os.close(fd)
            communicate = edge_tts.Communicate(text, "uz-UZ-MadinaNeural")
            await communicate.save(temp_path)
            
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
                
            pygame.mixer.music.unload()
            try: os.remove(temp_path)
            except: pass
        except Exception as e:
            print(f"TTS Error: {e}")

    def announce(self, text):
        """Helper to run speech in thread"""
        threading.Thread(target=lambda: asyncio.run(self.speak_uz(text)), daemon=True).start()

    def enter_category(self, category):
        self.current_category = category
        path = self.audiobooks_path if category == "audiobooks" else self.music_path
        self.current_items = [f for f in os.listdir(path) if f.lower().endswith(('.mp3', '.wav', '.txt', '.pdf'))]
        
        # Update UI
        self.list_label.config(text=f"{'Kitoblar' if category == 'audiobooks' else 'Musiqalar'} ro'yxati")
        self.items_listbox.delete(0, tk.END)
        for i, item in enumerate(self.current_items):
            self.items_listbox.insert(tk.END, f"{i+1}. {item}")

        # Announce
        count = len(self.current_items)
        msg = f"Sizda {count} ta {'kitob' if category == 'audiobooks' else 'musiqa'} bor."
        if count > 0:
            msg += " Qaysi birini eshitishni xohlaysiz? Tartib raqamini ayting."
        self.announce(msg)

    def play_item(self, index):
        if 0 <= index < len(self.current_items):
            filename = self.current_items[index]
            path = os.path.join(self.audiobooks_path if self.current_category == "audiobooks" else self.music_path, filename)
            
            print(f"Playing item: {path}")
            self.root.after(0, lambda: self.status_bar.config(text=f"Ijro etilmoqda: {filename}"))
            
            if filename.lower().endswith(('.mp3', '.wav')):
                try:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.stop()
                    pygame.mixer.music.unload() # Clear previous
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.play()
                except Exception as e:
                    print(f"Playback Error: {e}")
                    self.announce("Faylni qo'yishda xatolik yuz berdi")
            elif filename.lower().endswith('.txt'):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.announce(content)
            elif filename.lower().endswith('.pdf'):
                threading.Thread(target=self.read_pdf_text, args=(path,), daemon=True).start()

    def read_pdf_text(self, path):
        try:
            with open(path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += (page.extract_text() or "") + " "
                self.announce(text[:2000]) # Limit to 2000 chars for safety
        except Exception as e:
            print(f"PDF Error: {e}")

    def listen_for_commands(self):
        fs = 44100
        seconds = 3
        print("Listening for category/index commands...")
        
        while self.is_listening:
            try:
                recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
                sd.wait()
                
                temp_file = tempfile.mktemp(suffix=".wav")
                wav.write(temp_file, fs, recording)
                
                with sr.AudioFile(temp_file) as source:
                    audio = self.recognizer.record(source)
                    try:
                        command = self.recognizer.recognize_google(audio, language="uz-UZ").lower()
                        print(f"Eshitildi: {command}")
                        
                        # Navigation
                        if "kitob" in command:
                            self.announce("Kitoblar bo'limiga kirildi")
                            self.root.after(0, lambda: self.enter_category("audiobooks"))
                        elif "musiqa" in command:
                            self.announce("Musiqalar bo'limiga kirildi")
                            self.root.after(0, lambda: self.enter_category("music"))
                        elif "orqaga" in command:
                            self.announce("Bosh menyuga qaytildi")
                            self.current_category = None
                            self.root.after(0, lambda: self.list_label.config(text="Kategoriyani tanlang"))
                            self.root.after(0, lambda: self.items_listbox.delete(0, tk.END))
                        elif "to'xta" in command or "to'xtatish" in command:
                            self.announce("To'xtatildi")
                            pygame.mixer.music.stop()
                        elif "yangila" in command:
                            self.announce("Ro'yxat yangilandi")
                            if self.current_category:
                                self.root.after(0, lambda: self.enter_category(self.current_category))
                        
                        # Selection by number (Checking both digits and words)
                        found_idx = None
                        
                        # 1. Check for digits in command (e.g. "1")
                        import re
                        digits = re.findall(r'\d+', command)
                        if digits:
                            found_idx = int(digits[0])
                        
                        # 2. Check for words (e.g. "bir", "birinchi")
                        if found_idx is None:
                            for word, val in UZBEK_NUMBERS.items():
                                if word in command:
                                    found_idx = val
                                    break
                        
                        if found_idx is not None and self.current_category:
                            if found_idx <= len(self.current_items):
                                print(f"Applying selection: {found_idx}")
                                # Sequence: Announce first, then play the item
                                def sequence_task(idx):
                                    # 1. Announce selection and WAIT for it to finish
                                    asyncio.run(self.speak_uz(f"{idx}-chi element tanlandi"))
                                    # 2. Start the actual playback
                                    self.root.after(0, lambda: self.play_item(idx-1))
                                
                                threading.Thread(target=sequence_task, args=(found_idx,), daemon=True).start()
                            else:
                                self.announce("Bunday tartib raqami mavjud emas")
                            
                    except Exception as e:
                        print(f"Recognition inner error: {e}")
                
                if os.path.exists(temp_file): os.remove(temp_file)
            except Exception as e:
                print(f"Rec Error: {e}")
                time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceLibraryApp(root)
    root.mainloop()
