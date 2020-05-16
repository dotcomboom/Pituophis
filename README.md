# Pituophis
[![Documentation Status](https://readthedocs.org/projects/pituophis/badge/?version=latest)](https://pituophis.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://img.shields.io/pypi/v/Pituophis.svg)](https://pypi.python.org/pypi/Pituophis/)
[![PyPI license](https://img.shields.io/pypi/l/Pituophis.svg)](https://pypi.python.org/pypi/Pituophis/)

Python 3 library for building Gopher clients and servers

Pituophis, at the moment, requires nine modules: os, re, sockets, asyncio, ssl, mimetypes, glob, and urllib, which are standard in most Python 3.7 installations, and natsort. Pituophis can simply be loaded as a module like this:
```python
import pituophis
```

## Server

Pituophis can act as a powerful Gopher server, with full Bucktooth-style gophermap and globbing support. Scripting, which entirely optional is also supported through alt handlers (used in the event of a 404) or fully custom handlers (replaces Pituophis' handler entirely).

The simplest method of getting a server up and running is with the `pituophis.serve()` function. See the [examples](https://github.com/dotcomboom/Pituophis/tree/master/examples) and [docs](https://pituophis.readthedocs.io/en/latest/#pituophis.serve) for more information. If you'd like to see a server built with Pituophis that can search an index, try [Gophew](https://github.com/dotcomboom/Gophew).

![server_def](https://github.com/dotcomboom/Pituophis/blob/master/server_def.png?raw=true)

## Client
Pituophis can also grab files and text from Gopher servers (both S/Gopher TLS and regular Gopher) through the `Request.get()` and `get()` functions.
### Examples
Getting menus and files as plain text:
```python
pituophis.get('gopher.floodgap.com').text()
pituophis.get('gopher://gopher.floodgap.com/1/').text()
pituophis.get('gopher://gopher.floodgap.com:70/0/gopher/proxy').text()
pituophis.get('gophers://khzae.net:105/1/').text() # gophers:// URL support

```
Getting a menu, parsed:
```python
menu = pituophis.get('gopher.floodgap.com').menu()
for item in menu:
    print(item.type)
    print(item.text)
    print(item.path)
    print(item.host)
    print(item.port)
```
Using search services:
```python
pituophis.get('gopher://gopher.floodgap.com:70/7/v2/vs%09toast').text()
```
Downloading a binary:
```python
pituophis.get('gopher://gopher.floodgap.com:70/9/gopher/clients/win/hgopher2_3.zip').binary
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
req = pituophis.parse_url('gopher://gopher.floodgap.com/7/v2/vs%09food')
print('Getting', req.url())
rsp = req.get()
print(rsp.text())
```
### TreeGopher
An interactive demo of Pituophis' client features is provided in the form of TreeGopher, a graphical Gopher client in ~200 lines of code. It uses Pituophis, PySimpleGUI, and Pyperclip. It can browse Gopher in a hierarchical structure (much like WSGopher32, Cyberdog, and Little Gopher Client), read text files, download and save binary files (writing in chunks using `Request().stream()`, and running on another thread), recognize URL: links and use search services.

![](https://github.com/dotcomboom/Pituophis/blob/master/treegopher.png?raw=true)
