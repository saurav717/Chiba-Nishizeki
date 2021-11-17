import numpy as np
import pandas as pd
import sys
import copy
from more_itertools import sort_together
sys.setrecursionlimit(10000)

import tree as t
import node as n 


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

        self.max_iter = n.node(d1) 
        self.min_iter = n.node(d1)
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
        