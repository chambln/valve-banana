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

    def ref(self, x):
        d = digest(x)
        reference = ('alias', d, x)
        self.bib.append(self.sen(reference))
        return d


class Keeb(Env):
    '''Keyboard environment.'''   

    def bind(self, k, dn):
        b = ('bind', k, dn)
        return(self.sen(b))


# Tests
if __name__ == '__main__':
    k = Keeb()

    print(k.bind('tab', '+showscores'))

    for i in k.bib:
        print(i)
