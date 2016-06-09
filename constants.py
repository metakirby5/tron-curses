import curses as cs

# Defaults
DEFAULTS = {
  'rate': 0.1,
  'cpus': 1,
}

# Cardinal directions
NORTH = 'NORTH'
SOUTH = 'SOUTH'
EAST = 'EAST'
WEST = 'WEST'

# Tile constants
T_FLOOR = 'T_FLOOR'
T_TRAIL = 'T_TRAIL'
T_PLAYER = 'T_PLAYER'
T_SPEEDUP = 'T_SPEEDUP'
T_SPEEDDOWN = 'T_SPEEDDOWN'

# Speed constants
SPEED_SLOW = 4
SPEED_DEFAULT = 2
SPEED_FAST = 1
SPEED_MAX_TICK = 8

# Powerup constants
POWERS = [T_SPEEDUP, T_SPEEDDOWN]
POWER_SIGMA = 5
POWER_SPAWN_RATE = 100
POWER_DESPAWN_RATE = 200
POWER_DURATION = 100

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

# MDP constants
REWARDS = {
    T_FLOOR: -0.05,
    T_TRAIL: -10.0,
    T_PLAYER: 10.0
}
POLICIES = {
    (-1, 0): WEST,
    (1, 0):  EAST,
    (0, -1): NORTH,
    (0, 1):  SOUTH
}
DISCOUNT = 0.99
MAX_ITERATIONS = 100
MOVE_LIST = [
    [0, 1],
    [0, -1],
    [1, 0],
    [-1, 0]
]

# Misc. constants
TICK_RATE = 0.05
PREGAME_DELAY = 3
