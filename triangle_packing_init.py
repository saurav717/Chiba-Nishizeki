import numpy as np
import networkx as nx
import pandas as pd 
import matplotlib.pyplot as plt
import os, sys
import triangle_packing as tp

args = sys.argv[1:]

# print("this worked")
graph_data = pd.read_csv(args[0], delimiter = "\t")


data = {
    "edge_list" : graph_data,
    "K" : 15, 
    "shuffle" : True,
}

packing = tp.triangle_packing(data)