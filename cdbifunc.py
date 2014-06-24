"""cdbifunc.py

Developer: Noelle Todd
Last Updated: June 24, 2014

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
	
	
#formerly new_client function; renamed for clarity
def new_household(houseInfo, visitInfo, newClientInfo_list):
	"""This function takes an object for house info, an object for
	visit info, and a list of objects for client info (one object per
	client).
	
	This function creates a new record for each new person, a new record
	for the household, and new record for the a visit.
	
	"""
	#create new household
	newhouse = insert_household(s, houseInfo.street, houseInfo.dateVerified,
					houseInfo.apt, houseInfo.city,
					houseInfo.state, houseInfo.zip)
	
	#create new person for every household member
	data = newClientInfo_list #variable renamed for simplicity	
	
	for i in range(0, len(data)):			
		fname = data[i].firstname
		lname = data[i].lastname
		dob = data[i].dob
		phone = data[i].phone
		dateJoined = data[i].dateJoined
		
		pers = insert_person(s, data[i].firstname, data[i].lastname,
					data[i].dob, newhouse, data[i].dateJoined,
					data[i].phone)
		
		#the first person is the actual visitor; save for insert_visit
		if i == 0:
			newpers = pers
	
	#create new visit for household
	insert_visit(s, visitInfo.Vol_ID, newpers, newhouse, 
			visitInfo.visitDate, visitInfo.notes)	
				
				
def update_all(I_ID, houseInfo, visitInfo, oldClientInfo_list, 
		newClientInfo_list=None):
				
	pers = s.query(Person).filter(Person.id == I_ID).one()
	house = s.query(Household).filter(Household.id == pers.HH_ID).one()
	
	#update household
	update_household(s, house.id, houseInfo.street, houseInfo.city, 
			houseInfo.state, houseInfo.zip, houseInfo.apt,
			houseInfo.dateVerified)
	
	#add new clients (if they exist)
	data = newClientInfo_list #renamed for simplicity
	if data == None: pass
	else:
		for i in range(0, len(data)):
			newpers = insert_person(s, data[i].firstname, data[i].lastname,
						data[i].dob, house.id, 
						phonenum=data[i].phone)
	
	#update old clients
	old = oldClientInfo_list #renamed for simplicity
	for i in range(0, len(old)):
		update_person(s, old[i].id, old[i].firstname, old[i].lastname, 
				old[i].dob, old[i].phone)
		
	
	#create a new visit	
	insert_visit(s, visitInfo.Vol_ID, pers.id, house.id, visitInfo.visitDate,
			visitInfo.notes)
	
	
	
def update_all(Vol_ID, I_ID, street, client_data_tuple_list, 
		new_client_list=None, visitDate=datetime.now(),
		dateVerified = None, apt = None,	city = 'Troy',
		state = 'NY', zip = '12180', notes=None):
	"""Input:
	update_all(int Vol_ID, int I_ID, string street, 
		list[(int id, string fname, string lname, date dob, int phone)],
		list[string fname, string lname, data dob, int phone)],
		date visitDate, date dateVerified, string apt,
		string city, string state, int zip, string notes)
				
	This function will update a household and all members in the household,
	add any new members, and create a new visit record.
	"""
	pers = s.query(Person).filter(Person.id == I_ID).one()
	house = s.query(Household).filter(Household.id == pers.HH_ID).one()
	
	#update household
	update_household(s, house.id, street, city, state,
			zip, apt, dateVerified)
	
	#add new clients (if they exist)
	ncl = new_client_list #renamed for simplicity
	if ncl == None: pass
	else:
		for i in range(0, len(ncl)):
			fname = ncl[i][0]
			lname = ncl[i][1]
			dob = ncl[i][2]
			
			#check for phone number
			if len(ncl[i]) > 3: pho = ncl[i][3]
			else: pho = None
			newpers = insert_person(s, fname, lname, dob, house.id, phonenum=pho)
	
	#update old clients
	ctl = client_data_tuple_list #renamed for simplicity
	for i in range(0, len(ctl)):
		iid = ctl[i][0]
		fname = ctl[i][1]
		lname = ctl[i][2]
		dob = ctl[i][3]
		
		#check for phone number
		if len(ctl[i]) > 4: pho = ctl[i][4]
		else: pho = None
		update_person(s, iid, fname, lname, dob, phonenum=pho)
		
	
	#create a new visit	
	insert_visit(s, Vol_ID, pers.id, house.id, visitDate, notes)
	
	
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
	
