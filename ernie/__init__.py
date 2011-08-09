"""BERT-ERNIE Library"""

__version__ = "0.0.1"

import SocketServer
from ernie import Ernie

def mod(name):
    return Ernie.mod(name)

def start(host='', port=9999):
    Ernie.log("Starting")
    SocketServer.TCPServer((host, port), Ernie).serve_forever()
