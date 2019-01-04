#!/path/to/python/bin
from flup.server.fcgi import WSGIServer
from main import app

if __name__ == '__main__':
    WSGIServer(app, bindAddress='/path/to/api.sock').run()