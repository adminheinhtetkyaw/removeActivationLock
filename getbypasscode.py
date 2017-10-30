#!/usr/bin/python

jssAPIUsername=""
jssAPIPassword=""
jssAddress=""
configProfileID=""


import requests, argparse

parser = argparse.ArgumentParser()
parser.add_argument("jssid", help="get the bypass lock code given the jss id")
args = parser.parse_args()

session = requests.Session()

data = {'username': jssAPIUsername, 'password': jssAPIPassword}
session.post(jssAddress, data=data)


def get_session_token(html_text):
    for line in html_text.splitlines():
        if 'session-token' in line:
            return line.encode('utf-8').translate(None, '<>"').split('=')[-1]
         

session_token = get_session_token(session.get(jssAddress+'/iOSConfigurationProfiles.html?id='+configProfileID+'&o=r').text)            

data = {'session-token': session_token, 'ajaxAction': 'AJAX_ACTION_READ_BYPASS_CODE'}
r = session.post(jssAddress+'/mobileDevices.ajax?id=%s&o=r&v=management' % args.jssid, data=data)
print r.content
