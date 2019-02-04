import pituophis

req = pituophis.Request()
req.host = 'khaze.net'
req.port = 105
req.tls = True

print('Sending request:')
print('   Host:', req.host)
print('   Port:', req.port)
print('   Path:', req.path)
print('   Query:', req.query)
print('   TLS:', req.tls)

resp = req.get()

print()
print(resp.text())
