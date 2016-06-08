import constants as ct

class Controller(object):
  def __init__(self, player=None):
    self.player = player


class KeyController(Controller):
  def __init__(self, key_n, key_s, key_e, key_w, player=None):
    super(self.__class__, self).__init__(player)

    self.keymap = {
      key_n: ct.NORTH,
      key_s: ct.SOUTH,
      key_e: ct.EAST,
      key_w: ct.WEST,
    }

  def handle_key(self, k):
    if self.player:
      try:
        self.player.set_dir(self.keymap[k])
      except KeyError:
        # Ignore
        pass


class AIController(Controller):
  def __init__(self, alg, player=None):
    super(self.__class__, self).__init__(player)

  def handle_tick(self, board):
    if self.player:
      self.player.set_dir(alg(board))
