# low.py

import os.path


class Cfg(list):
    '''Subclass of list so that each element is a line of the file. Do 
    Cfg().write(path) to export the file.'''

    def write(self, path):
        '''Export as file to path. Uses .cfg if no extension is 
        provided.'''
        root, ext = os.path.splitext(path)
        self.path = path if ext else root + '.cfg'
        with open(path, 'w') as cfg:
            for line in self:
                cfg.write(line + '\n')


class Command(list):
    _prefix = []

    def __str__(self):
        last = '"{}"'.format(self.pop())
        return ' '.join(self._prefix + self + [last])


class Alias(Command):
    _prefix = ['alias',]


class Bind(Command):
    _prefix = ['bind',]


class Unbind(Command):
    _prefix = ['unbind',]


def test():
    foo = Command(('foo',))
    print(foo)

    c = Command(('foo', 'bar', 'baz', 'qux'))
    print(c)

    a = Alias(('+info', 'cl_showscores 1'))
    print(a)

    b = Bind(('f', '+moveright'))
    print(b)

    u = Unbind(('enter',))
    print(u)

    hs = Command(('hud_scaling', '0.90'))

if __name__ == '__main__':
    test()
