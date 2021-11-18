import numpy as np
import networkx as nx
import pandas as pd 
import matplotlib.pyplot as plt
import os, sys, psutil
import triangle_packing as tp
import time 

args = sys.argv[1:]

import time
start_time = time.time()
myProcess = psutil.Process(os.getpid())

if(args[0][-3:] == "csv"):
    graph_data = pd.read_csv(sys.path[0] + "/../datasets/"+args[0], delimiter = ",")
if(args[0][-3:] == "txt"):
    graph_data = pd.read_csv(sys.path[0] + "/../datasets/"+args[0], delimiter = "\t")
columns = list(graph_data.columns)

# print("columns = ", columns)

graph_data = graph_data.rename(columns = {columns[0] : "FromNodeId", columns[1]: "ToNodeId"})

K = [1,5,10,15,20]

for k in K:
    start_time = time.time()
    data = {
        "edge_list" : graph_data,
        "K" : k, 
        "shuffle" : True,
    }

    packing = tp.triangle_packing(data)
    print("time for execution = ", (time.time() - start_time))
    # print("CPU time = ", myProcess.cpu_times())
    print("memory used = ", myProcess.memory_full_info()[2], "\n\n")

