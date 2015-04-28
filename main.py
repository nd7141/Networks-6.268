__author__ = 'sivanov'
import networkx as nx
import matplotlib.pyplot as plt
import powerlaw
import numpy as np

def read_file(filename):
    G = nx.Graph()
    with open(filename) as f:
        for line in f:
            d = line.split()
            G.add_edge(d[0],d[1])
    print 'n: %s m: %s' %(len(G), len(G.edges()))
    return G

def CC_analysis(G):
    CCs = list(nx.connected_components(G))
    print len(CCs)
    # sizes = sorted([len(cc) for cc in CCs], reverse=True)
    # for i, size in enumerate(sizes[:10]):
    #     print i+1, size

def powerlaw_fit(G):
    degrees = G.degree().values()
    fit = powerlaw.Fit(degrees, xmin=None)
    print fit.power_law.alpha
    print fit.power_law.sigma
    print fit.power_law.xmin
    fig = fit.plot_pdf()
    fit.power_law.plot_pdf(linestyle='--')
    plt.title('Degree Distribution')
    plt.xlabel('Degree k')
    plt.ylabel('P(x = k)')
    plt.show()
    print fit.distribution_compare('power_law', 'exponential', normalized_ratio=True)


if __name__ == "__main__":

    G1 = read_file("Email-Enron.txt")
    # G2 = read_file("CA-HepPh.txt")
    # G3 = read_file("roadNet-TX.txt")

    powerlaw_fit(G1)
    # powerlaw_fit(G2)
    # powerlaw_fit(G3)

    console = []