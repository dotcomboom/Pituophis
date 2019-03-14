import pituophis

# Run a server on localhost, port 70

req = pituophis.Request()
req.host = '[::1]'  # or [0:0:0:0:0:0:0:1] (make sure you have [])
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
