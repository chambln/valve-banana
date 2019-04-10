# writer.py

# Constants
PREFIX = '_vb'

# Utitlity functions
quote = lambda x: '"{}"'.format(x)
digest = lambda x: PREFIX + str(abs(hash(str(x))))[:3]


class Env(object):
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

    def ref(self, x):
        d = digest(x)
        reference = ('alias', d, x)
        self.bib.append(self.sen(reference))
        return d

# Tests
if __name__ == '__main__':
    # Test 1: complex sentence with no references.
    env = Env()
    print('\n** TEST 1 **')
    p = [('bind', 'tab', [
        ('+showscores',),
        ('net_graphtext', '1'),
        ('cl_showpos', '1'),
    ]),]
    print(env.par(p))
    # -> bind tab "+showscores; net_graphtext 1; cl_showpos 1"

    # Test 2: complex sentence: complex sentence with
    # references.
    print('\n** TEST 2 **')
    env = Env()
    rebinds = [
        ('bind', 't', [('buy', 'awp')]),
        (
            'bind',
            'space',
            [('buy', 'kevlar'), ('cl_crosshaircolor', '0')],
        )
    ]
    p = [('bind', 'mouse3', rebinds),]
    print(env.par(p))
    for i in env.bib:
        print(i)
