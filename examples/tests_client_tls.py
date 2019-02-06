import pituophis

#    ____       Here rests my sanity, since *each* time I tested TLS
#   /    \      I wrote "khaze.net" instead of "khzae.net".
#  |2019  |     This goes to the multitude of minutes spent trying to debug
#  | -2019|     TLS, when it was just fine all along and it was just
#  |      |     me misremembering the domain name. I apologize. Nice gopherhole btw~
# ~~~~~~~~~~

req = pituophis.Request()
req.host = input('Host: ')
req.port = int(input('Port: '))  # usually 105
req.tls = True
req.tls_verify = False

print('Sending request:')
print('   Host:', req.host)
print('   Port:', req.port)
print('   Path:', req.path)
print('   Query:', req.query)
print('   TLS:', req.tls)
print('   Verify TLS:', req.tls_verify)

resp = req.get()

menu = resp.menu()

for selector in menu:
    print('--')
    print(selector.type)
    print(selector.text)
    print(selector.path)
    print(selector.host)
    print(selector.port)
    print(selector.tls)

print('--')
