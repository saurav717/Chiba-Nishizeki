
## **CS599 Graph Analytics** by  **Dr. Charalampos Tsourkakis** at Boston University 

To run the codes: 

*  Clone the repository 


python3.9 cs599.py <dataset.txt> <operation>

We basically do two operations 
    - Find_triangles
    - triangle_packing

Then you will come across this text 

Methods available 
1) Chiba_nishizeki
2) leapfrog trijoin

Select the method index : 1/2

after selecting the index, the code will automatically run on the selected dataset and will display two images 

one is a flame graph which will open in a browser which is firefox by default. If you dont have firefox, please change the browser name in the code for now. This will be update in future 

You will be able to see how long the algorithm took to execute and the memory it occupied during the whole duration of its execution

The code will run twice, first time to check the duration of execution and the second time to check how much memory the code is occupying during the execution of the code 


## To find triangle packing for a data 

#### An example for grqc dataset
- For grqc dataset
``` python3.9 cs599.py grqc.txt triangle_packing ```

- For github social
``` python3.9 cs599.py musae_git_edges.csv triangle_packing```

- For web berkstan dataset
```python3.9 cs599.py web-BerkStan.txt triangle_packing```

## To find Triangles in a given dataset

After you execute one of the below commands in terminal, you will be prompted to select one of the two methods specified 

1) Chiba Nishizeki 
2) Leapfrog trijoin 

- For grqc dataset
``` python3.9 cs599.py grqc.txt find_triangles ```

- For github social
``` python3.9 cs599.py musae_git_edges.csv find_triangles```

- For web berkstan dataset
```python3.9 cs599.py web-BerkStan.txt find_triangles```



