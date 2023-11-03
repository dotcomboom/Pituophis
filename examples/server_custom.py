import pituophis
from pituophis import Item


def handle(request):
    if request.path == '/txt':
        return """
This is plain text.
Nothing fancy.
        """
    elif request.path == '/server.png':
        with open("server.png", "rb") as in_file:
            data = in_file.read()
        return data
    else:
        return [
            Item(text=f"Path: {request.path}"),
            Item(text=f"Query: {request.query}"),
            Item(text=f"Host: {request.host}"),
            Item(text=f"Port: {str(request.port)}"),
            Item(text=f"Client: {request.client}"),
            Item(),
            Item(
                itype="I",
                text="View server.png",
                path="/server.png",
                host=request.host,
                port=request.port,
            ),
            Item(
                itype="0",
                text="View some text",
                path="/txt",
                host=request.host,
                port=request.port,
            ),
        ]


# serve with custom handler
pituophis.serve("127.0.0.1", 70, handler=handle)
