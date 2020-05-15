import pituophis
from pituophis import Item


def handle(request):
    if request.path == '/txt':
        text = """
This is plain text.
Nothing fancy.
        """
        return text
    elif request.path == '/server.png':
        in_file = open("server.png", "rb")  # you'd need a file with the name server.png in the working directory, naturally
        data = in_file.read()
        in_file.close()
        return data
    else:
        menu = [
            Item(text="Path: " + request.path),
            Item(text="Query: " + request.query),
            Item(text="Host: " + request.host),
            Item(text="Port: " + str(request.port)),
            Item(text="Client: " + request.client),
            Item(),
            Item(itype="I", text="View server.png", path="/server.png", host=request.host, port=request.port),
            Item(itype="0", text="View some text", path="/txt", host=request.host, port=request.port)
        ]
        return menu


# serve with custom handler
pituophis.serve("127.0.0.1", 70, handler=handle)
