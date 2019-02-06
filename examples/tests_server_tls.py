import pituophis
from pituophis import Selector


def handle(request):
    if request.path == '/txt':
        text = """
This is plain text.
Nothing fancy.
        """
        return text
    elif request.path == '/server.png':
        in_file = open("server.png", "rb")
        data = in_file.read()
        in_file.close()
        return data
    else:
        menu = [
            Selector(text="Path: " + request.path),
            Selector(text="Query: " + request.query),
            Selector(text="Host: " + request.host),
            Selector(text="Port: " + str(request.port)),
            Selector(text="Client: " + request.client)
        ]
        return menu


# serve with custom handler
pituophis.serve("127.0.0.1", 50400, handler=handle, tls=True,
                tls_cert_chain='cacert.pem', tls_private_key='privkey.pem')  # typical S/Gopher port is 105
