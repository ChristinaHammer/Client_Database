"""cdbfunctions.py

Developer: Noelle Todd
Last Updated: August 30, 2014

This module consists of functions which will be called by the user
interface, in order to insert, delete, update, etc. data in the database.
This module is still in its early testing stages; many more functions will
be added or edited in the following weeks.

"""
import sqlalchemy
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy import desc
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta, date
from cdbtabledef import Household, Person, Volunteer, Visit


class volunteerData:
        """This class is used for inserting/selecting a volunteer into/from
        the database.
        """
        def __init__(self, firstname, lastname, color, phone=None, active=True):
                self.firstname = str(firstname)
                self.lastname = str(lastname)
                self.color = color
                self.phone = str(phone)
                self.active = active

		
class newClientData:
	"""This class is used for inserting a new client into the
	database.
	"""
	def __init__(self, firstname, lastname, dob, phone=None,
				dateJoined=datetime.now()):
		self.firstname = str(firstname)
		self.lastname = str(lastname)
		self.dob = dob
		self.phone = str(phone)
		self.dateJoined = dateJoined

		
class oldClientData:
	"""This class is used for updating old clients and for 
	returning information for a client.
	"""
	def __init__(self, id, firstname, lastname, dob, phone=None,
				dateJoined=datetime.now()):
		self.id = id
		self.firstname = str(firstname)
		self.lastname = str(lastname)
		self.dob = dob
		self.age = age(dob)
		self.phone = str(phone)
		self.dateJoined = dateJoined

		
class houseData:
	"""This class is used to hold data for inserting a household,
	updating a household, or returning household information.
	"""
	def __init__(self, street, city='Troy', state='NY', zip='12180', 
				dateVerified=None, apt=None):
		self.street = street
		self.city = city
		self.state = state
		self.zip = zip
		self.dateVerified = dateVerified
		self.apt = apt
		
		
class visitData:
	"""This class is used to hold data for inserting a visit
	"""
	def __init__(self, Vol_ID, visitDate=datetime.now(), notes=None):
		self.Vol_ID = Vol_ID
		self.visitDate = visitDate
		self.notes = notes
		
		
class visitDataReturn:
	"""This class is used for returning data for the list_visits function.
	"""
	def __init__(self, visitDate, clientname, volname, notes=None,
                     vid=None):
		self.date = visitDate
		self.visitor = clientname
		self.volunteer = volname
		self.notes = notes
		self.visitID = vid
		

#functions for inserts	
def insert_household(s, street, dateverified=None, Apt=None, 
					City='Troy', State='NY', Zip='12180'):
	"""This function creates a new row to hold a household's data. It returns
	the household id, which will be used when we insert household members.

	"""
	newhouse = Household(street_address = street, apt = Apt, city = City,
						  state = State, zip = Zip, 
						  date_verified = dateverified)
	s.add(newhouse)
	s.commit()
	#return newhouse.id
	return newhouse
	
	
def insert_person(s, firstname, lastname, dob, newhouse, 
				datejoined=datetime.now(), phonenum=None):
	"""This function creates a new row to hold an individual's data. There is
	no return.
	
	"""
	newpers = Person(first_name=firstname, last_name=lastname, DOB=dob,
					date_joined=datejoined, phone=phonenum)
	newpers.HH_ID = newhouse
	newpers.age = age(dob)
	s.add(newpers)
	s.commit()
	#return newpers.id
	return newpers


def insert_volunteer(s, firstname, lastname, phonenum=None, active=True, color='light blue'):
	"""This function creates a new row in the Volunteer table, to hold
	a volunteer's data.
	
	"""
	new_vol = Volunteer(first_name=firstname, last_name=lastname, 
						phone=phonenum, active=active, color=color)
	s.add(new_vol)
	s.commit()
	
	
def insert_visit(s, Vol_id, pers_id, house_id, date_of_visit=datetime.now(),
				notes=None):
	"""This function creates a new row in the Visits table to hold
	the data for a visit.
	"""
	new_visit = Visit(I_ID=pers_id, HH_ID=house_id, Vol_ID=Vol_id,
					date=date_of_visit, visit_notes=notes)
	s.add(new_visit)
	s.commit()
	
	
#functions for updating records
def update_household(s, HH_ID, street, city, state, zip, apt=None,
					date_verified=None):
	"""This function will update a households records
	"""
	house = s.query(Household).filter(Household.id == HH_ID).one()
	house.street_address = street
	house.city = city
	house.state = state
	house.zip = zip
	house.apt = apt
	house.date_verified = date_verified
	s.commit()
	
	
def update_person(s, I_ID, firstname, lastname, dob, phonenum=None):
	"""This function will update a person's records.
	"""
	pers = s.query(Person).filter(Person.id == I_ID).one()
	pers.first_name = firstname
	pers.last_name = lastname
	pers.DOB = dob
	pers.phone = phonenum
	pers.age = age(dob)
	s.commit()


