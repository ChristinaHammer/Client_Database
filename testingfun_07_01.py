"""testingfun.py
Developer: Noelle Todd
Last Updated: July 1, 2014

This program will test the new_household and update_all functions,
and the select_client function.
"""

from cdbifunc import *
from cdbfunctions import *
from datetime import date

def creation_example():
	#create new volunteer
	new_volunteer("Henry", "York")

	#create visit object
	visitInfo = visitData(1, notes="No id")

	#create newClient objects
	ncd1 = newClientData("Harry", "Potter", date(year=1994, month=7, day=9))
	ncd2 = newClientData("Ron", "Weasley", date(year=1993, month=12, day=12))

	newClientInfo_list = [ncd1, ncd2]

	#create household object
	houseInfo = houseData("Hogwartz", city="London")

	#send all objects to new_household function
	new_household(houseInfo, visitInfo, newClientInfo_list)

	print("Here is the list of people in the database right now: \n", list_people())

	#end database session (cleanly close database)
	quit_session()


def update_example():
	#update household and insert client
	print("\n")

	visitInfo = visitData(1, visitDate=date(year=2014, month=3, day=11), notes="Brought a dog named Snuffles")

	ocd1 = oldClientData(1, "Harry", "Potter", date(year=1994, month=7, day=9))
	ocd2 = oldClientData(2, "Ron", "Weasley", date(year=1993, month=12, day=12))

	oldClientInfo_list = [ocd1, ocd2]

	ncd = newClientData("Hermione", "Granger", date(year=1994, month=9, day=7))
	newClientInfo_list = [ncd]

	houseInfo = houseData("Hogwartz", city="London")

	update_all(1, houseInfo, visitInfo, oldClientInfo_list, newClientInfo_list)

	print("After update & add: \n")
	print(list_people())

	quit_session()
	
	
def select_example():
	info = select_client(1)
	#Return should look something like this:
	#info = {"visitor":visitor, "household":household, "member_list":members,
	#		"visit_list":visits, "agegroup_dict":agegroups}
	#
	#below is how to find all of the information you will need to pre-populate 
	#fields (entry boxes), and find the ids of every member.
	#

	#Example of getting data from "visitor" object
	visitor = info["visitor"]
	print("Visitor's id:", visitor.id)
	print("Visitor's first name: ", visitor.firstname)
	print("Visitor's last name: ", visitor.lastname)
	print("Visitor's dob: ", visitor.dob)
	print("Visitor's dob:", visitor.dob.month, visitor.dob.day, visitor.dob.year)
	print("Visitor's phone:", visitor.phone)
	print("Date visitor joined food pantry:", visitor.dateJoined)

	print("\n")

	#Example of getting data from "household" object
	house = info["household"]
	print("street, apt:", house.street, house.apt)
	print("city, state, zip:", house.city, house.state, house.zip)
	print("Date verified:", house.dateVerified)
	if house.dateVerified != None:
		print("Date verified:", house.dateVerified.month, house.dateVerified.day, house.dateVerified.year)
		
	print("\n")
			
	#Getting data from "member_list" object
	for member in info["member_list"]:
		print("Member's id:", member.id)
		print("First name is:", member.firstname)
		print("Last name is:", member.lastname)
		print("dob is:", member.dob)
		print("dob is:", member.dob.month, member.dob.day, member.dob.year)
		print("\n")

	#Getting data from "visit_list" object
	for visit in info["visit_list"]:
		print("Date of visit: ", visit.date)
		print("Name of visitor: ", visit.visitor)
		print("Name of volunteer: ", visit.volunteer)
		print("Visit notes: ", visit.notes)
		print("\n")

	#Getting data from "agegroup_dict" object
	print("Number of seniors are: ", info["agegroup_dict"]["seniors"])
	print("Number of adults are: ", info["agegroup_dict"]["adults"])
	print("Number of children are:", info["agegroup_dict"]["children"])
	print("Number of infants are: ", info["agegroup_dict"]["infants"])

	#end database session (cleanly close database)
	quit_session()

def main():
	creation_example()
	print('\n')
	update_example()
	print('\n')
	select_example()
	
if __name__ == "__main__":
	main()
