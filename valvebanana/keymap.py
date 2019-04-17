# keymap.py

import writer

class Keymap(dict):
    def bind(self, ks, dn, up=None):
        '''Associates a key combination (ks) to a command
        (dn, up).'''
        ks = ks.split('-')
        k, ks = ks[0], ks[1:]
        if ks:
            if k not in self:
                self[k] = Keymap()
            self[k].bind('-'.join(ks), dn, up)
        else:
            self[k] = (dn, up)

    def expand(self):
        '''Returns a paragraph of ('bind', ...) sentences
        which completely implement this keymap.'''
        return [self._bind(k, v) for k, v in self.items()]
    
    def _bind(self, k, v):
        if isinstance(v, dict):
            d = {i: self[i] if i in self else None for i in v}
            binds_old = Keymap(**d).expand()
            binds_new = Keymap(v).expand()
            return ('bind', k, binds_new, binds_old)
        if v is None:
            return ('unbind', k)
        return ('bind', k, *v)


# Testing
if __name__ == '__main__':
    print('EXAMPLE: q to drop, but shift-q to drop C4')
    drop_bomb = [
        ('use', 'weapon_knife'),
        ('use', 'weapon_c4'),
        ('drop',),
        ('slot1',)
    ]

    km = Keymap(**{})
    km.bind('enter', 'say')
    km.bind('q', 'drop')
    km.bind('shift-enter', 'say_team')
    km.bind('shift-q', drop_bomb)
    km.bind('shift-tab', [
        ('+showscores',),
        ('net_graphtext', '1'),
        ('cl_showpos', '1')
    ], [
        ('-showscores',),
        ('net_graphtext', '0'),
        ('cl_showpos', '0')
    ])
    #km.bind('ctrl-alt-shift-r', [('mp_restartgame', '1')])
    #km.bind('alt', '+speed')
    #km.bind('alt-space', '+duck')
    binds = km.expand()
    env = writer.Env()
    print(env.paragraph(binds, delimiter='\n'))
    [print(i) for i in env.bib]
