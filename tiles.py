class Tile(object):
  pass


class FloorTile(Tile):
  pass


class TrailTile(Tile):
  def __init__(self, player, dir):
    self.player = player
    self.dir = dir


class PlayerTile(Tile):
  def __init__(self, player):
    self.player = player
