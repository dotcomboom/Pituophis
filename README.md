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

Pituophis can act as a powerful Gopher server, with full Bucktooth-style gophermap and globbing support. Scripting is also supported through alt handlers (used in the event of a 404) or fully custom handlers (replaces Pituophis' handler entirely).

The simplest method of getting a server up and running is with the `pituophis.serve()` function. See the [examples](https://github.com/dotcomboom/Pituophis/tree/master/examples) and [docs](https://pituophis.readthedocs.io/en/latest/#pituophis.serve) for more information. If you'd like to see a server built with Pituophis that can search an index, try [Gophew](https://github.com/dotcomboom/Gophew).

![server_def](https://github.com/dotcomboom/Pituophis/blob/master/server_def.png?raw=true)

## Client
Pituophis can also grab files and parse menus from Gopher servers. Simple fetching is done with `Request().get()` and `get()`, and `Request().stream()` can be used for lower-level access as a BufferedReader.  The `get` functions return a Response type. [See the docs](https://pituophis.readthedocs.io/en/latest/index.html) for more information.

### TreeGopher
An interactive demo of Pituophis' client features is provided in the form of [TreeGopher](https://github.com/dotcomboom/Pituophis/blob/master/TreeGopher.py), a graphical Gopher client in ~200 lines of code. It uses Pituophis, [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI), and [Pyperclip](https://pypi.org/project/pyperclip). It can browse Gopher in a hierarchical structure (similarly to WSGopher32, Cyberdog, and [Little Gopher Client](http://runtimeterror.com/tools/gopher/)), read text files, download and save binary files (writing in chunks using `Request().stream()`, and running on another thread), recognize URL: links and use search services.

![](https://github.com/dotcomboom/Pituophis/blob/master/treegopher.png?raw=true)

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
Requests can also be created from a URL:
```python
import pituophis
req = pituophis.parse_url('gopher://gopher.floodgap.com/7/v2/vs%09food')
print('Getting', req.url())
rsp = req.get()
print(rsp.text())
```