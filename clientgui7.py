#christina Hammer
#client info page
#updates July 18th, very much in progress

#v6, compatible with cdbtfunc and cdbtfunctions from July 3rd, 2014

from datetime import datetime, timedelta, date
from tkinter import *
from tkinter import ttk
from cdbifunc import *


def familyEntryBoxes(*args):

    n=int(q.get())
    
    famfn.grid(row=24,column=3)
    famln.grid(row=24,column=4)
    famdob.grid(row=24,column=5)
    famphone.grid(row=24,column=8)
    fammon.grid(row=25,column=5,sticky=S)
    famday.grid(row=25,column=6,sticky=S)
    famyear.grid(row=25,column=7,sticky=S)
    
    for i in range(n):
        
        Entry(gridframe).grid(row=26+i, column=3)
        Entry(gridframe).grid(row=26+i, column=4)
        Entry(gridframe, width=8).grid(row=26+i, column=5)
        Entry(gridframe, width=8).grid(row=26+i, column=6)
        Entry(gridframe, width=8).grid(row=26+i, column=7)
        Entry(gridframe).grid(row=26+i, column=8)

    ##need to figure out how to get data from spawned entry boxes
    return
    
def newClientDisplay(*args):

    ##new client

    newFirst.grid(row=2, column=4,sticky=W)
    newLast.grid(row=2,column=6,sticky=W)
    newPhone.grid(row=2, column=8,sticky=W)
    newMob.grid(row=4,column=4,sticky=W)
    newDob.grid(row=4,column=5,sticky=W)
    newYob.grid(row=4,column=6,sticky=W)

    ##first visit info

    firstVisitDate.grid(row=9, column=3)
    firstNotes.grid(row=9, column=4, columnspan=3)
    firstVolun.grid(row=9, column=7,sticky=W)
    firstVisitor.grid(row=9, column=8)

    ##new household info

    newAddress.grid(row=16, column=4,columnspan=2)
    newAptn.grid(row=16,column=7)
    newCity.grid(row=16,column=9,sticky=W) 
    newState.grid(row=18,column=4)
    newZipc.grid(row=18, column=6)

    addhhsep.grid(row=20,column=3,columnspan=40,sticky=EW)
    addhhtitle.grid(row=20,column=3,columnspan=12, sticky=W)

    
    Label(gridframe, text='   ',font=('Helvetica',10),bg='LemonChiffon2').grid(row=21,column=3,sticky=E)

    ##temporarily remove display
    adultsLabel.grid_forget()
    childrenLabel.grid_forget()
    seniorsLabel.grid_forget()
    infantsLabel.grid_forget()
    totalLabel.grid_forget()
    family_listbox.grid_forget()
    addmemb.grid_forget()
    removmemb.grid_forget()
    viewmemb.grid_forget()
    housetitle.grid_forget()
    houseSep.grid_forget()
    saveB.grid_forget()
    cancelB.grid_forget()
    dispad.grid_forget()
    dischil.grid_forget()
    dissen.grid_forget()
    disinf.grid_forget()
    distot.grid_forget()

    ##enter family members
    famNum.grid(row=22, column=4)
    
    entNum.grid(row=22, column=3)

    newMembersB.grid(row=22, column=5)
    
    newClientSave.grid(row=40,column=3, columnspan=2)
    cancelNewB.grid(row=40, column=5, columnspan=2)

    return

def clearToMain():

    newFirst.grid_forget()
    newLast.grid_forget()
    newPhone.grid_forget()
    newMob.grid_forget()
    newDob.grid_forget()
    newYob.grid_forget()
    firstVisitDate.grid_forget()
    firstNotes.grid_forget()
    firstVolun.grid_forget()
    firstVisitor.grid_forget()
    newAddress.grid_forget()
    newAptn.grid_forget()
    newCity.grid_forget()
    newState.grid_forget()
    newZipc.grid_forget()
    famNum.grid_forget()
    entNum.grid_forget()
    newMembersB.grid_forget()
    newClientSave.grid_forget()
    cancelNewB.grid_forget()
    famfn.grid_forget()
    famln.grid_forget()
    famdob.grid_forget()
    famphone.grid_forget()
    fammon.grid_forget()
    famday.grid_forget()
    famyear.grid_forget()
    addhhsep.grid_forget()
    addhhtitle.grid_forget()
    
    #####add back
    adultsLabel.grid(row=20,column=3,sticky=W)
    childrenLabel.grid(row=20,column=4,sticky=W)
    seniorsLabel.grid(row=20,column=5,sticky=W)
    infantsLabel.grid(row=20,column=6,sticky=W)
    totalLabel.grid(row=20,column=7,sticky=W)
    family_listbox.grid(row=26, column=3,rowspan=4,columnspan=3) 
    addmemb.grid(row=26,column=7)
    removmemb.grid(row=27,column=7)
    viewmemb.grid(row=28,column=7)
    housetitle.grid(row=24,column=3,columnspan=12, sticky=W)
    houseSep.grid(row=24,column=3,columnspan=40,sticky=EW)
    saveB.grid(row=33, column=3, columnspan=2)
    cancelB.grid(row=33, column=5, columnspan=2)
    
    return

