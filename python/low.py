# low.py

import os.path


class Cfg(list):
    def write(self, path):
        root, ext = os.path.splitext(path)
        if not ext:
            path = root + '.cfg'
        with open(path, 'w') as cfg:
            for line in self:
                cfg.write(line + '\n')
