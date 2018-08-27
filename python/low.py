# low.py

import os.path


class Cfg(list):
    def write(self, path):
        root, ext = os.path.splitext(path)
        if not ext:
            path = root + '.cfg'
        with open(path, 'w') as cfg:
            for line in self:
                cfg.write(str(line) + '\n')


class Command(list):
    '''Generic command. Also used for cvar commands since they have no prefix.'''
    def __init__(self, *args):
        list.__init__(self, *args)

    def __str__(self):
        if len(self) == 1:
            # Don't use quotes for singleton commands like unbindall
            return self[0]
        else:
            # Quote only the final argument
            final = '"{}"'.format(self[-1])
            return ' '.join(self[:-1] + [final])


class Echo(Command):
    def __init__(self, msg):
        super().__init__(('echo', msg))
        
class Exec(Command):
    def __init__(self, path):
        super().__init__(('exec', path))
        
class Alias(Command):
    def __init__(self, alias, cmd):
        super().__init__(('alias', alias, cmd))
        
class Bind(Command):
    def __init__(self, key, cmd):
        super().__init__(('bind', key, cmd))

class Unbind(Command):
    def __init__(self, key):
        super().__init__(('unbind', key))

class Unbindall(Command):
    def __init__(self):
        super().__init__(('unbindall',))
        

def test_bind():
    b = Bind('q', 'drop')
    print(b)
    u = Unbind('r')
    print(u)
    e = Echo('foo')
    print(e)

def test_command():
    c = Command(('unbindall',))
    print(c)
    d = Command(('bind', 'enter', 'say'))
    print(d)

def test_cfg():
    c = Cfg([Command(('foo', 'bar'))])
    print(c)
    c.write('foo')

if __name__ == '__main__':
    test_bind()
