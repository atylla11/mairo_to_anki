import json
import re
import socket
import urllib.request as urllib2
import urllib.parse as parse
import urllib.error as error
from datetime import date

from classes import MLStripper, Note


def serialize(obj):
    if isinstance(obj, date):
        serial = obj.isoformat()
        return serial

    return obj.__dict__


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def create_request_body_anki_connect(action, params=None):
    request_body = {'action': action, 'version': 6}
    if params is not None:
        request_body.update({'params': params})
    return request_body


def print_usage():
    print(
        'mairo_to_anki '
        '-u <username> '
        '-p <password> '
        '-a <mairo_address_api=https://curso.mairovergara.com/api/v1/> '
        '-l <lesson_ids 10 or 18,168,48> '
        '-d <deck_name>'
    )


def execute_request(resource, headers=None, params=None):
    if params is None and headers is not None:
        req = urllib2.Request(url=resource, headers=headers)
    elif headers is None and params is not None:
        req = urllib2.Request(resource, json.dumps(params).encode('utf-8'))
    else:
        req = urllib2.Request(resource, parse.urlencode(params).encode('utf-8'), headers)
    try:
        return json.load(urllib2.urlopen(req))
    except error.HTTPError as e:
        print(e)
        return None


def create_notes(deck_name, response_json):
    notes = []
    for phrases in response_json:
        notes.append(serialize(Note(deck_name, strip_tags(phrases['fraseEn']), strip_tags(phrases['frasePt']))))
    return notes


def create_params_to_authenticate(username, password):
    return {
        'grant_type': 'password',
        'username': username,
        'password': password
    }


def create_header():
    return {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64)",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json, text/plain, */*'
    }


def is_open(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False


def validate_token_address(address, address_ends):
    # Find everything after the last '/' and replace it with address_ends
    if not address.endswith(address_ends):
        regex = re.compile(R'^(.*[/])')
        match = regex.match(address)
        address = match.group()
        address = address + address_ends

    return address


def list_by_delimiter(term, delimiter):
    if term.find(delimiter) > 0:
        list = term.split(delimiter)
    else:
        list = [term]
    return list