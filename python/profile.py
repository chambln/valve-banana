# profile.py

import keeb

class Profile:
    '''Configures and builds a user's config'''

    def __init__(self):
        self.keeb = keeb.Keeb()

    def __str__(self):
        return '{} mappings'.format(len(self.keeb))
