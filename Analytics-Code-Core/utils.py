
class Frozen:
    def __setattr__(self, key, value):
        if hasattr(self, 'frozen') and not hasattr(self, key):
            raise TypeError( 'Cannot add attribute "%s" to %r'  % (key,self) )
        object.__setattr__(self, key, value)



