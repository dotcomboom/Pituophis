import pituophis
from pituophis import Selector

# TODO: Save comment entries to a file.

comments = []


def handle(request):
    if request.path == '/add':
        menu = [Selector(text="Comment added."),
                Selector(itype='1', text="View comments", path="/", host=request.host, port=request.port)]
        comments.append(request.query)
        return menu

    menu = [Selector(text='Welcome!'),
            Selector(),
            Selector(itype='7', text="Add a comment.", path="/add", host=request.host, port=request.port),
            Selector()]
    if len(comments) == 0:
        menu.append(Selector(text="There are no messages yet.. be the first!"))
    for entry in comments:
        menu.append(Selector(text=str(entry)))
    return menu


# serve with custom handler
pituophis.serve("127.0.0.1", 50000, handler=handle)
