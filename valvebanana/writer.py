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
            self.sentence(x, nested=nested) for x in xs
        )

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
        #dn = self.paragraph(dn, nested=True)
        if up is None:
            a = self.alias(dig, dn)
            self.bib.append(a)
            return dig
        #up = self.paragraph(up, nested=True)
        self.bib.append(self.alias('+'+dig, dn))
        self.bib.append(self.alias('-'+dig, up))
        return '+' + dig

    def bind(self, k, dn, up=None):
        if up is None:
            return self.sentence(('bind', k, dn))
        ref = self.refer(dn, up)
        return self.sentence(('bind', k, ref))

    def alias(self, name, par):
        return self.sentence(('alias', name, par))



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
#    ('bind', 'enter', [ ('god',), ('noclip',) ])
]
s = ('bind', 'shift', [
    (e.bind('tab', info_dn, info_up),),
    ('bind', 'enter', 'say_team',),
])
#print(e.bind('tab', info_dn, info_up))
#print(e.bind('enter', [('say',)], [('noclip',)]))
print(e.sentence(s))
for i in e.bib:
    print(i)
