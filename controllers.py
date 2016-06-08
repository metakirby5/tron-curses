import constants as ct
from game_exceptions import InvalidDirectionError

class Controller(object):
  def __init__(self, player=None):
    self.player = player

  def direct_player(self, dir):
    if self.player:
      try:
        self.player.set_dir(dir)
      except InvalidDirectionError:
        pass

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
    try:
      self.direct_player(self.keymap[k])
    except KeyError:
      pass


class AIController(Controller):
  def __init__(self, alg, player=None):
    super(self.__class__, self).__init__(player)
    self.alg = alg

  def handle_tick(self, board, players):
    self.direct_player(self.alg(board, players, self.player))
