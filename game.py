import numpy as np
import random as rd
import constants as ct
from collections import defaultdict
from threading import Thread
from time import sleep
from player import Player
from controllers import AIController


# TODO make classes for tile types so we don't have janky fields
class Tile(object):
  def __init__(self, kind, x, y):
    self.kind = kind
    self.x = x
    self.y = y
    self.neighbors = {}

    # AI-specific
    self.policy = {}
    self.value = defaultdict(int)
    self.cone_multiplier = 1

  def add_neighbor(self, direction, neighbor):
    self.neighbors[direction] = neighbor

  def reset_cone(self):
    self.cone_multiplier = 1


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
    self.power_tiles = []
    self.build_graph()

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
    self.next_power_spawn = int(rd.gauss(ct.POWER_SPAWN_RATE, ct.POWER_SIGMA))
    while self.running:
      if not self.paused:

        # Tell AIs to pick next move
        for ai in self.ai_controllers:
          ai.handle_tick(self.grid, self.players)

        # Move each player
        for player in self.players.itervalues():
          if not player.alive:
            continue

          prev_x, prev_y = player.x, player.y
          player.step()

          # If moved
          if player.x != prev_x or player.y != prev_y:
            self.grid[prev_x, prev_y].kind = ct.T_TRAIL

            # Check collision
            if 0 <= player.x < self.width and 0 <= player.y < self.height:
              cur = self.grid[player.x, player.y]
              if cur.kind in ct.POWERS:
                player.set_power(cur.kind)
                cur.kind = ct.T_PLAYER
                cur.id = player.id
              elif cur.kind == ct.T_FLOOR:
                cur.kind = ct.T_PLAYER
                cur.id = player.id
              else:
                player.kill()
                player.unstep()
            else:
              player.kill()
              player.unstep()

        # If one player left, end the game
        num_alive = sum(player.alive for player in self.players.itervalues())
        if num_alive <= 1:
          self.running = False
          if num_alive == 0:
            self.tie = True
          else:
            self.tie = False
            self.winner = filter(
              lambda p: p.alive, self.players.itervalues())[0]

        # Spawn power
        self.next_power_spawn -= 1
        if self.next_power_spawn <= 0:
          # Find a place to spawn
          power_tile = rd.choice([t for t in self.grid.flat
                                  if t.kind == ct.T_FLOOR])

          power_tile.kind = rd.choice(ct.POWERS)
          power_tile.despawn_timer = int(rd.gauss(
            ct.POWER_DESPAWN_RATE, ct.POWER_SIGMA))
          self.power_tiles.append(power_tile)

          self.next_power_spawn = int(
            rd.gauss(ct.POWER_SPAWN_RATE, ct.POWER_SIGMA))

        # Despawn powers
        for power_tile in self.power_tiles[:]:
          power_tile.despawn_timer -= 1
          if power_tile.despawn_timer <= 0:
            power_tile.kind = ct.T_FLOOR
            self.power_tiles.remove(power_tile)

      self.redraw(self)
      sleep(ct.TICK_RATE)

  def stop(self):
    self.running = False

  def build_graph(self):
    for tile in self.grid.flat:
      for dx, dy in ct.MOVE_LIST:
        x = tile.x + dx
        y = tile.y + dy
        if 0 <= x < self.width and 0 <= y < self.height:
          tile.add_neighbor((dx, dy), self.grid[x, y])

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
