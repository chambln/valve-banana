# writer.py

# Constants
PREFIX = '_vb'

# Utitlity functions
quote = lambda x: '"{}"'.format(x)
digest = lambda x: PREFIX + str(abs(hash(str(x))))[:3]


class Env(object):
    '''Writer environment.  Feed me paragraphs and
    sentences, and I'll return the corresponding low-level
    cfg strings while keeping a list of aliases (self.bib)
    necessary for them to work.'''

    def __init__(self, bib=[]):
        self.bib = bib

    def par(self, ss):
        return '; '.join(self.sen(s) for s in ss)

    def sen(self, ts):
        return ' '.join(self.term(t) for t in ts)

    def term(self, x):
        return x if isinstance(x, str) else quote(self.subpar(x))

    def subpar(self, ss):
        return '; '.join(self.subsen(s) for s in ss)

    def subsen(self, ts):
        return ' '.join(self.subterm(t) for t in ts)

    def subterm(self, x):
        return x if isinstance(x, str) else self.ref(x)

    def ref(self, x, prefix=''):
        d = prefix + digest(x)
        #reference = ('alias', d, x)
        #self.bib.append(self.sen(reference))
        self.alias(d, x)
        return d

    def alias(self, a, x):
        self.bib.append(self.sen(('alias', a, x)))


class Keeb(Env):
    '''Keyboard environment.'''   

    def bind(self, k, dn, up=None):
        if up:
            return self.sen(('bind', k, self.hold(dn, up)))
        return self.sen('bind', k, dn)

    def hold(self, dn, up):
        dig = digest(dn)
        self.alias('+'+dig, dn)
        self.alias('-'+dig, up)
        return '+' + dig

# Tests
if __name__ == '__main__':
    k = Keeb()

    print(k.bind(
        'tab',
        dn=[
            ('+showscores',),
            ('net_graphtext', '1'),
            ('cl_showpos', '1')
        ],
        up=[
            ('-showscores',),
            ('net_graphtext 0',),
            ('cl_showpos', '0')
        ])
    )

    for i in k.bib:
        print(i)
