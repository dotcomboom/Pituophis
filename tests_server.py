from pituophis import serve, parse_gophermap


def handle(request):
    gmap = [
        "Path: " + request.path,
        "Query: " + request.query,
        "Host: " + request.host,
        "Port: " + str(request.port)
    ]
    return parse_gophermap(gmap)


# serve with custom handler
serve("127.0.0.1", 50500, customHandler=handle)
