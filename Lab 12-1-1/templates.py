STATUS = """<!DOCTYPE html>
                <html lang='en'>
                <head>
                    <title>Garage Status</title>
                </head>
                <body>
                    <p>{}</p>
                    <p>{}</p>
                    <br>
                    <p> Click <a href="http://127.0.0.1:8765/login">Here</a> to enable/disable the alarm. </p>
                </body>
                </html>"""

BAD_PASS = """<!DOCTYPE html>
                <html lang='en'>
                <head>
                    <title>Garage Login : Bad Password</title>
                    <meta http-equiv="refresh" content="10;URL='http://127.0.0.1:8765/status'" />
                </head>
                <body>
                    <p>{}</p>
                    <p>{}</p>
                </body>
                </html>""" 