import pituophis

# this is an antique already!

yes = ['y', 'yes', 'yeah', 'yep', 'yup', 'ye', 'sure']

print("""
pituophis testing grounds
would you like to...
1. view a gopher menu, parsed
2. view a gopher menu, unparsed
3. run a search for "test" with veronica 2
4. download a file
5. try it yourself
6. enter a host or URL
""")

choices = ['1', '2', '3', '4', '5', '6']

choice = ''
while not choice in choices:
    choice = input('> ')

host = 'gopher.floodgap.com'
port = 70
path = '/'
query = ''
binary = False
menu = False

if choice == '1':
    menu = True
if choice == '2':
    pass
if choice == '3':
    path = '/v2/vs'
    query = 'test'
if choice == '4':
    binary = True
    #path = '/archive/info-mac/edu/yng/kid-pix.hqx'
    path = '/gopher/clients/win/hgopher2_3.zip'
if choice == '5':
    host = input('host: ')
    port = int(input('port: '))
    path = input('path: ')
    query = input('query: ')
    binary = False
    if input('binary? (y/n): ') in yes:
        binary = True
    menu = False
    if not binary:
        if input('menu? (y/n): ') in yes:
            menu = True
if choice == '6':
    if input('binary? (y/n): ') in yes:
        binary = True
    host = input('host/url: ')

response = pituophis.get(host, port=port, path=path, query=query)
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
                f.write(response.binary)
else:
    if menu:
        print(response.menu())
    else:
        print(response.text())