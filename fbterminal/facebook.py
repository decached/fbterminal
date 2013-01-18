import pycurl
import getpass
import cStringIO
import json
from ConfigParser import ConfigParser
from urllib import urlencode


class Facebook:
    app_id = ""
    app_secret = ""
    app_url = "https://www.facebook.com/connect/login_success.html"
    permissions = "friends_online_presence, manage_notifications, publish_stream"
    access_token = ""

    def __init__(self):
        config = ConfigParser()
        config.read('/home/' + getpass.getuser() +'/.fbterminal')
        self.app_id = config.get('app_details', 'APP_ID')
        self.app_secret = config.get('app_details', 'APP_SECRET')
        self.access_token = config.get('access_token', 'access_token')
        if not self.valid_access_token():
            self.authorize()
        self.access_token = config.get('access_token', 'access_token')

    def authorize(self):
        dialog_url = "https://www.facebook.com/dialog/oauth"
        fields = "client_id=" + self.app_id + "&redirect_uri=" + self.app_url
        print "Goto -> " + dialog_url + "?" + fields
        code = raw_input('Enter the URL you are redirected to: ')
        code = code.split('#')[0].split('=')[1]
        code_url = "https://graph.facebook.com/oauth/access_token"
        fields = "client_id=" + self.app_id + "&redirect_uri=" + self.app_url + "&client_secret=" + self.app_secret + "&code=" + code
        buf = cStringIO.StringIO()
        req = pycurl.Curl()
        req.setopt(req.URL, code_url)
        req.setopt(req.POSTFIELDS, fields)
        req.setopt(req.WRITEFUNCTION, buf.write)
        req.perform()
        config = ConfigParser()
        config.read('/home/' + getpass.getuser() +'/.fbterminal')
        config.set('access_token', 'access_token', buf.getvalue().split('&')[0])
        config.write(open('/home/' + getpass.getuser() +'/.fbterminal', 'w+'))

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
