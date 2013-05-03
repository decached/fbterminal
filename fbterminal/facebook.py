import pycurl
import getpass
import cStringIO
import json
from ConfigParser import ConfigParser
from urllib import urlencode
import sys
import BaseHTTPServer
import urlparse
import webbrowser

code = ''


class httpServHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if not self.path.find('?') == -1:
            parsed_path = urlparse.urlparse(self.path)
            try:
                params = dict([p.split('=') for p in parsed_path[4].split('&')])
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("Success! You may close this tab.")
                global code
                code = params['code']
                return
            except:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("")
                return


class Facebook:
    app_id = ""
    app_secret = ""
    app_url = "http://localhost:7777/"
    permissions = "friends_online_presence, manage_notifications, publish_stream, read_mailbox"
    access_token = ""

    def __init__(self):
        config = ConfigParser()
        config.read('/home/' + getpass.getuser() + '/.fbterminal')
        self.app_id = config.get('app_details', 'APP_ID')
        self.app_secret = config.get('app_details', 'APP_SECRET')
        if self.app_id == "YOUR_APP_ID" or self.app_secret == "YOUR_APP_SECRET":
            sys.exit("Please create a new Facebook app (https://developers.facebook.com/apps/) and enter your APP_ID and APP_SECRET in ~/.fbterminal file")
        self.access_token = config.get('access_token', 'access_token')
        if not self.valid_access_token():
            self.authorize()
        config.read('/home/' + getpass.getuser() + '/.fbterminal')
        self.access_token = config.get('access_token', 'access_token')

    def authorize(self):
        dialog_url = "https://www.facebook.com/dialog/oauth"
        fields = urlencode({"client_id": self.app_id, "redirect_uri": self.app_url, "scope": self.permissions})
        webbrowser.open(dialog_url + "?" + fields)
        serv = BaseHTTPServer.HTTPServer(('localhost', 7777), httpServHandler)
        serv.handle_request()
        code_url = "https://graph.facebook.com/oauth/access_token"
        fields = "client_id=" + self.app_id + "&redirect_uri=" + self.app_url + "&client_secret=" + self.app_secret + "&code=" + code
        buf = cStringIO.StringIO()
        req = pycurl.Curl()
        req.setopt(req.URL, code_url)
        req.setopt(req.POSTFIELDS, fields)
        req.setopt(req.WRITEFUNCTION, buf.write)
        req.perform()
        config = ConfigParser()
        config.read('/home/' + getpass.getuser() + '/.fbterminal')
        config.set('access_token', 'access_token', buf.getvalue().split('&')[0])
        config.write(open('/home/' + getpass.getuser() + '/.fbterminal', 'w+'))

    def fqlQuery(self, query):
        fql_url = "https://graph.facebook.com/fql?"
        query = urlencode({'q': query})
        curl_request_url = fql_url + query + "&" + self.access_token
        buf = cStringIO.StringIO()
        req = pycurl.Curl()
        req.setopt(req.URL, curl_request_url)
        req.setopt(req.WRITEFUNCTION, buf.write)
        req.perform()
        return json.loads(buf.getvalue())

    def valid_access_token(self):
        response = self.fqlQuery('SELECT name FROM user WHERE uid=me()')
        if 'data' in response:
            if len(response['data']):
                return True
        return False
