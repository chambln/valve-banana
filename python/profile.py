# profile.py
# vim: fdm=marker

import writer
import action

class Build(object):
    '''Holds instructions for writing cfg files'''

    def __init__(self, *args):
        self.args = args  # temporary
    

class Profile(object):
    # docstring {{{
    '''\
    Holds a collection of abstract instructions, called Specifications. Examples of 
    Specifications:
      - bind the 'enter' key to the 'say' command
            (simple)
      - bind 'shift+enter' to 'say_team'
            (complex... solution will involve the shift key rebinding the enter
            key somehow, along with all other shift key combos)
      - change a bunch of cvars
            (e.g. to set up sandbox/god mode or 1v1 gamemode)
            (moderately complex... solution might be e.g. to execute cfg file with 
            those values inside)
    ''' # }}}

    def __init__(self, *specs):
        self.specs = specs

    def build(self):
        return [spec.build() for spec in self.specs]


