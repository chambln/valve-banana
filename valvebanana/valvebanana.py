# writer.py

# Constants
PREFIX = '_vb'

# Utility functions
quote = lambda x: '"{}"'.format(x)
digest = lambda x: PREFIX + str(abs(hash(str(x))))[:5]

# Writer functions
class Env(object):
    '''Providess methods to expand high-level sentences into
    cfg code. Collects a list of necessary aliases along the
    way.'''
    def __init__(self, bib=[]):
        self.bib = bib

    def bibliography(self):
        return '\n'.join(self.bib)

    def paragraph(self, xs, nested=False, delimiter='; '):
        return delimiter.join(
            self.expand(x, nested=nested) for x in xs
        )

    def expand(self, xs, nested=False):
        cmd, args = xs[0], xs[1:]
        if cmd == 'bind':
            return self._bind(*args, nested=nested)
        return self._sentence(xs, nested=nested)

    def _sentence(self, xs, nested=False):
        return ' '.join(
            self._term(x, nested=nested) for x in xs
        )

    def _term(self, x, nested=False):
        if isinstance(x, str):
            return x
        if nested:
            return self._refer(x)
        return quote(self.paragraph(x, nested=True))

    def _refer(self, dn, up=None):
        dig = digest((dn, up))
        if up is None:
            f = lambda xs: any('+' in x for x in xs)
            if any(map(f, dn)):
                # Make an exception if dn contains a
                # plus/minus bind.
                r = lambda x: x.replace('+', '-')
                up = (tuple(map(r, x)) for x in dn if f(x))
                #return self._bind(k, dn, up)
                return self._refer(dn, up)
            a = self.alias(dig, dn)
            self.bib.append(a)
            return dig
        self.bib.append(self.alias('+'+dig, dn))
        self.bib.append(self.alias('-'+dig, up))
        return '+' + dig

    def _bind(self, k, dn, up=None, nested=False):
        if up is None:
            return self._sentence(('bind', k, dn), nested=nested)
        ref = self._refer(dn, up)
        return self._sentence(('bind', k, ref), nested=nested)

    def alias(self, name, par, nested=False):
        return self._sentence(('alias', name, par), nested=nested)


class Keymap(dict):
    '''Provides methods to bind hyphen-separated key
    combinations to arbitrary high-level sentences.'''
    def bind(self, ks, dn, up=None):
        '''Associates a key combination (ks) to a command
        (dn, up).'''
        if isinstance(ks, str):
            ks = ks.split('-')
        k, ks = ks[0], ks[1:]
        if ks:
            if k not in self:
                self[k] = Keymap()
            self[k].bind('-'.join(ks), dn, up)
        else:
            self[k] = (dn, up)

    def expand(self):
        '''Returns an extended paragraph of binds and
        aliases which completely implement this keymap.'''
        env = Env()
        return '\n'.join((
            env.paragraph(self.binds(), delimiter='\n'),
            env.bibliography()
        ))

    def binds(self):
        return [self._bind(k, v) for k, v in self.items()]
    
    def _bind(self, k, v):
        if isinstance(v, dict):
            d = {i: self[i] for i in v if i in self}
            binds_old = Keymap(d).binds()
            binds_new = Keymap(v).binds()
            return ('bind', k, binds_new, binds_old)
        if v is None:
            return ('unbind', k)
        return ('bind', k, *v)


# Test Env.
def test_env():
    print('TESTS:')
    env = Env()
    info_dn = [
        ('+showscores',),
        ('net_graphtext', '1'),
        ('cl_showpos', '1')
    ]
    info_up = [
        ('-showscores',),
        ('net_graphtext', '0'),
        ('cl_showpos', '0'),
        #('bind', 'enter', [ ('god',), ('noclip',) ]),
        #('bind', 'enter', [ ('god',)], [('noclip',) ]),
    ]
    s = ('bind', 'shift', [
        ('bind', 'tab', info_dn, info_up),
        ('bind', 'enter', 'say_team'),
    ])
    #print(env.expand(('bind', 'enter', [('say',)], [('noclip',)])))
    print(env.expand(s))
    [print(i) for i in env.bib]

    # Example: Buy binds.
    print('\nEXAMPLE: BUY BINDS')
    env.bib = []  # Clear bibliography of previous references.
    buynds_dn = {
        'd': 'defuser',
        't': 'tec9'
    }
    buynds_up = {
        'd': '+moveright',
        't': 'say'
    }
    dn = [('bind', k, [('buy', wpn)]) for k, wpn in buynds_dn.items()]
    up = [('bind', k, cmd)            for k, cmd in buynds_up.items()]
    s = ('bind', 'mouse3', dn, up)
    print(env.expand(s))
    [print(i) for i in env.bib]

# Test Keymap
def test_keymap():
    print('EXAMPLE: q to drop, but shift-q to drop C4')
    km = Keymap()
    drop_bomb = [
        ('use', 'weapon_knife'),
        ('use', 'weapon_c4'),
        ('drop',),
        ('slot1',)
    ]
    km.bind('enter', 'say')
    km.bind('q', 'drop')
    km.bind('shift-enter', 'say_team')
    km.bind('shift-q', drop_bomb)
    km.bind('shift-tab', [
        ('+showscores',),
        ('net_graphtext', '1'),
        ('cl_showpos', '1')
    ], [
        ('-showscores',),
        ('net_graphtext', '0'),
        ('cl_showpos', '0')
    ])
    #km.bind('ctrl-alt-shift-r', [('mp_restartgame', '1')])
    #km.bind('alt', '+speed')
    #km.bind('alt-space', '+duck')
    print(km.expand())

def test_keymap2():
    km = Keymap()
    km.bind('f', [('+moveright',), ('r_cleardecals',)])
    km.bind('shift-f', [('buy', 'ak47')])
    print(km.expand())

if __name__ == '__main__':
    test_keymap2()
