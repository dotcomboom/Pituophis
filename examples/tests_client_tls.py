import pituophis

req = pituophis.Request()
req.host = input()
req.port = 105
req.tls = True

print('Sending request:')
print('   Host:', req.host)
print('   Port:', req.port)
print('   Path:', req.path)
print('   Query:', req.query)
print('   TLS:', req.tls)

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
