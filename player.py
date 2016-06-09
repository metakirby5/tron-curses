import constants as ct
from game_exceptions import InvalidDirectionError

class Player(object):
  cur_id = 0

  def __init__(self, id=None, x=0, y=0, dir=None):
    if id is None:
      self.id = self.__class__.cur_id
      self.__class__.cur_id += 1
    else:
      self.id = id

    self.set_pos(x, y)
    self.set_dir(dir)
    self.set_power(None)

    self.tick = 0
    self.alive = True

  def __repr__(self):
    return '{}@({},{})'.format(self.id, self.x, self.y)

  def set_pos(self, x, y):
    self.x = x
    self.y = y

  def set_dir(self, dir):
    try:
      # No 180 degree turns allowed
      # TODO: fix bug of turning twice before next tick
      if self.dir == ct.NORTH and dir == ct.SOUTH or \
         self.dir == ct.SOUTH and dir == ct.NORTH or \
         self.dir == ct.EAST  and dir == ct.WEST  or \
         self.dir == ct.WEST  and dir == ct.EAST:
        raise InvalidDirectionError
    except AttributeError:
      pass

    self.dir = dir
    self.dx = 1 if dir == ct.EAST else -1 if dir == ct.WEST else 0
    self.dy = 1 if dir == ct.SOUTH else -1 if dir == ct.NORTH else 0

  def set_power(self, power):
    self.power = power

    if power is None:
      self.speed = ct.SPEED_DEFAULT
    else:
      self.power_lifetime = ct.POWER_DURATION
      if power == ct.T_SPEEDUP:
        self.speed = ct.SPEED_FAST
      elif power == ct.T_SPEEDDOWN:
        self.speed = ct.SPEED_SLOW

  # Performs motion update
  def step(self):
    if self.alive:
      if not self.tick % self.speed:
        self.x += self.dx
        self.y += self.dy

      if self.power:
        self.power_lifetime -= 1
        if not self.power_lifetime:
          self.set_power(None)

      self.tick += 1
      self.tick %= ct.SPEED_MAX_TICK

  def unstep(self):
    self.x -= self.dx
    self.y -= self.dy

  def kill(self):
    self.alive = False
