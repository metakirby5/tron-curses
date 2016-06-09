import constants as ct
import numpy as np
from game import Tile
from sys import stderr

dirs = {
    ct.NORTH: (0, -1),
    ct.SOUTH: (0, 1),
    ct.WEST:  (-1, 0),
    ct.EAST:  (1, 0)
}

adj = {
    ct.NORTH: [ct.WEST, ct.EAST],
    ct.SOUTH: [ct.WEST, ct.EAST],
    ct.WEST:  [ct.NORTH, ct.SOUTH],
    ct.EAST:  [ct.NORTH, ct.SOUTH]
}


def weight_cone(board, players, player, depth=3):
    """ Basic idea: go forward, left & right (recursively)
             o -> ...
        o -> o -> ...
             o -> ...
    """

    # Create density cone for all enemy players
    for p in [p for p in players.itervalues() if p != player]:
        tile = board[p.x, p.y]
        if dirs[p.dir] in tile.neighbors:
            next = tile.neighbors[dirs[p.dir]]
            set_cone(p, next, depth)


def set_cone(player, tile, depth):

    if depth == 0 or tile.kind == ct.T_TRAIL or dirs[player.dir] not in tile.neighbors:
        return

    # Set multiplier for this tile
    tile.cone_multiplier += 0.2 * depth
    tile = tile.neighbors[dirs[player.dir]]
    set_cone(player, tile, depth - 1)

    # Do the same for the adjacent tiles
    for direction in adj[player.dir]:
        if dirs[direction] in tile.neighbors:
            left = tile.neighbors[dirs[direction]]
            left.cone_multiplier += 0.2 * depth
            set_cone(player, left, depth - 1)


def move(board, players, player):

    player_tile = board[player.x, player.y]
    h, w = board.shape

    # Recalculate cone multipliers
    np.vectorize(Tile.reset_cone)(board)
    weight_cone(board, players, player)

    # Calculate optimal policy
    for i in xrange(ct.MAX_ITERATIONS):

        # For every node, calculate policy and values
        for src in board.flat:

            if src.kind == ct.T_TRAIL:
                continue

            # Find best policy and value out of all actions
            policy = None
            best = src.value[player.id]
            for a in src.neighbors:

                # Get the value, assuming certain movement
                dest = src.neighbors[a]
                if dest.kind == ct.T_TRAIL or (dest.kind == ct.T_PLAYER and dest != player_tile):
                    continue
                elif dest.cone_multiplier != 1:
                    reward = ct.REWARDS[ct.T_ATTACK] * dest.cone_multiplier
                else:
                    reward = ct.REWARDS[ct.T_FLOOR if dest.kind == ct.T_PLAYER else dest.kind]
                value = (reward + ct.DISCOUNT * dest.value[player.id])

                # Update if we hava a better expected value
                if policy is None or value > best:
                    policy = a
                    best = value

            src.policy[player.id] = ct.POLICIES.get(policy, policy)
            src.value[player.id] = best

    """out = ""
    for col in xrange(w):
        for row in xrange(h):
            n = board[row, col]
            #out += "{}".format(str(n.cone_multiplier) + "    ")[0:3]
            #out += str(n.kind)
            out += 'X   ' if n.kind == ct.T_PLAYER else str(n.value[player.id])[0:3] + " "
        out += "\n"
    print >>stderr, out"""


    return player_tile.policy[player.id]
