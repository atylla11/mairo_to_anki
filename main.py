import getopt
import sys

from util import create_header, execute_request, is_open, create_request_body_anki_connect, \
    create_params_to_authenticate, print_usage, validate_token_address, create_notes, list_by_delimiter

header = create_header()
username = ''
password = ''
mairo_api_address = ''
lessons = ''
deck_name = ''
ENDS_OF_MAIRO_ADDRESS_TO_TOKEN = 'oauth/token'
ANKI_CONNECT_PORT = '8765'
ANKI_CONNECT_ADDRESS = 'localhost'
ANKI_CONNECT_ADDRESS_FULL = 'http://' + ANKI_CONNECT_ADDRESS + ':' + ANKI_CONNECT_PORT


def main(argv):
    process_args(argv)

    print('Checking if AnkiConnect is running...')
    if not is_open(ANKI_CONNECT_ADDRESS, ANKI_CONNECT_PORT):
        print('Finished without success, check if Anki is running and has been installed Anki Connect. =(')
        sys.exit()

    print('Synchronizing...')
    print('If synchronization is slow, check Anki, you may not be logged in.')
    execute_request(ANKI_CONNECT_ADDRESS_FULL, params=create_request_body_anki_connect('sync'))

    print('Getting token with Mairo API...')
    mairo_token = execute_request(mairo_api_address, header, create_params_to_authenticate(username, password))

    print('Creating notes at Anki...')
    execute_request(
        ANKI_CONNECT_ADDRESS_FULL,
        params=create_request_body_anki_connect(
            'addNotes', {'notes': create_notes_by_lessons(mairo_token)}))

    print('Synchronizing...')
    execute_request(ANKI_CONNECT_ADDRESS_FULL, params=create_request_body_anki_connect('sync'))

    print('Done with success!!! =D')


def process_args(argv):
    global mairo_api_address, lessons, deck_name, password, username
    try:
        options, args = getopt.getopt(argv, 'hu:p:a:l:d:')
    except getopt.GetoptError:
        print_usage()
        sys.exit(-1)

    for option, arg in options:
        if option == '-h':
            print_usage()
            sys.exit()
        elif option == '-u':
            username = arg
        elif option == '-p':
            password = arg
        elif option == '-a':
            mairo_api_address = arg
        elif option == '-l':
            lessons = arg
        elif option == '-d':
            deck_name = arg

    if username == '' or password == '' or lessons == '' or deck_name == '':
        print_usage()
        sys.exit(-1)
    if mairo_api_address == '':
        mairo_api_address = 'https://curso.mairovergara.com/api/v1/'
    mairo_api_address = validate_token_address(mairo_api_address, ENDS_OF_MAIRO_ADDRESS_TO_TOKEN)


def create_notes_by_lessons(mairo_token):
    notes = []
    if mairo_token is not None:
        token = 'Bearer ' + mairo_token['access_token']
        print('Getting phrases...')
        header.pop('Content-Type')
        header.update({'Authorization': token})
        notes = []
        LESSONS_DELIMITER = ','
        for class_id in list_by_delimiter(lessons, LESSONS_DELIMITER):
            response_json = execute_request(
                mairo_api_address.replace(ENDS_OF_MAIRO_ADDRESS_TO_TOKEN, '') +
                'estudoTexto/' + class_id + '/frases', header)
            if response_json is not None:
                created_notes = create_notes(deck_name, response_json)
                notes += created_notes
    return notes


if __name__ == '__main__':
    main(sys.argv[1:])