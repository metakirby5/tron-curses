import constants as ct

class Player(object):
  cur_id = 0

  def __init__(self, x=0, y=0, dir=None):
    self.id = self.__class__.cur_id
    self.__class__.cur_id += 1

    self.set_pos(x, y)
    self.set_dir(dir)

    self.alive = True

  def __repr__(self):
    return '{}@({},{})'.format(self.id, self.x, self.y)

  def set_pos(self, x, y):
    self.x = x
    self.y = y

  def set_dir(self, dir):
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
