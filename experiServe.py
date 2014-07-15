"""experiServe.py
Developer: Noelle Todd
Last visit: July 15, 2014

This file tests the creation of a simple Python server, 
printing to a web page, html forms, and basic I/O.

"""

import cgi
from wsgiref.simple_server import make_server
from io import 

def get_form_values(post_str): pass
    #This function retrieves the information submitted to the form.
    #form_values = {item.split("=")[0]: item.split[1] for item in post_str.split("&")}
    #return form_values


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
						First name: <input type="text" name="first" size=16/>
						Last name: <input type="text" name="last" size=16/>
						Phone: <input type="text" name="phone" size=16/>
						<br>
						DOB: 
						<input type="int" name="month" size=2 maxlength=2/>
						<input type="text" name="day" size=2 maxlength=2/>
						<input type="text" name="year" size=4 maxlength=4/>
						Age: ?
						<hr/>
						
						<h3>Household Information</h3>
						Street: <input type="text" name="street"/>
						Apt: <input type="text" name="apt" size=3/>
						<br>
						City: <input type="text" name="city" value="Troy" size=16/>
						State: <input type="text" name="state" value="NY" size=2 maxlength=2/>
						Zip: <input type="int" name="zip" size=5/>
						
						<hr/>
						<h3>Visit Information</h3>
						date of last visit, etc.
						
						<hr/>
						<h3>Household Members</h3>
						selection box thing?
						
						<input type="submit" value="submit" />
					</form>
				</td>				
			</tr>
		</table>
		</body>
		</html> """, file=output)
		
	value = output.getvalue()
	byt = bytes(value, "ascii")
	return [byt]

httpd = make_server('', 8000, hullo_world_app)
print("Serving on port 8000...")
httpd.serve_forever()


