import constants as ct
import numpy as np
from sys import stderr

def build_graph(board):

    width, height = board.shape
    for tile in board.flat:

        if tile.kind == ct.T_TRAIL:
            tile.value = ct.REWARDS[tile.kind]
            continue

        for dx, dy in ct.MOVE_LIST:
            x = tile.x + dx
            y = tile.y + dy

            if 0 <= x < width and 0 <= y < height:
                neighbor = board[x, y]
                if neighbor.kind != ct.T_TRAIL:
                    tile.add_neighbor((dy, dx), neighbor)

def weight_cone(board, players):

    pass
    """for tile in board.flat:
        if tile.kind != ct.T_PLAYER:
            continue

        for n in tile.neighbors.itervalues():
            n.dist += 1

            for nn in n.neighbors.itervalues():
                #nn.value += 20.0
                if nn.kind == ct.T_FLOOR:
                    #nn.kind = ct.T_SEMI_OUT
                    pass
    """

def move(board, players, player):
    print >>stderr, "it works!"

    build_graph(board)
    weight_cone(board, players)
    h, w = board.shape

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
            best = src.value
            for a in src.neighbors:

                dest = src.neighbors[a]
                reward = ct.REWARDS[ct.T_FLOOR if dest is player_tile else dest.kind]
                value = (reward + ct.DISCOUNT * dest.value)

                if policy is None or value > best:
                    policy = a
                    best = value

            src.policy = ct.POLICIES.get(policy, policy)
            src.value = best

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
                lambda n: 'X\t' if n.kind == ct.T_PLAYER else str(n.value)[0:5] + '\t'
            )(board)
        )

    print >>stderr, "moving:", player_tile.policy

    return player_tile.policy

    # return ct.WEST
