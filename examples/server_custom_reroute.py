import pituophis

# This example directly reroutes the client's request to another server and port.
# It then fetches the request, then sends the received binary data.

def handle(request):
    request.host = 'gopher.floodgap.com'
    request.port = 70
    resp = request.get()
    return resp.binary

# serve with custom handler
pituophis.serve("127.0.0.1", 70, handler=handle)
