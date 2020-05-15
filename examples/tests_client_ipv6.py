import pituophis

# Run a server on localhost, port 70

req = pituophis.Request()
req.host = '[::1]'  # or [0:0:0:0:0:0:0:1] (make sure you have [])
resp = req.get()

menu = resp.menu()

for item in menu:
    print('--')
    print(item.type)
    print(item.text)
    print(item.path)
    print(item.host)
    print(item.port)
    print(item.tls)

print('--')
