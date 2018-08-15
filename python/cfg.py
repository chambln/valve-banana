# cfg.py


class Cfg:
    '''
    Provides methods for building a low-level cfg file line-by-line. 
    Lines are added by keyword (bind, alias, etc.).
    '''
    
    def __init__(self, *lines):
        self.lines = list(lines)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '\n'.join([str(line) for line in self.lines])

    def __add__(self):
        return Cfg(*(self.lines + other.lines))

    def __iter__(self):
        for line in self.lines:
            yield line

    def append(self, line):
        self.lines.append(line)

    def bind(self, *args):
        self.append(Bind(*args))

    def unbind(self, *args):
        self.append(Unbind(*args))

    def alias(self, *args):
        self.append(Alias(*args))

    def exec(self, *args):
        self.append(Exec(*args))

    def cvar(self, *args):
        self.append(Cvar(*args))


class Sentence:
    '''
    Represents a generic line of low-level cfg code. Superclass of 
    keyword-based sentences like bind, alias, etc. as well as cvar 
    assignment.
    '''

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
    '''
    Represents a line of low-level cfg code, specifically a bind 
    sentence, i.e. bind <key> <sentence>
    '''

    def __init__(self, key, action):
        super().__init__('bind', key, action)


class Unbind(Sentence):
    '''
    Represents a line of low-level cfg code, specifically an unbind 
    sentence, i.e. unbind <key>
    '''

    def __init__(self, key):
        super().__init__('unbind', key)


class Alias(Sentence):
    '''
    Represents a line of low-level cfg code, specifically an alias 
    assignment, i.e. alias <alias> <sentence>
    '''

    def __init__(self, alias, sentence):
        super().__init__('alias', alias, sentence)


class Exec(Sentence):
    '''
    Represents a line of low-level cfg code, specifically an instruction 
    to execute another script by reference, i.e. exec <ref>
    '''
    
    def __init__(self, ref):
        super().__init__('exec', ref)


class Cvar(Sentence):
    '''
    Represents a line of low-level cfg code, specifically a cvar 
    assignment, i.e. cvar <value>
    '''

    def __init__(self, cvar, *values):
        super().__init__(cvar, *values)


## TESTING
## =======
#
## init.cfg
#init = Cfg()
#init.unbind('tab')
#keymap = {
#    'enter': 'say',
#    'w': '+forward',
#    's': '+back',
#    'a': '+moveleft',
#    'd': '+moveright',
#    'space': '+jump',
#    'shift': '+_shift'
#}
#for key, sen in keymap.items():
#   init.bind(key, sen)
#init.alias('+_shift', 'exec bind/shift_dn')
#init.alias('-_shift', 'exec bind/shift_up')
#init.cvar('setvideomode', '1920', '1080', '1')
##with open('init.cfg', 'w') as f:
##    f.write(str(init))
#print(init)
#
## shift_dn.cfg
#shift_dn = Cfg()
#shift_dn.bind('enter', 'say_team')
##with open('shift_dn.cfg', 'w') as f:
##    f.write(str(shift_dn))
#print()
#print(shift_dn)
#
## shift_up.cfg
#shift_up = Cfg()
#shift_up.bind('enter', 'say')
##with open('shift_up.cfg', 'w') as f:
##    f.write(str(shift_up))
#print()
#print(shift_up)
