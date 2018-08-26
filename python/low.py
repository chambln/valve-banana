# low.py

import os.path


class Cfg(object):
    '''Low level *.cfg file'''

    def __init__(self, *commands):
        self.commands = list(commands)

    def __repr__(self):
        return '<Cfg object with {} commands>'.format(len(self))

    def __str__(self):
        '''Return my commands with carriage returns after them'''
        return ''.join([str(command)+'\n' for command in self.commands])

    def __len__(self):
        return len(self.commands)

    def __iter__(foo, self):
        for command in self.commands:
            yield command

    def write(self, path):
        # Use '.cfg' unless an extension was provided
        root, ext = os.path.splitext(path)
        if not ext:
            path = root + '.cfg'
        # Write to file
        with open(path, 'w') as cfg:
            cfg.write(str(self))
        # Print what just happened to help with debugging
        print('Wrote {} commands to {}'.format(len(self), path))
    
    def append(self, command):
        '''Append a command to this file'''
        self.commands.append(command)

    def set_generators(cls):
        generators = ('Command', 'Bind', 'Unbind', 'Alias', 'Unalias', 
                      'Comment', 'Exec', 'Cvar', 'Unbindall', 
                      'BindToggle')
        for gen in generators:
            setattr(Cfg, gen.lower(), eval('lambda self, *args: self.append({}(*args))'.format(gen)))


class Command(object):
    '''Represents a generic command that belongs to a *.cfg file'''

    def __init__(self, *params):
        self.params = params

    def __repr__(self):
        args = [repr(i) for i in self.params]
        return 'Command({})'.format(', '.join(args))

    def __len__(self):
        return len(self.params)

    def __str__(self):
        '''
        Return my low level line of code, surrounding only my last 
        argument with quote marks. Single argument commands such as 
        unbindall have no quotes.
        '''
        if len(self) > 1:
            # Multiple argument command
            args, last = self.params[:-1], self.params[-1]
            return ' '.join(args) + ' "{}"'.format(last)
        else:
            # Single argument command, so no quotes
            return self.params[0]


class Comment(Command):
    def __init__(self, comment):
        super().__init__('// ', comment)

    def __str__(self):
        '''Override: don't use quotes for comments'''
        return '{}{}'.format(*self.params)


class Exec(Command):
    def __init__(self, path):
        super().__init__('exec', path)


class Cvar(Command):
    def __init__(self, cvar, value):
        super().__init__(cvar, value)


class Alias(Command):
    def __init__(self, alias, cmd):
        super().__init__('alias', alias, cmd)


class Unalias(Alias):
    def __init__(self, alias):
        super().__init__(alias, '')


class Bind(Command):
    def __init__(self, key, cmd):
        super().__init__('bind', key, cmd)


class Unbind(Command):
    def __init__(self, key):
        super().__init__('unbind', key)


class Unbindall(Command):
    def __init__(self):
        super().__init__('unbindall')

    def __str__(self):
        '''Override: don't use quotes at all'''
        return '{}'.format(*self.params)


class BindToggle(Command):
    def __init__(self, key, cvar):
        super().__init__('BindToggle', key, cvar)


def test_Command():
    cmd = Command('bind', 'enter', 'say')
    print('repr(cmd) ==', repr(repr(cmd)))
    print(' str(cmd) ==', repr( str(cmd)))

def test_Cfg():
    cfg = Cfg('bind enter say', 'bind space +jump')
    print('repr(cfg) ==', repr(repr(cfg)))
    print(' str(cfg) ==', repr( str(cfg)))
    cfg.write('foo')

def test():
    cfg = Cfg()
    cfg.set_generators()
    cfg.cvar('hud_scaling', '0.90')
    cfg.bind('w', '+forward')
    cfg.bind('d', '+back')
    cfg.unbindall()
    cfg.alias('foo', 'bar')
    cfg.exec('mode/sandbox.cfg')
    cfg.comment('TODO: ALL THE THINGS')
    print('repr(cfg) ==', repr(repr(cfg)))
    cfg.write('test')

if __name__ == '__main__':
    test()
    pass
