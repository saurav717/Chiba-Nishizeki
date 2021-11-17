import numpy as np
import pandas as pd
import sys
import copy
from more_itertools import sort_together
import node as n
sys.setrecursionlimit(10000)



class tree:
    def __init__(self, data):
    # within class used variables

        self.table = data["table"]
        self.columns = list(np.unique(list(self.table.columns)))
        self.current_column = None
        self.init_nodes = None
        self.current_nodes = self.init_nodes
        self.init()
        self.iterator = None
        self.started = False

    # outside class using variables 
        self.open = None 
        self.up = None 
    
    def get_open(self, nodes_list):
        return self.init_nodes[0]
        for node in nodes_list:
            if(node.explored == False):
                return node
            else: 
                return node.parent


    def open_(self):
        # return self.init_nodes[0]
        if self.started == False:
            self.started  = True 
            self.iterator = self.init_nodes[0]
            return self.iterator

        self.iterator = self.get_open(self.iterator.children)        


    def makeTree(self,current_nodes):
        for i in range(len(current_nodes)):
            node_ = current_nodes[i]
            current_column = node_.column
            if(current_column == self.columns[-1]):
                return
            node_children = list(node_.child_vals)
            cnodes = []
            data = {
                    "peers" : node_children, 
                    "current column": self.columns[self.columns.index(self.current_column)+1],
                    "explored" : False  
                    }
            
            if(len(node_children)!=0):
                for cnode in node_children:
                    data["value"] = cnode 
                    if(current_column != self.columns[-1]):

                        data["child vals"] = self.table[self.table[self.current_column]==cnode][self.columns[self.columns.index(self.current_column)+1]]
                    else:
                        data["child vals"] = [] 
                    if(cnode == node_children[-1]):
                        data["atEnd"] = True
                    else:
                        data["atEnd"] = False
                    obj = n.node(data,node_)
                    cnodes.append(obj)
                for i in range(len(cnodes)-1):
                    cnodes[i].next = cnodes[i+1]
                cnodes[-1].next = None
                node_.children = cnodes 
                self.makeTree(cnodes)


    def init(self): 
        if self.current_column == None:
            self.current_column = self.columns[0]
            print("columns = ",self.columns)
            # col_vals = list(self.table.sort_values(by=self.current_column, ascending=True)[self.current_column].values)
            # col_vals = np.sort(list(self.table[self.current_column].values))
            col_vals = list(set(self.table[self.current_column].values))
            cols = []
            data = {
                    "peers" : col_vals, 
                    "current column": self.current_column,
                    "explored" : False  
                    }
            for i in range(len(col_vals)):
                val = col_vals[i]                
                data["value"] = val
                if(len(self.columns)!=1): 
                    data["child vals"] = self.table[self.table[self.current_column]==val][self.columns[self.columns.index(self.current_column)+1]]
                else:
                    data["child vals"] = []
                if(val == col_vals[-1]):
                    data["atEnd"] = True 
                else:
                    data["atEnd"] = False
                obj = n.node(data, None)
                cols.append(obj)
            self.init_nodes = cols
            for i in range(len(self.init_nodes)-1):
                self.init_nodes[i].next = self.init_nodes[i+1]
            self.init_nodes[-1].next = None
                
            if(len(self.columns)!=1):
                self.makeTree(self.init_nodes)

