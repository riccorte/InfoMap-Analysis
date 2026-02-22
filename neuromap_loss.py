import os
import time
import math
import random

import numpy as np
import networkx as nx   # used to load and visualize graphs and handle partitions
import matplotlib.pyplot as plt

import torch    # Pytorch will be extensively used 
import torch.nn as nn   # used to define neural networks (nn)
import torch.nn.functional as F  # important to define relevant functions 
from torch import Tensor

from infomap import Infomap # Python wrapper of infomap algorithm

def smart_teleport(A, alpha=0.15, iter=1000):
    # build the transition matrix
    T = torch.nan_to_num(A.T * torch.sum(A, 1).to_dense() ** (-1), nan=0.0).T.to(
        device=A.device
    )

    # distribution according to nodes' in-degrees
    e_v = (torch.sum(A, dim=0) / torch.sum(A)).to_dense().to(device=A.device)

    # calculate the flow distribution with a power iteration
    # p = (1/len(T) * torch.ones(len(T))).to(device = device)
    p = e_v
    for _ in range(iter):
        p = alpha * e_v + (1 - alpha) * p @ T

    # make the flow matrix for minimising the map equation
    F = alpha * A / torch.sum(A) + (1 - alpha) * (p * T.T).T

    return F, p


class NeuromapPooling(torch.nn.Module):
    r"""This criterion computes the map equation codelength for an undirected or directed weighted graph.

    Args:
        A (torch.Tensor): (Unnormalized) Adjacency matrix of the weighted graph.
        epsilon (float, optional): Small epsilon to ensure differentiability of logs.

    """

    def __init__(
        self,
        adj: Tensor,
        epsilon: float = 1e-8,
    ):
        super().__init__()

        self.epsilon = epsilon
        self.F, self.p = smart_teleport(adj)

    def forward(
        self,
        x: Tensor,
        s: Tensor,
        eps: float = 1e-8,
    ):
        s = s + eps

        out_adj = s.T @ self.F @ s

        diag = torch.sparse_coo_tensor(
            indices=[range(len(out_adj)), range(len(out_adj))],
            values=torch.diag(out_adj),
            size=out_adj.shape,
        ).to(device=s.device)

        e1 = torch.sum(out_adj) - torch.trace(out_adj)
        e2 = torch.sum(out_adj - diag, 1)
        e3 = self.p
        e4 = torch.sum(out_adj, 1) + torch.sum(out_adj.T - diag, 1)

        e1 = torch.sum(e1 * torch.nan_to_num(torch.log2(e1), nan=0.0))
        e2 = torch.sum(e2 * torch.nan_to_num(torch.log2(e2), nan=0.0))
        e3 = torch.sum(e3 * torch.nan_to_num(torch.log2(e3), nan=0.0))
        e4 = torch.sum(e4 * torch.nan_to_num(torch.log2(e4), nan=0.0))

        map_equation_loss = e1 - 2 * e2 - e3 + e4

        out = torch.matmul(s.T, x)

        return out, out_adj, map_equation_loss