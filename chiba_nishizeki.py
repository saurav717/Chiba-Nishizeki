import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

gqrc = pd.read_csv("data.txt", delimiter = "\t")

information = {
"total nodes" : 5242,
"total edges" : 28980, 
"total triangles" : 48260
}
print("total nodes = 5242")
print("total edges = 28980")
print("total triangles = 48260")
print()
print("edge list")
print()
print(gqrc.head())


def degree_sorted_nodes(dictionary): # sorts the nodes in decreasing order of their degrees
    return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse = True)}


def chiba_nishizeki(data):

    graph_data = data["edgelist"] # columns = [FromNodeId, ToNodeId]
    graph_data = graph_data[graph_data["FromNodeId"]!=graph_data["ToNodeId"]]
    edge_list = graph_data
    nodes = np.unique(graph_data["FromNodeId"])
    node_degree = dict()
    for x in nodes:
        node_degree[x] = graph_data[graph_data["FromNodeId"] == x].shape[0]
    nodes = degree_sorted_nodes(node_degree)
    nodeIDs = list(nodes.keys())
    triangles = []
    for i in range(len(nodeIDs)-2):
        node = nodeIDs[i]
        node_neighbours = np.unique(list(edge_list[edge_list["FromNodeId"] == node]["ToNodeId"]))
        marked_nodes = list(node_neighbours)
        for neighbour in node_neighbours:
            neighbour_neighbours = np.unique(list(edge_list[edge_list["FromNodeId"]==neighbour]["ToNodeId"]))
            for third_neighbour in neighbour_neighbours:
                if(third_neighbour in marked_nodes):
                    triangles.append([node,neighbour,third_neighbour])
            marked_nodes.remove(neighbour)
        edge_list = edge_list[edge_list["FromNodeId"]!=node]
        edge_list = edge_list[edge_list["ToNodeId"]!=node]


    print("_____________________________________________________")
    print("total triangles = ",len(triangles))
    print("_____________________________________________________")


data = {
        "edgelist" : gqrc,
        }
        

chiba_nishizeki(data)
