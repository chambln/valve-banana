# cfg.py

import os


class Cfg:
    '''
    Provides methods for building a low-level cfg file line-by-line. 
    Lines are added by keyword (bind, alias, etc.).
    '''
    
    def __init__(self, path, *lines):
        self.path = path
        self.lines = list(lines)

    def __add__(self):
        return Cfg(*(self.lines + other.lines))

    def __repr__(self):
        return "./{}.cfg with {} lines".format(self.path, len(self))

    def __len__(self):
        return len(self.lines)

    def __bool__(self):
        return bool(self.lines)

    def __iter__(self):
        for line in self.lines:
            yield line

    def __getitem__(self, key):
        return self.lines[key]

    # Input
    def append(self, line):
        self.lines.append(line)
        # Print this for debugging purposes
        print('appended' line, 'to', self.path)

    # Append lines by keyword
    def   bind(self, *args):    self.append(  Bind(*args))
    def unbind(self, *args):    self.append(Unbind(*args))
    def  alias(self, *args):    self.append( Alias(*args))
    def   exec(self, *args):    self.append(  Exec(*args))
    def   cvar(self, *args):    self.append(  Cvar(*args))

    # Output
    def __str__(self):
        '''This is the final string output that you'd write to a file'''
        return '\n'.join([str(line) for line in self])

    def write(self):
        # Create my path's directory if it doesn't exist already
        dirname = os.path.dirname(self.path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
            print('Made directory {}/'.format(dirname))
        # Write my string to my path
        with open(self.path+'.cfg', 'w') as f:
            f.write(str(self))
            print('Wrote {} lines to {}.cfg'.format(len(self), self.path))


class Sentence:
    '''
    Represents a generic line of low-level cfg code. Superclass of 
    keyword-based sentences like bind, alias, etc. as well as cvar 
    assignment.
    '''

    def __init__(self, *args):
        self.args = args

    def __repr__(self):
        args = ', '.join([repr(arg) for arg in self.args[1:]])
        return '{}({})'.format(self.__class__.__name__, args)

    def __str__(self):
        return self.syntax.format(*self.args)

    @property
    def syntax(self):
        '''
        Return the command keyword followed by space-separated 
        arguments, but only quote the last one.
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

    def __init__(self, key, *actions):
        self.actions = actions
        super().__init__('bind', key, '; '.join(self.actions))


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

    def __repr__(self):
        args = ', '.join([repr(arg) for arg in self.args])
        return '{}({})'.format(self.__class__.__name__, args)


#
## TESTING
## =======
#
## init.cfg
#init = Cfg('init')
#init.unbind('tab')
#mybinds = {
#    'enter': 'say',
#    'w': '+forward',
#    's': '+back',
#    'a': '+moveleft',
#    'd': '+moveright',
#    'space': '+jump',
#    'shift': '+_shift'
#}
#for key, sen in mybinds.items():
#   init.bind(key, sen)
#init.alias('+_shift', 'exec bind/shift_dn')
#init.alias('-_shift', 'exec bind/shift_up')
#init.cvar('setvideomode', '1920', '1080', '1')
#print('\n{}:'.format(repr(init)))
#print(init)
#
## shift_dn.cfg
#shift_dn = Cfg('shift_dn')
#shift_dn.bind('enter', 'say_team')
#print('\n{}:'.format(repr(shift_dn)))
#print(shift_dn)
#
## shift_up.cfg
#shift_up = Cfg('shift_up')
#shift_up.bind('enter', 'say')
#print('\n{}:'.format(repr(shift_up)))
#print(shift_up)
