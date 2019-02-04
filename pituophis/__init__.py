# BSD 2-Clause License
#
# Copyright (c) 2019, dotcomboom <dotcomboom@protonmail.com> and contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Portions copyright solderpunk & VF-1 contributors, licensed under the BSD 2-Clause License above.

import socket
import ssl
import re

# Quick note:
# selectors and item types are actually *not* sent to the server, just the path of the resource


# Both client & server
class Request:
    def __init__(self, host='127.0.0.1', port=70, path='/', query='', type='9', tls=False, client=''):
        self.host = host
        self.port = port
        self.path = path
        self.query = query
        self.type = type
        self.tls = tls # only used in client
        self.client = '' # only used in server

    def get(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.tls:
            context = ssl.create_default_context()
            s = context.wrap_socket(s, server_hostname=self.host)
        else:
            s.settimeout(10.0)
        s.connect((self.host, self.port))
        if self.query == '':
            msg = self.path + '\r\n'
        else:
            msg = self.path + '\t' + self.query + '\r\n'
        s.sendall(msg.encode('utf-8'))
        return Response(s.makefile('rb'))

    def url(self):
        protocol = 'gopher'
        if self.tls:
            protocol = 'gophers'
        path = self.path
        if not (path.startswith('/')):
            path = '/' + path
        query = ''
        if not (self.query == ''):
            query = '?' + self.query
        return protocol + '://' + str(self.host) + ':' + str(self.port) + '/' + str(self.type) + str(path) + str(query)


# Client stuff
class Selector:
    def __init__(self):
        # NOT YET IMPLEMENTED
        pass


class Response:
    def __init__(self, stream):
        self.binary = stream.read()

    def text(self):
        return self.binary.decode('utf-8')

    def menu(self):
        # NOT YET IMPLEMENTED
        # Returns array of Selector class
        return self.binary.decode('utf-8')


def parse_url(url):
    req = Request(host='', port=70, path='/', query='', tls=False)

    # condense multiple slashes to one
    url = re.sub(r'/+', '/', url)
    url = url.split('/')
    # split into protocol, host & port, and then the following items for the selector/path
    # gopher:
    # gopher.floodgap.com:70
    # gopher/
    # detect tls and remove protocol
    if url[0].endswith(':'):
        if url[0] == 'gophers:':
            req.tls = True
        url.pop(0)
    # set and remove host/port
    if len(url[0].split(':')) > 1:
        req.host = url[0].split(':')[0]
        req.port = url[0].split(':')[1]
    else:
        req.host = url[0]
    url.pop(0)
    # remove selector if it is there
    if len(url[0]) == 1:
        req.type = url[0]
        url.pop(0)
    # set url to path?query
    url = '/' + '/'.join(url)
    req.path = url
    # split query if it is there
    if '?' in url:
        url = url.split('?')
        req.path = url[0]
        url.pop(0)
        req.query = '?'.join(url)
    return req


def get(host, port=70, path='/', query='', tls=False):
    req = Request(host=host, port=port, path=path, query=query, tls=tls)
    if '/' in host:
        req = parse_url(host)
    return req.get()


# Server stuff
def parse_gophermap(source, defHost='127.0.0.1', defPort='70', debug=False):
    # NOTICE:
    # Relative links are *not* fixed with this function!
    # The path isn't ever touched, so this is more for convenience of making menus
    # (filling in the blank fields, information selectors...)
    if type(source) == str:
        source = source.replace('\r\n', '\n').split('\n')
    newMenu = []
    for selector in source:
        if '\t' in selector:
            # this is not information
            selector = selector.split('\t')
            # 1Text    pictures/    host.host    port
            #  ^           ^           ^           ^
            itype = selector[0][0]
            text = selector[0][1:]
            path = '/' + selector[1] + '/'
            host = defHost
            port = defPort

            if len(selector) > 1:
                path = selector[1]
            if len(selector) > 2:
                host = selector[2]
            if len(selector) > 3:
                port = selector[3]

            selector = [itype + text, path, host, port]
            newMenu.append('\t'.join(selector))
        else:
            selector = 'i' + selector
            newMenu.append(selector)
    if debug:
        print(newMenu)
    # return '\r\n'.join(newMenu)
    return newMenu


def handle(request):
    gmap = [
        "Path: " + request.path,
        "Query: " + request.query,
        "Host: " + request.host,
        "Port: " + str(request.port),
        "",
        "This is the default Pituophis handler."
    ]
    return parse_gophermap(gmap)


def serve(host="127.0.0.1", port=70, handler=handle, debug=True):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            with conn:
                if debug:
                    print('Connected by', addr)
                data = conn.recv(1024)
                request = data.decode('utf-8').split('\t')
                path = request[0].replace('\r\n', '')
                query = ''
                if len(request) > 1:
                    query = request[1].replace('\r\n', '')
                if debug:
                    print('Client requests:', path, query)
                resp = handler(Request(path=path, query=query, host=host, port=port, client=addr))
                for r in resp:
                    if not r.endswith('\r\n'):
                        r += '\r\n'
                    conn.send(bytes(r, 'utf-8'))
                conn.send(b'.')
                conn.close()
                if debug:
                    print('Connection closed')