import numpy as np
import networkx as nx
import pandas as pd 
import matplotlib.pyplot as plt
import os, sys
import triangle_packing as tp

args = sys.argv[1:]

# print("this worked")
graph_data = pd.read_csv(sys.path[0] + "/../datasets/"+args[0], delimiter = "\t")


K = [1,5,10,15,20]

for k in K:
    data = {
        "edge_list" : graph_data,
        "K" : k, 
        "shuffle" : True,
    }

    packing = tp.triangle_packing(data)