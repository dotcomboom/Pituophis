# BSD 2-Clause License
#
# Copyright (c) 2020, dotcomboom <dotcomboom@somnolescent.net> and contributors
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

import asyncio
import glob
import mimetypes
import os
import re
import socket
import ssl
from operator import itemgetter
from os.path import realpath
from urllib.parse import urlparse

from natsort import natsorted

# Quick note:
# item types are not sent to the server, just the selector/path of the resource


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
        Decodes the binary as UTF-8 text and parses it as a Gopher menu. Returns a List of Gopher menu items parsed as the Item type.
        """
        return parse_menu(self.binary.decode('utf-8'))


class Request:
    """
    *Client/Server.* Represents a request to be sent to a Gopher server, or received from a client.
    """

    def __init__(self, host='127.0.0.1', port=70,
                 advertised_port=None, path='/', query='',
                 itype='9', tls=False, tls_verify=True, client='',
                 pub_dir='pub/', alt_handler=False):
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
        if advertised_port is None:
            advertised_port = self.port

        self.advertised_port = int(advertised_port)
        """
        *Server.* Used by the default handler. Set this if the server itself
        is being hosted on another port than the advertised port (like port 70), with
        a firewall or some other software rerouting that port to the server's real port. 
        """
        self.path = str(path)
        """
        *Client/Server.* The selector string to request, or being requested.
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
        *Client/Server.* Whether the request is to be, or was sent to an S/Gopher server over TLS.
        """
        self.tls_verify = tls_verify
        """
        *Client.* Whether to verify the certificate sent from the server, rejecting self-signed and invalid certificates.
        """
        self.client = str(client)  # only used in server
        """
        *Server.* The IP address of the connected client.
        """
        self.pub_dir = str(pub_dir)  # only used in server
        """
        *Server.* The default handler uses this as which directory to serve. Default is 'pub/'.
        """
        self.alt_handler = alt_handler

    def stream(self):
        """
        *Client.* Lower-level fetching. Sends the request and returns a BufferedReader.
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.host.count(':') > 1:
            # ipv6
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        if self.tls:
            context = ssl._create_unverified_context()
            if self.tls_verify:  # TODO: for some reason this is always true when using the get() shorthand
                context = ssl.create_default_context()
            s = context.wrap_socket(s, server_hostname=self.host)
        else:
            s.settimeout(10.0)
        s.connect((self.host.replace('[', '').replace(']', ''),
                   int(self.port)))
        if self.query == '':
            msg = self.path + '\r\n'
        else:
            msg = self.path + '\t' + self.query + '\r\n'
        s.sendall(msg.encode('utf-8'))
        return s

    def get(self):
        """
        *Client.* Sends the request and returns a Response object.
        """
        return Response(self.stream().makefile('rb'))

    def url(self):
        """
        Returns a URL equivalent to the Request's properties.
        """
        protocol = 'gopher'
        if self.tls:
            protocol = 'gophers'
        path = self.path
        query = ''
        if not (self.query == ''):
            query = '%09' + self.query
        hst = self.host
        if not self.port == 70:
            hst += ':{}'.format(self.port)
        return '{}://{}/{}{}{}'.format(protocol, hst, self.type, path, query)


class Item:
    """
    *Server/Client.* Represents an item in a Gopher menu.
    """

    def __init__(self, itype='i', text='', path='/', host='', port=0, tls=False):
        """
        Initializes a new Item object.
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
        True if the item leads to an S/Gopher server with TLS enabled.
        """

    def source(self):
        """
        Returns the item as a line in a Gopher menu.
        """
        port = int(self.port)
        if self.tls:
            # Add digits to display that this is a TLS item
            while len(str(port)) < 5:
                port = '0' + str(port)
            port = '1' + str(port)
            port = int(port)
        return str(self.type) + str(self.text) + '\t' + str(self.path) + '\t' + str(self.host) + '\t' + str(
            port) + '\r\n'

    def request(self):
        """
        Returns a Request to where the item leads.
        """
        req = Request()
        req.type = self.type
        req.host = self.host
        req.port = self.port
        req.path = self.path
        req.tls = self.tls
        return req


