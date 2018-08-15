# profile.py

import keeb


class Profile:
    '''Provides methods for building a user's config'''

    def __init__(self):
        self.keeb = keeb.Keeb()

    def __str__(self):
        return str(self.keeb)
