# user.py (exemplar)

from profile import *

my_specs = [
    Map('w', '+forward'),
    Map('a', '+moveleft'),
    Map('s', '+back'),
    Map('d', '+moveright'),
    Map('space', '+jump'),
    Map('enter', 'say_team'),
]

prof = Profile(*my_specs)
print(prof)  # ... profile.output or something?