def parse_menu(source):
    """
    *Client.* Parses a String as a Gopher menu. Returns a List of Items.
    """
    parsed_menu = []
    menu = source.replace('\r\n', '\n').replace('\n', '\r\n').split('\r\n')
    for line in menu:
        item = Item()
        if line.startswith('i'):
            item.type = 'i'
            item.text = line[1:].split('\t')[0]
            item.path = '/'
            item.host = ''
            item.port = 0
        else:
            line = line.split('\t')
            while len(
                    line) > 4:  # discard Gopher+ and other naughty stuff
                line = line[:-1]
            line = '\t'.join(line)
            matches = re.match(r'^(.)(.*)\t(.*)\t(.*)\t(.*)', line)
            if matches:
                item.type = matches[1]
                item.text = matches[2]
                item.path = matches[3]
                item.host = matches[4]
                item.port = matches[5]
                try:
                    item.port = int(item.port)
                except:
                    item.port = 70
                # detect TLS
                if item.port > 65535:
                    item.tls = True
                    # typically the port is sent as 100105
                    # remove first number to get at 5 digits
                    item.port = int(str(item.port)[1:])
        parsed_menu.append(item)
    return parsed_menu


def parse_url(url):
    """
    *Client.* Parses a Gopher URL and returns an equivalent Request.
    """
    req = Request(host='', port=70, path='/', query='', tls=False)

    up = urlparse(url)

    if up.scheme == '':
        up = urlparse('gopher://' + url)

    if up.scheme == 'gophers':
        req.tls = True

    req.path = up.path
    if up.query:
        req.path += '?{}'.format(up.query)  # NOT to be confused with actual gopher queries, which use %09
                                            # this just combines them back into one string
    req.host = up.hostname
    req.port = up.port
    if up.port is None:
        req.port = 70
    if req.path:
        if req.path.endswith('/'):
            req.type = '1'
        if len(req.path) > 1:
            req.type = req.path[1]
        req.path = req.path[2:]
    else:
        req.type = '1'

    if '%09' in req.path:       # handle gopher queries
        req.query = ''.join(req.path.split('%09')[1:])
        req.path = req.path.split('%09')[0]

    return req


def get(host, port=70, path='/', query='', tls=False, tls_verify=True):
    """
    *Client.* Quickly creates and sends a Request. Returns a Response object.
    """
    req = Request(host=host, port=port, path=path,
                  query=query, tls=tls, tls_verify=tls_verify)
    if '/' in host or ':' in host:
        req = parse_url(host)
    return req.get()


# Server stuff
mime_starts_with = {
    'image': 'I',
    'text': '0',
    'audio/x-wav': 's',
    'image/gif': 'g',
    'text/html': 'h'
}

errors = {
    '404': Item(itype='3', text='404: {} does not exist.'),
    '403': Item(itype='3', text='403: Resource outside of publish directory.'),
    '403_glob': Item(itype='3', text='403: Gopher glob is out of scope.'),
    'no_pub_dir': Item(itype='3', text='500: Publish directory does not exist.')
}


