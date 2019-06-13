import pituophis

def alt(request):
    if request.path == '/test':
        return [pituophis.Selector(text='test!')]

pituophis.serve("127.0.0.1", 50400, pub_dir='pub/', alt_handler=alt, tls=False)  # typical Gopher port is 70
