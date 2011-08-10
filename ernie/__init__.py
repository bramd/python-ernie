"""BERT-ERNIE Library"""

__version__ = "0.0.2"

from SocketServer import TCPServer
from ernie import Ernie, ThreadingTCPServer

def mod(name):
    return Ernie.mod(name)

def register_module(module):
  """
  Register a subset of functions to be remotely accessible via ernie.
  
  This function assumes the given module has a list named 'ernie_func_list'.
  The functions in that list are registered with ernie, under an external
  module with the same name as the internal module.
  """

  for func in module.ernie_func_list:
    Ernie.mod(module.__name__).register(func)

def start(host='', port=9999, threading=True):
    Ernie.log("Starting")
    server = ThreadingTCPServer if threading else TCPServer
    server((host, port), Ernie).serve_forever()
