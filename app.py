# -*- coding: utf-8 -*-

import os
import sqlite3
from wsgiref.simple_server import make_server

from api_endpoint import application
def app():
    pass



def main():
    if not os.path.isfile("comments.db"):
        db_script = open("db_script.sql", "r").read()
        conn = sqlite3.connect("comments.db")
        c = conn.cursor()
        c.executescript(db_script)
        conn.commit()
        c.close()
    app()

if __name__ == '__main__':
    print "Serving api on port 8000..."
    httpd = make_server('localhost', 8000, application)
    httpd.serve_forever()
    main()