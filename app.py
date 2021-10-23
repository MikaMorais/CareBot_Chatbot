import tkinter
import customtkinter
from tkinter import *
from tkinter import font


from chat import get_response, bot_name

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
BG_BTN = "#491F58"
TEXT_COLOR = "#EAECEE"



FONT = "Helvetica 12"
FONT_BOLD = "Helvetica 11 bold"

class ChatApp:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()


    def _setup_main_window(self):
        self.window.title("ChatBot CareBot") #centralize title
        self.window.resizable(width=False, height=False)
        self.window.configure(width=545, height=590, bg=BG_COLOR)

        #Head Label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                            text="Bem vindo!", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1, rely=0.02)

        #tiny divider
        #line = Label(self.window, width=450, bg=BG_GRAY)
        #line.place(relwidth=1, rely=0.07, relheight=0.012)
        

        #text widget. For every text we display 20 character for each line and padding around so dont start to the very beggining
        self.text_widget = Text(self.window, wrap=WORD, width=22, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.770, relwidth=1, rely=0.13) 
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        

        #scroll bar
        #scrollbar = Scrollbar(self.text_widget, width=-1) #here changes it the width of the actual scrollbar
        ###scrollbar.place(relheight=1, relx=0.974, rely=0.008) alternative scrollbar, but the cursor keeps going back itself
        #scrollbar.pack(side=RIGHT, fill=Y)
        #self.text_widget.configure(yscrollcommand=scrollbar.set) # configuring the scrollbar in the text wigdet
        #scrollbar.configure(command=self.text_widget.yview) #chanching y of srollbar and view
        

        #bottom label
        bottom_label = Label(self.window, bg=BG_GRAY, height=50)
        bottom_label.place(relwidth=1, rely=0.900)

        #message entry box
        self.msg_entry = Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.05, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        
        #send button
        #send_button = Button(bottom_label, text="Enviar", font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda: self._on_enter_pressed(None))

        send_button = customtkinter.CTkButton(master=bottom_label, text="Enviar", fg_color=BG_BTN, corner_radius=10,
                                                command=lambda: self._on_enter_pressed(None))
        send_button.place(relwidth=0.22, relheight=0.043, rely=0.010, relx=0.77)

    

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "Você")

    
    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        msg2 = f"{bot_name}: {get_response(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)


        self.text_widget.see(END)
        



if __name__ == "__main__":
    app = ChatApp()
    app.run()