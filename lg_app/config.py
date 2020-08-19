INPUT_CHOICE    = ['bgp summary',                                           # то, что показывает форма
                   'bgp route terse',
                   'bgp route detail',
                   'mtr',
                   'ping']

COMMAND_MAPPING = {'bgp summary': 'show bgp summary',
                   'bgp route terse': 'show route terse protocol bgp',
                   'bgp route detail': 'show route detail protocol bgp',
                   'mtr': ['mtr', '-oLSDW', '-r', '-c 10', '-n'],           # subprocess принимает команды с параметрами в виде списка
                   'ping': ['ping', '-c 4', '-n', '-O']                     # subprocess принимает команды с параметрами в виде списка
                   }

IGNORE_TARGET   = [COMMAND_MAPPING.get('bgp summary')]
ANY_TARGET      = [COMMAND_MAPPING.get('bgp route terse'), COMMAND_MAPPING.get('bgp route detail')]
LINUX_COMMAND   = [COMMAND_MAPPING.get('mtr'), COMMAND_MAPPING.get('ping')]

# Flask app config
ENV = 'production'
DEBUG = 1
SECRET_KEY = 'apha3Oodohrohneihiefiedohfeema'
