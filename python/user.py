# user.py (exemplar)

from profile import *

lines = [
    Bind('w', '+forward'),
    Bind('a', '+moveleft'),
    Bind('s', '+back'),
    Bind('d', '+moveright'),
    Bind('space', '+jump'),
    Bind('enter', 'say_team'),
    Exec('binds.cfg')
]

prof = Profile(*lines)
print(prof)
