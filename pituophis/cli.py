import importlib
import sys
import pituophis

# check if the user is running the script with the correct number of arguments
if len(sys.argv) < 2:
    # if not, print the usage
    print('usage: pituophis [command] cd [options]')
    print('Commands:')
    print('  serve [options]')
    print('  fetch [url] [options]')
    print('Server Options:')
    print('  -H, --host=HOST\t\tAdvertised host (default: 127.0.0.1)')
    print('  -p, --port=PORT\t\tPort to bind to (default: 70)')
    print('  -a, --advertised-port=PORT\tPort to advertise')
    print('  -d, --directory=DIR\t\tDirectory to serve (default: pub/)')
    print('  -A, --alt-handler=HANDLER\tAlternate handler to use if 404 error is generated (python file with it defined as "def alt(request):")')
    print('  -s, --send-period\t\tSend a period at the end of each response (default: False)')
    print('  -D, --debug\t\t\tPrint requests as they are received (default: False)')
    print('  -v, --version\t\t\tPrint version')
    print('Fetch Options:')
    print('  -o, --output=FILE\t\tFile to write to (default: stdout)')
else:
    # check if the user is serving or fetching
    if sys.argv[1] == 'serve':
        # check for arguments
        # host
        host = '127.0.0.1'
        if '-H' in sys.argv or '--host' in sys.argv:
            host = sys.argv[sys.argv.index('-H') + 1]
        # port
        port = 70
        if '-p' in sys.argv or '--port' in sys.argv:
            port = int(sys.argv[sys.argv.index('-p') + 1])
        # advertised port
        advertised_port = None
        if '-a' in sys.argv or '--advertised-port' in sys.argv:
            advertised_port = int(sys.argv[sys.argv.index('-a') + 1])
        # directory
        pub_dir = 'pub/'
        if '-d' in sys.argv or '--directory' in sys.argv:
            pub_dir = sys.argv[sys.argv.index('-d') + 1]
        # alternate handler
        alt_handler = False
        if '-A' in sys.argv or '--alt-handler' in sys.argv:
            alt_handler = sys.argv[sys.argv.index('-A') + 1]
            # get the function from the file
            alt_handler = getattr(
            importlib.import_module(alt_handler), 'handler')
        
        # send period
        send_period = False
        if '-s' in sys.argv or '--send-period' in sys.argv:
            send_period = True
        # debug
        debug = False
        if '-D' in sys.argv or '--debug' in sys.argv:
            debug = True
        # start the server
        pituophis.serve(host=host, port=port, advertised_port=advertised_port,
            handler=pituophis.handle, pub_dir=pub_dir, alt_handler=alt_handler,
            send_period=send_period, debug=debug)
    elif sys.argv[1] == 'fetch':
        # check for arguments
        # url
        url = sys.argv[2]
        # output file
        output = 'stdout'
        if '-o' in sys.argv or '--output' in sys.argv:
            output = sys.argv[sys.argv.index('-o') + 1]
        # start the fetch
        o = pituophis.get(url)
        if output == 'stdout':
            sys.stdout.buffer.write(o.binary)
        else:
            with open(output, 'wb') as f:
                f.write(o.binary)
                f.close()