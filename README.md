# InfoMap-Analysis

Implementation and benchmarking of **Infomap**, **Infomap + Louvain initialization**, and **Neuromap** for community detection.

This repository explores flow-based community detection methods from both classical and neural perspectives, comparing classical compression-based algorithms with differentiable entropy-minimization approaches.

---

## Overview

Community detection can be framed as an **information compression problem**.

This project implements and compares:

- **Infomap** (flow-based community detection)
- **Infomap initialized with Louvain partitions**
- **Neuromap** (differentiable, neural entropy minimization framework)

We analyze:

- Stability  
- Partition quality  
- Sensitivity to initialization  
- Behavior across simple and real-world graphs  

---

## Methods

### Infomap

Classical **Infomap** minimizes the Map Equation:

$$
L(M) = q_{\curvearrowright} H(Q) + \sum_{i=1}^{m} p_{\circlearrowright}^{i} H(P^{i})
$$

Where:

- $q_{\curvearrowright}$ = probability of exiting modules  
- $H(Q)$ = entropy of module transitions  
- $p_{\circlearrowright}^{i}$ = probability of staying within module $i$  
- $H(P^{i})$ = entropy inside module $i$ 

Key characteristics:

- Flow-based  
- Hard partitions  
- Greedy optimization  

---

### Infomap with Louvain Initialization

To study the impact of initialization, we:

1. Compute a **Louvain partition**
2. Use it as an initial assignment
3. Refine it using Infomap

This allows us to analyze:

- Sensitivity to starting conditions  
- Local minima effects  
- Structural bias in flow optimization  

---

### Neuromap

Neuromap reformulates the Map Equation as a **differentiable objective**.

We implemented:

- Linear Neuromap  
- MLP-based Neuromap  
- GCN-based Neuromap  

Core features:

- Soft cluster assignments  
- Temperature annealing  
- Entropy regularization  
- Multiple restarts  
- Hard partition extraction after convergence  

Unlike Infomap, Neuromap allows:

- End-to-end gradient optimization  
- Integration of node features  
- Architecture experimentation  

---

## Datasets Used

Experiments include:

- Karate Club  
- Football network  
- Cora  

Each dataset is evaluated using:

- Number of modules `|M|`
- Hard codelength `L_hard`
- Adjusted Mutual Information (AMI)
- Runtime  
