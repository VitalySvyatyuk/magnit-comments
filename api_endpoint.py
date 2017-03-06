import json

def application(environ, start_response):
    # if environ["PATH_INFO"] == "/comment/":

    #     response_body = open("templates/comment.html", "r").read()
    #     status = '200 OK'
    #     response_headers = [
    #         ('Access-Control-Allow-Origin', '*'),
    #         ('Content-Type', 'text/html'),
    #         ('Content-Length', str(len(response_body))),
    #     ]
        
    # else:  
    response_body = [
        '%s: %s' % (key, value) for key, value in sorted(environ.items())
    ]
    response_body = '\n'.join(response_body)

    status = '200 OK'
    response_headers = [
        ('Access-Control-Allow-Origin', '*'),
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body))),
    ]
    start_response(status, response_headers)
    return [response_body]