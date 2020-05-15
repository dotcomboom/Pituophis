# Pituophis
[![Documentation Status](https://readthedocs.org/projects/pituophis/badge/?version=latest)](https://pituophis.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://img.shields.io/pypi/v/Pituophis.svg)](https://pypi.python.org/pypi/Pituophis/)
[![PyPI license](https://img.shields.io/pypi/l/Pituophis.svg)](https://pypi.python.org/pypi/Pituophis/)

Python 3 library for building Gopher clients and servers

Pituophis, at the moment, requires nine modules: os, re, sockets, asyncio, ssl, mimetypes, glob, and urllib, which are standard in most Python 3.7 installations, and natsort. Pituophis can simply be loaded as a module like this:
```python
import pituophis
```

## Client
Pituophis can grab files and text from Gopher servers (both S/Gopher TLS and regular Gopher) through the `Request.get()` and `get()` functions.
### Examples
Getting menus and files as plain text:
```python
pituophis.get('gopher.floodgap.com').text()
pituophis.get('gopher://gopher.floodgap.com/1/').text()
pituophis.get('gopher://gopher.floodgap.com:70/0/gopher/proxy').text()
pituophis.get(host='gopher.floodgap.com', port=70, path='/').text()
pituophis.get(host='gopher.floodgap.com', port=70, path='/gopher/proxy').text()
pituophis.get(host='khzae.net', port=105, path='/', tls=True).text() # TLS!
pituophis.get('gophers://khzae.net:105/1/').text() # gophers:// URLs!

```
Getting a menu, parsed:
```python
menu = pituophis.get('gopher.floodgap.com').menu()
for selector in menu:
    print(selector.type)
    print(selector.text)
    print(selector.path)
    print(selector.host)
    print(selector.port)
```
Using search services:
```python
pituophis.get('gopher://gopher.floodgap.com:70/7/v2/vs?toast').text()
pituophis.get(host='gopher.floodgap.com', port=70, path='/v2/vs', query='toast').text()
```
Downloading a binary:
```python
pituophis.get('gopher://gopher.floodgap.com:70/9/gopher/clients/win/hgopher2_3.zip').binary
pituophis.get(host='gopher.floodgap.com', port=70, path='/gopher/clients/win/hgopher2_3.zip').binary
```
Requests can also be created and worked with directly:
```python
import pituophis
req = pituophis.Request()
req.host = 'gopher.floodgap.com'  # set to 127.0.0.1 by default
req.port = 70  # set to 70 as default, as per tradition
req.type = '7'  # set to 9 by default, purely for client usage
req.path = '/v2/vs'  # set to '/' by default
req.query = 'food'  # set to '' (nothing) by default
req.tls = False  # set to False by default
print('Getting', req.url())
rsp = req.get()
print(rsp.text())
```
They can also be created from a URL:
```python
import pituophis
req = pituophis.parse_url('gopher://gopher.floodgap.com/7/v2/vs?food')
print('Getting', req.url())
rsp = req.get()
print(rsp.text())
```
## Server
### Default Handler
Pituophis now lets you serve a directory. Serving gophermaps, directories, and files is supported out of the box.

![server_def](https://github.com/dotcomboom/Pituophis/blob/master/server_def.png?raw=true)
### Custom Handler
Pituophis also lets you write a custom handler for Gopher requests.

![server](https://github.com/dotcomboom/Pituophis/blob/master/server.png?raw=true)


