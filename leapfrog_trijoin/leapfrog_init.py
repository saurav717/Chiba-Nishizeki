import numpy as np
import pandas as pd
import sys
import copy
from more_itertools import sort_together
sys.setrecursionlimit(10000)

import node as n
import tree as t
import lptj as l
import sys, os 

args = sys.argv[1:]

data = pd.read_csv(sys.path[0]+"/../datasets/"+args[0], delimiter = "\t")
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

tree1 = t.tree(info1)
tree2 = t.tree(info2)
tree3 = t.tree(info3)

columns = set(list(relation1.columns) + list(relation2.columns) + list(relation3.columns))

n1 = tree1.open_() #open_ gives you the iterator of the tree
n2 = tree2.open_()
n3 = tree3.open_()

# information = {
#     "iterators": [n1,n2, n3], 
#     "columns"  : columns,
#     "relation" : relation1
# }

# lj = l.lptj(information)



# print("intersection = ", lj.intersection)

keys = list(np.unique(relation1["X"]))
vals = np.zeros(len(np.unique(relation1["X"])))
dictionary = dict(zip(keys, vals))


n1.peer_nodes = np.unique(list(relation1["X"].values))
information = {
    "iterators" : [n1,n2,n3],
    "columns"   : columns, 
    "relation"  : relation1,
    "hash_table": dictionary
}



tj = l.lptj(information)

print("triangles found = ", tj.triangles)