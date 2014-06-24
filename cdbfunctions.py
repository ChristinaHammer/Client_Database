"""cdbfunctions.py

Developer: Noelle Todd
Last Updated: June 24, 2014

This module consists of helper functions which will be called by another
module that will called directly by the user interface. This module is 
still in its early testing stages; many more functions will be added or
edited in the following weeks.

"""

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from cdbtabledef import Household, Person, Volunteer, Visit


#objects to hold data for function calls
class newClientData:
	def __init__(self, firstname, lastname, dob, phone=None,
				dateJoined=datetime.now()):
		self.firstname = str(firstname)
		self.lastname = str(lastname)
		self.dob = dob
		self.phone = str(phone)
		self.dateJoined = dateJoined

class oldClientData:
	def __init__(self, id, firstname, lastname, dob, phone=None,
				dateJoined=datetime.now()):
		self.id = id
		self.firstname = str(firstname)
		self.lastname = str(lastname)
		self.dob = dob
		self.phone = str(phone)
		self.dateJoined = dateJoined

class houseData:
	def __init__(self, street, city='Troy', state='NY', zip='12180', 
				dateVerified=None, apt=None):
		self.street = street
		self.city = city
		self.state = state
		self.zip = zip
		self.dateVerified = dateVerified
		self.apt = apt
		
class visitData:
	def __init__(self, Vol_ID, visitDate=datetime.now(), notes=None):
		self.Vol_ID = Vol_ID
		self.visitDate = visitDate
		self.notes = notes
		


#Functions for inserts
#Note: the argument 's' refers to the current session
def insert_household(s, street, dateverified=None, Apt=None, City='Troy',
					State='NY', Zip='12180'):
	"""This function creates a new row to hold a household's data. It returns
	the household id, which will be used when we insert household members.

	"""
	newhouse = Household(street_address=street, apt=Apt, city=City,
						  state=State, zip=Zip, 
						  date_verified=dateverified)
	s.add(newhouse)
	s.commit()
	return newhouse.id
			  
	
def insert_person(s, firstname, lastname, dob, datejoined, newhouse,
				phonenum=None):
	"""This function creates a new row to hold an individual's data. There is
	no return.
	
	"""
	newpers = Person(first_name=firstname, last_name=lastname,
					  DOB=dob, date_joined=datejoined, phone=phonenum)
	newpers.HH_ID = newhouse
	newpers.age = age(dob)
	s.add(newpers)
	s.commit()
	return newpers.id

	
def insert_volunteer(s, firstname, lastname, phonenum):
	"""This function creates a new row in the Volunteer table, to hold
	a volunteer's data.
	
	"""
	new_vol = Volunteer(first_name=firstname, last_name=lastname, 
						phone=phonenum)
	s.add(new_vol)
	s.commit()
	

def insert_visit(s, Vol_id, pers_id, house_id, date_of_visit=datetime.now(),
				notes=None):
	"""This function creates a new row in the Visit table to hold
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
	house.street = street
	house.city = city
	house.state = state
	house.zip = zip
	house.apt = apt
	house.date_verified = date_verified
	s.commit()
	
	
def update_person(s, I_ID, firstname, lastname, dob):
	"""This function will update a person's records.
	"""
	pers = s.query(Person).filter(Person.id == I_ID).one()
	pers.first_name = firstname
	pers.last_name = lastname
	pers.DOB = dob
	pers.age = age(dob)
	s.commit()
	

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
			
	agegroups = {'infants':infants, 'children':children, 'adults':adults,
				'seniors':seniors}	
	return agegroups
