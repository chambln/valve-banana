# low.py

import os.path


class Cfg(object):
    '''Low level *.cfg file'''
    def __init__(self, *lines):
        self.lines = lines

    def __repr__(self):
        return '<Cfg object with {} lines>'.format(len(self))

    def __str__(self):
        '''Return my lines with carriage returns after them'''
        return ''.join([line+'\n' for line in self.lines])

    def __len__(self):
        return len(self.lines)

    def __iter__(foo, self):
        for line in self.lines:
            yield line
    
    def append(self, line):
        '''Append a line to this file'''
        self.lines.append(line)

    def write(self, path):
        # Use '.cfg' unless an extension was provided
        root, ext = os.path.splitext(path)
        if not ext:
            path = root + '.cfg'
        # Write to file
        with open(path, 'w') as cfg:
            cfg.write(str(self))
        # Print what just happened to help with debugging
        print('Wrote {} lines to {}'.format(len(self), path))


class Command:
    '''Represents any command that belongs to a *.cfg file'''

    def __init__(self, *params):
        self.params = params

    def __repr__(self):
        return 'Command({})'.format(
            ', '.join([repr(i) for i in self.params])
        )

    def __str__(self):
        '''
        Return my low level line of code, surrounding only my last 
        argument with quote marks.
        '''
        # Surround only the last argument with ""
        args, last = self.params[:-1], self.params[-1]
        return ' '.join(args) + ' "{}"'.format(last)


def test_Command():
    cmd = Command('bind', 'enter', 'say')
    print('repr(cmd):', repr(repr(cmd)))
    print(' str(cmd):', repr( str(cmd)))

def test_Cfg():
    cfg = Cfg('bind enter say', 'bind space +jump')
    print('repr(cfg):', repr(repr(cfg)))
    print(' str(cfg):', repr( str(cfg)))
    cfg.write('foo')

if __name__ == '__main__':
    test_Command()
