
from tkinter import *
from tkinter import filedialog, font
import PyPDF2
from data import DataManager
import os

class GuiAppInterface():
    def __init__(self):
        self.add_file_path = ""
        self.files = []
        self.preview_file_path = ""
        self.pdf_text = []

        self.root = Tk()
        self.root.title("PDF to Audio App")
        self.root.config(padx=50, pady=50)
        self.frame = Frame(self.root)  
        self.frame.grid(row=0, column=0)
        self.app_font = font.Font(family="Arial", size=10)

        # preview_text:
        self.preview_text = Text(self.frame, width=80, height=50, font=("Arial", 10, "normal"))
        self.preview_text.grid(row=0, column=1, rowspan=15, padx=10, sticky=E)
        
        # general labels
        self.title_label = Label(self.frame, text="Why read when you can listen?", font=("Arial", 10, "italic"))
        self.title_label.grid(row=0, column=0, sticky=W, padx=5)

        self.subtitle_label = Label(self.frame, text="Add a PDF..", font=("Arial", 10, "underline"))
        self.subtitle_label.grid(row=1, column=0, sticky=W, padx=5)

        '''ADD FILE FRAME:'''
        self.file_frame = LabelFrame(self.frame, text="Add File", font=("Arial", 10, "bold"))  
        self.file_frame.grid(row=2, column=0, sticky=W, padx=1)

        # labels:
        self.browse_label = Label(self.file_frame, text="Select a file:", font=self.app_font)
        self.browse_label.grid(row=0, column=0, sticky=W, padx=10)

        self.select_label = Label(self.file_frame, text='Uploded files:', font=self.app_font)
        self.select_label.grid(row=1, column=0, sticky=W, padx=10)

        # buttons:
        self.select_file = Button(self.file_frame, text="Browse File", font=("Arial", 9, "normal"), command=self.add_file)
        self.select_file.grid(row=0, column=1, padx=10, pady=5, sticky=EW)

        self.clear_listbox_button = Button(self.file_frame, text="Clear Files", font=("Arial", 9, "normal"), command=self.clear_listbox)
        self.clear_listbox_button.grid(row=0, column=3, padx=10, pady=5, sticky=EW)

        '''CHOOSE VOICE:'''
        self.language_frame = LabelFrame(self.frame, text="Choose a voice", font=("Arial", 10, "bold"))
        self.language_frame.grid(row=3, column=0, pady=10, sticky=EW)

        # labels:
        self.options_label = Label(self.language_frame, text="Reading options:", font=self.app_font)
        self.options_label.grid(row=2, column=0, rowspan=3, sticky=W, padx=10)

        #buttons:
        '''READING OPTIONS FRAME:'''

        self.radio_state = IntVar()
        self.eng_button = Radiobutton(self.language_frame, text='Linda', value='1', variable=self.radio_state, command=self.set_voice)
        self.eng_button.grid(row=2, column=1, sticky=W)

        self.medium_button = Radiobutton(self.language_frame, text='John', value='2', variable=self.radio_state, command=self.set_voice)
        self.medium_button.grid(row=2, column=2, padx=100, sticky=EW)

        self.easy_button = Radiobutton(self.language_frame, text='Amy', value='3', variable=self.radio_state, command=self.set_voice)
        self.easy_button.grid(row=2, column=3, sticky=E)

        self.listbox = Listbox(self.file_frame, height=5, width=70, exportselection=False)
        self.listbox.grid(row=1, column=1, columnspan=3, padx=13, pady=10, sticky="news")
        self.listbox.bind("<<ListboxSelect>>", self.select_item)  

        self.read_file = Button(self.frame, text='Read!', font=self.app_font, command=self.read_file)
        self.read_file.grid(row=4, column=0, pady=10, padx=10)

        self.root.mainloop()

    def add_file(self):
        ''' opens a filedialog and loads files in the listbox to be selected'''
        self.add_file_path = filedialog.askopenfilename(initialdir="pdf_to_audio_API", title="Select a file!")
        if self.add_file_path not in self.files:
            self.files.append(self.add_file_path)
        for text in self.files:
            self.listbox.insert(self.files.index(text), text)
            self.files.remove(text)
            
    def clear_listbox(self):
        self.listbox.delete(0, END)
        self.files.clear()
        self.preview_text.delete(0.0, END)
        
    def select_item(self, event1):
        self.pdf_text=[]
        self.preview_file_path = self.listbox.get(self.listbox.curselection())
        self.preview_doc()

    def preview_doc(self):
        ''' loads and reads the PDF file setting a preview in the right text element of the tkinter interface'''
        self.preview_text.delete(0.0, END)
        with open(self.preview_file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for num in range(len(pdf_reader.pages)):
                book_pages = pdf_reader.pages[num]
                self.pdf_text.append(book_pages.extract_text())
        self.preview_text.insert(0.0, self.pdf_text)
            
    def set_voice(self):
        ''' sets the voice for reading the loaded PDF file'''
        if self.radio_state.get() == 1:
            return "Linda"   
        elif self.radio_state.get() == 2:
            return "John"   
        elif self.radio_state.get() == 3:
            return "Amy"
        
    def clear_previous_mp3(self):
        ''' delete any existing mp3 file when another read is activated'''
        dir_content = os.listdir("pdf_to_audio_API")
        for file in dir_content:
            if file[-4::] == ".mp3":
                os.remove(f'pdf_to_audio_API\\{file}')

    def read_file(self):
        ''' reads the file, by sending the request to voicerss API
        plays in windows media player the mp3 received'''
        self.clear_previous_mp3()
        data = DataManager(self.set_voice(), self.pdf_text)
        data.get_mp3()
        dir_content = os.listdir("pdf_to_audio_API")
        for file in dir_content:
            if file[-4::] == ".mp3":
                os.system(f'start pdf_to_audio_API\\{file}')
                

if __name__ == "__main__":    
    app = GuiAppInterface()