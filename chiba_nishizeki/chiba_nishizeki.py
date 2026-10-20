import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import os,sys 
from tqdm import tqdm

args = sys.argv[1:]
# args = "musae_git_edges.csv"

if(args[0][-3:] == "csv"):
    gqrc = pd.read_csv(sys.path[0] + "/../datasets/"+args[0], delimiter = ",")
if(args[0][-3:] == "txt"):
    gqrc = pd.read_csv(sys.path[0] + "/../datasets/"+args[0], delimiter = "\t")
# gqrc = pd.read_csv(sys.path[0]+"/../datasets/" + args[0], delimiter = "\t")

columns = list(gqrc.columns)

print("columns = ", columns)

gqrc = gqrc.rename(columns = {columns[0] : "FromNodeId", columns[1]: "ToNodeId"})


# information = {
# "total nodes" : 5242,
# "total edges" : 28980, 
# "total triangles" : 48260
# }

columns = gqrc.columns
print("total nodes = ", len(np.unique(gqrc[columns[0]])))
print("total edges = ", gqrc.shape[0])
if(args[0] == "data.txt"):
    print("total triangles = 48260")
print()
print("edge list")
print()
print(gqrc.head())


def build_adjacency(edge_list): # undirected adjacency sets; each edge counted once regardless of direction
    adjacency = dict()
    for u, v in zip(edge_list["FromNodeId"].to_numpy(), edge_list["ToNodeId"].to_numpy()):
        if u == v:
            continue
        adjacency.setdefault(u, set()).add(v)
        adjacency.setdefault(v, set()).add(u)
    return adjacency


def chiba_nishizeki(data):

    adjacency = build_adjacency(data["edgelist"]) # columns = [FromNodeId, ToNodeId]
    # process nodes in decreasing order of degree
    nodeIDs = sorted(adjacency, key = lambda x: len(adjacency[x]), reverse = True)
    print("complete")
    triangles = []
    for node in tqdm(nodeIDs, desc = "running"):
        marked_nodes = set(adjacency[node])
        for neighbour in adjacency[node]:
            for third_neighbour in adjacency[neighbour]:
                if third_neighbour in marked_nodes:
                    triangles.append([node, neighbour, third_neighbour])
            marked_nodes.discard(neighbour)
        # delete node from the graph
        for neighbour in adjacency[node]:
            adjacency[neighbour].discard(node)
        adjacency[node] = set()

    print("completed")
    print("_____________________________________________________")
    print("total triangles = ",len(triangles))
    print("_____________________________________________________")
    return triangles


data = {
        "edgelist" : gqrc,
        }
        

chiba_nishizeki(data)
