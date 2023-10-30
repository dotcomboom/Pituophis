# Pituophis
[![Documentation Status](https://readthedocs.org/projects/pituophis/badge/?version=latest)](https://pituophis.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://img.shields.io/pypi/v/Pituophis.svg)](https://pypi.python.org/pypi/Pituophis/)
[![PyPI license](https://img.shields.io/pypi/l/Pituophis.svg)](https://pypi.python.org/pypi/Pituophis/)

Python 3 library for building Gopher clients and servers

## Installation
At a prompt, run `pip3 install pituophis` or `pip install pituophis` depending on your setup. You'll be able to import the package with `import pituophis`.

## Features

- Make and send Gopher requests with the `Request` class
- URL parsing with `pituophis.parse_url()`
- Parse and iterate through Gopher menus with `Response.menu()`
- Host Gopher servers on Python 3.7+, accepting requests asynchronously (using the same `Request` class)
- Serve directories, files, and gophermaps out of the box from a publish directory ('pub/' by default) with the default handler
- Use either a custom handler altogether or a handler to use when the default handler encounters a 404 for dynamic functionality

## Server

Pituophis can act as a powerful Gopher server, with full Bucktooth-style gophermap and globbing support. Scripting is also supported through alt handlers (used in the event of a 404) or fully custom handlers (replaces Pituophis' handler entirely).

The simplest method of getting a server up and running is with the `pituophis.serve()` function. See the [examples](https://github.com/dotcomboom/Pituophis/tree/master/examples) and [docs](https://pituophis.readthedocs.io/en/latest/#pituophis.serve) for more information. If you'd like to see a server built with Pituophis that can search an index, try [Gophew](https://github.com/dotcomboom/Gophew).

![server_def](https://github.com/dotcomboom/Pituophis/blob/master/server_def.png?raw=true)

### Quick Start
A simple quick-start snippet is the following:
```py
import pituophis
pituophis.serve('127.0.0.1', 7070, pub_dir='pub/')  # typical Gopher port is 70
```

Here's a basic alt handler, if you're familiar with Python scripting and would like to add more interactivity to your server:

```py
def alt(request):
    if request.path == '/test':
        return [pituophis.Item(text='test!')]
```

You can return a list of Item objects, bytes, or text. To use your alt handler, add the argument `alt_handler=alt` to your serve() like this:

```py
pituophis.serve("127.0.0.1", 7070, pub_dir='pub/', alt_handler=alt)
```

## Client
Pituophis can also grab files and parse menus from Gopher servers. Simple fetching is done with `Request().get()` and `get()`, and `Request().stream()` can be used for lower-level access as a BufferedReader.  The `get` functions return a Response type. [See the docs](https://pituophis.readthedocs.io/en/latest/index.html) for more information.

### TreeGopher
An interactive demo of Pituophis' client features is provided in the form of [TreeGopher](https://github.com/dotcomboom/Pituophis/blob/master/TreeGopher.py), a graphical Gopher client in <250 lines of code. It uses Pituophis, [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI), and [Pyperclip](https://pypi.org/project/pyperclip). It can browse Gopher in a hierarchical structure (similarly to WSGopher32, Cyberdog, and [Little Gopher Client](http://runtimeterror.com/tools/gopher/)), cache menus, read text files, download and save binary files (writing in chunks using `Request().stream()`, and running on another thread), recognize URL: links and use search services.

![](https://github.com/dotcomboom/Pituophis/blob/master/treegopher.png?raw=true)

### Examples
Getting menus and files as plain text:
```python
pituophis.get('gopher.floodgap.com').text()
pituophis.get('gopher://gopher.floodgap.com/1/').text()
pituophis.get('gopher://gopher.floodgap.com:70/0/gopher/proxy').text()
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
