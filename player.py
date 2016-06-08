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

    self.alive = True

  def __repr__(self):
    return '{}@({},{})'.format(self.id, self.x, self.y)

  def set_pos(self, x, y):
    self.x = x
    self.y = y

  def set_dir(self, dir):
    try:
      # No 180 degree turns allowed
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

  # Performs motion update
  def step(self):
    if self.alive:
      self.x += self.dx
      self.y += self.dy

  def unstep(self):
    self.x -= self.dx
    self.y -= self.dy

  def kill(self):
    self.alive = False
