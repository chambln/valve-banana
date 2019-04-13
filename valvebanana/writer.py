# writer.py

# Constants
PREFIX = '_vb'

# Utitlity functions
quote = lambda x: '"{}"'.format(x)
digest = lambda x: PREFIX + str(abs(hash(str(x))))[:3]


class Env(object):
    '''Writer environment. Feed me paragraphs and sentences,
    and I'll return the  corresponding low-level cfg strings
    while keeping a list of aliases (self.bib) necessary for
    them to work.'''

    def __init__(self, bib=[]):
        self.bib = bib

    par = lambda self, xs: '; '.join(map(self.sen, xs))
    sen = lambda self, xs: ' '.join(map(self.term, xs))
    term = lambda self, x: x if isinstance(x, str) else quote(self.subpar(x))
    subpar = lambda self, xs: '; '.join(map(self.subsen, xs))
    subsen = lambda self, xs: ' '.join(map(self.subterm, xs))
    subterm = lambda self, x: x if isinstance(x, str) else self.ref(x)[0]
    ref = lambda self, x, prefix='': self.alias(digest(x), x)

    def alias(self, a, x):
        self.bib.append(self.sen(('alias', a, x)))
        return a


class Keeb(Env):
    '''Keyboard environment.'''   

    def bind(self, k, dn, up=None):
        if up:
            return self.sen(('bind', k, self.hold(dn, up)))
        return self.sen(('bind', k, dn))

    def hold(self, dn, up):
        dig = digest(dn)
        self.alias('+'+dig, dn)
        self.alias('-'+dig, up)
        return '+' + dig

# Tests
if __name__ == '__main__':
    keeb = Keeb()

    binds = [
        ('enter', 'say'),
        ('shift', [
                ('bind', 'enter', 'say_team'),
                ('bind', 'k', 'kill'),
                ('bind', 'tab', [
                    ('+showscores',),
                    ('net_graphtext', '1',),
                    ('cl_showpos', '1',)
                ]) 
            ], [
                ('bind', 'enter', 'say'),
                ('bind', 'k', [
                    ('foo',),
                    ('bar',),
                    ('baz',),
                ]),
                ('bind', 'tab', '+showscores')
            ]
        )
    ]

    for i in binds:
        print(keeb.bind(*i))
    for i in keeb.bib:
        print(i)
