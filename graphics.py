import constants as ct
import curses as cs


CHARS = {
  'TRAIL':  'o',
  ct.NORTH: '^',
  ct.SOUTH: 'v',
  ct.EAST:  '>',
  ct.WEST:  '<',
}


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
    # Handle field
    self._field.clear()
    for tile in game.grid.flat:
      if tile.kind == ct.T_FLOOR:
        pass
      elif tile.kind in [ct.T_TRAIL, ct.T_PLAYER]:
        self._field.addstr(
          tile.y, tile.x,
          CHARS['TRAIL'] if tile.kind == ct.T_TRAIL else \
          CHARS[game.players[tile.id].dir],
          cs.color_pair(tile.id % ct.CPU_COLORS + 1))
    self._field.refresh()
