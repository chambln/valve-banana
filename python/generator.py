# generator.py

import writer


class Bind(writer.Sentence):
    '''Represents a bind command; i.e. bind <key> <action>'''

    def __init__(self, key, action):
        super().__init__('bind', key, action)


class Unbind(writer.Sentence):
    '''Represents an unbind command; i.e. unbind <key>'''

    def __init__(self, key):
        super().__init__('unbind', key)


class Exec(writer.Sentence):
    '''Represents a script execution command; i.e. exec <ref>; where ref points 
    to the script you want to execute'''

    def __init__(self, ref):
        super().__init__('exec', ref)


class Alias(writer.Sentence):
    '''Represents an alias name; i.e. alias <alias> <action>'''

    def __init__(self, alias, action):
        super().__init__('alias', alias, action)


class Cvar(writer.Sentence):
    '''Represents a game variable assignment; i.e. <cvar> <args>*. This is 
    really just an arbitrary Sentence.'''

    def __init__(self, cvar, *args):
        super().__init__(cvar, *args)
