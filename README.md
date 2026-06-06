# Event-Driven 6G Scheduling using SimPy + Sionna

**Project Goal**

To develop and study an event-driven scheduling framework for future 6G networks using discrete-event simulation (SimPy), graph-based network modeling (NetworkX), and physical-layer channel simulation (Sionna), with intelligent resource management techniques based on Game Theory and Machine Learning.

---

## Team Members

| Name | Roll Number |
|---|---|
| Snehitha | AP24110011008 |
| Shahistha Anjum | AP24110010993 |
| Shanmukh | AP24110011010 |
| Sandeep | AP24110010992 |

**Mentor:** Dr. Ch Anil Carie
**Institution:** SRM University AP, Amaravati
**Programme:** Summer Research Internship 2025 (8 Weeks)

---

## Repository Structure

```
6G-Scheduling-Intern/
│
├── simulation/
│   └── simpy_demo.py           # Event-driven SimPy simulation
│
├── notebooks/
│   └── python_basics.py        # Python fundamentals practice
│
├── notes/
│   └── important_notes.md      # Nash Equilibrium + Stackelberg + Modbus notes
│
├── results/
│   └── network_topology.png    # 5-node network graph output
│
├── week1/
│   └── network_topology.py     # 5-node NetworkX graph code
│
├── requirements.txt
└── README.md
```

---

## Week 1 Tasks Completed

* Installed Python, VS Code, Git, and required libraries (NetworkX, SimPy, Matplotlib)
* Created GitHub repository and set up project structure
* Learned Python fundamentals — variables, loops, functions, lists, dictionaries
* Built a 5-node IoT network topology using NetworkX
* Implemented a basic event-driven simulation using SimPy to model packet transmission and attacker behavior
* Studied Game Theory concepts — Nash Equilibrium and Stackelberg Game
* Analyzed the Modbus dataset structure, features, and attack categories
* Maintained project progress using GitHub

---

## Week 1 Topics Learned

- Python Fundamentals (variables, loops, functions, lists, dictionaries)
- NetworkX (graph creation, node/edge attributes, visualization)
- SimPy (discrete-event simulation, processes, timeout)
- Game Theory (Nash Equilibrium, Stackelberg Game)
- Modbus Dataset Overview (features, attack types, purpose)

---

## Dataset Reference

**CIC Modbus 2023 Dataset**
Source: [https://www.unb.ca/cic/datasets/modbus-2023.html](https://www.unb.ca/cic/datasets/modbus-2023.html)
Purpose: Industrial IoT attack detection — used to understand attack patterns (DoS, Scanning, Injection) for future ML-based risk classification.

---

## Week 2 Plan

- Graph Theory (centrality, density, connectivity)
- 50-Node IoT Network creation
- IoT Security attacks (DoS, DDoS, Reconnaissance)
- Attack simulation using NetworkX
- Network monitoring and defender logic

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run network topology
python week1/network_topology.py

# Run SimPy simulation
python simulation/simpy_demo.py

# Run Python basics
python notebooks/python_basics.py
```
