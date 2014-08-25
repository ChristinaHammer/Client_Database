"""cdbhelp.py

This file will define a window which displays help information.
"""

from tkinter import *
from tkinter import ttk

class cdbHelp:
    def __init__(self, tag):
        
        self.bgcolor = 'lavender'
        
        self.helpwin = Tk()
        #self.frame=Frame(self.helpwin).grid()
        self.helpwin.configure(background=self.bgcolor)
        self.helpwin.title('Help')

        self.instruct = Text(self.helpwin, font=('Helvetica', 10))

        self.instruct.grid(row=3, column=1, padx=20, pady=10)

        if tag == 'login':
            self.volunteer_help()
        else:
            return

    def volunteer_help(self):
        """This function will give volunteer help.
        """
        vinstruct = "Instructions: \n 1. Select your name from the list."+\
                    "\n2. Press the 'Login' button to proceed to the"+\
                    "database.\n3. Press the 'View' button to see and make"+\
                    "changes to your information."
                    
        self.helpwin.configure(background=self.bgcolor)
        self.instruct.insert('1.0', vinstruct)
        return
                                          
