# cfg.py

import sentence


class Cfg:
    '''
    Provides methods for building a low-level cfg file line-by-line.
    '''
    
    def __init__(self, *lines):
        self.lines = list(lines)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '\n'.join([str(line) for line in self.lines])

    def __add__(self):
        return Cfg(*(self.lines + other.lines))

    def __iter__(self):
        for line in self.lines:
            yield line

    def append(self, line):
        self.lines.append(line)

    def bind(self, *args):
        self.append(sentence.Bind(*args))

    def unbind(self, *args):
        self.append(sentence.Unbind(*args))

    def alias(self, *args):
        self.append(sentence.Alias(*args))

    def exec(self, *args):
        self.append(sentence.Exec(*args))

    def cvar(self, *args):
        self.append(sentence.Cvar(*args))


# TESTING
# =======

# init.cfg
init = Cfg()
init.unbind('tab')
keymap = {
    'enter': 'say',
    'w': '+forward',
    's': '+back',
    'a': '+moveleft',
    'd': '+moveright',
    'space': '+jump',
    'shift': '+_shift'
}
for key, sen in keymap.items():
    init.bind(key, sen)
init.alias('+_shift', 'exec bind/shift_dn')
init.alias('-_shift', 'exec bind/shift_up')
init.cvar('setvideomode', '1920', '1080', '1')
with open('init.cfg', 'w') as f:
    f.write(str(init))

# shift_dn.cfg
shift_dn = Cfg()
shift_dn.bind('enter', 'say_team')
with open('shift_dn.cfg', 'w') as f:
    f.write(str(shift_dn))

# shift_up.cfg
shift_up = Cfg()
shift_up.bind('enter', 'say')
with open('shift_up.cfg', 'w') as f:
    f.write(str(shift_up))