def addNew():
	"""This function adds a new household to the database.
	#NOTE: lots of error testing/resetting still to be done.
	"""
	
	#adds visitor's information
	try:
		fname = str(nfnv.get())
		lname = str(nlnv.get())
		dy = int(nyv.get())
		dm = int(nmv.get())
		dd = int(ndv.get())
		#IMPLEMENT get phone = str(phone.get()) and test
		#IMPLEMENT get dateJoined, and test
		ncd1 = newClientData(firstname=fname, lastname=lname,
							dob=date(year=dy, month=dm, day=dd))
							#phone=phone, dateJoined=datetime.now())
		newClientInfo_list = [ncd1]
							
	except ValueError:
		#IMPLEMENT POP-UP ERROR MESSAGE
		print("Oops! Did you forget your name or birthday?")
		
		
	#Creates household object
	try:
		streeta = str(nadv.get())
		citya = str(ctyv.get())
		statea = str(nstav.get())
		zipa = int(nzpv.get())
		apta = str(napv.get())
		#IMPLEMENT get dateVerified
		houseInfo = houseData(street=streeta, city=citya, state=statea, zip=zipa, apt=apta)
	
	except ValueError:
		#IMPLEMENT POP-UP ERROR WINDOW
		print("Oops! Did you forget where you live?")
		
		
	#adds visit information
	try:
		#IMPLEMENT get volunteer id
		#IMPLEMENT get visit date, test, set to default, etc.
		vnote = str(nnotv.get())
		visitInfo = visitData(Vol_ID=1, visitDate=datetime.now(), notes=vnote)
   	
	except ValueError:
		#IMPLEMENT POP UP ERROR WINDOW
		print("Oops! Did you forget when you visited?")

    #send all objects to new_household function
    #(houseInfo, visitInfo, newClientInfo_list)
	new_household(houseInfo, visitInfo, newClientInfo_list)
	clearToMain()

    return
	

	
def quitprogram():
    quit_session()
    ciGui.destroy()
    return

def logoff():
    import logGui
    ciGui.destory()
    return

def monthlyReport(*args):
    generate_monthly_report()
    return

def yearlyReport(*args):
    generate_yearly_report()
    return
    
def updateInfo(*args):

    #(self, Vol_ID, visitDate=datetime.now(), notes=None)
    print (notv.get())
    try:
        vol_id = int(volv.get())
        vdate = datetime.now()
        note = str(notv.get())
        visitInfo = visitData(vol_id, visitDate=vdate, notes=note)
        #visitInfo = visitData(volv.get(), visitDate=datetime.now(),notes=notv.get())
    except ValueError:
        print("ooops!")

    #(self, id, firstname, lastname, dob, phone=None, dateJoined=datetime.now())
    cd= oldClientData(int(cl_id.get()), fnv.get(), lnv.get(), date(int(yv.get()), int(mv.get()), int(dv.get())),phone=phv.get())
    
    ClientInfo_list = [cd]
    
    #(self, street, city='Troy', state='NY', zip='12180',dateVerified=None, apt=None)
    houseInfo = houseData(adv.get(),city=ctyv.get(),state=stav.get(), zip=zpv.get(),apt=apv.get())
    
    #(I_ID, houseInfo, visitInfo, oldClientInfo_list,newClientInfo_list=None)
    update_all(cl_id.get(), houseInfo, visitInfo, ClientInfo_list)
    print ('Changes have been saved!')
    return



