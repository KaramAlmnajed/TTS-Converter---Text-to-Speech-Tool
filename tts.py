import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import pyttsx3
import threading
import os

class TTSHandler:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
    
    def save_speech_to_file(self, text, file_path):
        try:
            self.engine.save_to_file(text, file_path)
            self.engine.runAndWait()
            return True, None
        except Exception as e:
            return False, str(e)

class TTSApp:
    def __init__(self, master):
        self.master = master
        self.master.title("TTS Converter")
        self.master.geometry("500x300")
        self.master.configure(bg="black")

        # Initialize TTS handler
        self.tts_handler = TTSHandler()

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title = ttk.Label(self.master, text="Text-to-Speech Converter", font=("Helvetica", 18, "bold"), background="black", foreground="white")
        title.pack(pady=10)

        # Text Input
        self.text_input = tk.Text(self.master, wrap=tk.WORD, height=10, font=("Helvetica", 12), bg="white", fg="black")
        self.text_input.pack(padx=10, pady=10, fill=tk.BOTH)

        # Save File Button
        self.save_button = ttk.Button(self.master, text="Choose Save Location", command=self.choose_save_location)
        self.save_button.pack(pady=5)

        # Convert Button
        self.convert_button = ttk.Button(self.master, text="Convert to Speech", command=self.convert_to_speech)
        self.convert_button.pack(pady=20)

        # Status Bar
        self.status_bar = ttk.Label(self.master, text="", anchor='w', background="black", foreground="white")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def choose_save_location(self):
        self.save_location = filedialog.asksaveasfilename(defaultextension=".mp3", 
                                                            filetypes=[("MP3 files", "*.mp3"), ("All files", "*.*")])
        if self.save_location:
            self.status_bar.config(text=f"Selected Save Location: {self.save_location}")

    def convert_to_speech(self):
        text = self.text_input.get("1.0", tk.END).strip()
        save_location = getattr(self, 'save_location', None)
        
        if text and save_location:
            self.status_bar.config(text="Converting...")
            threading.Thread(target=self.run_conversion, args=(text, save_location)).start()
        else:
            messagebox.showerror("Error", "Please enter text and select a save location.")

    def run_conversion(self, text, save_location):
        success, error = self.tts_handler.save_speech_to_file(text, save_location)
        if success:
            self.status_bar.config(text=f"Audio saved to: {save_location}")
            messagebox.showinfo("Success", f"Audio successfully saved to {save_location}")
        else:
            self.status_bar.config(text="Conversion failed.")
            messagebox.showerror("Error", f"Conversion failed: {error}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TTSApp(root)
    root.mainloop()
