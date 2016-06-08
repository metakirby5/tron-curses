import constants as ct
from threading import Thread
from time import sleep
from player import Player

class Game(Thread):
  def __init__(self, redraw, rate, width, height):
    super(self.__class__, self).__init__()
    
    self.redraw = redraw
    self.rate = rate
    self.width = width
    self.height = height

    self.running = True
    self.players = []
    self.ai_controllers = []

  # Game loop
  def run(self):
    self.place_players()
    while self.running:
      for player in self.players:
        player.step()
      self.redraw(self)
      sleep(self.rate)

  def stop(self):
    self.running = False

  # TODO better player placement
  def place_players(self):
    mid_y = self.height / 2
    inc = self.width / (len(self.players) + 1)
    for i, player in enumerate(self.players):
      player.set_pos((i + 1) * inc, mid_y)
      player.set_dir(ct.NORTH)

  def new_player(self):
    p = Player()
    self.players.append(p)
    return p
