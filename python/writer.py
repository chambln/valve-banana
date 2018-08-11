# writer.py

class Script(object):
    '''Represents a .cfg file as a list of lines of low-level code'''

    def __init__(self, *lines):
        self.lines = lines
        
    def __str__(self):
        '''This is the final output for any given script. You'd write this to a 
        file.'''
        return '\n'.join([str(l) for l in self.lines])

    def append(self, line):
        self.lines.append(line)
        

class Sentence(object):
    '''Represents a sentence; that is, a command that should occupy a line in a 
    cfg file'''

    def __init__(self, command, *args):
        self.command = command  # Its command string, e.g. 'bind'.
        self.args = args        # The parameters passed to it.

    def __str__(self):
        return self.pattern.format(self.command, *self.args)

    @property
    def pattern(self):
        if self.dimension == 1:    # Command and single parameter
            return '{} "{}"'
        elif self.dimension == 2:  # Command and two parameters
            return '{} {} "{}"'
        else:                      # General case, no speech marks
            return ' '.join(['{}' for _ in self.args])

    @property
    def dimension(self):
        return len(self.args)