def parse_gophermap(source, def_host='127.0.0.1', def_port='70',
                    gophermap_dir='/', pub_dir='pub/', tls=False):
    """
    *Server.* Converts a Bucktooth-style Gophermap (as a String or List) into a Gopher menu as a List of Items to send.
    """
    if not gophermap_dir.endswith('/'):
        gophermap_dir += '/'
    if not pub_dir.endswith('/'):
        pub_dir += '/'

    if type(source) == str:
        source = source.replace('\r\n', '\n').split('\n')
    new_menu = []
    for item in source:
        if '\t' in item:
            # this is not information
            item = item.split('\t')
            expanded = False
            # 1Text    pictures/    host.host    port
            #  ^           ^           ^           ^
            itype = item[0][0]
            text = item[0][1:]
            path = gophermap_dir + text
            if itype == '1':
                path += '/'
            host = def_host
            port = def_port

            if len(item) > 1:
                path = item[1]
            if len(item) > 2:
                host = item[2]
            if len(item) > 3:
                port = item[3]

            if path == '':
                path = gophermap_dir + text
                if itype == '1':
                    path += '/'

            if not path.startswith('URL:'):
                # fix relative path
                if not path.startswith('/'):
                    path = realpath(gophermap_dir + '/' + path)

                # globbing
                if '*' in path:
                    expanded = True
                    if os.path.abspath(pub_dir) in os.path.abspath(
                            pub_dir + path):
                        g = natsorted(glob.glob(pub_dir + path))

                        listing = []

                        for file in g:
                            file = re.sub(
                                r'/{2}', r'/', file).replace('\\', '/')
                            s = Item()
                            s.type = itype
                            if s.type == '?':
                                s.type = '9'
                                if path.startswith('URL:'):
                                    s.type = 'h'
                                elif os.path.exists(file):
                                    mime = \
                                        mimetypes.guess_type(file)[0]
                                    if mime is None:  # is directory or binary
                                        if os.path.isdir(file):
                                            s.type = '1'
                                        else:
                                            s.type = '9'
                                            if file.endswith('.md'):
                                                s.type = 1
                                    else:
                                        for sw in mime_starts_with.keys():
                                            if mime.startswith(sw):
                                                s.type = \
                                                    mime_starts_with[
                                                        sw]
                            splt = file.split('/')
                            while '' in splt:
                                splt.remove('')
                            s.text = splt[len(splt) - 1]
                            if os.path.exists(file + '/gophertag'):
                                s.text = ''.join(list(open(
                                    file + '/gophertag'))).replace(
                                    '\r\n', '').replace('\n', '')
                            s.path = file.replace(pub_dir, '/', 1)
                            s.path = re.sub(r'/{2}', r'/', s.path)
                            s.host = host
                            s.port = port
                            if s.type == 'i':
                                s.path = ''
                                s.host = ''
                                s.port = '0'
                            if s.type == '1':
                                d = 0
                            else:
                                d = 1
                            if not s.path.endswith('gophermap'):
                                if not s.path.endswith(
                                        'gophertag'):
                                    listing.append(
                                        [file, s, s.text, d])

                        listing = natsorted(listing,
                                            key=itemgetter(0))
                        listing = natsorted(listing,
                                            key=itemgetter(2))
                        listing = natsorted(listing,
                                            key=itemgetter(3))

                        for item in listing:
                            new_menu.append(item[1])
                    else:
                        new_menu.append(errors['403_glob'])

            if not expanded:
                item = Item()
                item.type = itype
                item.text = text
                item.path = path
                item.host = host
                item.port = port

                if item.type == '?':
                    item.type = '9'
                    if path.startswith('URL:'):
                        item.type = 'h'
                    elif os.path.exists(
                            pub_dir + path):
                        mime = mimetypes.guess_type(
                            pub_dir + path)[0]
                        if mime is None:  # is directory or binary
                            if os.path.isdir(file):
                                s.type = '1'
                            else:
                                s.type = '9'
                        else:
                            for sw in mime_starts_with.keys():
                                if mime.startswith(sw):
                                    item.type = \
                                        mime_starts_with[sw]

                if item.host == def_host and item.port == def_port:
                    item.tls = tls

                new_menu.append(item.source())
        else:
            item = 'i' + item + '\t\t\t0'
            new_menu.append(item)
    return new_menu


