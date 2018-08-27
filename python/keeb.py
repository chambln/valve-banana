# keeb.py

import low


class Keymap(dict):
    def __missing__(self, key):
        self[key] = {}
        return self[key]

    def map(self, combo, value):
        keys = combo.split('-')
        final = keys[-1]
        if len(keys) == 1:
            # No modifier keys
            mod = ''
        else:
            # Just take first of modifiers given
            mod = keys[0]
        self[mod][final] = value

    def build_(self):
        # First, handle master bindings if any
        if '' in self:
            binds = [low.Command(('bind', key, val))
                     for key, val in self[''].items()]
            master = low.Cfg(binds)
            master.write('master')
            self.master = self['']
            del self['']
        # Then handle any modified bindings
        for mod, mapdict in self.items():
            print(mod, mapdict)
            up = low.Cfg([low.Command(('bind', key, self.master[key])) 
                          for key in mapdict])
            dn = low.Cfg([low.Command(('bind', key, val))
                          for key, val in mapdict.items()])
            dn.write(mod + '_dn')
            up.write(mod + '_up')

    def build(self):
        # Isolate the master bindings
        self.master = self.pop('')
        # Handle modified bindings
        for mod, mapdict in self.items():
            dn = low.Cfg([
                low.Bind(key, val)
                for key, val in mapdict.items()
            ])
            up = low.Cfg([
                low.Bind(key, self.master[key])
                for key in mapdict
            ])
            dn.write(mod + '_dn')
            up.write(mod + '_up')
        # Handle master bindings and aliases


def test():
    k = Keymap()
    k.map('enter', 'say')
    k.map('shift-enter', 'say_team')
    k.build()

if __name__ == '__main__':
    test()
