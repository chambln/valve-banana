# sentence.py

class Sentence:
    '''Represents a line of low-level cfg code'''

    def __init__(self, *args):
        self.args = args

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.syntax.format(*self.args)

    @property
    def syntax(self):
        '''
        Return the command keyword followed by space-separated 
        parameters, but only quote the last one.
        '''
        n = self.dimension - 1      # Number of unquoted parameters
        return n * '{} ' + '"{}"'   # Quote only the last parameter
        
    @property
    def dimension(self):
        return len(self.args)


class Bind(Sentence):
    '''Represents a bind sentence, i.e. bind <key> <sentence>'''

    def __init__(self, key, action):
        super().__init__('bind', key, action)


class Unbind(Sentence):
    '''Represents an unbind sentence, i.e. unbind <key>'''

    def __init__(self, key):
        super().__init__('unbind', key)


class Alias(Sentence):
    '''Represents an alias assignment, i.e. alias <alias> <sentence>'''

    def __init__(self, alias, sentence):
        super().__init__('alias', alias, sentence)


class Exec(Sentence):
    '''
    Represents an instruction to execute another script by reference, 
    i.e. exec <ref>
    '''
    
    def __init__(self, ref):
        super().__init__('exec', ref)


class Cvar(Sentence):
    '''Represents a cvar assignment, i.e. cvar <value>'''

    def __init__(self, cvar, *values):
        super().__init__(cvar, *values)
