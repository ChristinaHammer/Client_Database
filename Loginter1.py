#Christina Hammer
#login menu

from tkinter import *
from tkinter import messagebox

def clearentry():
    ##clear user and password entries
    pass
    return

def login():
    import mainmenu2
    logGui.destroy()
    return

logGui=Tk()

logGui.geometry('400x200+200+200')
logGui.title('Food Pantry Client Database')

usern=StringVar()
passw=StringVar()

userlabel=Label(text='Username: ').pack()
userEnt=Entry(logGui,textvariable=usern).pack()
passlabel=Label(text='Password: ').pack()
passEnt=Entry(logGui,textvariable=passw).pack()

clearb=Button(logGui,text='Clear', command=clearentry).pack()
logb=Button(logGui, text='Log In', command=login).pack()

logGui.mainloop()
