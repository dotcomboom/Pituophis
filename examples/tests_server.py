import pituophis


def handle(request):
    gmap = [
        "Path: " + request.path,
        "Query: " + request.query,
        "Host: " + request.host,
        "Port: " + str(request.port),
        "Client: " + request.client
    ]
    return pituophis.encode_lines(pituophis.parse_gophermap(gmap))


# serve with custom handler
pituophis.serve("127.0.0.1", 50400, handler=handle)
