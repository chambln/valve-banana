# user.py (exemplar)

from profile import *
from pprint import pprint


p = Profile()

p.map('w', '+forward'),
p.map('a', '+moveleft'),
p.map('s', '+back'),
p.map('d', '+moveright'),
p.map('space', '+jump'),
p.map('enter', 'say')
p.map('shift-enter', 'say_team')
p.map('ctrl-k', 'kill')
p.map('ctrl-shift-s', 'exec sandbox.cfg')

pprint(p.keymap.keymap)
