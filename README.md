# Pituophis
Experimental Gopher client/server library for Python
## Client
Pituophis can grab files and text from Gopher servers through the `get()` function.
### Examples
Getting menus and files as plain text:
```python
get('gopher.floodgap.com').text()
get('gopher://gopher.floodgap.com/1/').text()
get('gopher://gopher.floodgap.com:70/0/gopher/proxy').text()
get(host='gopher.floodgap.com', port=70, path='/').text()
get(host='gopher.floodgap.com', port=70, path='/gopher/proxy').text()
```
Using search services:
```python
get('gopher://gopher.floodgap.com:70/7/v2/vs?toast').text()
get(host='gopher.floodgap.com', port=70, path='/v2/vs', query='toast').text()
```
Downloading a binary:
```python
get('gopher://gopher.floodgap.com:70/9/gopher/clients/win/hgopher2_3.zip').binary()
get(host='gopher.floodgap.com', port=70, path='/gopher/clients/win/hgopher2_3.zip').binary()
```
## Server
Pituophis can be used with a custom handler to serve Gopher requests. Primitive Bucktooth-like gophermap parsing (excluding path resolution) is available.

![server](https://github.com/dotcomboom/Pituophis/blob/master/server.png?raw=true)
## Planned features/Wishlist
Client:
- Menu parsing

Server:
- Server default handler with proper gophermap and directory/file serving
- Asynchronous connections? Right now everything is on one thread, one request at a time

Both:
- SSL/TLS support ([S/Gopher](https://umbrellix.net/software:ugopherserver) on port 105)
- Less bugs
- Documentation, oh, documentation...
- ~~Prego~~