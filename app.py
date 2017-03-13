# -*- coding: utf-8 -*-

import os
import re
import sqlite3
import json
from wsgiref.simple_server import make_server
from urlparse import parse_qs


def application(environ, start_response):
    if environ["PATH_INFO"].lower().startswith("/comment"):
        comment_template = open("templates/comment.html", "r")
        html = comment_template.read()
        comment_template.close()
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
        if environ["QUERY_STRING"] == "":
            option = '<option value="none"></option>'
            response_body = htm % option
            status = '200 OK'
            response_headers = [
                ('Access-Control-Allow-Origin', '*'),
                ('Content-Type', 'text/html'),
                ('Content-Length', str(len(response_body))),
            ]
        else:
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
    elif (environ["PATH_INFO"].lower() == "/view" or 
          environ["PATH_INFO"].lower() == "/view/"):
        if environ["REQUEST_METHOD"] == "GET":
            if environ["QUERY_STRING"] != "":
                remove_id = environ["QUERY_STRING"].replace("to_remove=", "")
                conn = sqlite3.connect("comments.db")
                c = conn.cursor()
                c.execute("DELETE FROM comments WHERE id={}".format(remove_id))
                conn.commit()
                c.close()
        elif environ["REQUEST_METHOD"] == "POST":
            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except (ValueError):
                request_body_size = 0
            request_body = environ['wsgi.input'].read(request_body_size)
            d = parse_qs(request_body)
            d_surname = d.get('surname', [''])[0]
            d_name = d.get('name', [''])[0]
            d_middlename = d.get('middlename', [''])[0]
            d_region = d.get('region', [''])[0]
            d_city = d.get('city', [''])[0]
            d_phone = d.get('phone', [''])[0]
            d_email = d.get('email', [''])[0]
            d_comment = d.get('comment', [''])[0]
            conn = sqlite3.connect("comments.db")
            c = conn.cursor()
            c.execute('INSERT INTO comments (surname, name, middlename, ' + \
                                  'region, city, phone, email, comment) ' + \
                      'VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'
                      .format(d_surname, d_name, d_middlename, d_region, 
                              d_city, d_phone, d_email, d_comment))
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
        response_body = view % comments_table
    elif (environ["PATH_INFO"].lower() == "/stat" or 
          environ["PATH_INFO"].lower() == "/stat/"):
        stat_template = open("templates/stat.html", "r")
        stat = stat_template.read()
        stat_template.close()
        conn = sqlite3.connect("comments.db")
        c = conn.cursor()
        c.execute("SELECT comments.region, regions.region, " +
                  "COUNT(comments.region)  " +
                  "FROM comments " +
                  "INNER JOIN regions ON comments.region = regions.id " +
                  "GROUP BY comments.region " +
                  "HAVING COUNT(*) > 5")
        regions = c.fetchall()
        c.close()
        stat_reg_table = ""
        for region in regions:
            stat_reg_table += '<tr>'
            stat_reg_table += '<td>' + str(region[0]) + '</td>' + \
                              '<td><a href="../stat/' + str(region[0]) + \
                              '">' + region[1] + '</a></td>' + \
                              '<td>' + str(region[2]) + '</td>'
            stat_reg_table += '</tr>'
        response_body = stat % stat_reg_table.encode('utf-8')
    elif re.search(r"^/stat/\d+$", environ["PATH_INFO"].lower()):
        region_id = environ["PATH_INFO"].lower()[6:]
        stat_cities_template = open("templates/stat_cities.html", "r")
        stat_cities = stat_cities_template.read()
        stat_cities_template.close()
        conn = sqlite3.connect("comments.db")
        c = conn.cursor()
        c.execute("SELECT comments.city, cities.city, " +
                  "COUNT(comments.city) " +
                  "FROM comments " +
                  "INNER JOIN cities ON comments.city = cities.id " +
                  "GROUP BY comments.city " +
                  "HAVING comments.region = {}"
                  .format(region_id))
        cities = c.fetchall()
        c.execute("SELECT region from regions WHERE regions.id={}"
                  .format(region_id))
        region_name = c.fetchall()
        c.close()
        stat_cities_table = ""
        for city in cities:
            stat_cities_table += '<tr>'
            stat_cities_table += '<td>' + str(city[0]) + '</td>' + \
                                 '<td>' + city[1] + '</td>' + \
                                 '<td>' + str(city[2]) + '</td>'
            stat_cities_table += '</tr>'
        response_body = stat_cities % (stat_cities_table.encode('utf-8'),
                                       region_name[0][0].encode('utf-8'))
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
