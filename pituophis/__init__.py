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

import os
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
        """
        The data received from the server as a Bytes binary object.
        """

    def text(self):
        """
        Returns the binary decoded as a UTF-8 String.
        """
        return self.binary.decode('utf-8')

    def menu(self):
        """
        Decodes the binary as text and parses it as a Gopher menu. Returns a List of Gopher menu items parsed as the Selector type.
        """
        return parse_menu(self.binary.decode('utf-8'))


class Request:
    """
    *Client/Server.* Represents a request to be sent to a Gopher server, or received from a client.
    """

    def __init__(self, host='127.0.0.1', port=70, path='/', query='', itype='9', tls=False, tls_verify=True, client=''):
        """
        Initializes a new Request object.
        """
        self.host = str(host)
        """
        *Client/Server.* The hostname of the server.
        """
        self.port = int(port)
        """
        *Client/Server.* The port of the server. For regular Gopher servers, this is most commonly 70, 
        and for S/Gopher servers it is typically 105.
        """
        self.path = str(path)
        """
        *Client/Server.* Path on the target server to request, or being requested.
        """
        self.query = str(query)
        """
        *Client/Server.* Search query for the server to process. Omitted when blank.
        """
        self.type = str(itype)
        """
        *Client.* Item type of the request. Purely for client-side usage, not used when sending or receiving requests.
        """
        self.tls = tls
        """
        *Client.* Whether the request is to be sent to an S/Gopher server over TLS.
        """
        self.tls_verify = tls_verify
        """
        *Client.* Whether to verify the certificate sent from the server, rejecting self-signed and invalid certificates.
        """
        self.client = str(client)  # only used in server
        """
        *Server.* The IP address of the connected client.
        """

    def get(self):
        """
        *Client.* Sends the Request and returns a Response object.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.tls:
            context = ssl._create_unverified_context()
            if self.tls_verify:  # TODO: for some reason this is always true when using the get() shorthand
                context = ssl.create_default_context()
            s = context.wrap_socket(s, server_hostname=self.host)
        else:
            s.settimeout(10.0)
        s.connect((self.host, int(self.port)))
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


class Selector:
    """
    *Server/Client.* Represents a selector in a parsed Gopher menu.
    """

    def __init__(self, itype='i', text='', path='/', host='error.host', port=0, tls=False):
        """
        Initializes a new Selector object.
        """
        self.type = itype
        """
        The type of item.
        """
        self.text = text
        """
        The name, or text that is displayed when the item is in a menu.
        """
        self.path = path
        """
        Where the item links to on the target server.
        """
        self.host = host
        """
        The hostname of the target server.
        """
        self.port = port
        """
        The port of the target server. For regular Gopher servers, this is most commonly 70, 
        and for S/Gopher servers it is typically 105.
        """
        self.tls = tls
        """
        True if the selector leads to an S/Gopher server with TLS enabled.
        """
    def source(self):
        """
        Returns a representation of what the selector looks like in a Gopher menu.
        """
        port = int(self.port)
        if port < 65535:
            # Add digits to display that this is a TLS selector
            while len(str(port)) < 5:
                port = '0' + str(port)
            port = '1' + str(port)
            port = int(port)
        return str(self.type) + str(self.text) + '\t' + str(self.path) + '\t' + str(self.host) + '\t' + str(
            port) + '\r\n'


def parse_menu(source):
    """
    *Client.* Parses a String as a Gopher menu. Returns a List of Selectors.
    """
    parsed_menu = []
    menu = source.replace('\r\n', '\n').replace('\n', '\r\n').split('\r\n')
    for line in menu:
        selector = Selector()
        if line.startswith('i'):
            selector.type = 'i'
            selector.text = line[1:].split('\t')[0]
            selector.path = '/'
            selector.host = 'error.host'
            selector.port = 0
        else:
            matches = re.match(r'^(.)(.*)\t(.*)\t(.*)\t(.*)', line)
            if matches:
                selector.type = matches[1]
                selector.text = matches[2]
                selector.path = matches[3]
                selector.host = matches[4]
                selector.port = matches[5]
                # detect TLS
                if int(selector.port) > 65535:
                    selector.tls = True
                    # typically the port is sent as 100105
                    # remove first number to get at 5 digits
                    selector.port = int(str(selector.port)[1:])
        parsed_menu.append(selector)
    return parsed_menu


def parse_url(url):
    """
    *Client.* Parses a Gopher URL and returns an equivalent Request.
    """
    req = Request(host='', port=70, path='/', query='', tls=False)

    # condense multiple slashes to one
    url = re.sub(r'/+', '/', url)
    # add protocol if not there
    if ':/' not in url:
        url = 'gopher:/' + url
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
        req.port = int(url[0].split(':')[1])
    else:
        req.host = url[0]
    url.pop(0)
    # remove selector if it is there
    if len(url) > 0:
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


def get(host, port=70, path='/', query='', tls=False, tls_verify=True):
    """
    *Client.* Quickly creates and sends a Request. Returns a Response object.
    """
    req = Request(host=host, port=port, path=path, query=query, tls=tls, tls_verify=tls_verify)
    if '/' in host or ':' in host:
        req = parse_url(host)
    return req.get()


# Server stuff
def parse_gophermap(source, def_host='127.0.0.1', def_port='70'):
    """
    *Server.* Converts a Gophermap (as a String or List) into a Gopher menu. Returns a List of lines to send.
    This is *not* as feature-complete as the actual Bucktooth implementation; one example being how paths
    are not resolved. It does, however, fill in missing selector, host, and port fields,
    given that the correct host and port values are passed to it.
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
            host = def_host
            port = def_port

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
    # return '\r\n'.join(newMenu)
    return newMenu


