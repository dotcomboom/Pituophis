import pituophis

def alt(request):
    if request.path == '/test':
        return [pituophis.Item(text='test!')]

pituophis.serve("127.0.0.1", 70, pub_dir='pub/', alt_handler=alt)  # typical Gopher port is 70
