"""cdbgui.py
Developers: Christina Hammer, Noelle Todd
Last Updated: August 2, 2014
This file contains a class version of the interface, in an effort to
make a program with no global variables.

"""


from datetime import datetime, timedelta, date
from tkinter import *
from tkinter import ttk
from cdbifunc2 import *

class allobjects:
    """This class attempts to contain ALL labels, entries, etc.,
    so that there are no global variables.
    """
    
    def __init__(self):
        """This function declares all variables that are used by
        more than one function.
        """
    
        #Variables used later on
        self.cursel = 0
        self.id_list = []
        self.mem_list = []
        self.clientlist = list_people()
        self.visitDict = {}

        #dictionaries/lists used for date entry
        self.month_li = ["January", "February", "March", "April",
                             "May", "June", "July", "August", "September",
                             "October", "November", "December"]
        self.month_day_dict = {"January":31, "February":29, "March":31,
                               "April":30, "May":31, "June":30, "July":31,
                               "August":31, "September":30, "October":31,
                               "November":30, "December":31}
        self.month_int = {1:"January", 2:"February", 3:"March",
                          4:"April", 5:"May", 6:"June", 7:"July",
                          8:"August", 9:"September", 10:"October",
                          11:"November", 12:"December"}
        self.int_month = {"January":1, "February":2, "March":3,
                          "April":4, "May":5, "June":6, "July":7,
                          "August":8, "September":9, "October":10,
                          "November":11, "December":12}
        
        #holds entryboxes for family members
        self.memDict = {}

        #customize colors/fonts
        #This will connect to the database itself,
        #and retrieve the colors from there.
        self.bgcolor = 'lavender'
        #self.labfont = 'Helvetica'
        #self.labBGcolor = 'gray10'
        #self.labFGcolor = 'white'
        #self.cliSearLabBG = 'Coral'
        #self.cliSearLabFG = 'white'

        
        #configuring window
        self.ciGui=Tk()
        self.gridframe=Frame(self.ciGui).grid()
        self.ciGui.configure(background=self.bgcolor)
        self.ciGui.title('Client Information')


        #CLIENT SEARCH SETUP        
        self.cslabel = Label(self.gridframe,text='Client Search',
                             font=("Helvetica", 16),fg='white',bg='Coral')\
                             .grid(row=0,column=0,columnspan=2, sticky=W)
        self.csblank = Label(self.gridframe, text='     ',
                             font=('Helvetica',10), bg=self.bgcolor)\
                             .grid(row=0,column=2,sticky=E)

        #name searchbox
        self.ns = StringVar()
        self.nameSearchEnt = Entry(self.gridframe, cursor = 'shuttle',
                                   textvariable=self.ns)
        self.nameSearchEnt.grid(row=2,column=0)
        self.nameSearchEnt.bind('<Key>',self.nameSearch) 

        self.id_list=[]
        self.searchButton = Button(self.gridframe, text='Search Clients',
                                    command=self.nameSearch)
        self.searchButton.grid(row=2, column=1)

        #client listbox (clframe)
        
        self.client_listbox = Listbox(self.gridframe,height=10,width=40)
        self.client_listbox.bind('<<ListboxSelect>>', self.displayInfo )

        self.scrollb = Scrollbar(self.gridframe)
        self.client_listbox.bind('<<ListboxSelect>>',self.displayInfo )
        self.client_listbox.config(yscrollcommand=self.scrollb.set)
        self.scrollb.config(command=self.client_listbox.yview)
        
        self.client_listbox.grid(row=3, column=0, rowspan=5, columnspan=2)
        self.scrollb.grid(row=3, column=1, rowspan=5, sticky=E+N+S)

        self.firstSep = ttk.Separator(self.gridframe, orient='vertical')\
                        .grid(row=1,column=2,rowspan=40,sticky=NS)

        self.NCButton = Button(self.gridframe, text='New Client',
                                command=self.newClientDisplay, width=25)\
                                .grid(row=9, column=0, columnspan=2)

        #CLIENT INFORMATION SETUP       
        self.secondSep = ttk.Separator(self.gridframe, orient='horizontal')\
                                .grid(row=0,column=3,columnspan=40,sticky=EW)
        cilabel = Label(self.gridframe, text='Client Information',
                           font=("Helvetica", 16),fg='white',bg='gray10')\
                           .grid(row=0,column=3,columnspan=12, sticky=W)
        ciblank = Label(self.gridframe, text='   ',font=('Helvetica',10),
                        bg=self.bgcolor).grid(row=1,column=3,sticky=E)
        
        #First name
        self.fnv = StringVar()
        self.fnlabel = Label(self.gridframe, text="First Name: ",
                             font=('Helvetica',12),bg=self.bgcolor)\
                             .grid(row=2, column=3,sticky=E)
        self.fname = Entry(self.gridframe, textvariable=self.fnv,bd=4)
        self.fname.grid(row=2, column=4, columnspan=2, sticky=W)

        #Last name
        self.lnv = StringVar()
        self.lnlabel = Label(self.gridframe, text='Last Name: ',
                             font=('Helvetica',12),bg=self.bgcolor)\
                             .grid(row=2,column=5,sticky=W)
        self.lname = Entry(self.gridframe, textvariable=self.lnv,bd=4)
        self.lname.grid(row=2,column=6, columnspan=2, sticky=W)

        #Phone
        self.phv = StringVar()
        self.phlabel = Label(self.gridframe, text='Phone: ',
                             font=('Helvetica',12),bg=self.bgcolor)\
                             .grid(row=2, column=7,sticky=E)
        self.phone = Entry(self.gridframe, textvariable=self.phv, bd=4)
        self.phone.grid(row=2, column=8, columnspan=2, sticky=W)

        #Date of Birth
        self.doblabel = Label(self.gridframe, text='Date of Birth: ',
                              font=('Helvetica',12),bg=self.bgcolor)\
                              .grid(row=4,column=3, rowspan=2, sticky=E)
        self.mv = StringVar()
        self.dv = StringVar()
        self.yv = StringVar()

        #dob month combobox
        self.mob = ttk.Combobox(self.gridframe, width=10, state='readonly',
                                values=self.month_li, textvariable=self.mv)
        self.mob.bind('<<ComboboxSelected>>', self.monthbox_select)
        #dob day spinbox
        self.dob = Spinbox(self.gridframe, from_=0, to=0,
                           textvariable=self.dv, width=5, bd=4)
        #dob year spinbox
        self.yob = Spinbox(self.gridframe, from_=1900, to=2500,
                           textvariable=self.yv, width=7, bd=4)
        self.mob.grid(row=4, column=4, sticky=W)
        self.dob.grid(row=4, column=4, sticky=E)
        self.yob.grid(row=4, column=5)

        #Age
        self.agev = StringVar()
        self.alabel = Label(self.gridframe, text='Age: ',font=('Helvetica',12),
                            bg=self.bgcolor).grid(row=4,column=6,sticky=W)
        self.avallabel = Label(self.gridframe, textvariable=self.agev,
                               font=('Helvetica',12),bg=self.bgcolor)\
                               .grid(row=4,column=6,sticky=E)

        #Date Joined
        self.datejoinv = StringVar()
        self.djlabel = Label(self.gridframe, text="Date Joined:",
                             font=('Helvetica',12), bg=self.bgcolor)\
                             .grid(row=4,column=7,sticky=E)
        self.djEntry = Entry(self.gridframe, textvariable=self.datejoinv,
                             bd=4, state='readonly').grid(row=4, column=8)
                             

        #Extra blank label
        self.blankLab = Label(self.gridframe, text='   ',font=('Helvetica',10),
                              bg=self.bgcolor).grid(row=5,column=3,sticky=E)


        #VISIT INFORMATION SETUP
        self.thirdSep = ttk.Separator(self.gridframe, orient='horizontal')\
                        .grid(row=6,column=3,columnspan=40,sticky=EW)
        self.vilabel = Label(self.gridframe,text='Visit Information',
                             font=("Helvetica", 16),fg='white', bg='gray10')\
                             .grid(row=6,column=3,columnspan=12, sticky=W)
        self.viblank = Label(self.gridframe, text='   ',font=('Helvetica',10),
                             bg=self.bgcolor).grid(row=7,column=3,sticky=E)
        self.datelab = Label(self.gridframe, text='Date: ',
                             font=('Helvetica',14), bg=self.bgcolor)\
                             .grid(row=8,column=3)
        self.notelab = Label(self.gridframe, text='Notes:',
                             font=('Helvetica',14), bg=self.bgcolor)\
                             .grid(row=8,column=4)
        self.vislab = Label(self.gridframe, text='Visitor: ',
                            font=('Helvetica',14),bg=self.bgcolor)\
                            .grid(row=8,column=7)
        self.vollab = Label(self.gridframe, text='Volunteer: ',
                            font=('Helvetica',14),bg=self.bgcolor)\
                            .grid(row=8, column=8, sticky=W)
        self.viblank = Label(self.gridframe, text='   ',font=('Helvetica',10),
                             bg=self.bgcolor).grid(row=23,column=0,sticky=E)

        self.visdatev = StringVar()
        self.visitdate = Entry(self.gridframe,textvariable=self.visdatev,bd=4)
        self.visitdate.grid(row=9, column=3)

        self.notv = StringVar()
        self.notescv = Entry(self.gridframe, textvariable=self.notv,
                             width=60,bd=4)
        self.notescv.grid(row=9, column=4, columnspan=3)

        self.visv = StringVar()
        self.visitor = Label(self.gridframe,textvariable=self.visv, bd=4,
                            font=('Helvetica',10),bg=self.bgcolor)
        self.visitor = Entry(self.gridframe,textvariable=self.visv,
                             state='readonly',bd=4)
        self.visitor.grid(row=9, column=7,sticky=E)

        self.volv = IntVar()
        self.volun = Entry(self.gridframe,textvariable=self.volv,width=8,bd=4)
        self.volun.grid(row=9, column=8)
        
        #Extra blank label
        self.blankLab2 = Label(self.gridframe, text='   ',
                               font=('Helvetica',10), bg=self.bgcolor)\
                               .grid(row=13,column=3,sticky=E)
        #records visit        
        self.visButton = Button(self.gridframe, text='Record Visit', width=15,
                                command=self.recordVisit)
        self.visButton.grid(row=9,column=9,sticky=W)

        self.allvisButton = Button(self.gridframe, text='View All Visits',
                                   width=15, command=self.allVisits)
        self.allvisButton.grid(row=10, column=9, sticky=W)


        #HOUSEHOLD INFORMATION SETUP
        self.fourthSep = ttk.Separator(self.gridframe, orient='horizontal')\
                    .grid(row=14,column=3,columnspan=40,sticky=EW)
        self.hilabel = Label(self.gridframe,text='Household Information',
                        font=("Helvetica", 16),fg='white', bg='gray10')\
                        .grid(row=14,column=3,columnspan=12, sticky=W)
        self.hiblank = Label(self.gridframe, text='   ',font=('Helvetica',10),
                        bg=self.bgcolor).grid(row=15,column=3,sticky=E)

        #street address
        self.adv = StringVar()
        self.adlab = Label(self.gridframe, text='Address: ',
                           font=('Helvetica',12), bg=self.bgcolor)\
                           .grid(row=16,column=3,sticky=E)
        self.address = Entry(self.gridframe,textvariable=self.adv,
                             width=40,bd=4)
        self.address.grid(row=16, column=4,columnspan=2)

        #apartment
        self.apv = StringVar()
        self.aplab = Label(self.gridframe, text='Apt: ',font=('Helvetica',12),
                           bg=self.bgcolor).grid(row=16,column=6,sticky=E)
        self.aptn = Entry(self.gridframe,textvariable=self.apv,width=10,bd=4)
        self.aptn.grid(row=16,column=7)

        #city
        self.ctyv = StringVar()
        cilab = Label(self.gridframe, text='City: ',font=('Helvetica',12),
                      bg=self.bgcolor).grid(row=16,column=8,sticky=W)
        self.city = Entry(self.gridframe,textvariable=self.ctyv,bd=4)
        self.city.grid(row=16,column=9,sticky=W)

        #blank label
        self.blankLab3 = Label(self.gridframe, text='   ',
                               font=('Helvetica',12), bg=self.bgcolor)\
                               .grid(row=17,column=3,sticky=E)

        #state
        self.stav = StringVar()
        self.stlab = Label(self.gridframe, text='State: ',
                           font=('Helvetica',12), bg=self.bgcolor)\
                           .grid(row=18,column=3,sticky=E)
        self.state = Entry(self.gridframe,textvariable=self.stav,bd=4)
        self.state.grid(row=18,column=4)

        #zip
        self.zpv = StringVar()
        zilab = Label(self.gridframe, text='Zip Code: ',font=('Helvetica',12),
                      bg=self.bgcolor).grid(row=18,column=5,sticky=E)
        self.zipc = Entry(self.gridframe,textvariable=self.zpv,bd=4)
        self.zipc.grid(row=18, column=6)

        #Blank Label
        self.blankLab34 = Label(self.gridframe, text='   ',
                               font=('Helvetica',12), bg=self.bgcolor)\
                               .grid(row=18,column=7,sticky=E)

        #Date Verified
        self.dverilabel = Label(self.gridframe, text='Last Verified: ',
                              font=('Helvetica',12),bg=self.bgcolor)\
                              .grid(row=19,column=8, rowspan=2, sticky=E)
        self.mvv = StringVar()
        self.dvv = StringVar()
        self.yvv = StringVar()
        
        #for month entry
        self.mov = ttk.Combobox(self.gridframe, width=10, state='readonly',
                                values=self.month_li, textvariable=self.mvv)
        #self.mob.bind('<<ComboboxSelected>>', self.monthbox_select)
        
        #for day entry
        self.dov = Spinbox(self.gridframe, from_=0, to=0,
                           textvariable=self.dvv, width=5, bd=4)
        #for year entry
        self.yov = Spinbox(self.gridframe, from_=1900, to=2500,
                           textvariable=self.yvv, width=9, bd=4)
        #blank labels        
        self.vLab1 = Label(self.gridframe, text="    ", bg=self.bgcolor)
        self.vLab2 = Label(self.gridframe, text="    ", bg=self.bgcolor)
        self.mov.grid(row=19, column=9, rowspan=2, sticky=E)
        self.vLab1.grid(row=19, column=10)
        self.dov.grid(row=19, column=11, columnspan=2)
        self.vLab2.grid(row=19, column=13)
        self.yov.grid(row=19, column=14)

        #formatting labels/objects
        self.blankLab4 = Label(self.gridframe, text='   ',
                               font=('Helvetica',12), bg=self.bgcolor)\
                               .grid(row=19,column=3,sticky=E)
        self.blankLab5 = Label(self.gridframe, text='   ',
                               font=('Helvetica',12), bg=self.bgcolor)\
                               .grid(row=23,column=3,sticky=E)
        self.blankLab6 = Label(self.gridframe, text='   ',
                               font=('Helvetica',10), bg=self.bgcolor)\
                               .grid(row=25,column=3,sticky=E)
        self.blankLab7 = Label(self.gridframe, text='   ',
                               font=('Helvetica',10), bg=self.bgcolor)\
                               .grid(row=30,column=3,sticky=E)
        self.fifthsep = ttk.Separator(self.gridframe, orient='horizontal')\
                        .grid(row=31,column=3,columnspan=40,sticky=EW)
        self.blankLab8 = Label(self.gridframe, text='   ',
                               font=('Helvetica',10), bg=self.bgcolor)\
                               .grid(row=32,column=3,sticky=E)


        #The following variables will be removed and re-gridded
        #as the function of the interface changes.
        #

        #HOUSEHOLD MEMBERS SETUP
        #These variables appear on the updateClientDisplay only
        #
        self.adultsLabel = Label(self.gridframe, text='Adults: ',
                                 bg=self.bgcolor,font=('Helvetica',12))
        self.adultsLabel.grid(row=20,column=3,sticky=W)
        self.childrenLabel = Label(self.gridframe, text='Children: ',
                                   bg=self.bgcolor,font=('Helvetica',12))
        self.childrenLabel.grid(row=20,column=4,sticky=W)
        self.seniorsLabel = Label(self.gridframe, text='Seniors: ',
                                  bg=self.bgcolor,font=('Helvetica',12))
        self.seniorsLabel.grid(row=20,column=5,sticky=W)
        self.infantsLabel = Label(self.gridframe, text='Infants: ',
                                  bg=self.bgcolor,font=('Helvetica',12))
        self.infantsLabel.grid(row=20,column=6,sticky=W)
        self.totalLabel = Label(self.gridframe, text='Total: ',
                                bg=self.bgcolor,font=('Helvetica',12))
        self.totalLabel.grid(row=20,column=7,sticky=W)

        #info display widgets
        self.adl = StringVar()
        self.dispad = Label(self.gridframe,textvariable=self.adl,
                            font=('Helvetica',12),bg=self.bgcolor)
        self.chil = StringVar()
        self.dischil = Label(self.gridframe,textvariable=self.chil,
                             font=('Helvetica',12),bg=self.bgcolor)
        self.sen = StringVar()
        self.dissen = Label(self.gridframe,textvariable=self.sen,
                            font=('Helvetica',12),bg=self.bgcolor)
        self.inf = StringVar()
        self.disinf = Label(self.gridframe,textvariable=self.inf,
                       font=('Helvetica',12),bg=self.bgcolor)
        self.tot = StringVar()
        self.distot = Label(self.gridframe, textvariable=self.tot,
                            bg=self.bgcolor,font=('Helvetica',12))

        self.houseSep = ttk.Separator(self.gridframe, orient='horizontal')
        self.houseSep.grid(row=24,column=3,columnspan=40,sticky=EW)
        self.housetitle = Label(self.gridframe,text='Household Members',
                                font=("Helvetica", 16),fg='white',bg='gray10')
        self.housetitle.grid(row=24,column=3,columnspan=12, sticky=W)

        
        #add members to new household variable
        self.q = IntVar()
        self.famNum = Entry(self.gridframe, textvariable=self.q)    

        #listbox of family members
        self.family_listbox = Listbox(self.gridframe,height=5,width=30,font=12)
        self.fam_scroll = Scrollbar(self.gridframe)
        self.family_listbox.config(yscrollcommand=self.fam_scroll.set)
        self.fam_scroll.config(command=self.family_listbox.yview)
        
        self.family_listbox.grid(row=26, column=3, rowspan=4, columnspan=3, sticky=W)
        self.fam_scroll.grid(row=26, column=3, rowspan=4, columnspan=2, sticky=E+N+S)

        #family member buttons
        self.addmemb = Button(self.gridframe, text='Add Member', width=12,
                              command=self.addMemberEntryBoxes)
        self.addmemb.grid(row=26,column=5,sticky=E)
        self.removmemb = Button(self.gridframe, text='Remove Member',width=12,
                                command=self.removeMemberConfirm)
        self.removmemb.grid(row=27,column=5,sticky=E)
        self.viewmemb = Button(self.gridframe, text='View Member',width=12,
                               command=self.runViewMember)
        self.viewmemb.grid(row=28,column=5,sticky=E)

        #list of objects to be removed/regridded
        self.updateClientDisplayObj = [self.visButton, self.adultsLabel,
                                       self.childrenLabel,self.seniorsLabel,
                                       self.infantsLabel, self.totalLabel,
                                       self.dispad, self.dischil, self.dissen,
                                       self.disinf, self.distot, self.houseSep,
                                       self.housetitle, self.famNum,
                                       self.family_listbox, self.addmemb,
                                       self.removmemb, self.viewmemb]

        #list of variables to be reset
        self.updateClientDisplayVar = [self.adl, self.chil, self.sen, self.inf,
                                      self.tot, self.q]
        

        #NEW CLIENT DISPLAY WIDGETS
        #These variables appear on the newClientDisplay only
        #

        self.addhhsep = ttk.Separator(self.gridframe, orient='horizontal')
        self.addhhtitle = Label(self.gridframe,text='Add Household Members',
                                font=("Helvetica", 16),fg='white',bg='gray10')

        self.entNum = Label(self.gridframe,
                            text='Number of Family Members: ',
                            font=('Helvetica',10),bg=self.bgcolor)
        self.famname = Label(self.gridframe, text='Name:',
                             font=('Helvetica',10),bg=self.bgcolor)
        self.famfn = Label(self.gridframe, text='First Name:',
                           font=('Helvetica',10),bg=self.bgcolor)
        self.famln = Label(self.gridframe, text='Last Name:',
                           font=('Helvetica',10),bg=self.bgcolor)
        self.famdob = Label(self.gridframe, text='Date of Birth:',
                            font=('Helvetica',10),bg=self.bgcolor)
        self.famphone = Label(self.gridframe, text='Phone',
                              font=('Helvetica',10),bg=self.bgcolor)
        self.fammon = Label(self.gridframe,text='mm',
                            font=('Helvetica',10),bg=self.bgcolor)
        self.famday = Label(self.gridframe,text='dd',
                            font=('Helvetica',10),bg=self.bgcolor)
        self.famyear = Label(self.gridframe,text='yyyy',
                             font=('Helvetica',10),bg=self.bgcolor)
   
        self.newMembersB = Button(self.gridframe, text='Add Members',
                                  command=self.familyEntryBoxes)
        self.newClientSave = Button(self.gridframe, text='Save Client',
                                    command=self.addNew)
        self.cancelNewB = Button(self.gridframe, text='Cancel New Entry',
                                 command=self.updateClientDisplay)

        #list of objects to be removed/regridded
        self.newClientDisplayObj = [self.addhhsep, self.addhhtitle,
                               self.entNum, self.famname, self.famfn,
                               self.famln, self.famdob, self.famphone,
                               self.fammon, self.famday, self.famyear,
                               self.newMembersB, self.newClientSave,
                               self.cancelNewB]

        #MENU SETUP
        self.menubar = Menu(self.ciGui)
        self.saveB = Button(self.gridframe, text='Save Changes',
                            command=self.updateInfo,width=20)
        self.saveB.grid(row=33, column=3, columnspan=2)

        self.cancelB = Button(self.gridframe, text='Cancel Changes',
                              command=self.updateClientDisplay,width=20)
        self.cancelB.grid(row=33, column=5, columnspan=2)
        #^Essentially re-selects client

        self.optionsmenu = Menu(self.menubar,tearoff=0)
        self.optionsmenu.add_command(label='Quit', command=self.quitprogram)
        self.optionsmenu.add_command(label='log off', command=self.logoff)
        self.optionsmenu.add_command(label='Account Settings')
        self.optionsmenu.add_command(label='Configure Color', command=self.configure_background)
        self.menubar.add_cascade(label='Options',menu=self.optionsmenu)
        self.clientmenu = Menu(self.menubar,tearoff=0)

        self.clientmenu.add_command(label='Add New Client',
                                    command=self.addNew)
        self.clientmenu.add_command(label='View Monthly Report',
                                    command=self.monthlyReport)
        self.clientmenu.add_command(label='View Yearly',
                                    command=self.yearlyReport)
        self.clientmenu.add_command(label='Remove Household') #remove_household
        self.menubar.add_cascade(label='Clients',menu=self.clientmenu)

        ###infomenu not defined ERROR
        #self.infomenu.add_command(label='View Households')#list_households
        #self.infomenu.add_command(label='View Visits')#list_vis
        #self.infomenu.add_command(label='View Volunteers')
            #list_active_volunteers, list_all_volunteers, reactivate,remove
        #self.menubar.add_cascade(label='Records',menu=self.infomenu)
        self.ciGui.config(menu=self.menubar)
        
        
        #Sets some sizing stuff
        for i in range(0, 15):
            self.ciGui.columnconfigure(i, weight=1, minsize=15)

        for i in range(0, 35):
            self.ciGui.rowconfigure(i, weight=1, minsize=15)

        #mainloop
        self.ciGui.mainloop()
        
         #list of all variables that can be set
        #self.setVariables = [ns, fnv, lnv, phv, mv, dv, yv, agev, visdatev,
         #                    notv, visv, volv, adv, apv, ctyv, stav, zpv]


    def monthbox_select(self, *args):
        """This function is called when a month is selected from the
        month combobox. It will look up the month in the month_day_dict,
        and assign the right number of days to the "dob" spinbox.
        """
        month = self.mv.get()
        days = self.month_day_dict[month]
        self.dob.config(from_=1, to=days)
        return

    def allVisits(self):
        """This function displays all of a client's
        visits in a separate window.
        """            
        pass
    
    def quitprogram(self):
       quit_session()
       self.ciGui.destroy()
       return

    def logoff(self):
       import logGui
       self.ciGui.destory()
       return

    def monthlyReport(self):
       generate_monthly_report()
       return

    def yearlyReport(self):
       generate_yearly_report()
       return

    def volunteerInfo(self):
       return

    def error_popup(self, errmessage):
       """This function implements a simple pop-up window to warn user
       about bad data entry.
       """
       conf = messagebox.showerror(title='Error', message=errmessage)

    def clearVisits(self):
       """This function clears the entry boxes/visit notes
       used for visits.
       """
       #forgets previous visit notes
       allvaries = [self.notv, self.volv, self.visv]
       for i in range(0, len(allvaries)):
          allvaries[i].set("")
       
       try:
           vdates = self.visitDict['dates']
           vnotes = self.visitDict['notes']
           vvis = self.visitDict['visitors']
           vvol = self.visitDict['volunteers']
           easylist = [vdates, vnotes, vvis, vvol]
           for i in range(0, 4):
               for j in range(0, len(easylist[i])):
                   easylist[i][j].grid_forget()
           for i in range(0, 4):
               easylist[i] = []
           visitDict = {} 
           
       except KeyError:
           pass

       
    def clearFamily(self):
       #forgets additional family members
       self.family_listbox.delete(0, END)
       
       try:
           mfname = self.memDict["first"]
           mlname = self.memDict["last"]
           mm = self.memDict["mm"]
           dd = self.memDict["dd"]
           yy = self.memDict["yy"]
           phnum = self.memDict["phone"]
           easylist = [mfname, mlname, mm, dd,
                       yy, phnum]
           for i in range(0, 6):
              for j in range(0, len(easylist[i])):
                  easylist[i][j].grid_forget()
           for i in range(0, 6):
              easylist[i] = []
           self.memDict = {}

       except KeyError:
           pass
        

    def clearEntries(self):
       """This function clears the entry boxes that will never be
       removed from the display.
       """
              
       allvaries = [self.fnv, self.lnv, self.phv, self.mv, self.dv, self.yv,
                    self.adv, self.apv, self.q, self.agev,
                    self.notv, self.volv, self.visv, self.adl, self.chil,
                    self.sen, self.inf, self.tot, self.datejoinv, self.mvv,
                    self.dvv, self.yvv]
       
       #Clears the entryboxes
       for i in range(0, len(allvaries)):
          allvaries[i].set("")

       #sets defaulted entries
       today = datetime.now()
       todaystr = str(today.month)+'/'+str(today.day)+\
                         '/'+str(today.year)
       self.visdatev.set(todaystr)
       self.datejoinv.set(todaystr)
       self.ctyv.set("Troy")
       self.stav.set("NY")
       self.zpv.set(12180)

       #new client stuff
       
       allforgets = [self.adultsLabel, self.childrenLabel, self.seniorsLabel,
                     self.infantsLabel, self.totalLabel, self.family_listbox,
                     self.fam_scroll, self.addmemb, self.removmemb,
                     self.viewmemb, self.housetitle, self.houseSep, self.saveB,
                     self.cancelB, self.dispad, self.dischil, self.dissen,
                     self.disinf, self.distot, self.addhhsep, self.addhhtitle,
                     self.famNum, self.entNum, self.newMembersB,
                     self.newClientSave, self.cancelNewB, self.famname,
                     self.famfn, self.famln, self.famdob, self.famphone,
                     self.fammon, self.famday, self.famyear, self.visButton,
                     self.allvisButton]
       
       
       for i in range(0, len(allforgets)):
          allforgets[i].forget()
          allforgets[i].grid_forget()
       
       #forgets additional family members
       self.clearFamily()
       
       #forgets previous visit notes
       self.clearVisits() 

       
    def recordVisit(self):
        """This function will insert a new visit, clear old visit
        display info, and reset the visit display.
        """
        #inserts new visit
        try:
           vol_id = int(self.volv.get())
           vdate = datetime.now()
           note = str(self.notv.get())
           visitInfo = visitData(vol_id, visitDate=vdate, notes=note)
           new_visit(self.cursel, visitInfo)
           
        except ValueError:
           self.error_popup("Uh, oh! Better check the visit info!")
           return

        #clears old visit notes
        self.clearVisits()
        
        #refreshes visit note display
        info = select_client(self.cursel)
        self.displayVisitInfo(info)
        
   
    def familyEntryBoxes(self, *args):
       """This function generates entry boxes for adding new family members.
       The entry boxes are saved in list form and added to the dictionary
       memDict.
       """
       #clears any boxes already displayed
       self.clearFamily()
       
       try:
           n = int(self.q.get())
       except ValueError:
           return
        
       #add instructive labels to grid
       self.famfn.grid(row=24,column=3)
       self.famln.grid(row=24,column=4)
       self.famdob.grid(row=24,column=5)
       self.famphone.grid(row=24,column=8)
       self.fammon.grid(row=25,column=5,sticky=S)
       self.famday.grid(row=25,column=6,sticky=S)
       self.famyear.grid(row=25,column=7,sticky=S)

       #create lists
       fnames = []
       lnames = []
       mm = []
       dd = []
       yy = []
       phnum = []

       #create entry boxes, grid them, and append them to a list
       for i in range(0, n):
           fname = Entry(self.gridframe)
           fname.grid(row=26+i, column=3)
           fnames.append(fname)
           
           lname = Entry(self.gridframe)
           lname.grid(row=26+i, column=4)
           lnames.append(lname)

           month = ttk.Combobox(self.gridframe, width=12, state='readonly',
                              values=self.month_li)
           #month.bind('<<ComboboxSelected>>', self.monthbox_select)
           month.grid(row=26+i, column=5)
           mm.append(month)
           
           day = Spinbox(self.gridframe, from_=0, to=0, width=5)
           day.grid(row=26+i, column=6)
           dd.append(day)
           
           year = Spinbox(self.gridframe, from_=1900, to=2500, width=7)
           year.grid(row=26+i, column=7)
           yy.append(year)
           
           phone = Entry(self.gridframe)
           phone.grid(row=26+i, column=8)
           phnum.append(phone)
           

       #add all lists to dictionary
       self.memDict["first"] = fnames
       self.memDict["last"] = lnames
       self.memDict["mm"] = mm
       self.memDict["dd"] = dd
       self.memDict["yy"] = yy
       self.memDict["phone"] = phnum


    def addMemberEntryBoxes(self, *args):
       """This function generates entry boxes for adding new family members.
       The entry boxes are saved in list form and added to the dictionary
       memDict.
       """
       #add instructive labels to grid
       self.famname.grid(row=26, column=6)
       self.famfn.grid(row=25,column=7, sticky=SW)
       self.famln.grid(row=25,column=8, sticky=SW)
       self.famdob.grid(row=28,column=6)
       self.famphone.grid(row=30,column=6)
       self.fammon.grid(row=27,column=7,sticky=SW)
       self.famday.grid(row=27,column=8,sticky=SW)
       self.famyear.grid(row=27,column=9,sticky=SW)

       #create entry boxes, grid them, and append them to a list

       #addmemfna=StringVar()
       self.fname = Entry(self.gridframe)
       self.fname.grid(row=26, column=7, sticky=W)
       self.memDict["first"]=[self.fname]

       #alna=StringVar()
       self.lname = Entry(self.gridframe)
       self.lname.grid(row=26, column=8, sticky=W)
       self.memDict["last"]=[self.lname]

       self.month = ttk.Combobox(self.gridframe, width=12, state='readonly',
                              values=self.month_li)
       #month.bind('<<ComboboxSelected>>', self.monthbox_select)
       self.month.grid(row=28, column=7, sticky=W)
       self.memDict["mm"]=[self.month]

       self.day = Spinbox(self.gridframe, from_=0, to=0, width=5)
       self.day.grid(row=28, column=8, sticky=W)
       self.memDict["dd"]=[self.day]
           
       self.year = Spinbox(self.gridframe, from_=1900, to=2500, width=7)
       self.year.grid(row=28, column=9, sticky=W)
       self.memDict["yy"]=[self.year]

       #pho=StringVar()
       self.phone = Entry(self.gridframe)
       self.phone.grid(row=30, column=7, sticky=W)
       self.memDict["phone"]=[self.phone]

       return

