import numpy as np
import networkx as nx
import pandas as pd 
import random
import matplotlib.pyplot as plt


class triangle_packing:

    def __init__(self, data):
        self.edge_list = data["edge_list"]
        self.nodeIDs = np.unique(list(self.edge_list["FromNodeId"]))

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


    def chiba_nishizeki(self,data):
        graph_data = data["edgelist"] # columns = [FromNodeId, ToNodeId]
        graph_data = graph_data[graph_data["FromNodeId"]!=graph_data["ToNodeId"]]
        edge_list = graph_data
        nodes = np.unique(graph_data["FromNodeId"])
        node_degree = dict()
        for x in nodes:
            node_degree[x] = graph_data[graph_data["FromNodeId"] == x].shape[0]
        nodes = self.degree_sorted_nodes(node_degree)
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
                        return "yes"
                marked_nodes.remove(neighbour)
            edge_list = edge_list[edge_list["FromNodeId"]!=node]
            edge_list = edge_list[edge_list["ToNodeId"]!=node]

        # if(len(triangles) > 0):
        #     print("triangles - ", len(triangles))
        #     return "yes"
        # else:
        return "no"


    def find_triangle(self, color):
        one_colored_nodes = [k for k,v in self.node_colors.items() if v == color]
        one_colored_edgelist = self.edge_list.loc[self.edge_list['FromNodeId'].isin(one_colored_nodes)]
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
                print("packing found")
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