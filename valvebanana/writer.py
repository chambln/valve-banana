# writer.py

# Constants
PREFIX = '_vb'

# Utility functions
quote = lambda x: '"{}"'.format(x)
digest = lambda x: PREFIX + str(abs(hash(str(x))))[:3]

# Writer functions
class Env(object):
    def __init__(self, bib=[]):
        self.bib = bib

    def paragraph(self, xs, nested=False):
        return '; '.join(
            self.expand(x, nested=nested) for x in xs
        )

    def expand(self, xs, nested=False):
        cmd, args = xs[0], xs[1:]
        if cmd == 'bind':
            return self.bind(*args, nested=nested)
        return self.sentence(xs, nested=nested)

    def sentence(self, xs, nested=False):
        return ' '.join(
            self.term(x, nested=nested) for x in xs
        )

    def term(self, x, nested=False):
        if isinstance(x, str):
            return x
        if nested:
            return self.refer(x)
        return quote(self.paragraph(x, nested=True))

    def refer(self, dn, up=None):
        dig = digest((dn, up))
        if up is None:
            a = self.alias(dig, dn)
            self.bib.append(a)
            return dig
        self.bib.append(self.alias('+'+dig, dn))
        self.bib.append(self.alias('-'+dig, up))
        return '+' + dig

    def bind(self, k, dn, up=None, nested=False):
        if up is None:
            return self.sentence(('bind', k, dn), nested=nested)
        ref = self.refer(dn, up)
        return self.sentence(('bind', k, ref), nested=nested)

    def alias(self, name, par, nested=False):
        return self.sentence(('alias', name, par), nested=nested)



# Testing
e = Env()
info_dn = [
    ('+showscores',),
    ('net_graphtext', '1'),
    ('cl_showpos', '1')
]
info_up = [
    ('-showscores',),
    ('net_graphtext', '0'),
    ('cl_showpos', '0'),
    #('bind', 'enter', [ ('god',), ('noclip',) ])
]
s = ('bind', 'shift', [
    ('bind', 'tab', info_dn, info_up),
    ('bind', 'enter', 'say_team'),
])
#print(e.expand(('bind', 'enter', [('say',)], [('noclip',)])))
print(e.expand(s))

print('\nBIBLIOGRAPHY:')
for i in e.bib:
    print(i)
