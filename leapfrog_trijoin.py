import numpy as np
import pandas as pd
import sys
import copy
from more_itertools import sort_together
sys.setrecursionlimit(10000)


class node:
    def __init__(self, data, parent=None):
        self.value      = data["value"]
        self.peer_nodes = data["peers"]
        self.column     = data["current column"]
        self.parent     = parent
        self.child_vals = data["child vals"]
        self.children   = None
        self.explored   = data["explored"] 
        self.atEnd      = data["atEnd"]
        self.next       = None

    def open(self):

        if(self.children != None):
            return self.children[0] 
        else:
            return None

    def up(self):
        return self.parent 
        

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
                    obj = node(data,node_)
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
                obj = node(data, None)
                cols.append(obj)
            self.init_nodes = cols
            for i in range(len(self.init_nodes)-1):
                self.init_nodes[i].next = self.init_nodes[i+1]
            self.init_nodes[-1].next = None
                
            if(len(self.columns)!=1):
                self.makeTree(self.init_nodes)


class leapfrog_join: # performs unary join
    def __init__(self, data):
        self.iterators = []
        for i in data["iterators"]:
            self.iterators.append(i)
        self.atEnd = False
        self.p = None

        d1 = {
            "value"          : -np.inf, 
            "peers"          : None, 
            "current column" : None, 
            "child vals"     : None, 
            "explored"       : None, 
            "atEnd"          : None 
        }

        self.max_iter = node(d1) 
        self.min_iter = node(d1)
        self.min_iter.value = np.inf

        self.intersection = []
        self.next = None 
        self.k = len(self.iterators)
        self.key = None 

        self.leapfrog_init()
    
    
    def seek(self, value):
        while(True):
            if(self.iterators[self.p]==None):
                return
            if(self.iterators[self.p].value < value):
                self.iterators[self.p] = self.iterators[self.p].next   
            else:
                return

    def leapfrog_seek(self, value): # To complete the linear iterator interface, we use leapfrog_seek()
        self.iterators[self.p] = self.iterators[self.p]
        if(self.iterators[self.p].atEnd == True):
            self.atEnd = True 
        else:
            self.p = self.p+1 % len(self.iterators)
            self.leapfrog_search()


    def check_all(self):
        for i in range(len(self.iterators)-1):
            if(self.iterators[i].value!=self.iterators[i+1].value):
                return False 
        return True 


    def leapfrog_search(self): # this follows leapfrog join init. The join iterator is positioned at the first result
        x_ = self.iterators[(self.p - 1)%self.k].value

        while(1):
            if(self.iterators[self.p]==None):
                return 
            x = self.iterators[self.p].value
            # print(x," ",  x_, " " , self.check_all())
            if(x == x_ and self.check_all()):
                self.key = x 
                self.intersection.append(x)
                self.next = self.iterators 
                self.Found = True
                return 
            else:
                self.seek(x_) # we seeked the max value among the iterators
                if(self.iterators[self.p]==None):
                    # print("this happened ", x_)
                    return 
                if(self.iterators[self.p].atEnd == True):
                    self.atEnd = True 
                    x_ = self.iterators[self.p].value 
                    self.p = (self.p+1)%len(self.iterators) 
                else:
                    x_ = self.iterators[self.p].value 
                    self.p = (self.p+1)%len(self.iterators) 



    def leapfrog_next(self): # subsequent results are obtained by this leapfrog_next()
        if(self.iterators[self.p]==None):
            return 
        
        if(self.iterators[self.p].atEnd == True ):
            return

        if(self.Found == True):
            return 
        
        self.iterators[self.p] = self.iterators[self.p].next 

        if(self.iterators[self.p].atEnd == True):
            self.atEnd = True
            self.leapfrog_search() 
            if(self.Found == True):
                return 

        else:
            self.p = (self.p+1)%self.k 
            self.leapfrog_search()
            if(self.Found == True):
                return
            self.leapfrog_next()


    def sort(self):
        flist = [] 
        for iterator in self.iterators:
            flist.append(iterator.value)
        s = sort_together([flist, self.iterators])[1]
        self.iterators = list(s)
        # print("flist = ", flist)
        # self.iterators = [x for _,x in sorted(zip(flist, self.iterators))]


    def leapfrog_init(self):  # initializes the leapfrog join algorithm
        # self.sort() 
        for iterator in self.iterators:
            if(iterator == None):
                return 
            if(iterator.atEnd==True): # iterator points to node, node has attributes
                self.atEnd=True 
        # self.sort()
        self.p = 0 
        self.leapfrog_search()
        self.leapfrog_next()
        self.Found = False
        
class lptj:
    def __init__(self, data):
        self.iterators         = data["iterators"]
        self.columns           = list(np.sort(list(data["columns"])))
        self.current_treeLevel = None
        self.depth             = -1 
        self.current_nodes     = self.iterators

        self.triangles         = 0
        self.explored          = data["hash table"]
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

        lj = leapfrog_join(information)

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
        lj = leapfrog_join(data)
        nodes = lj.next

        # next_column = []
        while(nodes != None):

            if(nodes[0].column == self.columns[0]):
                self.explored[nodes[0].value] = 1

            else:
                while(self.explored[nodes[0].value]==1):
                    nodes = self.get_next(nodes, tlist+[nodes[0].value])
                    if(nodes == None):
                        break 
                if(nodes == None):
                    break


            if(nodes[0].column == self.columns[1]):
                ecolumn.append(nodes[0].value) 

            if (nodes[0].column == self.columns[-1]):
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

data = pd.read_csv("data.txt", delimiter = "\t")
data = data[data["FromNodeId"] != data["ToNodeId"]]
relation1 = data.rename(columns = {"FromNodeId": "X", "ToNodeId": "Y"})
relation2 = data.rename(columns = {"FromNodeId": "Y", "ToNodeId": "Z"})
relation3 = data.rename(columns = {"FromNodeId": "X", "ToNodeId": "Z"})

info1 = {
        "table" : relation1
        }

info2 = {
        "table" : relation2
        }
        
info3 = {
        "table" : relation3
        }

tree1 = tree(info1)
tree2 = tree(info2)
tree3 = tree(info3)

columns = set(list(relation1.columns) + list(relation2.columns) + list(relation3.columns))

n1 = tree1.open_() #open_ gives you the iterator of the tree
n2 = tree2.open_()
n3 = tree3.open_()

information = {
    "iterators": [n1,n2, n3], 
    "columns"  : columns,
    "relation" : relation1
}

lj = leapfrog_join(information)

print("intersection = ", lj.intersection)


keys = list(np.unique(relation1["X"]))
vals = np.zeros(len(np.unique(relation1["X"])))
dictionary = dict(zip(keys, vals))


n1.peer_nodes = np.unique(list(relation1["X"].values))
information = {
    "iterators" : [n1,n2,n3],
    "columns"   : columns, 
    "relation"  : relation1,
    "hash table": dictionary
}

tj = lptj(information)

print("triangles found = ", tj.triangles)