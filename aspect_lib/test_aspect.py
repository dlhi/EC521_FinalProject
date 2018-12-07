import aspectlib, socket, sys
from aspectlib import debug

aspectlib.weave(socket.socket, debug.log(print_to=sys.stdout, stacktrace=None,), lazy=True,)

http = b'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n'

s = socket.socket()
s.connect(('google.com', 80))
s.send(http)
s.recv(8)
s.close()