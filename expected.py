from __future__ import division
__author__ = 'sivanov'
import networkx as nx
from copy import copy
import random
import matplotlib.pyplot as plt
import numpy as np

def read_graph(filename, weighted=True):
    G = nx.Graph()
    with open(filename) as f:
        for line in f:
            d = line.split()
            if weighted:
                G.add_edge(int(d[0]), int(d[1]), weight=float(d[2]))
            else:
                G.add_edge(int(d[0]), int(d[1]))
    return G

def expected_degree(G):
    return {node: sum([G[node][u]['weight'] for u in G[node]]) for node in G}

def get_world(G):
    Q = nx.Graph()
    for e in G.edges(data=True):
        if e[2]['weight'] > random.random():
            Q.add_edge(e[0], e[1], weight=1)
    return Q

def get_volume(G, subset):
    return sum([sum([G[node][u]['weight'] for u in G[node]]) for node in subset])

def get_statistics(G):
    degrees = expected_degree(G)
    Vol_G = sum(degrees.values())
    w = Vol_G/len(G)
    w_max = max(degrees.values())
    w_hat = sum(map(lambda x: x**2, degrees.values()))/Vol_G
    return w, w_hat, Vol_G, w_max

def get_coverage(G, S):
    T = copy(S)
    activated = {u: False for u in G}
    for u in S:
        activated[u] = True
    i = 0
    while i < len(T):
        node = T[i]
        for u in G[node]:
            if not activated[u] and random.random() < G[node][u]['weight']:
                activated[u] = True
                T.append(u)
        i+=1
    return len(T)
def runIC(G, S, I):
    total = 0
    for _ in range(I):
        total += get_coverage(G, S)
    return total/I

def infectious_node(G):
    CCs = list(nx.connected_components(G))
    gcc = max(CCs, key=len)
    degrees = expected_degree(G)
    max_degree, max_node = max([(degrees[node],node) for node in gcc])
    return max_node

def bar_spread(spreads, labels):
    N = len(spreads)
    ind = np.arange(N)
    width = 0.25

    fig, ax = plt.subplots()
    ax.bar(ind, spreads, width)

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Number of infected nodes')
    ax.set_xlabel('Algorithm')
    ax.set_title('Spread by different algorithms')
    ax.set_xticks(ind+width/2)
    ax.set_xticklabels(labels)

    plt.show()

if __name__ == "__main__":

    G = nx.Graph()
    with open("flixster.txt") as f:
        for line in f:
            d = line.split()
            G.add_edge(int(d[0]), int(d[1]), weight=float(d[2]))

    print len(G), len(G.edges())

    CCs = list(nx.connected_components(G))
    print sorted([len(cc) for cc in CCs], reverse=True)[0], len(G)
    Q = get_world(G)
    CCs = list(nx.connected_components(Q))
    print sorted([len(cc) for cc in CCs], reverse=True)[0], len(Q)

    degrees = expected_degree(G)
    w, w_hat, Vol_G, w_max = get_statistics(G)
    print w, w_hat, Vol_G, w_max

    top_degree = [211247, 87929, 101384, 16656, 1079, 5479, 28987, 105469, 58186, 32335]

    max_node = infectious_node(G)
    spread1 = runIC(G, [max_node], 10)
    total = 0
    I = 100
    for _ in range(I):
        node = random.choice(G.nodes())
        spread = runIC(G, [node], 10)
        print _+1, node, spread
        total += spread
    spread2 = total/I
    print spread1, spread2

    spreads = (spread1, spread2)
    labels = ('Selected', 'Random')
    bar_spread(spreads, labels)

    Q = read_graph("Q.txt")
    print len(Q), len(Q.edges())
    print get_statistics(Q)

    degrees = expected_degree(Q)
    CCs = list(nx.connected_components(Q))
    print CCs[2]
    print sorted(degrees.items(), key=lambda (k,v): v, reverse=True)

    for i in range(0):
        top_degree = random.sample(G.nodes(), 25)
        Vol_S = sum([degrees[u] for u in top_degree])
        print Vol_S, Vol_G/w_max
        print Vol_S*(w_hat - sum([degrees[node]**2 for node in top_degree])/Vol_G),
        top_subset = set()
        for node in top_degree:
            top_subset.update(G.neighbors(node))
        top_subset = top_subset.difference(top_degree)
        print get_volume(G, top_subset)
        print

    for i in range(0):
        Q = get_world(G)
        nodes = random.sample(Q.nodes(), 25)
        Vol = sum([degrees[u] for u in nodes])
        vol = get_volume(Q, nodes)
        print Vol, vol
        print abs(len(Q.edges()) - .5*Vol_G)
        print


    console = []