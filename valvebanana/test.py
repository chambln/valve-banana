# test.py

from valvebanana import *

# Bindings with modifiers.
user = User(**{'enter': 'say',
               'v': '+voicerecord',
               'shift-enter': 'say_team',
               'shift-v':'voice_enable 0'})

# Assigning variables.
user.set('hud_scaling', '0.8')
user.set('mat_setvideomode', '1920 1080 0')

# Write to disk.
user.write()
