# writer.py

# Constants
PREFIX = '_vb'


# Utitlity functions
quote = lambda x: '"{}"'.format(x)
digest = lambda x: PREFIX + str(abs(hash(str(x))))[:3]


# Writer functions

par = lambda ss: '; '.join(sen(s) for s in ss)
sen = lambda ts: ' '.join(term(t) for t in ts)
term = lambda x: x if isinstance(x, str) else quote(subpar(x))
subpar = lambda ss: '; '.join(subsen(s) for s in ss)
subsen = lambda ts: ' '.join(subterm(t) for t in ts)
subterm = lambda x: x if isinstance(x, str) else ref(x)

def ref(x):
    d = digest(x)
    bib = ('alias', d, x)
    print('Bib:', sen(bib))
    return d

# Tests
if __name__ == '__main__':
    # Test 1: complex sentence with no references.
    p = [('bind', 'tab', [
        ('+showscores',),
        ('net_graphtext', '1'),
        ('cl_showpos', '1'),
    ]),]
    print(par(p))
    # -> bind tab "+showscores; net_graphtext 1; cl_showpos 1"

    # Test 2: complex sentence: complex sentence with
    # references.
    rebinds = [
        ('bind', 't', [('buy', 'awp')]),
        (
            'bind',
            'space',
            [('buy', 'kevlar'), ('cl_crosshaircolor', '0'),
            (p,)]
        )
    ]
    p = [('bind', 'mouse3', rebinds),]
    print(par(p))