def displayClientInfo(*args):
    clearToMain()
    
    client_id=cl_id.get()
    client_id=int(client_id)
    info = select_client(client_id)
    visitor = info["visitor"]
    print (info)
    
    
    fnv.set(visitor.firstname)
    lnv.set(visitor.lastname)
    
    mv.set(visitor.dob.month)
    dv.set(visitor.dob.day)
    yv.set(visitor.dob.year)
    agev.set(age(visitor.dob))
    phv.set(visitor.phone)
    
    return

def displayHouseholdInfo(*args):
    client_id=cl_id.get()
    client_id=int(client_id)
    info = select_client(client_id)
    
    house = info["household"]
    adv.set(house.street)
    apv.set(house.apt)
    ctyv.set(house.city)
    stav.set(house.state)
    zpv.set(house.zip)

    ad=str(info["agegroup_dict"]["adults"])
    a="Adults: "
    ad=str(a+ad)
    adl.set(ad)
    
    ch=str(info["agegroup_dict"]["children"])
    c="Children: "
    ch=c+ch
    chil.set(ch)
    
    sn=str(info["agegroup_dict"]["seniors"])
    s="Seniors: "
    sn=s+sn
    sen.set(sn)
    
    infa=str(info["agegroup_dict"]["infants"])
    i="Infants: "
    infa=i+infa
    inf.set(infa)
    
    tl=int(info["agegroup_dict"]["adults"])+int(info["agegroup_dict"]["children"])+int(info["agegroup_dict"]["seniors"])+int(info["agegroup_dict"]["infants"])
    tl=str(tl)
    t='Total: '
    tl=t+tl
    tot.set(tl)
    
    dispad.grid(row=20,column=3, sticky=W)
    dischil.grid(row=20,column=4, sticky=W)
    dissen.grid(row=20,column=5, sticky=W)
    disinf.grid(row=20,column=6, sticky=W)
    distot.grid(row=20,column=7,sticky=W)
    
    return

def displayVisitInfo(*args):
	"""This function will display all visit information
	"""
	#IMPLEMENT SELECTION FUNCTION THING
	#Would return the client's id.
	
    client_id=cl_id.get()
    client_id=int(client_id)
    info = select_client(client_id)
	
    visitor = info["visitor"]

    #name=str(visitor.firstname)+str(visitor.lastname)
    visdatev.set(date.today())
    visv.set(visitor.firstname)
    
    #visit info
    visits=info["visit_list"]
	
	for v in visits:
        d=v.date
        n=v.notes
        vi=v.visitor
        vol=v.volunteer

        Label(gridframe,text=d,font=('Helvetica',10),bg='LemonChiffon2').grid(row=10+i,column=3)
        Label(gridframe,text=n,font=('Helvetica',10),bg='LemonChiffon2').grid(row=10+i,column=4,columnspan=3)
        Label(gridframe,text=vi,font=('Helvetica',10),bg='LemonChiffon2').grid(row=10+i,column=7)
        Label(gridframe,text=vol,font=('Helvetica',10),bg='LemonChiffon2').grid(row=10+i,column=8)
	
		
    """
    if len(visits) >= 3:    
        #list of visits is already in reverse order, yo    
        tol=visits[0]
        sol=visits[1]
        lv=visits[2]

        d1=lv.date
        d2=sol.date
        d3=tol.date
        
        n1=lv.notes
        n2=sol.notes
        n3=tol.notes
        
        vi1=lv.visitor
        vi2=sol.visitor
        vi3=tol.visitor
        
        vol1=lv.volunteer
        vol2=sol.volunteer
        vol3=tol.volunteer

        #Dates
        Label(gridframe,text=d1,font=('Helvetica',10),bg='LemonChiffon2').grid(row=10,column=3)
        Label(gridframe,text=d2,font=('Helvetica',10),bg='LemonChiffon2').grid(row=11,column=3)
        Label(gridframe,text=d3,font=('Helvetica',10),bg='LemonChiffon2').grid(row=12,column=3)
        #Notes
        Label(gridframe,text=n1,font=('Helvetica',10),bg='LemonChiffon2').grid(row=10,column=4,columnspan=3)
        Label(gridframe,text=n2,font=('Helvetica',10),bg='LemonChiffon2').grid(row=11,column=4,columnspan=3)
        Label(gridframe,text=n3,font=('Helvetica',10),bg='LemonChiffon2').grid(row=12,column=4,columnspan=3)
        #Visitors
        Label(gridframe,text=vi1,font=('Helvetica',10),bg='LemonChiffon2').grid(row=10,column=7)
        Label(gridframe,text=vi2,font=('Helvetica',10),bg='LemonChiffon2').grid(row=11,column=7)
        Label(gridframe,text=vi3,font=('Helvetica',10),bg='LemonChiffon2').grid(row=12,column=7)
        #Volunteers
        Label(gridframe,text=vol1,font=('Helvetica',10),bg='LemonChiffon2').grid(row=10,column=8)
        Label(gridframe,text=vol2,font=('Helvetica',10),bg='LemonChiffon2').grid(row=11,column=8)
        Label(gridframe,text=vol3,font=('Helvetica',10),bg='LemonChiffon2').grid(row=12,column=8)
        
        return
    
    elif 0<len(visits)<3:
        
        for v in visits:
            d=v.date
            n=v.notes
            vi=v.visitor
            vol=v.volunteer

            Label(gridframe,text=d,font=('Helvetica',10),bg='LemonChiffon2').grid(row=10+i,column=3)
            Label(gridframe,text=n,font=('Helvetica',10),bg='LemonChiffon2').grid(row=10+i,column=4,columnspan=3)
            Label(gridframe,text=vi,font=('Helvetica',10),bg='LemonChiffon2').grid(row=10+i,column=7)
            Label(gridframe,text=vol,font=('Helvetica',10),bg='LemonChiffon2').grid(row=10+i,column=8)

            return
	"""
        
