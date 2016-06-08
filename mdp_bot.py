import constants as ct
from sys import stderr

def build_graph(board):

    for tile in board.flat:

        if tile.kind == ct.T_TRAIL:
            tile.value = ct.REWARDS[tile.kind]
            continue

        for dx, dy in ct.MOVE_LIST:
            x = tile.x + dx
            y = tile.y + dy

            width, height = board.shape

            if 0 <= x < width and 0 <= y < height:
                neighbor = board[x, y]
                tile.add_neighbor((dy, dx), neighbor)


def move(board, player):
    print >>stderr, "it works!"

    build_graph(board)
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

    print >>stderr, "moving:", player_tile.policy

    return player_tile.policy

    # return ct.WEST
