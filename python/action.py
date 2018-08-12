# action.py

class Action(object):
    '''Represents an in-game or scripting action to be carried out. Typically a 
    simple one-WORD command or alias thereto.'''

    def __init__(self, action=''):
        self.action = action

    def __str__(self):
        return self.action
