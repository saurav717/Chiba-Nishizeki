import numpy as np
import networkx as nx
import pandas as pd 
import matplotlib.pyplot as plt
import getopt, sys
import random

# print("this worked too")
# graph_data = pd.read_csv("data.txt", delimiter = "\t")


# print("total nodes = 5242")
# print("total edges = 28980")
# print()
# print("edge list")
# print()
# print(graph_data.head())


class triangle_packing:

    def __init__(self, data):
        self.edge_list = data["edge_list"]
        self.nodeIDs = np.unique(np.concatenate([self.edge_list["FromNodeId"].to_numpy(), self.edge_list["ToNodeId"].to_numpy()]))

        self.num_colors = data["K"]
        self.colors = list(range(self.num_colors))
        random.shuffle(self.colors)
        self.shuffle = data["shuffle"]

        self.node_colors = None
        self.one_colored_edgelist = None
        self.tpacking = False
        self.init() 
        # self.packing_init()

    def degree_sorted_nodes(self, dictionary): # sorts the nodes in decreasing order of their degrees
        return {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse = True)}

    def check_exhaustion(self, lst1):
        lst3 = [value for value in lst1 if value in self.colors]
        if(len(lst3)>0):
            return "no"
        elif(len(lst3)==0):
            return "yes"

    def color_nodes(self):
        node_colors = dict()
        for i in self.nodeIDs:
            node_colors[i] = self.colors[i%self.num_colors]
            if(len(node_colors)%self.num_colors == 0 and self.shuffle == True):
                np.random.shuffle(self.colors)
        self.node_colors = node_colors 


    def build_adjacency(self, edge_list): # undirected adjacency sets; each edge counted once regardless of direction
        adjacency = dict()
        for u, v in zip(edge_list["FromNodeId"].to_numpy(), edge_list["ToNodeId"].to_numpy()):
            if u == v:
                continue
            adjacency.setdefault(u, set()).add(v)
            adjacency.setdefault(v, set()).add(u)
        return adjacency

    def chiba_nishizeki(self,data): # returns "yes" as soon as one triangle is found
        adjacency = self.build_adjacency(data["edgelist"]) # columns = [FromNodeId, ToNodeId]
        nodeIDs = sorted(adjacency, key = lambda x: len(adjacency[x]), reverse = True)
        for node in nodeIDs:
            marked_nodes = set(adjacency[node])
            for neighbour in adjacency[node]:
                if not adjacency[neighbour].isdisjoint(marked_nodes):
                    return "yes"
                marked_nodes.discard(neighbour)
            for neighbour in adjacency[node]:
                adjacency[neighbour].discard(node)
            adjacency[node] = set()
        return "no"


    def find_triangle(self, color):
        one_colored_nodes = [k for k,v in self.node_colors.items() if v == color]
        # subgraph induced on the one-colored nodes: both endpoints must have this color
        one_colored_edgelist = self.edge_list.loc[self.edge_list['FromNodeId'].isin(one_colored_nodes) & self.edge_list['ToNodeId'].isin(one_colored_nodes)]
        # one_colored_edgelist = self.edge_list[self.edge_list["FromNodeId"]==one_colored_nodes]
        data = {
            "edgelist" : one_colored_edgelist
        }
        triangle_found = self.chiba_nishizeki(data)
        return triangle_found

    def packing(self, colorlist, edgelist):
        unexplored_colors = list(set(self.colors) - set(colorlist))
        # print("len = ",len(unexplored_colors))
        if(len(unexplored_colors)==0):
            # print("ptacking found")
            return "yes"
        found = None

        for color in unexplored_colors:
            # one_colored_nodes = [k for k,v in self.node_colors.items() if v == color]
            if(self.find_triangle(color) == "no"):
                # print("this happened")
                break
            colorlist.append(color)
            one_color_nodes = [k for k,v in self.node_colors.items() if v == color]
            # updated_edgelist = edgelist[edgelist["FromNodeId"]!=one_color_nodes]
            # updated_edgelist = edgelist[edgelist["ToNodeId"]!=one_color_nodes]
            found = self.packing(colorlist,edgelist) 
        
        return found


    def packing_init(self):
        # color_list = self.colors
        self.color_nodes()
        
        for color in self.colors:
            # print(color)
            current_colorlist = []
            one_colored_nodes = [k for k,v in self.node_colors.items() if v == color] # we picked one colored nodes
            if(self.find_triangle(color) == "no"):
                break
            
            current_colorlist.append(color)
            one_colored_nodes = [k for k,v in self.node_colors.items() if v == color]
            edgelist = self.edge_list
            # updated_edgelist = edgelist[edgelist["FromNodeId"]!=one_colored_nodes]
            # updated_edgelist = edgelist[edgelist["ToNodeId"]!=one_colored_nodes]
            # print("this working?")
            if(self.packing(current_colorlist, self.edge_list)=="yes"):
                print("K = ",self.num_colors, " -- packing found")
                self.tpacking = True
                break

            else:
                print("no packing found")
                break
    
    def init(self):
        # print(self.num_colors)
        for i in range(int(np.exp(self.num_colors))):
            self.packing_init() 
            if(self.tpacking == True):
                break 

# %%time
# data = {
#     "edge_list" : graph_data,
#     "K" : 15, 
#     "shuffle" : True,
# }

# packing = triangle_packing(data)
# # packing.packing_init()