def handle(request):
    """
    *Server.* Default handler function for Gopher requests while hosting a server.
    Serves files and directories from the pub/ directory by default, but the path can
    be changed in serve's pub_dir argument or changing the Request's pub_dir directory.
    """
    #####
    pub_dir = request.pub_dir
    #####

    if request.advertised_port is None:
        request.advertised_port = request.port
    if request.path.startswith('URL:'):
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Gopher Redirect</title>
            <meta http-equiv="refresh" content="0; url={0}">
        </head>
        <body>
            <h1>Gopher Redirect</h1>
            <p>You will be redirected to <a href="{0}">{0}</a> shortly.</p>
        </body>
        """.format(request.path.split('URL:')[1])

    if not os.path.exists(pub_dir):
        return [errors['no_pub_dir']]

    menu = []
    if request.path == '':
        request.path = '/'
    res_path = os.path.abspath(
        (pub_dir + request.path).replace('\\', '/').replace('//', '/'))
    if not res_path.startswith(os.path.abspath(pub_dir)):
        # Reject connections that try to break out of the publish directory
        return [errors['403']]
    if os.path.isdir(res_path):
        # is directory
        if os.path.exists(res_path):
            if os.path.isfile(res_path + '/gophermap'):
                in_file = open(res_path + '/gophermap', "r+")
                gmap = in_file.read()
                in_file.close()
                menu = parse_gophermap(source=gmap,
                                       def_host=request.host,
                                       def_port=request.advertised_port,
                                       gophermap_dir=request.path,
                                       pub_dir=pub_dir,
                                       tls=request.tls)
            else:
                gmap = '?*\t\r\n'
                menu = parse_gophermap(source=gmap,
                                       def_host=request.host,
                                       def_port=request.advertised_port,
                                       gophermap_dir=request.path,
                                       pub_dir=pub_dir,
                                       tls=request.tls)
            return menu
    elif os.path.isfile(res_path):
        in_file = open(res_path, "rb")
        data = in_file.read()
        in_file.close()
        return data

    if request.alt_handler:
        alt = request.alt_handler(request)
        if alt:
            return alt

    e = errors['404']
    e.text = e.text.format(request.path)
    return [e]


def serve(host="127.0.0.1", port=70, advertised_port=None,
          handler=handle, pub_dir='pub/', alt_handler=False,
          send_period=False, tls=False,
          tls_cert_chain='cacert.pem',
          tls_private_key='privkey.pem', debug=True):
    """
    *Server.*  Starts serving Gopher requests. Allows for using a custom handler that will return a Bytes, String, or List
    object (which can contain either Strings or Items) to send to the client, or the default handler which can serve
    a directory. Along with the default handler, you can set an alternate handler to use if a 404 error is generated for
    dynamic applications.
    """
    if pub_dir is None or pub_dir == '':
        pub_dir = '.'
    if tls:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

        if os.path.exists(tls_cert_chain) and os.path.exists(tls_private_key):
            context.load_cert_chain(tls_cert_chain, tls_private_key)
        else:
            print("""TLS certificate and/or private key is missing. TLS has been disabled for this session.
Run this command to generate a self-signed certificate and private key:
    openssl req -x509 -newkey rsa:4096 -keyout {} -out {} -days 365
Note that clients may refuse to connect to a self-signed certificate.
            """.format(tls_private_key, tls_cert_chain))
            tls = False

    if tls:
        print('S/Gopher server is now running on',
              host + ':' + str(port) + '.')
    else:
        print('Gopher server is now running on', host + ':' + str(port) + '.')

    class GopherProtocol(asyncio.Protocol):
        def connection_made(self, transport):
            self.transport = transport
            print('Connected by', transport.get_extra_info('peername'))

        def data_received(self, data):
            request = data.decode('utf-8').replace('\r\n', '').split('\t')
            path = request[0]
            query = ''
            if len(request) > 1:
                query = request[1]
            if debug:
                print('Client requests: {}'.format(request))
            is_tls = False

            if self.transport.get_extra_info('sslcontext'):
                is_tls = True

            resp = handler(
                Request(path=path, query=query, host=host,
                        port=port, advertised_port=advertised_port,
                        client=self.transport.get_extra_info(
                            'peername')[0], pub_dir=pub_dir,
                        alt_handler=alt_handler, tls=is_tls))

            if type(resp) == str:
                resp = bytes(resp, 'utf-8')
            elif type(resp) == list:
                out = ""
                for line in resp:
                    if type(line) == Item:
                        out += line.source()
                    elif type(line) == str:
                        line = line.replace('\r\n', '\n')
                        line = line.replace('\n', '\r\n')
                        if not line.endswith('\r\n'):
                            line += '\r\n'
                        out += line
                resp = bytes(out, 'utf-8')
            elif type(resp) == Item:
                resp = bytes(resp.source(), 'utf-8')

            self.transport.write(resp)
            if send_period:
                self.transport.write(b'.')

            self.transport.close()
            if debug:
                print('Connection closed')

    async def main(h, p):
        loop = asyncio.get_running_loop()
        if tls:
            server = await loop.create_server(GopherProtocol, h, p, ssl=context)
        else:
            server = await loop.create_server(GopherProtocol, h, p)
        await server.serve_forever()

    asyncio.run(main('0.0.0.0', port))
