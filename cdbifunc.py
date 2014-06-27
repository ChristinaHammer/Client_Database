"""cdbifunc.py

Developer: Noelle Todd
Last Updated: June 26, 2014

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
	
#Function to retrieve all data for a client
#Two versions of this function are in this module until it is determined which one
#is the most consistent and easy to use.
#

#Version 1:

def select_client(I_ID):
	"""This function returns all client data for a selected client.
	"""
	
	#find person and associated household
	pers = s.query(Person).filter(Person.id == I_ID).one()	
	house = s.query(Household).filter(Household.id == pers.HH_ID).one()
	
	#update person's age in database
	pers.age = age(pers.DOB)
	s.commit()
	
	#create list of all info, listing the individual's info in a tuple in 
	#the first position.
	#
	info = [(pers.id, pers.first_name, pers.last_name, pers.DOB, pers.age,
			pers.phone), pers.date_joined, house.street_address, house.apt,
			house.city, house.state, house.zip, house.date_verified]
	
	#append all other members' info, where each member has its own tuple,
	#to the end of the list.
	#
	for member in house.members:
		if member.first_name == pers.first_name: pass
		else:
			#update member's age in database
			member.age = age(member.DOB)
			s.commit()
			#add member's data to list
			info.append((member.id, member.first_name, member.last_name,
						member.DOB, member.age, member.phone))
	
	#append the age dictionary to the end of the list
	agegroups = get_age_breakdown(house.members)
	info.append(agegroups)
	
	visits = list_visits(s, I_ID)
	info.append(visits)
	
	return info


"""
#Version 2:
def select_client(I_ID):
	#This a dictionary of objects containing all data for a selected
	#client.
	
	#find person and associated household
	pers = s.query(Person).filter(Person.id == I_ID).one()	
	house = s.query(Household).filter(Household.id == pers.HH_ID).one()
	
	#create new object to hold visitor's data
	visitor = oldClientData(id=pers.id, firstname=pers.first_name,
				lastname=pers.last_name, dob=pers.DOB,
				phone=pers.phone, dateJoined=pers.date_joined)
	
	#create new object to hold household data
	household = houseData(street=house.street_address, city=house.city,
				state=house.state, zip=house.zip, 
				dateVerified=house.date_verified, apt=house.apt)
							
	#list to hold member-data objects
	members = []
	
	#create new objects to hold data for each additional household member
	for member in house.members:
		if member.first_name == pers.first_name: pass
		else:
			mem = oldClientData(id=member.id, firstname=member.first_name,
						lastname=member.last_name, dob=member.DOB,
						phone=member.phone,
						dateJoined=member.date_joined)
			members.append(mem)
			
	#get list of information about past 3 visits
	visits = list_visits(s, I_ID)
	
	#call to function to get dictionary of ages
	agegroups = get_age_breakdown(house.members)
	
	#create dictionary of all objects to be returned
	info = {"visitor":visitor, "household":household, "member_list":members,
			"visit_list":visits, "agegroup_dict":agegroups}
	return info
"""


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
	"""This function will update all records for a household and members
	of a household. A new record for a visit and new records for any new
	household members will also be created.
	
	"""
				
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
	
