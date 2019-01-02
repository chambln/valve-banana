# valvebanana.py


class Cmd(tuple):
    def __str__(self):
        last = self[-1] if any('"' in x for x in self) else '"{}"'.format(self[-1])
        return ' '.join((*self[:-1], last))


class User(dict):
    def __init__(self, kwargs):
        dict.__init__(self, **kwargs)
        self.cvars = {}

    def set(self, cvar, val):
        self.cvars[cvar] = val

    def write(self):
        '''Export this configuration as cfg files on disk, readable by
        the Source engine.'''
        cfgs = self.cfgs()
        for cfg, lines in cfgs.items():
            lines = '\n'.join(str(Cmd(xs)) for xs in lines)
            with open(cfg+'.cfg', 'w') as f:
                f.write(lines + '\n')

    def cfgs(self):
        cfgs = {}
        mms = self.modmaps()
        # Handle the init binds separately.
        init = mms.pop('init')
        cfgs['init'] = [('bind', k, cmd) for k, cmd in init.items()]

        # Add each bind line to its modifier's down file, and the
        # corresponding init bind to its up file.
        for mod, modmap in mms.items():
            cfgs[mod+'_dn'], cfgs[mod+'_up'] = [], []
            for k, cmd in modmap.items():
                cfgs[mod+'_dn'].append(('bind', k, cmd))
                upbind = ('bind', k, init[k]) if k in init else ('unbind', k)
                cfgs[mod+'_up'].append(upbind)

        # Add to init.cfg the aliases and binds necessary to make
        # modifiers work.
        for mod in self.modmaps():
            if mod != 'init':
                modbind = ('bind', mod, '+_'+mod)
                dn = ('alias', '+_'+mod, 'exec {}.cfg'.format(mod+'_dn'))
                up = ('alias', '-_'+mod, 'exec {}.cfg'.format(mod+'_up'))
                cfgs['init'] += [modbind, dn, up]

        # Add our cvars to init.cfg.
        for cvar, val in self.cvars.items():
            cfgs['init'].append((cvar, val))

        # Finally, return this dictionary of cfg files.
        return cfgs

    def modmaps(self):
        modmaps = {}
        for ks, cmd in self.items():
            mod, k = ks.split('-') if '-' in ks else ('init', ks)
            if mod not in modmaps:
                modmaps[mod] = {}
            modmaps[mod][k] = cmd
        return modmaps
