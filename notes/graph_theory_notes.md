# Week 2 Notes — Graph Theory
**Summer Research Internship 2025 | Group 4**
**Project: Event-Driven 6G Scheduling using SimPy + Sionna**

---

## 1. Degree Centrality

### Definition
Measures how many direct connections a node has relative to the maximum possible.

**Formula:** `DC(v) = degree(v) / (N - 1)`

Where N = total number of nodes.

### In Our Project
A device with high degree centrality has many direct links to other devices. It is a communication hub. If an attacker compromises it, many devices immediately lose their direct path to the hub. The defender should monitor high-degree nodes closely.

### Code
```python
degree_c = nx.degree_centrality(G)
top_node = max(degree_c, key=degree_c.get)
```

---

## 2. Betweenness Centrality

### Definition
Measures how often a node lies on the shortest path between any two other nodes in the network.

**Formula:** `BC(v) = Σ (σ_st(v) / σ_st)` for all pairs s ≠ v ≠ t

Where σ_st = number of shortest paths from s to t, and σ_st(v) = those passing through v.

### In Our Project
A high-betweenness device is a critical relay — all other devices depend on it for routing. If compromised, entire regions of the network may become isolated. **This is the primary metric used by our defender engine to select monitored nodes.**

### Code
```python
between_c = nx.betweenness_centrality(G)
top5 = sorted(between_c, key=between_c.get, reverse=True)[:5]
```

---

## 3. Closeness Centrality

### Definition
Measures how close a node is to all other nodes on average (inverse of average shortest path length).

**Formula:** `CC(v) = (N - 1) / Σ d(v, u)` for all u ≠ v

### In Our Project
A device with high closeness can communicate efficiently with every other device in the network. Compromising it slows down all network-wide communications. Useful as a secondary metric for defender prioritisation.

### Code
```python
close_c = nx.closeness_centrality(G)
```

---

## 4. Network Density

### Definition
Ratio of actual edges to the maximum possible number of edges.

**Formula:** `D = 2E / N(N - 1)` for undirected graphs

### In Our Project
Low density (sparse network) means the network is vulnerable to targeted attacks on critical relay nodes — removing one node can disconnect many others. Our 50-node Barabasi-Albert network is intentionally sparse (scale-free) to reflect realistic IoT deployments.

### Code
```python
density = nx.density(G)
```

---

## 5. Barabasi-Albert Scale-Free Model

### Why We Use It
Real IoT networks follow a scale-free distribution — a few hubs have many connections, most devices have few. The Barabasi-Albert (BA) model replicates this via **preferential attachment**: new nodes connect to existing nodes proportionally to their degree.

**Our setting:** `nx.barabasi_albert_graph(50, 3)` — each new node attaches to 3 existing nodes.

### Key Implication
Scale-free networks are resilient to random failures (most nodes have low degree) but highly vulnerable to targeted attacks on hubs (few nodes have high degree). This directly motivates the Targeted attack mode and the betweenness-guided defender.

---

## Week 2 Key Insight

> Betweenness centrality connects graph theory directly to Stackelberg game theory from Week 1. The defender uses it to make a data-driven, proactive strategy — monitoring the nodes that matter most — rather than monitoring randomly. This is exactly the leader's advantage in the Stackelberg model: commit first to an informed strategy, knowing the attacker will respond rationally.