def update_visit(s, vis_id, date_of_visit=datetime.now(),
				notes=None):
        """This function will update a visit's record.
        """
        visit = s.query(Visit).filter(Visit.id == vis_id).one()
        visit.date = date_of_visit
        visit.visit_notes = notes
        s.commit()
                 
	
def update_volunteer(s, vol_id, firstname, lastname, phonenum, active, color):
	"""This function will update a volunteer's records.
	"""
	vol = s.query(Volunteer).filter(Volunteer.id == vol_id).one()
	vol.first_name = firstname
	vol.last_name = lastname
	vol.phone = phonenum
	vol.active = active
	vol.color = color
	s.commit()
	
	
#delete functions
def delete_household(s, HH_ID):
	"""This function deletes a household record from the database.	
	"""
	house = s.query(Household).filter(Household.id == HH_ID).one()
	s.delete(house)
	s.commit()
	
	
def delete_person(s, I_ID):
	"""This function will delete an individual from the database.
	"""
	pers = s.query(Person).filter(Person.id == I_ID).one()
	s.delete(pers)
	s.commit()

	
def delete_volunteer(s, Vol_ID):
	"""This function will delete a volunteer if the volunteer has
	not participated in a visit. Else, it will "deactivate" the 
	volunteer.
	
	"""
	vol = s.query(Volunteer).filter(Volunteer.id == Vol_ID).one()
	s.delete(vol)
	s.commit()
		
		
def delete_visit(s, Vi_ID):
	"""This function will delete a visit from the database.
	"""
	vis = s.query(Visit).filter(Visit.id == Vi_ID).one()
	s.delete(vis)
	s.commit()
	
	
#helper functions
def age(dob):
	"""This function calculates a person's age using the dob input to it.
	"""
	timey = datetime.now()
	if timey.month > dob.month:
		return timey.year - dob.year
	elif timey.month < dob.month:
		return timey.year - dob.year - 1
	else:
		if timey.day >= dob.day:
			return timey.year - dob.year
		else:
			return timey.year - dob.year - 1		


def list_visits(s, I_ID):
	"""This function will find the past visits for a household
	and return them as a list of visitDataReturn objects.
	"""
	visits = []
	pers = s.query(Person).filter(Person.id == I_ID).one()
	house = s.query(Household).filter(Household.id == pers.HH_ID).one()
	
	#returns all visits for the household in descending order of date
	visithistory = s.query(Visit, Person, Volunteer).\
						filter(Visit.HH_ID == house.id).\
						filter(Visit.I_ID == Person.id).\
						filter(Visit.Vol_ID == Volunteer.id).\
						order_by(desc(Visit.date)).all()
	
	#retrieves information for past three visits and returns in a list.
	for instance in visithistory:
		clientname = instance.Person.first_name + " " +\
						instance.Person.last_name
		volname = instance.Volunteer.first_name + " " +\
						instance.Volunteer.last_name
		visit = visitDataReturn(instance.Visit.date, clientname, volname, 
					notes=instance.Visit.visit_notes,
                                        vid=instance.Visit.id)
		visits.append(visit)
						
	return visits
	

def get_age_breakdown(members):
	"""This function will retrieve all the ages of the members, and return the
	number of adults, seniors, children, and infants accordingly.
	
	"""	
	infants = 0
	children = 0
	adults = 0
	seniors = 0
	
	for member in members:
		if member.age < 2:
			infants = infants + 1
		elif member.age >= 2 and member.age < 18:
			children = children + 1
		elif member.age >= 18 and member.age < 65:
			adults = adults + 1
		else:
			seniors = seniors + 1
			
	total = infants + children + adults + seniors
	
	agegroups = {'infants':infants, 'children':children, 'adults':adults,
				'seniors':seniors, 'total':total}	
	return agegroups

	
def generate_report(s, duration):
	"""This function will generate a csv/excel file that holds all
	relevant info for a monthly report. 
	
	First name, Last name (of visitor only)
	City of household
	#of children, seniors, adults, and infants
	total number of each of the above
	total number of households
	total number of people served
	"""
	
	import csv
	
	#open file and so on
	today = datetime.now()
	filename = str(today.month)+ "-" + str(today.day) + "-" + str(today.year) +\
                   "-report.csv"
	csvfile = open(filename, 'w', newline='')	
	outcsv = csv.writer(csvfile)     
	
	#calculate a month ago
	today = datetime.now()
	#duration = timedelta(days=31)
	month_ago = today - duration
	
	#convert date objects to strings for comparison purposes
	month_ago = str(month_ago)
	
	#one giant massive query
	select = sqlalchemy.sql.select([Person.first_name, Person.last_name,
									Household.seniors, Household.adults,
									Household.children, Household.infants,
									Household.city, Visit.date])\
							.where(Visit.I_ID == Person.id)\
							.where(Visit.HH_ID == Household.id)\
							.where(Visit.date >= month_ago)
	records = s.execute(select)
	outcsv.writerow(records.keys())
	outcsv.writerows(records)
	
	csvfile.close()
	s.close()
