from math import atan2, hypot


def dist_diff(x2, y2, x1, y1):
    return x2 - x1, y2 - y1


def calc_dist(node2, node1):
    adj, opp = dist_diff(node2.x, node2.y, node1.x, node1.y)
    return hypot(adj, opp)


def calc_angle(node2, node1):
    adj, opp = dist_diff(node2.x, node2.y, node1.x, node1.y)
    return atan2(opp, adj)
