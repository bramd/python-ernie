"""BERT-ERNIE Library"""

__version__ = "0.0.1"

from ernie import Ernie

def mod(name):
    return Ernie.mod(name)

def start():
    server = Ernie()
    server.start()