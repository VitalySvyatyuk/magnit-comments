import json

def application(environ, start_response):
	response_body = json.dumps({
		'success': True
	})

	status = '200 OK'
	response_headers = [
		('Access-Control-Allow-Origin', '*'),
		('Content-Type', 'application/json'),
		('Content-Length', str(len(response_body))),
	]

	start_response(status, response_headers)
	return [response_body]