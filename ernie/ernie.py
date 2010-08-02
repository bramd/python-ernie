import logging
import bert
import struct
import SocketServer


class Ernie(SocketServer.StreamRequestHandler):
    mods = {}
    logger = None
    
    @classmethod
    def mod(cls, name):
        return cls.mods.setdefault(name, Mod(name))
    
    @classmethod
    def logfile(cls, file):
        logging.basicConfig(filename=file,level=logging.DEBUG)
        cls.logger = logging.getLogger('ernie')
    
    @classmethod
    def log(cls, text):
        if cls.logger != None:
            cls.logger.debug(text)
    
    def dispatch(self, mod, fun, args):
        try:
            mod = Ernie.mods[mod]
        except KeyError:
            raise ServerError("No such module '" + mod + "'")
        
        try:
            func = mod.funs[fun]
        except KeyError:
            raise ServerError("No such function '" + mod + ":" + fun + "'")
        
        return func(*args)
    
    def read_size(self):
        raw = self.rfile.read(4)
        return struct.unpack('!L', raw)[0] if raw else None
    
    def read_berp(self):
        packet_size = self.read_size()
        return bert.decode(self.rfile.read(packet_size)) if packet_size else None
    
    def write_berp(self, obj):
        data = bert.encode(obj)
        self.wfile.write(struct.pack("!L", len(data)))
        self.wfile.write(data)
        self.wfile.flush()
    
    def handle(self):
        ipy = self.read_berp()
        
        if not ipy:
            print 'Could not read BERP length header. Ernie server may have gone away. Exiting now.'
            exit()
        
        self.log("-> " + ipy.__str__())
        
        if len(ipy) is 4 and ipy[0] == bert.Atom('call'):
            mod, fun, args = ipy[1:4]
            
            try:
                res = self.dispatch(mod, fun, args)
            except ServerError, e:
                opy = (bert.Atom('error'), (bert.Atom('server'), 0, str(type(e)), str(e), ''))
            except Exception, e:
                opy = (bert.Atom('error'), (bert.Atom('user'), 0, str(type(e)), str(e), ''))
            else:
                opy = (bert.Atom('reply'), res)
            finally:
                self.log("<- " + opy.__str__())
                self.write_berp(opy)
                
        elif len(ipy) is 4 and ipy[0] == bert.Atom('cast'):
            mod, fun, args = ipy[1:4]
            try:
                res = self.dispatch(mod, fun, args)
            finally:
                self.write_berp(bert.Atom('noreply'))
        else:
            opy = (bert.Atom('error'), (bert.Atom('server'), 0, "Invalid request: " + ipy.__str__()))
            self.log("<- " + opy.__str__())
            self.write_berp(opy)
    

class ServerError(Exception):
    def __str__(self):
        return repr(self.args[0])


class Mod(object):
    def __init__(self, name):
        self.name = name
        self.funs = {}
    
    def fun(self, name, func):
        self.funs[name] = func
