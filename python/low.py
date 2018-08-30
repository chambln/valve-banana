# low.py

import os


class Cfg(list):
    def write(self, path):
        # Use .cfg unless another extension is provided for some reason
        root, ext = os.path.splitext(path)
        if not ext:
            path = root + '.cfg'
        # Create path's containing directory if it doesn't already exist
        dirname = os.path.dirname(path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        # Finally, write to file
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

# Programmatically generate a subclass of Prefix for each supported
# cfg command
names = ('Comment', 'Exec', 'Alias', 'Bind', 'Echo', 'Exec', 'Alias', 
         'Bind', 'Unbind', 'BindToggle')
for name in names:
    prefix = name.lower()
    genstring = "{0} = type('{0}', (Prefix,), dict(prefix='{1}'))"
    exec(genstring.format(name, prefix))
    

def test_bind():
    b = Bind('q', 'drop')
    print(b)

    u = Unbind('r')
    print(u)

    e = Echo('foo')
    print(e)

    unbindall = Command('unbindall')
    print(unbindall)

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
