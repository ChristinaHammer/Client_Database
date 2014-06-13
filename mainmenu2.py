#Christina Hammer
#main menu Gui

from tkinter import *
from tkinter import messagebox


def addnew():
    import newclientinter2
    return

def quitprogram():
    mmGui.destroy()
    return

def logoff():
    import logGui
    mmGui.destory()
    
    return
    
def csearch():
    #messagebox.INFO(title='Client Search', text='Searching Database...')
    #connect to client database!
    pass
    return

def hsearch():
    #connectto household database
    pass
    return

mmGui=Tk()

mmGui.geometry('700x400+200+200')

mmGui.title=('Main Menu -- Name of Food Pantry')

topframe=Frame(mmGui).pack()

toptitle=Label(topframe,text='Food Pantry Database', font=("Helvetica", 16)).pack()
#photo=PhotoImage(file="foodpantryimg.jpg")
#imagelabel=Label(topframe,image=photo).pack()

searchl=Label(mmGui, text='Client Search: ').pack()

seav=StringVar()
searchent=Entry(mmGui,textvariable=seav, width=60).pack()
seav.set('Please Enter a Name')

searb=Button(mmGui,text='Search!', command=csearch).pack()

houseav=StringVar()
housear=Label(mmGui, text='Household Search: ').pack()
housent=Entry(mmGui, textvariable=houseav, width=60).pack()
houseav.set('Please Enter an Address')
hsearb=Button(mmGui,text='Search!',command=hsearch).pack()

menubar=Menu(mmGui)

optionsmenu=Menu(menubar,tearoff=0)
optionsmenu.add_command(label='Quit',command=quitprogram)
optionsmenu.add_command(label='log off',command=logoff)
optionsmenu.add_command(label='Account Settings')
menubar.add_cascade(label='Options',menu=optionsmenu)
clientmenu=Menu(menubar,tearoff=0)

clientmenu.add_command(label='Add New Client', command=addnew)
clientmenu.add_command(label='Search Clients')
clientmenu.add_command(label='Add member to household')
menubar.add_cascade(label='Clients',menu=clientmenu)

mmGui.config(menu=menubar)

mmGui.mainloop()
