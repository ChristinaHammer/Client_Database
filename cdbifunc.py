"""cdbifunc.py

Developer: Noelle Todd
Last Updated: June 18, 2014

This module holds all functions that will be called directly by the user
interface. This module uses several functions in cdbfunctions.py; the two
modules have been split to make designing the user interface as simple as
simple as possible.

"""

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from cdbtabledef import Household, Person, Volunteer, Visit
from cdbfunctions import *
from sqlafuntest import *

engine = create_engine('sqlite:///test_db.sqlite')
session = sessionmaker()
session.configure(bind=engine)

base = declarative_base()

s = session()

#Functions to connect to buttons
def quit_session():
	"""This function will close the session.
	"""
	s.close()
	
	
def cancel_changes():
	"""This function will rollback transactions & close session.
	"""
	s.rollback()
	s.close()
	
	
def reset(I_ID):
	"""	This function sends the original data back.
	"""
	info = select_client(I_ID)
	return info


def new_volunteer(s, firstname, lastname, phonenum=None):
	"""This function creates a new record for a volunteer.
	"""
	insert_volunteer(s, firstname, lastname, phonenum)
	
	
def new_client(Vol_ID, street, client_data_tuple_list, 
		dateJoined=datetime.now(), dateVerified=None,
		visitDate=datetime.now(), Apt=None,
		City='Troy', State='NY', Zip='12180', notes=None
		):
	"""Input:
	new_client(int Vol_ID, string street, 
			list[(string fname, string lname, date dob, int phone)],
			date dateJoined, date dateVerified, date visitDate, string Apt,
			string City, string State, int Zip, string Notes)
				
	This function creates a new person, household, and first visit.
	If the page viewed is for a new_client, then this connects to the SAVE
	button in the interface.
	
	For input, the function takes lists of strings for firstnames and 
	lastnames, a list of date objects for dobs, a list of integers for
	phonenums, strings for Apt, City, and State, and an integer for Zip.
	There is no return.
	
	"""
	
	#create new household
	newhouse = insert_household(s, street, dateVerified,
								Apt, City, State, Zip)
	
	#create new person for every household member
	data = client_data_tuple_list #variable renamed for simplicity	
	
	for i in range(0, len(data)):			
		fname = data[i][0]
		lname = data[i][1]
		dob = data[i][2]
		
		#check for phone number
		if len(data[i]) > 3: phone = data[i][3]
		else: phone = None
		pers = insert_person(s, fname, lname, dob, dateJoined, newhouse, phone)
		
		#the first person is the actual visitor; save for insert_visit
		if i == 0:
			s.commit()
			newpers = pers
	s.commit()
	
	#create new visit for household
	insert_visit(s, Vol_ID, newpers, newhouse, visitDate, notes)	
	s.commit()
	
	
#Function to retrieve all data for a client
def select_client(I_ID):
	"""This function returns all client data for a selected client.
	"""
	
	#find person and associated household
	pers = s.query(Person).filter(Person.id == I_ID).one()	
	house = s.query(Household).filter(Household.id == pers.HH_ID).one()
	
	info = [pers.id, pers.first_name, pers.last_name, pers.DOB, pers.age,
			pers.phone, pers.date_joined, house.street_address, house.apt,
			house.city, house.state, house.zip, house.date_verified]
			
	for member in house.members:
		info.append( (member.first_name, member.last_name, member.DOB, member.age) )

	agegroups = get_age_breakdown(house.members)
	info.append(agegroups)
	return info
	

#Function for drop-down, selection menu
def list_people():
	"""This function takes no arguments and returns a list of tuples.
	Each tuple contains a string for a person's full name, a string for
	the person's street_address, and an integer for the person's unique id.
	
	"""
	people = []
	
	#create a list of tuples, where each tuple contains a string holding a 
	#person's full-name, a string holding the person's street, and an integer
	#holding the person's unique id. The names are added in alphabetic (A-Z)
	#order.
	#
	for instance in s.query(Person).order_by(Person.last_name):
		h = s.query(Household).filter(Household.id == instance.HH_ID).one()
		fullname = instance.first_name + " " + instance.last_name
		people.append((fullname, h.street_address, instance.id))
		
	return people
	
