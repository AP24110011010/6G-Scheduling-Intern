# iot_network.py
# Week 2 - 50-Node IoT Network Generator
# Topic: Graph Theory, Centrality Analysis, Scale-Free Network
# Summer Research Internship 2025 - Group 4

import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random
import os

random.seed(42)
os.makedirs('results', exist_ok=True)

# ─────────────────────────────────────────────
# 1. Create 50-Node IoT Network
# ─────────────────────────────────────────────

def create_iot_network(n=50, seed=42):
    """
    Creates a scale-free IoT network using Barabasi-Albert model.
    Each node represents an IoT device with risk and vulnerability attributes.
    """
    G = nx.barabasi_albert_graph(n, 3, seed=seed)

    # Rename nodes to Device1, Device2, ...
    mapping = {i: f'Device{i+1}' for i in range(n)}
    G = nx.relabel_nodes(G, mapping)

    # Assign attributes to each device
    for node in G.nodes():
        G.nodes[node]['risk_score']    = round(random.uniform(0.1, 0.9), 2)
        G.nodes[node]['vulnerability'] = round(random.uniform(0.1, 0.9), 2)
        G.nodes[node]['status']        = 'normal'
        G.nodes[node]['packets_sent']  = 0

    return G

# ─────────────────────────────────────────────
# 2. Centrality Analysis
# ─────────────────────────────────────────────

def analyse_network(G):
    """
    Computes graph centrality metrics to identify critical nodes.
    Used by defender engine to prioritise monitoring.
    """
    degree_c  = nx.degree_centrality(G)
    between_c = nx.betweenness_centrality(G)
    close_c   = nx.closeness_centrality(G)
    density   = nx.density(G)

    print("=" * 55)
    print(f"  Network Summary")
    print("=" * 55)
    print(f"  Nodes     : {G.number_of_nodes()}")
    print(f"  Edges     : {G.number_of_edges()}")
    print(f"  Density   : {density:.4f}")
    print(f"  Connected : {nx.is_connected(G)}")
    print()

    # Top 5 most critical nodes
    top5 = sorted(between_c, key=between_c.get, reverse=True)[:5]
    print("  Top 5 Critical Nodes (Betweenness Centrality):")
    for node in top5:
        print(f"    {node:12s} | Degree: {degree_c[node]:.3f}"
              f" | Between: {between_c[node]:.3f}"
              f" | Closeness: {close_c[node]:.3f}")
    print("=" * 55)

    return degree_c, between_c, close_c, density

# ─────────────────────────────────────────────
# 3. Network Visualisation
# ─────────────────────────────────────────────

def visualise_network(G, path='results/network_visualization.png'):
    """
    Draws 50-node network with risk heatmap and degree-scaled node sizes.
    """
    risk   = [G.nodes[n]['risk_score'] for n in G.nodes()]
    degree = dict(G.degree())
    sizes  = [200 + degree[n] * 80 for n in G.nodes()]
    pos    = nx.spring_layout(G, seed=42, k=1.2)

    fig, ax = plt.subplots(figsize=(13, 9))
    ax.set_title(
        '50-Node IoT Network Topology\nWeek 2 — Risk Heatmap + Degree-Scaled Nodes',
        fontsize=13, fontweight='bold'
    )

    nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.25, edge_color='gray', width=0.7)
    sc = nx.draw_networkx_nodes(G, pos, ax=ax, node_color=risk,
                                cmap=plt.cm.RdYlGn_r, node_size=sizes, alpha=0.9)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=5, font_weight='bold')

    fig.colorbar(sc, ax=ax, label='Risk Score (Red = High, Green = Low)', shrink=0.6)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {path}")

# ─────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────

if __name__ == '__main__':
    G = create_iot_network(50)
    analyse_network(G)
    visualise_network(G)