def encode(str_or_lines):
    """
    *Server.* Encode a List of lines or Selector objects, or a String, as bytes to be sent by serve().
    """
    if type(str_or_lines) == str:
        return bytes(str_or_lines, 'utf-8')

    if type(str_or_lines) == list:
        out = ""
        for line in str_or_lines:
            if type(line) == str:
                line = line.replace('\r\n', '\n')
                line = line.replace('\n', '\r\n')
                if not line.endswith('\r\n'):
                    line += '\r\n'
                out += line
            if type(line) == Selector:
                out += line.source()
        return bytes(out, 'utf-8')

    if type(str_or_lines) == bytes:
        return str_or_lines

    raise Exception("encode() accepts items of type String, List, or Bytes.")


def handle(request):
    """
    *Server.* Default handler function for Gopher requests while hosting a server. Currently a stub.
    """
    menu = [
        Selector(text="Path: " + request.path),
        Selector(text="Query: " + request.query),
        Selector(text="Host: " + request.host),
        Selector(text="Port: " + str(request.port)),
        Selector(text="Client: " + request.client),
        Selector(),
        Selector(text="This is the default Pituophis handler.")
    ]
    return encode(menu)


def serve(host="127.0.0.1", port=70, handler=handle, tls=False, tls_cert_chain='cacert.pem',
          tls_private_key='privkey.pem', debug=True):
    """
    *Server.*  Listens for Gopher requests. Allows for using a custom handler that will return a binary (Bytes) object
    to send to the client. After sending them, the finishing "." is sent and the connection is closed.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if tls:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

        if os.path.exists(tls_cert_chain) and os.path.exists(tls_private_key):
            context.load_cert_chain(tls_cert_chain, tls_private_key)
            s = context.wrap_socket(s, server_side=True)
        else:
            print('TLS certificate and/or private key is missing. TLS has been disabled for this session.')
            print('Run this command to generate a self-signed certificate and private key:')
            print(
                '  openssl req -x509 -newkey rsa:4096 -keyout "' + tls_private_key + '" -out "' + tls_cert_chain + '" -days 365')
            print('Note that clients might refuse to connect to a self-signed certificate.')
            print()
            tls = False

    with s:
        s.bind((host, port))
        s.listen(1)
        if tls:
            print('S/Gopher server is now running on', host + ':' + str(port) + '.')
        else:
            print('Gopher server is now running on', host + ':' + str(port) + '.')
        while True:
            try:
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
            except Exception as e:
                if debug:
                    print('Error:', e)
