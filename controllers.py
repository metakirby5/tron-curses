import constants as ct

class Controller(object):
  def __init__(self, player):
    self.player = player


class KeyController(Controller):
  def __init__(self, player, key_n, key_s, key_e, key_w):
    super(self.__class__, self).__init__(player)

    self.keymap = {
      key_n: ct.NORTH,
      key_s: ct.SOUTH,
      key_e: ct.EAST,
      key_w: ct.WEST,
    }

  def handle_key(self, k):
    try:
      self.player.set_dir(self.keymap[k])
    except KeyError:
      # Ignore
      pass


class AIController(Controller):
  def __init__(self, player, alg):
    super(self.__class__, self).__init__(player)

  def handle_tick(self, board):
    self.player.set_dir(alg(board))
