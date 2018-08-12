# profile.py

import writer

class Build(object):
    '''Holds instructions for writing cfg files'''

    def __init__(self, *args):
        self.args = args  # temporary
    

class Profile(object):
    '''\
    Builds a script or collection thereof from abstract instructions (specs).

    Examples of abstract instructions:

      - bind the 'enter' key to the 'say' command
            (simple)

      - bind 'shift+enter' to 'say_team'
            (complex... solution will involve the shift key rebinding the enter
            key somehow, along with all other shift key combos)

      - change a bunch of cvars
            (e.g. to set up sandbox/god mode or 1v1 gamemode)
            (moderately complex... solution might be e.g. to execute cfg file 
            with those values inside)
      - 
    '''

    def __init__(self, *specs):
        self.specs = specs

    def build(self):
        return Build(*[spec.build() for spec in self.specs])


class Spec(object):
    '''Short for specification. Building block instruction for making the 
    profile.'''
    pass

    def build(self):
        print("Building:", self)


class Map(Spec):
    '''Specifies how a key combination should map to an action'''

    def __init__(self, keycombo, action):
        self.keycombo = keycombo  # Keycombo object
        self.action = action      # Action object

    def __str__(self):
        return 'map {} "{}"'.format(self.keycombo, self.action)

    def build(self):
        print("Building:", self)
        if self.keycombo.modifiers:
            # Build with modifiers
            if len(self.keycombo.modifiers) > 1:
                print("Multiple modifiers not yet supported")
            else:
                pass
        else:
            # Build with no modifiers
            pass


class Keycombo(object):
    '''\
    Represents an arbitrary key or combination thereof; i.e (<modifier>-)*key.

    Examples:
        'enter'        -> Keycombo('enter')
        'alt-p'        -> Keycombo('alt', 'p')
        'ctrl-shift-r' -> Keycombo('ctrl', 'shift', 'r')
    '''

    def __init__(self, *keys):
        self.keys = keys

    def __str__(self):
        return '-'.join(self.keys)

    @property
    def modifiers(self):
        return self.keys[:-1]

    @property
    def modificand(self):
        return self.keys[-1]


class Action(object):
    '''Represents an in-game or scripting action to be carried out. Usually a 
    simple one-WORD command or alias thereto.'''

    def __init__(self, action=''):
        self.action = action

    def __str__(self):
        return self.action

