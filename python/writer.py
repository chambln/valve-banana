# writer.py

class Script(object):
    '''Represents a cfg file as a list of lines of low-level code'''

    def __init__(self, *lines):
        self.lines = lines
        
    def __str__(self):
        '''This is the final output for any given script. You'd write this to a 
        file.'''
        return '\n'.join([str(l) for l in self.lines])

    def append(self, line):
        self.lines.append(line)
        

class Sentence(object):
    '''Represents a sentence; that is, a command that should occupy a line in a 
    cfg file'''

    def __init__(self, command, *args):
        self.command = command  # Its command string, e.g. 'bind'.
        self.args = args        # The parameters passed to it.

    def __str__(self):
        return self.pattern.format(self.command, *self.args)

    @property
    def pattern(self):
        if self.dimension == 1:    # Command and single parameter
            return '{} "{}"'
        elif self.dimension == 2:  # Command and two parameters
            return '{} {} "{}"'
        else:                      # General case, no speech marks
            return ' '.join(['{}' for _ in self.args])

    @property
    def dimension(self):
        return len(self.args)


class Bind(Sentence):
    '''Represents a bind command; i.e. bind <key> <action>'''

    def __init__(self, key, action):
        super().__init__('bind', key, action)


class Unbind(Sentence):
    '''Represents an unbind command; i.e. unbind <key>'''

    def __init__(self, key):
        super().__init__('unbind', key)


class Exec(Sentence):
    '''Represents a script execution command; i.e. exec <ref>; where ref points 
    to the script you want to execute'''

    def __init__(self, ref):
        super().__init__('exec', ref)


class Alias(Sentence):
    '''Represents an alias name; i.e. alias <alias> <action>'''

    def __init__(self, alias, action):
        super().__init__('alias', alias, action)


class Cvar(Sentence):
    '''Represents a game variable assignment; i.e. <cvar> <args>*. This is 
    really just an arbitrary Sentence.'''

    def __init__(self, cvar, *args):
        super().__init__(cvar, *args)
