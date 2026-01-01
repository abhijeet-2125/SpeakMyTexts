from tkinter import *
from tkinter import filedialog, messagebox
from gtts import gTTS
from pypdf import PdfReader as pdfreader
import os

root=Tk()
root.title("Text to speech convertor")
root.geometry("500x500")

canvas = Canvas(root, width=500, height=500, bg="lightblue")
canvas.pack()

#languages
languages = {
    "English": "en",
    "Hindi": "hi",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Chinese": "zh-cn",
    "Japanese": "ja",  
}

lang_var= StringVar(root)
lang_var.set("English") # default value
lang_dropdown = OptionMenu(root, lang_var, *languages.keys())
canvas.create_window(250, 60, window=lang_dropdown)

#text box
entry = Text(root, height=15, width=50, wrap=WORD)
canvas.create_window(250,250,window=entry)


def load_text_file():
    path=filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not path:
        return
    
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
        entry.delete(1.0, END)
        entry.insert(END, content)


def load_pdf_file():
    path=filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if not path:
        return
    
    try:
        reader=pdfreader(path)
        text=""
        for page in reader.pages:
            text += page.extract_text() or ""

        if not text.strip():
            messagebox.showerror("Error", "No extractable text found in the PDF.")
            return
        entry.delete(1.0, END)
        entry.insert(END, text)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read PDF file: {e}")


def text_to_speech():
    text=entry.get(1.0, END).strip()
    if not text:
        messagebox.showwarning("Empty","Please enter or load some text.")
        return
    lang_code = languages[lang_var.get()]

    tts =gTTS(text=text,lang=lang_code, slow=False)
    tts.save("Book_audio.mp3")


    os.system("start Book_audio.mp3" if os.name == "nt" else "open Book_audio.mp3")


#Buttons
btn_text=Button(text="Open text file", command=load_text_file)
canvas.create_window(150, 110, window=btn_text)

btn_pdf= Button(text="Open PDF file", command=load_pdf_file)
canvas.create_window(350, 110, window=btn_pdf)

btn_play= Button(text="convert and play", command=text_to_speech)
canvas.create_window(250, 340, window=btn_play)

root.mainloop()
