# -*- coding: utf-8 -*-

import os
import re
import sqlite3
import json
from wsgiref.simple_server import make_server
from cgi import parse_qs


html = """
<html>
<head>
    <meta charset="UTF-8">
    <title>Magnit | View comments</title>
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
    <script>
        function changeCities(region) {
            $.ajax({
                url: "comment.html",
                context: document.body,
                data: {"region": region},
                success: function(response){
                    // $(#city).
                    console.log(response);
                }
            });
            // var selectedValue = region; 
        }
    </script>
</head>
<body>
    <form action="" method="POST">
        <input type="text" name="surname" id="surname">
        <input type="text" name="name" id="name">
        <input type="text" name="middlename" id="middlename">
        <select id="region" onchange="changeCities(this.value)">
            <option value="default"></option>
            <option value="1">Краснодарский край</option>
            <option value="2">Ростовская область</option>
            <option value="3">Ставропольский край</option>
        </select>
        <select id="city">%s</select>
        <input type="text" name="phone" id="phone">
        <input type="text" name="email" id="phone">
        <input type="text" name="comment" id="comment">
        <input type="submit" value="Добавить" id="button">
    </form>
</body>
</html>
"""

def application(environ, start_response):
    if "/comment" in environ["PATH_INFO"].lower():
        if environ["QUERY_STRING"] == "" or environ["QUERY_STRING"] == "default":
            option = '<option value="none"></option>'
            response_body = html % option
            status = '200 OK'
            response_headers = [
                ('Access-Control-Allow-Origin', '*'),
                ('Content-Type', 'text/html'),
                ('Content-Length', str(len(response_body))),
            ]   
        else:
            conn = sqlite3.connect("comments.db")
            c = conn.cursor()
            c.execute("SELECT * FROM cities WHERE region_id = {}".format(int(environ["QUERY_STRING"].replace("region=", ""))))
            cities = c.fetchall()
            option = {}
            for city in cities:
                option[str(city[0])] = city[1].encode('utf-8').strip()
            c.close()
            print option
            response_body = json.dumps(option)
            status = '200 OK'
            response_headers = [
                ('Access-Control-Allow-Origin', '*'),
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(response_body))),
            ]
    else:
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

def main():
    if not os.path.isfile("comments.db"):
        db_script = open("db_script.sql", "r").read()
        conn = sqlite3.connect("comments.db")
        c = conn.cursor()
        c.executescript(db_script)
        conn.commit()
        c.close()

if __name__ == '__main__':
    main()
    print "Serving api on port 8000..."
    httpd = make_server('localhost', 8000, application)
    httpd.serve_forever()
