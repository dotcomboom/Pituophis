# BSD 2-Clause License
#
# Copyright (c) 2018, dotcomboom <dotcomboom@protonmail.com> and contributors
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

# Portions copyright solderpunk & VF-1 contributors, licensed under the BSD 2-Clause License above.

import socket, ssl

nonBinaryTypes = ['0', '1', '7']

# quick note:
# selectors and item types are actually *not* sent to the server, just the path of the resource

def get(host, port=70, path='/', query='', binary=False, menu=True, filterSelector=True, tls=False):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if tls:
        context = ssl.create_default_context()
        s = context.wrap_socket(s, server_hostname=host)
    else:
        s.settimeout(10.0)
    s.connect((host, port))
    query = '\t' + query
    msg = path + query + '\r\n'
    s.sendall(msg.encode('utf-8'))
    if binary:
        return s.makefile('rb').read()
    else:
        text = ''
        data = True
        while data:
            data = s.recv(1024)
            text = text + data.decode('utf-8')
        if menu:
            return parseMenu(text)
        else:
            return text


def parseMenu(menu):
    return menu

def parseUrl(url):
    parsed = {
        'host': '',
        'port': '70',
        'type': '1',
        'path': '',
        'menu': True,
        'tls': False
    }
    url = 'gopher://' + url


class Request:
    def __init__(self, path, query, host, port):
        self.path = path
        self.query = query
        self.host = host
        self.port = port


def serve(host="127.0.0.1", port=70, mapFileName='gophermap', useGophermaps=True, customHandler=False, debug=True):
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
                if customHandler:
                    resp = customHandler(Request(path, query, host, port))
                else:
                    resp = ['iHello! You asked for... ' + path + '\t/\terror.host\t0\r\n',
                            'iQuery, if you asked: ' + query + '\t/\terror.host\t0\r\n',
                            'iThere is no custom handler enabled.\t/\terror.host\t0\r\n']
                for r in resp:
                    if not r.endswith('\r\n'):
                        r += '\r\n'
                    conn.send(bytes(r, 'utf-8'))
                conn.send(b'.')
                conn.close()
                print('Connection closed')


def parse_gophermap(source, defHost='127.0.0.1', defPort='70'):
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
            itype = '3'
            text = 'error'
            path = '/'
            host = defHost
            port = defPort

            itype = selector[0][0]
            text = selector[0][1:]

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
    print(newMenu)
    # return '\r\n'.join(newMenu)
    return newMenu