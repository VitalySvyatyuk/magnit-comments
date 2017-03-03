# -*- coding: utf-8 -*-

import os
import sqlite3



# # this specifies that there is a WSGI server running on port 8000
# upstream app_server_djangoapp {
#     server localhost:8000 fail_timeout=0;
# }

# # Nginx is set up to run on the standard HTTP port and listen for requests
# server {
#   listen 80;

#   # nginx should serve up static files and never send to the WSGI server
#   location /static {
#     autoindex on;
#     alias /srv/www/assets;
#   }

#   # requests that do not fall under /static are passed on to the WSGI
#   # server that was specified above running on port 8000
#   location / {
#     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#     proxy_set_header Host $http_host;
#     proxy_redirect off;

#     if (!-f $request_filename) {
#       proxy_pass http://app_server_djangoapp;
#       break;
#     }
#   }
# }
    


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
    main()