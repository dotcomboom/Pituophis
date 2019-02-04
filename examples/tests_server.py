import pituophis
from pituophis import Selector


# TODO: Serve a binary

def handle(request):
    if request.path == '/txt':
        text = """
This is plain text.

Nothing fancy.
        """
        return pituophis.encode(text)
    elif request.path == '/bin':
        return pituophis.encode('nyi')
    else:
        menu = [
            Selector(text="Path: " + request.path),
            Selector(text="Query: " + request.query),
            Selector(text="Host: " + request.host),
            Selector(text="Port: " + str(request.port)),
            Selector(text="Client: " + request.client),
            Selector(),
            Selector(text="This is the default Pituophis handler.")
        ]
        return pituophis.encode(menu)


# serve with custom handler
pituophis.serve("127.0.0.1", 50400, handler=handle)
