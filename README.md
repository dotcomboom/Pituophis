# Pituophis
Experimental Gopher client/server library for Python
## Client
Pituophis can grab files and text from Gopher servers through the `get()` function.
### Examples
Getting menus and files as plain text:
```python
get(host='gopher.floodgap.com', port=70, path='/')
get(host='gopher.floodgap.com', port=70, path='/gopher/proxy')
```
Using search services:
```python
get(host='gopher.floodgap.com', port=70, path='/v2/vs', query='toast')
```
Downloading a binary:
```python
get(host='gopher.floodgap.com', port=70, path='/gopher/clients/win/hgopher2_3.zip', binary=True)
```
## Server
Pituophis can be used with a custom handler to serve Gopher requests. Primitive Bucktooth-like gophermap parsing (excluding path resolution) is available.

![server](https://github.com/dotcomboom/Pituophis/blob/master/server.png?raw=true)
## Planned features/Wishlist
Both:
- SSL/TLS support ([S/Gopher](https://umbrellix.net/software:ugopherserver) on port 105)
- Less bugs
- ~~Prego~~

Client:
- Client menu parsing

Server:
- Server default handler with proper gophermap and directory/file serving
- Asynchronous connections? Right now everything is on one thread, one request at a time
