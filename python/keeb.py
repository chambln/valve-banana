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

    def build(self):
        # Isolate the master bindings
        self.master = KeymapBlank(**self.pop(''))

        # Implement master bindings and aliases as nomod
        nomod = low.Cfg([
            low.Bind(key, val)
            for key, val in self.master.items()
        ])

        # Implement each modifier's bindings
        for mod, modmap in self.items():
            # Down script to effect modified binds
            dn = low.Cfg([
                low.Bind(key, val)
                for key, val in modmap.items()
            ])
            dn.path = mod + '_dn'
            dn.write(dn.path)

            # Up script to restore those binds
            up = low.Cfg([
                low.Bind(key, self.master[key])
                for key in modmap
            ])
            up.path = mod + '_up'
            up.write(up.path)

            # Append necessary master bindings
            dn.alias = '+_'+mod
            up.alias = '-_'+mod
            nomod += [
                low.Alias(dn.alias, low.Exec(dn.path)),
                low.Alias(up.alias, low.Exec(up.path)),
                low.Bind(mod, dn.alias)
            ]

        # Finally write the master script now that it's ready
        nomod.write('nomod')


class KeymapBlank(dict):
    '''Subclass of dict for which missing keys become an empty string'''
    def __missing__(self, key):
        self[key] = ''
        return self[key]



def test():
    k = Keymap()
    k.map('enter', 'say')
    k.map('shift-enter', 'say_team')
    k.map('ctrl-enter', 'say ggwp')
    k.map('alt-k', 'kill')
    k.map('w', '+forward')
    k.map('a', '+moveleft')
    k.map('s', '+back')
    k.map('d', '+moveright')
    k.build()

if __name__ == '__main__':
    test()
