import constants as ct
import curses as cs


CHARS = {
  ct.T_TRAIL:     'o',
  ct.T_SPEEDUP:   '*',
  ct.T_SPEEDDOWN: '@',
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
    self._field = scr.subwin(self.height, self.width, 1, 0)

    cs.init_pair(ct.P_BLUE,    cs.COLOR_BLUE,   -1)
    cs.init_pair(ct.P_RED,     cs.COLOR_RED,    -1)
    cs.init_pair(ct.P_YELLOW,  cs.COLOR_YELLOW, -1)
    cs.init_pair(ct.P_GREEN,   cs.COLOR_GREEN,  -1)

  def redraw(self, game):
    # Handle status
    self._status.clear()
    if game.running:
      if game.paused:
        self._status.addstr(0, 0, 'PAUSED')
    else:
      if game.pregame:
        self._status.addstr(0, 0, '{}...'.format(game.countdown))
      elif game.tie:
        self._status.addstr(0, 0, 'TIE')
      else:
        self._status.addstr(0, 0, 'WINNER: PLAYER {}'.format(game.winner.id))
    self._status.refresh()

    # Handle field
    self._field.clear()

    # Player markers
    if game.pregame:
      for player in game.players.itervalues():
        self._field.addstr(
          player.y - 2, player.x,
          'PLAYER {}'.format(player.id))

    # Tiles
    for tile in game.grid.flat:
      if tile.kind in [ct.T_TRAIL, ct.T_PLAYER]:
        self._field.addstr(
          tile.y, tile.x,
          CHARS[game.players[tile.id].dir] if tile.kind == ct.T_PLAYER else \
          CHARS[tile.kind],
          cs.color_pair(tile.id % ct.CPU_COLORS + 1))
      elif tile.kind != ct.T_FLOOR:
        self._field.addstr(tile.y, tile.x, CHARS[tile.kind])

    self._field.refresh()