def displayHouseholdMem(*args):

    client_id=cl_id.get()
    info=select_client(client_id)
    family_listbox.delete(0,END)
    a=[]
    
    for member in info["member_list"]:
        s=str(age(member.dob))
        q='Age: '
        s=q+s
        x=(member.firstname, member.lastname,s)
        a.append(x)

    for i in range(len(a)):
        family_listbox.insert(i,a[i])

    return
        
def displayInfo(*args):
    
    displayHouseholdMem()
    displayVisitInfo()
    displayClientInfo()
    displayHouseholdInfo()
    
    
    
    return

def clientIDSelection(*args):
    
    cl_id.set(client_listbox.curselection())
    return
    
ciGui=Tk()

ciGui.geometry('1400x1100')

ciGui.configure(background='LemonChiffon2')

ciGui.title('Client Information')

gridframe=Frame(ciGui).grid()


####################Client Search#####################################

Label(gridframe,text='Client Search', font=("Helvetica", 16),fg='white',bg='PaleGreen4').grid(row=0,column=0,columnspan=2, sticky=W)

c=list_people()


#listing just the names and addresses of the people
x=[]
for i in range(len(c)):
    a=(c[i][0],c[i][1])
    x.append(a)

Label(gridframe, text='     ',font=('Helvetica',10),bg='LemonChiffon2').grid(row=0,column=2,sticky=E)

client_listbox= Listbox(gridframe,height=10,width=40)
for i in range(len(x)):
    client_listbox.insert(i,x[i])
    
client_listbox.grid(row=2, column=0,rowspan=5,columnspan=2)    

   
ttk.Separator(gridframe, orient='vertical').grid(row=1,column=2,rowspan=40,sticky=NS)

cl_id=IntVar()
cl_ident=Entry(gridframe,textvariable=cl_id)
cl_ident.grid(row=9,column=0)

Button(gridframe, text='Select Client', command=displayInfo).grid(row=9, column=1)

Button(gridframe, text='New Client', command=newClientDisplay).grid(row=11, column=0)

####################Client Search#####################################

ttk.Separator(gridframe, orient='horizontal').grid(row=0,column=3,columnspan=40,sticky=EW)
Label(gridframe,text='Client Information', font=("Helvetica", 16),fg='white',bg='PaleGreen4').grid(row=0,column=3,columnspan=12, sticky=W)
Label(gridframe, text='   ',font=('Helvetica',10),bg='LemonChiffon2').grid(row=1,column=3,sticky=E)

fnv=StringVar()
Label(gridframe, text="First Name: ",font=('Helvetica',12),bg='LemonChiffon2').grid(row=2, column=3,sticky=E)
fname = Entry(gridframe,textvariable=fnv,bd=4)
fname.grid(row=2, column=4,sticky=W)

lnv=StringVar()
Label(gridframe, text='Last Name: ',font=('Helvetica',12),bg='LemonChiffon2').grid(row=2,column=5,sticky=W)
lname=Entry(gridframe,textvariable=lnv,bd=4)
lname.grid(row=2,column=6,sticky=W)

