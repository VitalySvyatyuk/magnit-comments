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
    <style>
        .elements { width: 170px };
    </style>
    <script type="text/javascript" src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
    <script>
        function changeCities(region) {
            $.ajax({
                url: "comment.html",
                context: document.body,
                data: {"region": region},
                success: function(response){
                    $('#city option[value!="none"]').remove();
                    $.each(response, function (i, item) {
                        $('#city').append($('<option>', {
                            value: i,
                            text: item
                        }));
                    });
                }
            });
        }
    </script>
</head>
<body>
    <form action="" method="POST">
        <label for="surname">Фамилия:</label><br>
        <input type="text" name="surname" id="surname" class="elements"><br>
        <label for="name">Имя:</label><br>
        <input type="text" name="name" id="name" class="elements"><br>
        <label for="middlename">Отчество:</label><br>
        <input type="text" name="middlename" id="middlename" class="elements"><br>
        <label for="region">Регион:</label><br>
        <select id="region" onchange="changeCities(this.value)" class="elements">
            <option value="default"></option>
        </select><br>
        <label for="city">Город:</label><br>
        <select id="city" class="elements">%s</select><br>
        <label for="phone">Телефон:</label><br>
        <input type="text" name="phone" id="phone" class="elements"><br>
        <label for="email">Email:</label><br>
        <input type="text" name="email" id="email" class="elements"><br>
        <label for="comment">Комментарий:</label><br>
        <textarea name="comment" id="comment" class="elements"></textarea><br>
        <input type="submit" value="Добавить" id="button">
    </form>
</body>
</html>
"""

def application(environ, start_response):
    if "/comment" in environ["PATH_INFO"].lower():
        conn = sqlite3.connect("comments.db")
        c = conn.cursor()
        c.execute("SELECT * FROM regions")
        regions = c.fetchall()
        options = ""
        for region in regions:
            options += '<option value="{}">{}</option>'.format(region[0], region[1].encode('utf-8'))
        htm = html.replace('"default"></option>', 'default"></option>' + options)
        

        if environ["QUERY_STRING"] == "" :
            option = '<option value="none"></option>'
            response_body = htm % option
            status = '200 OK'
            response_headers = [
                ('Access-Control-Allow-Origin', '*'),
                ('Content-Type', 'text/html'),
                ('Content-Length', str(len(response_body))),
            ]   
        elif environ["REQUEST_METHOD"] == "GET":
            region_ = environ["QUERY_STRING"].replace("region=", "")
            print region_
            if region_ != "default%22":
                conn = sqlite3.connect("comments.db")
                c = conn.cursor()
                c.execute("SELECT * FROM cities WHERE region_id = {}".format(int(region_)))
                cities = c.fetchall()
                option = {}
                for city in cities:
                    option[str(city[0])] = city[1]
                c.close()
                response_body = json.dumps(option)
            else:
                response_body = json.dumps({})
            
            status = '200 OK'
            response_headers = [
                ('Access-Control-Allow-Origin', '*'),
                ('Content-Type', 'application/json'),
                ('Content-Length', str(len(response_body))),
            ]
        elif environ["REQUEST_METHOD"] == "POST":
            pass
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
