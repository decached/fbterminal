#!/usr/bin/python
from facebook import Facebook
import argparse
import sys
import pycurl
import cStringIO


def custom_FQL(fb, query):
    response = fb.fqlQuery(query)
    if 'data' in response:
        attributes = map(lambda x: x.replace(" ", ""), query.split('from')[0].split('select')[1].split(','))
        print ''
        for record in response['data']:
            for attribute in attributes:
                print record[attribute], '\t ',
            print ""
    elif 'error' in response:
        print "\nFQL Error: ", response['error']['message']


def show_unread_messages(fb):
    query = 'SELECT sender,body,timestamp FROM unified_message WHERE thread_id IN (SELECT thread_id FROM unified_thread WHERE has_tags("inbox") AND unread=1) AND unread!=0 ORDER BY timestamp DESC'
    response = fb.fqlQuery(query)
    if 'data' in response and response['data'] != []:
        print "\nUnread Messages \n\n[Name]: Message\n"
        for friend in response['data']:
            print "[%s]: %s" % (friend['sender']['name'], friend['body'])
    else:
        print "\nNo unread messages"


def show_friends_online(fb):
    query = 'SELECT online_presence,name FROM user WHERE online_presence in ("active","idle") AND uid IN (SELECT uid2 FROM friend WHERE uid1 = me()) ORDER BY online_presence'
    response = fb.fqlQuery(query)
    if 'data' in response:
        print "\nFriends Online \nStatus \t Name\t"
        for friend in response['data']:
            print "%5s \t %s" % (friend['online_presence'], friend['name'])
    else:
        print "\nNo one online"


def show_notifications(fb):
    query = 'SELECT href, title_text, body_text FROM notification WHERE recipient_id = me() AND is_unread!=0 ORDER BY updated_time ASC'
    response = fb.fqlQuery(query)
    if 'data' in response:
        if len(response['data']):
            print "\nNotifications"
            for notif in response['data']:
                print notif['title_text'], notif['body_text'], notif['href']
        else:
            print "\nNo Notifications!"


def show_friend_online_status(fb, friend):
    query = 'SELECT online_presence, name FROM user WHERE online_presence in ("active","idle") AND uid IN (SELECT uid2 FROM friend WHERE uid1 = me()) ORDER BY online_presence'
    response = fb.fqlQuery(query)
    if 'data' in response:
        print "\n" + friend + ' is',
        try:
            [element for element in response['data'] if element['name'].lower() == friend.lower()][0]['online_presence']
            print "ONLINE"
        except:
            print "offline"


def post_on_wall(fb, post):
    buf = cStringIO.StringIO()
    req = pycurl.Curl()
    req.setopt(req.URL, 'https://graph.facebook.com/me/feed')
    fields = fb.access_token + "&message=" + post
    req.setopt(req.POSTFIELDS, fields)
    req.setopt(req.WRITEFUNCTION, buf.write)
    req.perform()
    print "Status Updated -> https://facebook.com/" + buf.getvalue().split('\"')[3]


def terminal(args):
    fb = Facebook()
    if args['messages']:
        show_unread_messages(fb)
    if args['notifications']:
        show_notifications(fb)
    if args['online']:
        show_friends_online(fb)
    if args['post']:
        post_on_wall(fb, args['post'])
    if args['query']:
        custom_FQL(fb, args['query'].lower())
    if args['spy_friend']:
        show_friend_online_status(fb, args['spy_friend'])


def command_line_runner():
    parser = argparse.ArgumentParser(description='Access Facebook on Terminal')
    parser.add_argument('-m', '--messages', help='Show unread messages', action='store_true')
    parser.add_argument('-n', '--notifications', help='Show notifications', action='store_true')
    parser.add_argument('-o', '--online', help='Show friends who are online', action='store_true')
    parser.add_argument('-p', '--post', help='Post on your wall', type=str)
    parser.add_argument('-q', '--query', help='Execute custom FQL')
    parser.add_argument('-s', '--spy-friend', help='Show if a particular friend is online')
    if len(sys.argv) == 1:
        print parser.print_usage()
        sys.exit("fbterminal: error: too few arguments")
    args = vars(parser.parse_args())
    terminal(args)


if __name__ == "__main__":
    command_line_runner()
