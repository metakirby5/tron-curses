import curses as cs

# Defaults
DEFAULTS = {
  'rate': 0.1,
  'cpus': 1,
}

# Cardinal directions
NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'

# Tile constants
T_FLOOR = 0
T_TRAIL = 1
T_PLAYER = 2

# Color constants
P_WHITE   = 0
P_BLUE    = 1
P_RED     = 2
P_YELLOW  = 3
P_GREEN   = 4
CPU_COLORS = 4

# Key consants
K_QUIT = ord('q')
K_RESTART = ord('r')
K_PAUSE = ord('p')

# Misc. constants
TICK_RATE = 0.1
PREGAME_DELAY = 3