#Q: WHAT HAPPENS WHEN TWO NEW CLIENTS ARE ADDED IN A ROW?
    #DOES ONE HAVE MEMBERS FROM THE PREVIOUS CLIENT?

    def addNew(self):
       """This function adds a new household to the database.
       #NOTE: lots of error testing/resetting still to be done.
       ##ANOTHER NOTE: we need to check checkboxes for dummy addresses
       #(domestic violence address, and homeless address)
       """
        
       #create newClientData object for visitor           
       try:
           fname = str(self.fnv.get())
           lname = str(self.lnv.get())
           dy = int(self.yv.get())
           month = str(self.mv.get())
           dm = self.int_month[month]
           dd = int(self.dv.get())
           phnum = str(self.phv.get())
           #IMPLEMENT get dateJoined
           
           ncd1 = newClientData(firstname=fname, lastname=lname,
                   dob=date(year=dy, month=dm, day=dd), phone=phnum)
                   #dateJoined=datetime.now())
           newClientInfo_list = [ncd1]

       except ValueError:
           self.error_popup("Oops! Check the visitor information again!")
           return
           
       #create newClientData objects for family members
       #memDict = md.getMemDict
       try:
           mfname = self.memDict["first"]
           mlname = self.memDict["last"]
           mm = self.memDict["mm"]
           dd = self.memDict["dd"]
           yy = self.memDict["yy"]
           phnum = self.memDict["phone"]

           for i in range(0, len(mfname)):
               #check for empty client in case of accident?
               try:
                   fname = str(mfname[i].get())
                   lname = str(mlname[i].get())
                   dy = int(yy[i].get())
                   month = str(mm[i].get())
                   dm = self.int_month[month]
                   dday = int(dd[i].get())
                   phn = str(phnum[i].get())

                   ncd = newClientData(firstname=fname, lastname=lname,
                   dob=date(year=dy, month=dm, day=dday), phone=phn)
                   newClientInfo_list.append(ncd)
               
               except ValueError:
                   self.error_popup(
                       "Oops! Some family members aren't entered properly!")
                   return

       except KeyError: pass
       
       #create houseData object for the household information
       try:
           streeta = str(self.adv.get())
           citya = str(self.ctyv.get())
           statea = str(self.stav.get())
           zipa = int(self.zpv.get())
           apta = str(self.apv.get())
           #IMPLEMENT get dateVerified
           houseInfo = houseData(street=streeta, city=citya, state=statea,
                                         zip=zipa, apt=apta)

       except ValueError:
           self.error_popup(
               "Oops! The household information isn't entered right...")
           return 
           
       #create visitData object to hold visit information
       try:
           #IMPLEMENT get volunteer id
           #IMPLEMENT get visit date
           vnote = str(self.notv.get())
           visitInfo = visitData(Vol_ID=1, visitDate=datetime.now(),
                                 notes=vnote)
      
       except ValueError:
           self.error_popup("Oops! Did you forget some visit information?")
           return

       #send all objects to new_household function
       client_id = new_household(houseInfo, visitInfo, newClientInfo_list)
       
       #adultsLabel.grid(row=20,column=3,sticky=W) #??

       self.clientlist = list_people()

       #self.updateClientDisplay()
       self.displayNewInfo(client_id)

   
    def nameSearch(self, *args):
       """This function returns relevant results
       """

       #removes old listbox contents
       self.client_listbox.delete(0, END)
       del self.id_list[:]
       
       name = str(self.ns.get()).capitalize()
       #NOTE:Get lowercase names, too

       #c = clientlist.getClients
       c = self.clientlist
       
       found_clients=[]
       for i in range(len(c)):
           if name in c[i][0]:
               found_clients.append(c[i])

       found_clients.sort()

       #listing just the names and addresses of the people
       x=[]
       for i in range(len(found_clients)):
           dobstr=str(found_clients[i][1].month)+\
                   "/"+str(found_clients[i][1].day)+\
                   '/'+str(found_clients[i][1].year)
           a=str(found_clients[i][0])+" --"+dobstr
           
           x.append(a)
           self.id_list.append(found_clients[i][2])  
       
       for i in range(len(x)):
           self.client_listbox.insert(i,x[i])
       
       return

    
    def newClientDisplay(self):
        self.clearEntries()
        
        self.addhhsep.grid(row=20,column=3,columnspan=40,sticky=EW)
        self.addhhtitle.grid(row=20,column=3,columnspan=12, sticky=W)

        Label(self.gridframe, text='   ',font=('Helvetica',10),bg=self.bgcolor)\
                              .grid(row=21,column=3,sticky=E)

        ##enter family members
        
        self.famNum.grid(row=22, column=4)
        self.entNum.grid(row=22, column=3)
        self.newMembersB.grid(row=22, column=5)
        self.newClientSave.grid(row=40,column=3, columnspan=2)
        self.cancelNewB.grid(row=40, column=5, columnspan=2)
        
        return


    def updateClientDisplay(self):
       self.clearEntries()
       #####add back
       self.visButton.grid(row=9,column=9,sticky=W)
       self.allvisButton.grid(row=10, column=9, sticky=W)
       self.adultsLabel.grid(row=20,column=3,sticky=W)
       self.childrenLabel.grid(row=20,column=4,sticky=W)
       self.seniorsLabel.grid(row=20,column=5,sticky=W)
       self.infantsLabel.grid(row=20,column=6,sticky=W)
       self.totalLabel.grid(row=20,column=7,sticky=W)
       self.family_listbox.grid(row=26, column=3, rowspan=4, columnspan=3, sticky=W)
       self.fam_scroll.grid(row=26, column=3, rowspan=4, columnspan=2, sticky=E+N+S)
       self.addmemb.grid(row=26,column=5)
       self.removmemb.grid(row=27,column=5)
       self.viewmemb.grid(row=28,column=5)
       self.housetitle.grid(row=24,column=3,columnspan=12, sticky=W)
       self.houseSep.grid(row=24,column=3,columnspan=40,sticky=EW)
       self.saveB.grid(row=33, column=3, columnspan=2)
       self.cancelB.grid(row=33, column=5, columnspan=2)
       
       return


   
    def updateInfo(self, *args):
       """This function will update the visitor's information, the household
       information, and the visit information. It will also add family members,
       but it will NOT update the family members.
       """
       sel_id = self.cursel

       try:
           fname = str(self.fnv.get())
           lname = str(self.lnv.get())
           dday = int(self.dv.get())
           month = str(self.mv.get())
           dm = self.int_month[month]
           dy = int(self.yv.get())
           phnum = str(self.phv.get())
           #IMPLEMENT get dateJoined
           
           cd = oldClientData(sel_id, firstname=fname, lastname=lname,
                              dob=date(year=dy, month=dm, day=dday),
                              phone=phnum)
           oldClientInfo_list = [cd]
           
       except ValueError:
           self.error_popup("Did you forget to enter visitor's data?")
           return
       
       try:
           addr = str(self.adv.get())
           cit = str(self.ctyv.get())
           stat = str(self.stav.get())
           zint = int(self.zpv.get())
           #IMPLEMENT get dateVerified
           apart = str(self.apv.get())
           houseInfo = houseData(street=addr, city=cit, state=stat,
                                 zip=zint, apt=apart)
       except ValueError:
           self.error_popup("Household info didn't get saved :(")
           return


       #create newClientData objects for family members
       newClientInfo_list = []

       try:
           mfname = self.memDict["first"]
           mlname = self.memDict["last"]
           mm = self.memDict["mm"]
           dd = self.memDict["dd"]
           yy = self.memDict["yy"]
           phnum = self.memDict["phone"]

           for i in range(0, len(mfname)):
               #check for empty client in case of accident?
               try:
                   fname = str(mfname[i].get())
                   lname = str(mlname[i].get())
                   dy = int(yy[i].get())
                   month = str(mm[i].get())
                   dm = self.int_month[month]
                   #dm = int(mm[i].get())
                   dday = int(dd[i].get())
                   phn = str(phnum[i].get())

                   ncd = newClientData(firstname=fname, lastname=lname,
                   dob=date(year=dy, month=dm, day=dday), phone=phn)
                   newClientInfo_list.append(ncd)
               
               except ValueError:
                   self.error_popup(
                       "Oops! Some family members aren't entered properly!")
                   return

       except KeyError: pass
       
       update_all(sel_id, houseInfo, oldClientInfo_list, newClientInfo_list)
       
       self.clientlist = list_people()
       self.updateClientDisplay()
       self.displayNewInfo(self.cursel)

       print ('Changes have been saved!')



    def displayClientInfo(self, info, *args):
       """This function displays the client information.
       """
       visitor = info["visitor"]
         
       
       self.fnv.set(visitor.firstname)
       self.lnv.set(visitor.lastname)

       month = self.month_int[visitor.dob.month]
       self.mv.set(month)
       self.dv.set(visitor.dob.day)
       self.yv.set(visitor.dob.year)
       self.agev.set(age(visitor.dob))
       self.phv.set(visitor.phone)

       joined = str(visitor.dateJoined.month) + "/" +\
                str(visitor.dateJoined.day) + "/" +\
                str(visitor.dateJoined.year)
       self.datejoinv.set(joined)       
       return


    def displayHouseholdInfo(self, info, *args):
       """This function displays the household information for
       a client.
       """
       house = info["household"]
       self.adv.set(house.street)
       self.apv.set(house.apt)
       self.ctyv.set(house.city)
       self.stav.set(house.state)
       self.zpv.set(house.zip)

       if house.dateVerified != None:
           month = house.dateVerified.month
           self.mvv(month_int[month])
           self.dvv(house.dateVerified.day)
           self.yvv(house.dateVerified.year)

       ad=str(info["agegroup_dict"]["adults"])
       a="Adults: "
       ad=str(a+ad)
       self.adl.set(ad)
       
       ch=str(info["agegroup_dict"]["children"])
       c="Children: "
       ch=c+ch
       self.chil.set(ch)
       
       sn=str(info["agegroup_dict"]["seniors"])
       s="Seniors: "
       sn=s+sn
       self.sen.set(sn)
       
       infa=str(info["agegroup_dict"]["infants"])
       i="Infants: "
       infa=i+infa
       self.inf.set(infa)
       
       tl=int(info["agegroup_dict"]["adults"])+\
           int(info["agegroup_dict"]["children"])+\
           int(info["agegroup_dict"]["seniors"])+\
           int(info["agegroup_dict"]["infants"])
       tl=str(tl)
       t='Total: '
       tl=t+tl
       self.tot.set(tl)
       
       self.dispad.grid(row=20,column=3, sticky=W)
       self.dischil.grid(row=20,column=4, sticky=W)
       self.dissen.grid(row=20,column=5, sticky=W)
       self.disinf.grid(row=20,column=6, sticky=W)
       self.distot.grid(row=20,column=7,sticky=W)
       
       return


    def displayVisitInfo(self, info, *args):
       """This function display the visit information for a client.
       """
       self.clearVisits() 
       visitor = info["visitor"]

       name = str(visitor.firstname)+ " " +str(visitor.lastname)
       self.visv.set(name)
       
       #visit info
       visits = info["visit_list"]

       vdatelabs = []
       vnlabs = []
       vvisitors = []
       vvols = []
       
       i=1
       for v in visits:
           d=str(v.date.month)+'/'+str(v.date.day)+'/'+str(v.date.year)
           n=v.notes
           vi=v.visitor
           vol=v.volunteer

           oneL = Label(self.gridframe,text=d,font=('Helvetica',10),
                        bg=self.bgcolor)
           oneL.grid(row=10+i,column=3)
           vdatelabs.append(oneL)
           
           twoL = Label(self.gridframe,text=n,font=('Helvetica',10),
                        bg=self.bgcolor)
           twoL.grid(row=10+i,column=4,columnspan=3)
           vnlabs.append(twoL)
           
           threeL = Label(self.gridframe,text=vi,font=('Helvetica',10),
                          bg=self.bgcolor)
           threeL.grid(row=10+i,column=7)
           vvisitors.append(threeL)
           
           fourL = Label(self.gridframe,text=vol,font=('Helvetica',10),
                         bg=self.bgcolor)
           fourL.grid(row=10+i,column=8)
           vvols.append(fourL)
           
           i+=1
           
       self.visitDict['dates'] = vdatelabs
       self.visitDict['notes'] = vnlabs
       self.visitDict['visitors'] = vvisitors
       self.visitDict['volunteers'] = vvols


    def displayHouseholdMem(self, info, *args):
       """This function displays the household information for a client.
       """ 
       self.family_listbox.delete(0,END)
       a=[]
       del self.mem_list[:]
       for member in info["member_list"]:
           self.mem_list.append(member.id)
           s=str(age(member.dob))
           q='Age: '
           s=q+s
           x=(member.firstname, member.lastname,s)
           a.append(x)

       for i in range(len(a)):
           self.family_listbox.insert(i,a[i])
       
       return


    def displayNewInfo(self, client_id):
       """This function displays the information for a specified
       client whose id is client_id.
       """
       cursel = client_id 
       info = select_client(cursel)
       self.updateClientDisplay()
       
       self.displayHouseholdMem(info)
       self.displayVisitInfo(info)
       self.displayClientInfo(info)
       self.displayHouseholdInfo(info)
       
       return
    
    def displayInfo(self, *args):
       """This function displays the information for a client that
       has been selected in the client_listbox.
       """
       self.cursel = int(self.id_list[self.client_listbox.curselection()[0]])
       info = select_client(self.cursel)
       self.updateClientDisplay()
       
       self.displayHouseholdMem(info)
       self.displayVisitInfo(info)
       self.displayClientInfo(info)
       self.displayHouseholdInfo(info)
       
       return

    def viewMember(self, mem_list):
       """This function displays the information for a client that
       has been selected in the family_listbox.
       """
       n = self.family_listbox.curselection()[0]
       self.cursel = mem_list[n]
       info = select_client(self.cursel)
       
       self.displayHouseholdMem(info)
       self.displayVisitInfo(info)
       self.displayClientInfo(info)
       self.displayHouseholdInfo(info)
       return

    def runViewMember(self):
       self.viewMember(self.mem_list)
       return

    def removeMember(self, tbd):
       remove_client(tbd)
       info = select_client(self.cursel)
       self.displayHouseholdMem(self, info)
       return

    def removeMemberConfirm(self):
       n = self.family_listbox.curselection()[0]
       tbd = self.mem_list[n]
       conf = messagebox.askquestion(
           title='Confirm Removal',
           message='Are you sure you want to delete this client?')
       
       if conf:
           remove_client(tbd)
           return
       else:
           return

    def configure_background(self, *args):
        """This function takes in a string and, if it matches a
        valid color, will set the color of the interface to
        the new color.
        """
        import tkinter.colorchooser as cc
        color = cc.askcolor()
        color_name = color[1]
        self.bgcolor = color_name
        #self.ciGui.update()
        
        #QUESTION: How do we save the color after the program is
        #closed?
        #
        #pass

if __name__ == '__main__':
    ao = allobjects()

"""
#lists of most variables
allvars = [ns, fnv, lnv, phv, mv, dv, yv, mob, agev, visdatev, notv, volv, visv,
              adv, apv, ctyv, stav, zpv, q, adl, chil, sen, inf, tot]
allents = [nameSearchEnt, fname, lname, phone, mob, dob, yob, visitdate, notescv, volun,
          visitor, address, aptn, city, state, zipc, famNum]
alllabs = [adultsLabel, childrenLabel, seniorsLabel, infantsLabel, totalLabel, housetitle,
          dispad, dischil, dissen, disinf, distot, addhhtitle, entNum, famfn, famln, famdob, famphone,
          fammon, famday, famyear]
allbut = [searchButton, addmemb, removmemb, viewmemb, newMembersB, newClientSave, cancelNewB, saveB,
           cancelB]
alllb = [client_listbox, family_listbox]
allsep = [houseSep, addhhsep]
allmenu = [menubar, optionsmenu, clientmenu]
"""







    