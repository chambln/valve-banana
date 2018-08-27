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
        list.__init__(self, args)

    def __str__(self):
        if len(self) == 1:
            # Don't use quotes for singleton commands like unbindall
            return self[0]
        else:
            # Quote only the final arg, removing any existing quotes
            final = '"{}"'.format(str(self[-1]).replace('"', ''))
            return ' '.join(self[:-1] + [final])


class Prefix(Command):
    prefix = 'PREFIX'
    def __init__(self, *args):
        super().__init__(self.prefix, *args)


class Echo(Prefix):
    prefix = 'echo'
        
class Exec(Prefix):
    prefix = 'exec'
        
class Alias(Prefix):
    prefix = 'alias'
        
class Bind(Prefix):
    prefix = 'bind'

class Unbind(Prefix):
    prefix = 'unbind'


def test_bind():
    b = Bind('q', 'drop')
    print(b)
    u = Unbind('r')
    print(u)
    e = Echo('foo')
    print(e)
    unbindall = Command('unbindall')
    print(unbindall)
    p = Prefix('foo', 'bar')
    print(p)
    nested = Bind('p', Exec('myscript.cfg'))
    print(nested)

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
