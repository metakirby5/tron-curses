import constants as ct
import numpy as np
from game import Tile
from sys import stderr

def weight_cone(board, players, depth=3):
    """ Basic idea: go forward, left & right (recursively)
             *
        o -> *
             *
    """
    pass


def move(board, players, player):
    print >>stderr, "it works!"

    weight_cone(board, players)
    h, w = board.shape

    # USE THIS TO RESET CONE MULTIPLIER
    # np.vectorize(Tile.reset_cone)(board)

    player_tile = board[player.x, player.y]
    print >>stderr, "x={}, y={}".format(player.x, player.y)
    print >>stderr, "player:", player_tile.kind, ", neighbors=", len(player_tile.neighbors)

    #for d, n in player_tile.neighbors.iteritems():
    #    print >>stderr, "dir=", d, ", n=", n.kind

    for i in xrange(ct.MAX_ITERATIONS):

        for src in board.flat:

            if src.kind == ct.T_TRAIL:
                continue

            policy = None
            best = src.value[player.id]
            for a in src.neighbors:

                dest = src.neighbors[a]
                if dest.kind == ct.T_TRAIL:
                    continue
                reward = ct.REWARDS[ct.T_FLOOR if dest is player_tile else dest.kind]
                value = (reward + ct.DISCOUNT * dest.value[player.id])

                if policy is None or value > best:
                    policy = a
                    best = value

            src.policy[player.id] = ct.POLICIES.get(policy, policy)
            src.value[player.id] = best

    for d, n in player_tile.neighbors.iteritems():
        print >>stderr, "\tdir=", d, ", val=", n.value, n.kind

    to_str = {
        ct.WEST: '^',
        ct.EAST: 'v',
        ct.NORTH: '>',
        ct.SOUTH: '<'
    }

    print >>stderr, '\n'.join(
            ''.join(r) for r in
            np.vectorize(
                #lambda n: to_str[n.policy] or n.kind
                lambda n: 'X\t' if n.kind == ct.T_PLAYER else str(n.value[player.id])[0:5] + '\t'
            )(board)
        )

    print >>stderr, "moving:", player_tile.policy[player.id]

    return player_tile.policy[player.id]

    # return ct.WEST
