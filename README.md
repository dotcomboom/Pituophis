# Pituophis
Experimental Gopher client/server library for Python
## Client
Pituophis can grab files and text from Gopher servers through the `get()` function.
### Examples
Getting menus and files as plain text:
```python
pituophis.get('gopher.floodgap.com').text()
pituophis.get('gopher://gopher.floodgap.com/1/').text()
pituophis.get('gopher://gopher.floodgap.com:70/0/gopher/proxy').text()
pituophis.get(host='gopher.floodgap.com', port=70, path='/').text()
pituophis.get(host='gopher.floodgap.com', port=70, path='/gopher/proxy').text()
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
req.host = 'gopher.floodgap.com'
req.port = 70
req.type = '7'
req.path = '/v2/vs'
req.query = 'food'
req.tls = False
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