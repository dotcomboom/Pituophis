import pituophis

# This example directly reroutes the client's request to another server and port.
# It then fetches the request, then decodes it to text.
# Since, right now, the serve() function expects an array of lines to send,
# \r\n (Windows newlines) are replaced with \n (Unix newlines) just in case, and
# then that's split into an array.

# The serve() function, of course, then sends each line followed by \r\n (as per the standard)


def handle(request):
    request.host = 'gopher.floodgap.com'
    request.port = 70
    return request.get().text().replace('\r\n', '\n').split('\n')


# serve with custom handler
pituophis.serve("127.0.0.1", 50700, handler=handle)