phv=StringVar()
Label(gridframe, text='Phone: ',font=('Helvetica',12),bg='LemonChiffon2').grid(row=2, column=7,sticky=W)
phone=Entry(gridframe,textvariable=phv,bd=4)
phone.grid(row=2, column=8,sticky=W)

mv=StringVar()
dv=StringVar()
yv=StringVar()

Label(gridframe, text='Date of Birth: ',font=('Helvetica',12),bg='LemonChiffon2').grid(row=4,column=3,sticky=E)

mob=Entry(gridframe,textvariable=mv,width=8,bd=4)
mob.grid(row=4,column=4,sticky=W)

Label(gridframe,text='mm',font=('Helvetica',10),bg='LemonChiffon2').grid(row=3,column=4,sticky=SW)

dob=Entry(gridframe,textvariable=dv,width=8,bd=4)
dob.grid(row=4,column=5,sticky=W)
Label(gridframe,text='dd',font=('Helvetica',10),bg='LemonChiffon2').grid(row=3,column=5,sticky=SW)


yob=Entry(gridframe,textvariable=yv,width=8,bd=4)
yob.grid(row=4,column=6,sticky=W)
Label(gridframe,text='yyyy',font=('Helvetica',10),bg='LemonChiffon2').grid(row=3,column=6,sticky=SW)


agev=StringVar()
Label(gridframe, text='Age: ',font=('Helvetica',12),bg='LemonChiffon2').grid(row=4,column=7,sticky=E)
Label(gridframe, textvariable=agev,font=('Helvetica',12),bg='LemonChiffon2').grid(row=4,column=8,sticky=W)

Label(gridframe, text='   ',font=('Helvetica',10),bg='LemonChiffon2').grid(row=5,column=3,sticky=E)

####################Visit Info#####################################

ttk.Separator(gridframe, orient='horizontal').grid(row=6,column=3,columnspan=40,sticky=EW)
Label(gridframe,text='Visit Information', font=("Helvetica", 16),fg='white', bg='PaleGreen4').grid(row=6,column=3,columnspan=12, sticky=W)
Label(gridframe, text='   ',font=('Helvetica',10),bg='LemonChiffon2').grid(row=7,column=3,sticky=E)

Label(gridframe, text='Date: ',font=('Helvetica',14),bg='LemonChiffon2').grid(row=8,column=3)
Label(gridframe, text='Notes:',font=('Helvetica',14),bg='LemonChiffon2').grid(row=8,column=4)
Label(gridframe, text='Visitor: ',font=('Helvetica',14),bg='LemonChiffon2').grid(row=8,column=7)
Label(gridframe, text='Volunteer: ',font=('Helvetica',14),bg='LemonChiffon2').grid(row=8, column=8, sticky=W)
Label(gridframe, text='   ',font=('Helvetica',10),bg='LemonChiffon2').grid(row=23,column=0,sticky=E)

visdatev=StringVar()
visitdate=Entry(gridframe,textvariable=visdatev,bd=4)
visitdate.grid(row=9, column=3)

notv=StringVar()
notescv=Entry(gridframe, textvariable=notv,width=60,bd=4)
notescv.grid(row=9, column=4, columnspan=3)

volv=IntVar()
volun=Entry(gridframe,textvariable=volv,bd=4)
volun.grid(row=9, column=7,sticky=W)

visv=StringVar()
visitor=Entry(gridframe,textvariable=visv,width=8,bd=4)
visitor.grid(row=9, column=8)


Label(gridframe, text='   ',font=('Helvetica',10),bg='LemonChiffon2').grid(row=13,column=3,sticky=E)

####################Household Info#####################################

ttk.Separator(gridframe, orient='horizontal').grid(row=14,column=3,columnspan=40,sticky=EW)
Label(gridframe,text='Household Information', font=("Helvetica", 16),fg='white', bg='paleGreen4').grid(row=14,column=3,columnspan=12, sticky=W)
Label(gridframe, text='   ',font=('Helvetica',10),bg='LemonChiffon2').grid(row=15,column=3,sticky=E)

adv=StringVar()
Label(gridframe, text='Address: ',font=('Helvetica',12),bg='LemonChiffon2').grid(row=16,column=3,sticky=E)
address=Entry(gridframe,textvariable=adv,width=40,bd=4)
address.grid(row=16, column=4,columnspan=2)


