import numpy as np
import pandas as pd
import sys
import copy
from more_itertools import sort_together
sys.setrecursionlimit(10000)

import leapfrog_join as l
import node as n 
import tree as t


class lptj:
    def __init__(self, data):
        self.iterators         = data["iterators"]
        self.columns           = list(np.sort(list(data["columns"])))
        self.current_treeLevel = None
        self.depth             = -1 
        self.current_nodes     = self.iterators

        self.triangles         = 0
        self.explored          = data["hash_table"]
        self.ltriangles        = []
        self.file              = open("triangles.txt", "w") 
        self.init()        



    def get_next(self, iterators, tlist):#, ecolumn):
        nodes = []
        for node in iterators:
            if(node.next == None):
                return None 
            nodes.append(node.next)

        information = {
            "iterators" : nodes
        }

        lj = l.leapfrog_join(information)

        if(lj.next == None):
            return None

        # while(lj.next[0].value in ecol):
        #     nodes = self.get_next(nodes, tlist+[nodes[0].value])
        #     if(nodes == None):
        #         return None  
        # if(nodes == None):
        #     break

        
        return lj.next 


    def get_children(self,nodes):
        cnodes = []
        for node in nodes:
            if(node.children!=None):
                cnodes.append(node.children[0])
        return cnodes



    def tri_iter(self, current_nodes, depth, tlist, ecolumn):
        iterators = []
        toIterate = []
        for iterator in current_nodes:
            if(iterator.column == self.columns[depth]):
                iterators.append(iterator)
            else:
                toIterate.append(iterator)

        data = {
            "iterators" : iterators
        }

        # if(tlist == None):
        #     print(tlist)
        lj = l.leapfrog_join(data)
        nodes = lj.next

        # next_column = []
        while(nodes != None):

            if(depth == 0):
                self.explored[nodes[0].value] = 1

            else:
                while(self.explored[nodes[0].value]==1):
                    nodes = self.get_next(nodes, tlist+[nodes[0].value])
                    if(nodes == None):
                        break 
                if(nodes == None):
                    break


            if(depth == 1):
                ecolumn.append(nodes[0].value) 

            if (depth == 2): # instead of checking column here, check depth
                # if(set(tlist + [nodes[0].value]) not in self.ltriangles):
                if(nodes[0].value not in ecolumn):
                    self.triangles+=1
                    # self.ltriangles.append(set(tlist + [nodes[0].value]))
                    self.file.write(str(tlist + [nodes[0].value, nodes[0].column]))
                

            else:
                cnodes = self.get_children(nodes)
                if(nodes[0].column == self.columns[0]):
                    self.tri_iter(cnodes+toIterate, depth+1, tlist + [nodes[0].value, nodes[0].column], [])
                    # nodes = self.get_next(nodes, tlist + [nodes[0].value], [])
                if(nodes[0].column == self.columns[1]):
                    self.tri_iter(cnodes+toIterate, depth+1, tlist + [nodes[0].value, nodes[0].column], ecolumn)
                    # nodes = self.get_next(nodes, tlist + [nodes[0].value], ecolumn)

                        
            nodes = self.get_next(nodes, tlist + [nodes[0].value])

        self.depth -=1 


    def init(self):
        if(self.current_treeLevel == None): #checks if we are at root 
            self.current_treeLevel = self.columns[self.depth + 1]
            self.depth += 1
            triangle = []
            # print(self.current_nodes[0].peer_)
            self.tri_iter(self.current_nodes, self.depth, triangle, [])  
            self.file.close()       

