from pituophis import get

yes = ['y', 'yes', 'yeah', 'yep', 'yup', 'ye', 'sure']

print("""
pituophis testing grounds
would you like to...
1. view a gopher menu over TLS, unparsed (not working right now)
2. view a gopher menu, parsed (not yet implemented)
3. view a gopher menu, unparsed
4. run a search for "test" with veronica 2
5. download a file
6. try it yourself
7. enter a host or URL
""")

choices = ['1', '2', '3', '4', '5', '6', '7']

choice = ''
while not choice in choices:
    choice = input('> ')

host = 'gopher.floodgap.com'
port = 70
path = '/'
query = ''
binary = False
menu = False
tls = False

if choice == '1':
    menu = True
    host = 'khaze.net'
    port = 105
    tls = True
if choice == '2':
    menu = True
if choice == '3':
    pass
if choice == '4':
    path = '/v2/vs'
    query = 'test'
if choice == '5':
    binary = True
    #path = '/archive/info-mac/edu/yng/kid-pix.hqx'
    path = '/gopher/clients/win/hgopher2_3.zip'
if choice == '6':
    host = input('host: ')
    port = int(input('port: '))
    tls = False
    if input('tls? (y/n): ') in yes:
        tls = True
    path = input('path: ')
    query = input('query: ')
    binary = False
    if input('binary? (y/n): ') in yes:
        binary = True
    menu = False
    if not binary:
        if input('menu? (y/n): ') in yes:
            menu = True
if choice == '7':
    if input('binary? (y/n): ') in yes:
        binary = True
    host = input('host/url: ')

response = get(host, port=port, path=path, query=query, tls=tls)
if binary:
    print("""
    what to do with this binary?
    1. decode utf-8
    2. save to disk
    """)
    choices = ['1', '2']
    choice = ''
    while not choice in choices:
        choice = input('> ')
    if choice == '1':
        print(response.text())
    else:
        if choice == '2':
            suggested_filename = path.split('/')[len(path.split('/')) - 1]
            filename = input('filename (' + suggested_filename + ')? ')
            if filename == '':
                filename = suggested_filename
            with open(filename, "wb") as f:
                f.write(response.binary())
else:
    if menu:
        print(response.menu())
    else:
        print(response.text())