apv=StringVar()
Label(gridframe, text='Apt: ',font=('Helvetica',12),bg='LemonChiffon2').grid(row=16,column=6,sticky=E)
aptn=Entry(gridframe,textvariable=apv,width=10,bd=4)
aptn.grid(row=16,column=7)

ctyv=StringVar()
Label(gridframe, text='City: ',font=('Helvetica',12),bg='LemonChiffon2').grid(row=16,column=8,sticky=W)
city=Entry(gridframe,textvariable=ctyv,bd=4)
city.grid(row=16,column=9,sticky=W)
Label(gridframe, text='   ',font=('Helvetica',12),bg='LemonChiffon2').grid(row=17,column=3,sticky=E)

stav=StringVar()
Label(gridframe, text='State: ',font=('Helvetica',12),bg='LemonChiffon2').grid(row=18,column=3,sticky=E)
state=Entry(gridframe,textvariable=stav,bd=4)
state.grid(row=18,column=4)

zpv=StringVar()
Label(gridframe, text='Zip Code: ',font=('Helvetica',12),bg='LemonChiffon2').grid(row=18,column=5,sticky=E)
zipc=Entry(gridframe,textvariable=zpv,bd=4)
zipc.grid(row=18, column=6)

Label(gridframe, text='   ',font=('Helvetica',12),bg='LemonChiffon2').grid(row=19,column=3,sticky=E)

adultsLabel=Label(gridframe, text='Adults: ',bg='LemonChiffon2',font=('Helvetica',12))
adultsLabel.grid(row=20,column=3,sticky=W)

childrenLabel=Label(gridframe, text='Children: ',bg='LemonChiffon2',font=('Helvetica',12))
childrenLabel.grid(row=20,column=4,sticky=W)

seniorsLabel=Label(gridframe, text='Seniors: ',bg='LemonChiffon2',font=('Helvetica',12))
seniorsLabel.grid(row=20,column=5,sticky=W)

infantsLabel=Label(gridframe, text='Infants: ',bg='LemonChiffon2',font=('Helvetica',12))
infantsLabel.grid(row=20,column=6,sticky=W)

totalLabel=Label(gridframe, text='Total: ',bg='LemonChiffon2',font=('Helvetica',12))
totalLabel.grid(row=20,column=7,sticky=W)

Label(gridframe, text='   ',font=('Helvetica',12),bg='LemonChiffon2').grid(row=23,column=3,sticky=E)



####################Household Members#####################################


houseSep=ttk.Separator(gridframe, orient='horizontal')
houseSep.grid(row=24,column=3,columnspan=40,sticky=EW)
housetitle=Label(gridframe,text='Household Members', font=("Helvetica", 16),fg='white',bg='PaleGreen4')
housetitle.grid(row=24,column=3,columnspan=12, sticky=W)
Label(gridframe, text='   ',font=('Helvetica',10),bg='LemonChiffon2').grid(row=25,column=3,sticky=E)

q=IntVar()
famNum=Entry(gridframe, textvariable=q)    
#Label(gridframe,text='select a family member to remove them, edit them, or view their full information',bg='PaleGreen3').grid(row=26, column=3, columnspan=4,sticky=W)

family_listbox= Listbox(gridframe,height=5,width=60,font=12)


family_listbox.grid(row=26, column=3,rowspan=4,columnspan=3) 

#Label(gridframe, text=' ',font=('Helvetica',12),bg='PaleGreen3').grid(row=28,column=3)
addmemb=Button(gridframe, text='Add Member')
addmemb.grid(row=26,column=7)
removmemb=Button(gridframe, text='Remove Member')
removmemb.grid(row=27,column=7)
viewmemb=Button(gridframe, text='View Member')
viewmemb.grid(row=28,column=7)
menubar=Menu(ciGui)

Label(gridframe, text='   ',font=('Helvetica',10),bg='LemonChiffon2').grid(row=30,column=3,sticky=E)
ttk.Separator(gridframe, orient='horizontal').grid(row=31,column=3,columnspan=40,sticky=EW)

Label(gridframe, text='   ',font=('Helvetica',10),bg='LemonChiffon2').grid(row=32,column=3,sticky=E)
####################Info Display Widgets#####################################

