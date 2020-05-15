import pituophis
from pituophis import Item

# TODO: Save comment entries to a file.

comments = []


def handle(request):
    if request.path == '/add':
        menu = [Item(text="Comment added."),
                Item(itype='1', text="View comments", path="/", host=request.host, port=request.port)]
        comments.append(request.query)
        return menu

    menu = [Item(text='Welcome!'),
            Item(),
            Item(itype='7', text="Add a comment.", path="/add", host=request.host, port=request.port),
            Item()]
    if len(comments) == 0:
        menu.append(Item(text="There are no messages yet.. be the first!"))
    for entry in comments:
        menu.append(Item(text=str(entry)))
    return menu


# serve with custom handler
pituophis.serve("127.0.0.1", 70, handler=handle)
