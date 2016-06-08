import numpy as np
import constants as ct
from threading import Thread
from time import sleep
from player import Player


class Tile(object):
  def __init__(self, kind, x, y):
    self.kind = kind
    self.x = x
    self.y = y


class Game(Thread):
  def __init__(self, redraw, rate, width, height):
    super(self.__class__, self).__init__()
    
    self.redraw = redraw
    self.rate = rate
    self.width = width
    self.height = height

    self.running = True
    self.players = {}
    self.ai_controllers = []
    self.grid = np.fromfunction(
      np.vectorize(lambda x, y: Tile(ct.T_FLOOR, x, y)),
      (width, height), dtype=int)

  # Game loop
  def run(self):
    self.place_players()

    while self.running:
      # Move each player
      for _, player in self.players.iteritems():
        if not player.alive:
          continue

        self.grid[player.x, player.y].kind = ct.T_TRAIL
        player.step()

        # Check collision
        if 0 <= player.x < self.width and 0 <= player.y < self.height:
          cur = self.grid[player.x, player.y]
          if cur.kind != ct.T_FLOOR:
            player.kill()
            player.unstep()
          else:
            cur.kind = ct.T_PLAYER
            cur.id = player.id
        else:
          player.kill()
          player.unstep()

      # TODO check if one player left

      self.redraw(self)
      sleep(self.rate)

  def stop(self):
    self.running = False

  # TODO better player placement
  def place_players(self):
    y = self.height / 2
    inc = self.width / (len(self.players) + 1)
    for i, player in self.players.iteritems():
      x = (i + 1) * inc
      player.set_pos(x, y)
      player.set_dir(ct.NORTH)

      tile = self.grid[x, y]
      tile.kind = ct.T_PLAYER
      tile.id = player.id

  def new_player(self):
    p = Player()
    self.players[p.id] = p
    return p
