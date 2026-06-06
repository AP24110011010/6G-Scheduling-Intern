# network_topology.py
# Week 1 - NetworkX: 5-Node IoT Network Topology
# Topic: Graph creation, node attributes, visualization
# Summer Research Internship 2025 - Group 4

import networkx as nx
import matplotlib.pyplot as plt
import random

random.seed(42)

# 1. Create the Graph


G = nx.Graph()

# Add nodes (IoT devices)
devices = ["Device1", "Device2", "Device3", "Device4", "Device5"]
G.add_nodes_from(devices)

# Add edges (communication links) as per assignment topology
G.add_edges_from([
    ("Device1", "Device2"),
    ("Device1", "Device3"),
    ("Device2", "Device4"),
    ("Device3", "Device4"),
    ("Device4", "Device5")
])


# 2. Assign Node Attributes


for node in G.nodes():
    G.nodes[node]["risk_score"]    = round(random.uniform(0.1, 1.0), 2)
    G.nodes[node]["vulnerability"] = round(random.uniform(0.1, 1.0), 2)
    G.nodes[node]["status"]        = "normal"


# 3. Print Network Summary


print("=" * 40)
print("  5-Node IoT Network - Summary")
print("=" * 40)
print(f"  Total Nodes : {G.number_of_nodes()}")
print(f"  Total Edges : {G.number_of_edges()}")
print(f"  Connected   : {nx.is_connected(G)}")
print()
print("  Node Attributes:")
for node, data in G.nodes(data=True):
    print(f"    {node} | Risk: {data['risk_score']} | Vuln: {data['vulnerability']} | Status: {data['status']}")

print()
print("  Edges (Communication Links):")
for edge in G.edges():
    print(f"    {edge[0]} <---> {edge[1]}")


# 4. Draw and Save the Network Graph


# Fixed positions to match assignment diagram
pos = {
    "Device1": (0, 2),
    "Device2": (2, 2),
    "Device3": (0, 0),
    "Device4": (2, 0),
    "Device5": (1, -1.5)
}

risk_values = [G.nodes[n]["risk_score"] for n in G.nodes()]

plt.figure(figsize=(7, 5))
plt.title("5-Node IoT Network Topology\nWeek 1 - Event-Driven 6G Scheduling", fontsize=12, fontweight="bold")

nx.draw(
    G,
    pos=pos,
    with_labels=True,
    node_color=risk_values,
    cmap=plt.cm.RdYlGn_r,
    node_size=2200,
    font_size=9,
    font_weight="bold",
    edge_color="#555555",
    width=2.0
)

sm = plt.cm.ScalarMappable(cmap=plt.cm.RdYlGn_r, norm=plt.Normalize(vmin=0, vmax=1))
sm.set_array([])
plt.colorbar(sm, label="Risk Score", shrink=0.75)

plt.tight_layout()
plt.savefig("results/network_topology.png", dpi=150, bbox_inches="tight")
plt.show()

print("Graph saved to: results/network_topology.png")
