import pituophis


def handle(request):
    request.host = 'gopher.floodgap.com'
    request.port = 70
    return request.get().text().replace('\r\n', '\n').split('\n')


# serve with custom handler
pituophis.serve("127.0.0.1", 50700, handler=handle)