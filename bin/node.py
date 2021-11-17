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
        