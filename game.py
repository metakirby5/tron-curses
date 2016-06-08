import numpy as np
import constants as ct
from threading import Thread
from time import sleep
from player import Player
from controllers import AIController


class Tile(object):
  def __init__(self, kind, x, y):
    self.kind = kind
    self.x = x
    self.y = y
    self.policy = None
    self.neighbors = {}
    self.value = 0
    self.dist = 0

  def add_neighbor(self, direction, neighbor):
    self.neighbors[direction] = neighbor


class Game(Thread):
  def __init__(self, redraw, width, height):
    super(self.__class__, self).__init__()
    self.daemon = True

    self.redraw = redraw
    self.width = width
    self.height = height

    self.cur_pid = 1
    self.players = {}
    self.ai_controllers = []
    self.grid = np.fromfunction(
      np.vectorize(lambda x, y: Tile(ct.T_FLOOR, x, y)),
      (width, height), dtype=int)

  # Game loop
  def run(self):
    # TODO state machine
    self.running = False
    self.pregame = True
    self.paused = False
    self.place_players()

    for i in xrange(ct.PREGAME_DELAY):
      self.countdown = ct.PREGAME_DELAY - i
      self.redraw(self)
      sleep(1)

    self.pregame = False
    self.running = True
    while self.running:
      if not self.paused:

        # Tell AIs to pick next move
        for ai in self.ai_controllers:
          ai.handle_tick(self.grid, self.players)

        # Move each player
        for player in self.players.itervalues():
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

        # If one player left, end the game
        if sum(player.alive for player in self.players.itervalues()) == 1:
          self.running = False
          self.winner = filter(
            lambda p: p.alive, self.players.itervalues())[0]

      self.redraw(self)
      sleep(ct.TICK_RATE)

  def stop(self):
    self.running = False

  # TODO better player placement
  def place_players(self):
    y = self.height / 2
    inc = self.width / (len(self.players) + 1)
    for i, player in enumerate(self.players.itervalues()):
      x = (i + 1) * inc
      player.set_pos(x, y)
      player.set_dir(ct.NORTH)

      tile = self.grid[x, y]
      tile.kind = ct.T_PLAYER
      tile.id = player.id

  def next_pid(self):
    pid = self.cur_pid
    self.cur_pid += 1
    return pid

  def new_player(self):
    p = Player(id=self.next_pid())
    self.players[p.id] = p
    return p

  def add_ai(self, alg):
    self.ai_controllers.append(AIController(alg, self.new_player()))
