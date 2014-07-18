"""experiServe.py
THIS FILE INCLUDES A WRAPPER AND STUFF BUT DOESN't WORK YET
This file contains test functions. These functions are testing the
creation of a simple Python server, printing to a web page, html forms,
and I/O.

This function creates a web server, uses html to create
        a form, and prints user input.
        
"""
import cgi
from wsgiref.simple_server import make_server
from io import StringIO

#html wrapper variables
header = "<html><header><title>Provisions Database</title></header><body>"
footer = "</body></html>"

def html_page(content):
	"""This function creates a simple html page.
	"""
	page = "%s\n%s\n%s" % (header, content, footer)
	return page
	

def get_form_values(post_str):
	"""This function analyzes the string returned, and gets the
	data it needs from it.
	"""
        form_values = {item.split("=")[0]: item.split("=")[1] for item in post_str.split("&")}
        return form_values	

def hullo_world_app(environ, start_response):
	output = StringIO()
	status = "200 OK" #HTTP status
	headers = [("Content-type", "text/html; charset=utf-8")]
	start_response(status, headers)
	
	#checks for POST instead of GET (more reliable)
	if environ['REQUEST_METHOD'] == 'POST': 
		size = int(environ['CONTENT_LENGTH'])
		post_str = environ['wsgi.input'].read(size)
		print(post_str, "<p>", file=output)
	
	"""This function defines the web page for a returning client.
	"""	
	info = select_client(7)
	visitor = info["visitor"]
	house = info["household"]
	
	
	print("""
		<html>
		<head>
		<title>Provisions Database</title>
		</head>
		<body>
		<table width="100%"  border="0" cellpadding="10" cellspacing="5" 
		background=#f5f5dc>
			<tr> <!--means table row-->
				<td colspan="2" bgcolor="#deb887">
					<h1><center>Provisions Food Pantry</center></h1>
				</td> <!--td means table cell-->
			</tr>
			<tr valign="top">
				<!--cell one-->
				<td bgcolor="#fafad2" width="30%">
					This will hold the
					select box, new client
					button, and search bar.
				</td>
				
				<!--cell two-->
				<td bgcolor="#f0f8ff" width="70%">
					<form method="POST">
						<h3>Visitor Information</h3>
						First name: <input type="text" name="first" value=""" + str(visitor.firstname) + """ size="16"/>
						Last name: <input type="text" name="last" value=""" + str(visitor.lastname) + """ size="16"/>
						Phone: <input type="text" name="phone" value=""" + str(visitor.phone) + """ size="16"/>
						<br>
						DOB: 
						<input type="int" name="month" size="2" value=""" + str(visitor.dob.month) + """ maxlength="2"/>
						<input type="int" name="day" size="2" value=""" + str(visitor.dob.day) + """ maxlength="2"/>
						<input type="int" name="year" size="4" value=""" + str(visitor.dob.year) + """ maxlength="4"/>
						Age: ??
						<hr/>
              
						<h3>Household Information</h3>
						Street: <input type="text" name="street" value=""" + str(house.street) + """ />
						Apt: <input type="text" name="apt" value=""" + str(house.apt) + """ size="3"/>
						<br>
						City: <input type="text" name="city" value=""" + str(house.city) + """ size="16"/>
						State: <input type="text" name="state" value=""" + str(house.state) + """ size="2" maxlength="2"/>
						Zip: <input type="int" name="zip" value=""" + str(house.zip) + """ size="5"/>

						<hr/>
						<h3>Visit Information</h3>
						Date: <input type="text" name="visitDate"/>
						Visitor: <input type="text" name="visitor" value=""" + visitor.firstname + " " + visitor.lastname + """ />
						Visit notes: <input type="text" name="notes"/>
						<br>                                           
						
						<hr/>
						<h3>Household Members</h3>
						selection box thing?
						
						<input type="submit" value="submit" />
					</form>
				</td>				
			</tr>
		</table>
		</body>
		</html>
		 """, file=output)
	
	value = output.getvalue()
	byt = bytes(value, "ascii")
	return [byt]
                
httpd = make_server('', 8000, hullo_world_app)
print("Serving on port 8000...")
httpd.serve_forever()