adl=StringVar()
dispad=Label(gridframe,textvariable=adl,font=('Helvetica',12),bg='LemonChiffon2')
chil=StringVar()
dischil=Label(gridframe,textvariable=chil,font=('Helvetica',12),bg='LemonChiffon2')
sen=StringVar()
dissen=Label(gridframe,textvariable=sen,font=('Helvetica',12),bg='LemonChiffon2')
inf=StringVar()
disinf=Label(gridframe,textvariable=inf,font=('Helvetica',12),bg='LemonChiffon2')
tot=StringVar()
distot=Label(gridframe, textvariable=tot,bg='LemonChiffon2',font=('Helvetica',12))


####################New Client Display Widgets#####################################


##new client
nfnv=StringVar()
newFirst = Entry(gridframe,textvariable=nfnv,bd=4)

nlnv=StringVar()
newLast=Entry(gridframe,textvariable=nlnv,bd=4)


nphv=StringVar()
newPhone=Entry(gridframe,textvariable=nphv,bd=4)

nmv=StringVar()
ndv=StringVar()
nyv=StringVar()

newMob=Entry(gridframe,textvariable=nmv,width=8,bd=4)
newDob=Entry(gridframe,textvariable=ndv,width=8,bd=4)
newYob=Entry(gridframe,textvariable=nyv,width=8,bd=4)



##first visit info

nvisdatev=StringVar()
firstVisitDate=Entry(gridframe,textvariable=visdatev,bd=4)


nnotv=StringVar()
firstNotes=Entry(gridframe, textvariable=notv,width=60,bd=4)


nvolv=StringVar()
firstVolun=Entry(gridframe,textvariable=volv,bd=4)


visv=StringVar()
firstVisitor=Entry(gridframe,textvariable=visv,width=8,bd=4)


##new household info

nadv=StringVar()
newAddress=Entry(gridframe,textvariable=nadv,width=40,bd=4)

napv=StringVar()
newAptn=Entry(gridframe,textvariable=napv,width=10,bd=4)


nctyv=StringVar()
newCity=Entry(gridframe,textvariable=nctyv,bd=4)

nstav=StringVar()
newState=Entry(gridframe,textvariable=nstav,bd=4)


nzpv=StringVar()
newZipc=Entry(gridframe,textvariable=nzpv,bd=4)

##new family members
addhhsep=ttk.Separator(gridframe, orient='horizontal')
addhhtitle=Label(gridframe,text='Add Household Members', font=("Helvetica", 16),fg='white',bg='PaleGreen4')


entNum=Label(gridframe, text='Enter Number of Family Members: ',font=('Helvetica',10),bg='LemonChiffon2')

famfn=Label(gridframe, text='First Name:',font=('Helvetica',10),bg='LemonChiffon2')
famln=Label(gridframe, text='Last Name:',font=('Helvetica',10),bg='LemonChiffon2')
famdob=Label(gridframe, text='Date of Birth:',font=('Helvetica',10),bg='LemonChiffon2')
famphone=Label(gridframe, text='Phone',font=('Helvetica',10),bg='LemonChiffon2')
fammon=Label(gridframe,text='mm',font=('Helvetica',10),bg='LemonChiffon2')
famday=Label(gridframe,text='dd',font=('Helvetica',10),bg='LemonChiffon2')
famyear=Label(gridframe,text='yyyy',font=('Helvetica',10),bg='LemonChiffon2')
    
newMembersB=Button(gridframe, text='Add Memebers',command=familyEntryBoxes)
newClientSave=Button(gridframe, text='Save Client', command=addNew)
cancelNewB=Button(gridframe, text='Cancel New Entry', command=clearToMain)

####################Menu#####################################
saveB=Button(gridframe, text='Save Changes',command=updateInfo,width=20)
saveB.grid(row=33, column=3, columnspan=2)

cancelB=Button(gridframe, text='Cancel Changes',command=displayInfo,width=20)
cancelB.grid(row=33, column=5, columnspan=2)
##^Essentially re-selects client

optionsmenu=Menu(menubar,tearoff=0)
optionsmenu.add_command(label='Quit', command=quitprogram)
optionsmenu.add_command(label='log off', command=logoff)
optionsmenu.add_command(label='Account Settings')
menubar.add_cascade(label='Options',menu=optionsmenu)
clientmenu=Menu(menubar,tearoff=0)

clientmenu.add_command(label='Add New Client', command=addNew)
clientmenu.add_command(label='View Monthly Report',command=monthlyReport)
clientmenu.add_command(label='View Yearly',command=yearlyReport)
menubar.add_cascade(label='Clients',menu=clientmenu)

ciGui.config(menu=menubar)

ciGui.mainloop()
