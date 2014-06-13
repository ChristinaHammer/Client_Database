
#Christina Hammer
#new client Gui

from tkinter import *
from tkinter import messagebox

'''
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from cdbtabledef import Household, Person, Volunteer, Visit'''

def clientinfoconfirm():
    confirm=messagebox.OKCANCEL(title="Confirm Client Entry", message="Confirm the following client information:")
    if confirm==True:
        #newclientfunction
        pass
        return
    
def cancelentry():
    ncGui.destroy()
    return
    
#new client GUI
ncGui=Tk()

ncGui.geometry('600x200+400+200')

ncGui.title('Add New Client')

#Label(ncGui, text="Please enter the following information: \n").grid(row=0, column=0)

#entry variables
fname = StringVar()
lname = StringVar()
dob = IntVar()
age= IntVar()
phone=IntVar()
address=StringVar()
apt = StringVar()
cityv = StringVar()
statev = StringVar()
zipcv = StringVar()
doe = IntVar()

#Labels and entries
Label(ncGui, text="First Name").grid(row=1, column=0)
fname = Entry(ncGui).grid(row=2, column=0)

Label(ncGui, text="Last Name \t\t").grid(row=1, column=1)
lname = Entry(ncGui).grid(row=2, column=1)

Label(ncGui, text="Date of Birth").grid(row=1, column=2)
dob=Entry(ncGui).grid(row=2, column=2)

Label(ncGui, text="Age").grid(row=1, column=3)
age = Entry(ncGui).grid(row=2, column=3)

Label(ncGui, text="Phone").grid(row=3, column=0)
phone = Entry(ncGui).grid(row=4, column=0)

Label(ncGui, text="Address").grid(row=3, column=1)
address=Entry(ncGui).grid(row=4, column=1)

Label(ncGui, text="Apt.").grid(row=3, column=2)
apt=Entry(ncGui).grid(row=4, column=2)

Label(ncGui, text="City").grid(row=3, column=3)
city=Entry(ncGui,textvariable=cityv).grid(row=4, column=3)
cityv.set('Troy')

Label(ncGui, text="State").grid(row=5, column=0)
state=Entry(ncGui, textvariable=statev).grid(row=6, column=0)
statev.set('NY')

Label(ncGui, text="Zip").grid(row=5, column=1)
zipc=Entry(ncGui,textvariable=zipcv).grid(row=6, column=1)
zipcv.set('12180')

Label(ncGui, text="Date of Entry").grid(row=5, column=2)
doe=Entry(ncGui).grid(row=6, column=2)
        
        
Cancel=Button(ncGui,text='Cancel', command=cancelentry).grid(row=7,column=1)
Confirm=Button(ncGui,text='Add Client', command=clientinfoconfirm).grid(row=7,column=2)


ncGui.mainloop()




