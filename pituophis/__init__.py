# BSD 2-Clause License
#
# Copyright (c) 2019, dotcomboom <dotcomboom@protonmail.com> and contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   List of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this List of conditions and the following disclaimer in the documentation
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

import re
import socket
import ssl


# Quick note:
# selectors and item types are actually *not* sent to the server, just the path of the resource


class Response:
    """
    *Client.* Returned by Request.get() and get(). Represents a received binary object from a Gopher server.
    """

    def __init__(self, stream):
        """
        Reads a BufferedReader to the object's binary property and initializes a new Response object.
        """
        self.binary = stream.read()

    def text(self):
        """
        Returns the binary decoded as a UTF-8 String.
        """
        return self.binary.decode('utf-8')

    def menu(self):
        """
        **NOT YET IMPLEMENTED.** Decodes the binary as text and parses it as a Gopher menu. Returns a List of Gopher menu items parsed as the Selector type.
        """
        # NOT YET IMPLEMENTED
        # Returns List of Selector class
        return self.binary.decode('utf-8')


class Request:
    """
    *Client/Server.* Represents a request to be sent to a Gopher server, or received from a client.

    The type property is not used when sending or receiving requests; it's purely for client-side usage.
    """

    def __init__(self, host='127.0.0.1', port=70, path='/', query='', type='9', tls=False, client=''):
        """
        Initializes a new Request object.
        """
        self.host = host
        self.port = port
        self.path = path
        self.query = query
        self.type = type
        self.tls = tls  # only used in client
        self.client = client  # only used in server

    def get(self):
        """
        Sends the Request and returns a Response object.
        """
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
        """
        Returns a URL equivalent to the Request's properties.
        """
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

    def is_text(self):
        """
        Returns a boolean for whether the Request's type property is text (0, 1, 7) or not.
        """
        if self.type in ['0', '1', '7']:
            return True
        else:
            return False

    def is_menu(self):
        """
        Returns a boolean for whether the Request's type property is a menu (1, 7) or not.
        """
        if self.type in ['1', '7']:
            return True
        else:
            return False

    def is_search(self):
        """
        Returns a boolean for whether the Request's type property is a search menu (7) or not.
        """
        if self.type == '7':
            return True
        else:
            return False


# Client stuff
class Selector:
    """
    **Not yet implemented.** *Client.* Represents a selector in a parsed Gopher menu.
    """

    def __init__(self):
        # NOT YET IMPLEMENTED
        pass


def parse_url(url):
    """
    *Client.* Parses a Gopher URL and returns an equivalent Request.
    """
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
    """
    *Client.* Quickly creates and sends a Request. Returns a Response object.
    """
    req = Request(host=host, port=port, path=path, query=query, tls=tls)
    if '/' in host:
        req = parse_url(host)
    return req.get()


# Server stuff
def parse_gophermap(source, defHost='127.0.0.1', defPort='70', debug=False):
    """
    *Server.* Converts a Gophermap (as a String or List) into a Gopher menu. Returns a List of lines to send.
    This is *not* as feature-complete as the actual Bucktooth implementation; one example being how paths
    are not resolved. It does, however, fill in missing selector, host, or port fields.
    """
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


def encode(str_or_lines):
    """
    *Server.* Encode a List of lines, or a String, as bytes to be sent by serve().
    """
    if type(str_or_lines) == str:
        return bytes(str_or_lines, 'utf-8')

    if type(str_or_lines) == list:
        out = ""
        for line in str_or_lines:
            line = line.replace('\r\n', '\n')
            line = line.replace('\n', '\r\n')
            if not line.endswith('\r\n'):
                line += '\r\n'
            out += line
        return bytes(out, 'utf-8')

    raise Exception("encode() accepts items of type String or List.")


def handle(request):
    """
    *Server.* Default handler function for Gopher requests while hosting a server. Currently a stub.
    """
    gmap = [
        "Path: " + request.path,
        "Query: " + request.query,
        "Host: " + request.host,
        "Port: " + str(request.port),
        "Client: " + str(request.client),
        "",
        "This is the default Pituophis handler."
    ]
    return encode(parse_gophermap(gmap))

def serve(host="127.0.0.1", port=70, handler=handle, debug=True):
    """
    *Server.*  Listens for Gopher requests. Allows for using a custom handler that will return a binary (Bytes) object
    to send to the client. After sending them, the finishing "." is sent and the connection is closed.
    """
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
                resp = handler(Request(path=path, query=query, host=host, port=port, client=addr[0]))
                conn.send(resp)
                conn.close()
                if debug:
                    print('Connection closed')
