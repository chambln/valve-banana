# profile.py

import generator

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

    def __init__(self, specs=[]):
        self.specs = specs


class Spec(object):
    '''Short for specification. Building block instruction for making the profile.'''
    pass


class Keymap(Spec):
    '''Specifies how a key combination should map to an action'''

    def __init__(self, keycombo, action):
        self.keycombo = keycombo
        self.action = action


class Action(object):
    '''Represents an in-game or scripting action to be carried out'''
    pass
