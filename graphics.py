import constants as ct
import curses as cs

class Drawer(object):
  def __init__(self, scr):
    self.height, self.width = scr.getmaxyx()
    self.height -= 1 # for status

    self._status = scr.subwin(1, self.width, 0, 0)
    self._field = scr.subwin(self.height - 1, self.width, 1, 0)

    cs.init_pair(ct.P_BLUE,    cs.COLOR_BLUE,   -1)
    cs.init_pair(ct.P_RED,     cs.COLOR_RED,    -1)
    cs.init_pair(ct.P_YELLOW,  cs.COLOR_YELLOW, -1)
    cs.init_pair(ct.P_GREEN,   cs.COLOR_GREEN,  -1)

  def redraw(self, game):
    cs.curs_set(0)
    for player in game.players:
      if 0 <= player.x < self.width and 0 <= player.y < self.height:
        self._field.addstr(player.y, player.x, 'X')
    self._field.refresh()
