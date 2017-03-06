import cgi
import sqlite3

data = cgi.FieldStorage()



# print "Content-Type: text/html"
print {'values': data["region"].value}
