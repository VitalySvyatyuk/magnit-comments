import cgi

data = cgi.FieldStorage()


print "Content-Type: text/x-json\n"
print data["region"].value
