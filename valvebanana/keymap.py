# keymap.py

import writer

class Keymap(dict):
    def bind(self, ks, dn, up=None):
        if len(ks) == 1:
            self[k] = (dn, up)
        else:
            k, ks = k[0], ks[1:]
            if k not in keymap:
                self[k] = Keymap()
            self[k].bind(ks, dn, up)

    def expand(self):
        '''Returns a paragraph of ('bind', ...) sentences
        which completely implement this keymap.'''
        return [('bind', k, *self._expand_val(v))
                for k, v in self.items()]
    
    def _expand_val(self, v):
        if isinstance(v, dict):
            return Keymap(v).expand(), None
        return v


# Testing
if __name__ == '__main__':
    print('EXAMPLE: q to drop, but shift-q to drop C4')
    drop_bomb = [
        ('use', 'weapon_knife'),
        ('use', 'weapon_c4'),
        ('drop',),
        ('slot1',)
    ]
    keymap = {
        'enter': ('say', None),
        'q': ('drop', None),
        'shift': {
            'enter': ('say_team', None),
            'q': (drop_bomb, None)
        }
    }
    km = Keymap(**keymap)
    binds = km.expand()
    env = writer.Env()
    print(env.paragraph(binds, delimiter='\n'))
    [print(i) for i in env.bib]
