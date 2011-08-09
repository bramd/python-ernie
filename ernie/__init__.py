"""BERT-ERNIE Library"""

__version__ = "0.0.1"

from SocketServer import TCPServer
from ernie import Ernie, ThreadingTCPServer

def mod(name):
    return Ernie.mod(name)

def start(host='', port=9999, threading=True):
    Ernie.log("Starting")
    server = ThreadingTCPServer if threading else TCPServer
    server((host, port), Ernie).serve_forever()
