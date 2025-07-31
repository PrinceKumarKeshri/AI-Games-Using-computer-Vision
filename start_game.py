from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from tkinter.font import BOLD, Font

def on_resize(event):
    
    image = bg_img.resize((event.width, event.height), Image.ANTIALIAS)
    
    l.image = ImageTk.PhotoImage(image)
    l.config(image=l.image)


root = Tk()
DIR = os.getcwd()
bg_img = Image.open(f"{DIR}\Resources\window_wallpaper.jpg")


root.geometry('1920x1080')
root.attributes('-fullscreen', True)
root.title('AI Game Zone')
root.iconbitmap(f'{DIR}\Resources\\vw.ico')


l = Label(root)
l.place(x = 0, y= 0, relwidth=1, relheight=1)
l.bind('<Configure>', on_resize)

bold_1 = Font(root, family="Papyrus", size=40, weight=BOLD)
bold_2 = Font(root, family="Arial", size=20, weight=BOLD)

Label(root, text='WELCOME   TO    AI    GAMEZONE', padx = 50, font=bold_1).pack(padx=  100, pady = 100, side=TOP)

def tic_tac_toe():
    os.system('python ' + DIR + '\\tic_tac_toe.py')

def snake():
    
    os.system('python ' + DIR + '\snake_game.py')
    
def popup_1():
    response = messagebox.askquestion('Quit Window!', 'Do you want to quit Game?')
    if response == 'yes':
        root.destroy()
    else:
        pass

    
button_1 = Button(root, text = 'Tic Tac Toe', command= lambda: [tic_tac_toe()], bg='white'
                    , fg='midnightblue', padx=40, font=bold_2)
button_1.place(relx=0.5, rely=0.5,anchor=CENTER)
button_1.pack(padx=470, pady = 0, side = LEFT)
button_2 = Button(root, text = 'Snake', command = lambda: [snake()], bg='white'
                    , fg='midnightblue', padx=62, font=bold_2)
button_2.place(relx=0.5, rely=0.5,anchor=CENTER)
button_2.pack(padx=0, pady=0, side = LEFT)


button_exit = Button(root, text='Exit', command=popup_1, bg='white',
                      fg='midnightblue', padx=40, font=bold_2).pack(padx=0, pady=50, side=BOTTOM, anchor=SE)

root.mainloop()
