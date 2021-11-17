
## **CS599 Graph Analytics** by  **Dr. Charalampos Tsourkakis** at Boston University 

Clone the repository and follow the below given instructions to run the codes


An example format of command you need to run is like the one below

```python3.9 cs599.py <dataset.txt> <operation>```

We basically do two operations 
- find_triangles
- triangle_packing

Then you will come across this text when you select find_triangles

Methods available 
1) Chiba_nishizeki
2) leapfrog trijoin

Select the method index : 

Based on the index you select, one of the methods will be executed and you will see the output in the terminal 

A **Flame Graph** will appear on firefox browser and **memory profile** will pop up after a while as a pop up




The code will run twice, first time to check the duration of execution and the second time to check how much memory the code is occupying during the execution of the code 


## To find triangle packing for a data 

### Try Executing the following codes mentioned
- For grqc dataset
``` python3.9 cs599.py grqc.txt triangle_packing ```

- For github social
``` python3.9 cs599.py musae_git_edges.csv triangle_packing```

- For web berkstan dataset
```python3.9 cs599.py web-BerkStan.txt triangle_packing```

### About Implemented Algorithm 

 It is a **Fixed parameter tractable problem** with 'K' as the parameter. K stands for the number of colors with which we are randomly coloring the graph. 

 ### Problem 2.1: Proof that the implemented algorithm is NP-complete [insert link here]

insert text here

 ### Problem2.2 Time Complexity
 
 Number of total combinations of colors we search for finding a triangle in each color = 2^(k)

 at each one colored nodes, we use chiba nishizeki algorithm to find the triangles. Worst case time complexity to find the triangles = O(n^3)

 Total time complexity = O(2^k n^3) ≈ O(2^k n^O(1))

 since the time complexity of our algorithm is equivalent to that of a fixed point tractable algorithm as it should be  



### Problem 2.3 Output for different values of 'k' for grqc graph
#### Algorithm output with k = 5, 10, 15, 20


|   K	|   output	            | Runtime  	| Memory usage  	|   
|---	|---	                |---	    |---	            |
|   5	|   Packing found	    |   	    |                	|
|   10	|   Packing found	    |        	|                	|
|   15	|   Packing found	    |        	|                	|
|   20	|   Packing found	    |       	|                	|


## Problem 3: Implementation of Triangle finding algorithms
After you execute one of the below commands in terminal, you will be prompted to select one of the two methods specified 

1) **Chiba Nishizeki** 
2) **Leapfrog trijoin** 

- For grqc dataset
``` python3.9 cs599.py grqc.txt find_triangles ```

- For github social
``` python3.9 cs599.py musae_git_edges.csv find_triangles```

- For web berkstan dataset
```python3.9 cs599.py web-BerkStan.txt find_triangles```


### Time comparison for different datasets with Chiba Nishizeki and leapfrog trijoin algorithm

|   	| Chiba Nishizeki  	|  Leapfrog Trijoin  	|   
|---	|---	|---	|
| **grqc dataset**  	|   	|   	|   	
| **github social dataset**  	|   	|   	|   	
| **web berkstan dataset**  	|   	|   	|   	

### Memory comparison for different datasets with Chiba Nishizeki and leapfrog trijoin algorithm

|   	|   Chiba Nishizeki	|  Leapfrog Trijoin  	|   	|   	|
|---	|---	|---	|---	|---	|
|  **grqc dataset**  	|   	|   	|   	|   	|
|  **github social dataset** 	|   	|   	|   	|   	|
|  **web berkstan dataset** 	|   	|   	|   	|   	|




