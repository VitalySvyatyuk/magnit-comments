# -*- coding: utf-8 -*-

import os
import re
import sqlite3
import json
from wsgiref.simple_server import make_server
from cgi import parse_qs


def application(environ, start_response):
    comment_template = open("templates/comment.html", "r")
    html = comment_template.read()
    comment_template.close()
    if environ["PATH_INFO"].lower().startswith("/comment"):
        conn = sqlite3.connect("comments.db")
        c = conn.cursor()
        c.execute("SELECT * FROM regions")
        regions = c.fetchall()
        options = ""
        for region in regions:
            options += '<option value="{}">{}</option>' \
                       .format(region[0], region[1].encode('utf-8'))
        htm = html.replace('"default"></option>', 
                            'default"></option>' + options)
        
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
            if region_ != "default%22":
                conn = sqlite3.connect("comments.db")
                c = conn.cursor()
                c.execute("SELECT * FROM cities WHERE region_id = {}"
                          .format(int(region_)))
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
            # if valid - return /view/ page
            # if not valid - retun /comment/ page with error fields
    else:
        if (environ["PATH_INFO"].lower() == "/view" or 
            environ["PATH_INFO"].lower() == "/view/"):
            if environ["QUERY_STRING"] != "":
                remove_id = environ["QUERY_STRING"].replace("to_remove=", "")
                conn = sqlite3.connect("comments.db")
                c = conn.cursor()
                c.execute("DELETE FROM comments WHERE id={}".format(remove_id))
                conn.commit()
                c.close()
            view_template = open("templates/view.html", "r")
            view = view_template.read()
            view_template.close()
            conn = sqlite3.connect("comments.db")
            c = conn.cursor()
            c.execute("SELECT * FROM comments " + \
                       "LEFT JOIN regions ON comments.region = regions.id " + \
                       "LEFT JOIN cities  ON comments.city = cities.id " )
            comments = c.fetchall()
            c.close()
            comments_table = ""
            for comment in comments:
                comment = list(comment)
                comment[4] = comment[10]
                comment[5] = comment[12]
                comment = comment[:9]
                comments_table += '<tr>'
                for com in comment:
                    if com == None:
                        comments_table += '<td></td>'
                    elif isinstance(com, int):
                        comments_table += '<td>' + str(com) + '</td>'
                    else:
                        comments_table += '<td>' + com.encode("utf-8") \
                                        + '</td>'
                comments_table += '<td><a onclick="removeComment(this)" \
                                   href="../view/">Удалить</a></td></tr>'
                # comments_table += '<td><button onclick="removeComment(this);">Удалить</button></td></tr>'

            
            response_body = view % comments_table

            if environ["QUERY_STRING"] != "":
                remove_id = environ["QUERY_STRING"].replace("to_remove=", "")
                


        elif (environ["PATH_INFO"].lower() == "/stat" or 
              environ["PATH_INFO"].lower() == "/stat/"):
            pass
        else:
            default_page = open("templates/default_page.html", "r")
            response_body =  default_page.read()
            default_page.close()

        status = '200 OK'
        response_headers = [
            ('Access-Control-Allow-Origin', '*'),
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(response_body))),
        ]
    start_response(status, response_headers)
    return [response_body]

def main():
    if not os.path.isfile("comments.db"):
        db_script = open("db_script.sql", "r")
        script = db_script.read()
        db_script.close()
        conn = sqlite3.connect("comments.db")
        c = conn.cursor()
        c.executescript(script)
        conn.commit()
        c.close()

if __name__ == '__main__':
    main()
    print "Serving api on port 8000..."
    httpd = make_server('localhost', 8000, application)
    httpd.serve_forever()
