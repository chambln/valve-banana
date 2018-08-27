# keeb.py

import low

class Keymap(dict):
    def __missing__(self, key):
        '''Recursively instantiate Keymap objects to implement key 
        modifiers.'''
        self[key] = Keymap()
        return self[key]

    def map(self, combostr, action):
        keys = combostr.split('-')
        mod, final = keys[0], keys[1]
        self[mod][final] = action

    def build(self):
        master = low.Cfg(
        

def test_Keymap():
    k = Keymap()
    k['enter'] = 'say'
    k['shift']['enter'] = 'say_team'
    print('repr(k) ==', repr(k))

def test_Keymap_map():
    k = Keymap()
    # Demonstrate that single modifiers work
    k.map('alt-g', 'say gg')
    k.map('alt-w', 'say ggwp')
    k.map('shift-k', 'kill')
    # Demonstrate that multiple modifiers do not work
    k.map('ctrl-alt-g', 'say ggwp')
    print("repr(k) ==", repr(k))

def test_Combo():
    c = Combo('ctrl-shift-p')
    print('repr(c) ==', repr(c))
    print('repr(c.keys) ==', repr(c.keys))
    print('repr(c.mods), repr(c.final) ==', repr(c.mods), repr(c.final))


if __name__ == '__main__':
    test_Keymap_map()
