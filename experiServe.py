"""experiServe.py
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

	#Create title
	print("<title>Provisions Database</title>", file=output)
	print("<h1>Hullo, World!</h1>", file=output)

	
	#checks for POST instead of GET (more reliable)
	if environ['REQUEST_METHOD'] == 'POST': 
		size = int(environ['CONTENT_LENGTH'])
		post_str = environ['wsgi.input'].read(size)
		print(post_str, "<p>", file=output)
			
	print('<form action="/cgi-bin/hello_post.cgi" method="POST">'
		'First name: <input type="text" name="first_name" />'
		'<br>'
		'Last name: <input type="text" name="last_name" />'
		'<input type="submit" value="submit" />'
		'</form>',
		file=output)
	
	value = output.getvalue()
	byt = bytes(value, "ascii")
	return [byt]

httpd = make_server('', 8000, hullo_world_app)
print("Serving on port 8000...")
httpd.serve_forever()


