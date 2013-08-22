Facebook on Terminal
===
[![Pypi Version](https://pypip.in/v/fbterminal/badge.png)](https://crate.io/packages/fbterminal) [![Downloads](https://pypip.in/d/fbterminal/badge.png)](https://crate.io/packages/fbterminal) [![Build Status](https://travis-ci.org/decached/fbterminal.png?branch=master)](https://travis-ci.org/decached/fbterminal)

Access Facebook on Terminal

- Check Notifications, Messages
- Check who's online
- Post a status
- Fire a custom FQL query (for the geeks)
- And More... (Coming Soon)

Requirements
---
- [Python 2.7/3.3]
- [Pip](http://pypi.python.org/pypi/pip) `$ apt-get install python-pip`
- [Requests](http://docs.python-requests.org/en/latest/) `$ pip install requests`

Installation
---
1. Fast Forward  
    `$ pip install fbterminal`

OR

1. Clone the Repository  
	`$ git clone git://github.com/decached/fbterminal.git`  
    `$ python setup.py install`

2. Go to Facebook Developers -> https://developers.facebook.com/apps/ and create a new app

3. Copy the APP ID and APP SECRET to ~/.fbterminal

Running
---
- Check online friends:
    `$ fbterminal -o`

- Post message:
    `$ fbterminal -p 'Hello World'`

Copyright and Licence
---

Released under MIT Licence  
Copyright (c) 2013 Akash Kothawale → http://decached.com
