import getopt, sys
import os 
 
argumentList = sys.argv[1:]

# print("args: ", argumentList[0])

if(len(argumentList) != 2 ):

    if(argumentList[0] == "datasets"):
        os.system("ls datasets")

    else:
        print("please enter two arguments \n")
        print("first argument: File Name ")
        print("second argument: operation ")
        print()
        print("Example command: python3.9 test_tripack.py CaGrQc triangle_packing")


elif(argumentList[0] == "--help"):
    print("available operations: triangle_packing, find_triangles")
    print("available methods for triangle_packing: FPT algorithm")
    print("available methods for find_triangles: chiba_nishizeki, leapfrog_trijoin")

    print("please enter two arguments")
    print("first argument: File Name ")
    print("second argument: operation ")
    print()
    print("Example command: python3.9 test_tripack.py CaGrQc triangle_packing")

# if(len(argumentList[1:]) < 2):
#     print("please enter two arguments")
#     print("first argument: File Name ")
#     print("second argument: operation ")
#     print()
#     print("Example command: python3.9 test_tripack.py CaGrQc triangle_packing")

else: 
    dataset    = argumentList[0]
    operation  = argumentList[1]

    # print("we came here")

    if(operation not in ["triangle_packing", "find_triangles"]):
        print("enter correct operation")
    
    else: 
        if(operation == "triangle_packing"):
            print("this worked")
            # os.system("python3.9 triangle_packing/triangle_packing_init.py "+ dataset )#+ ".txt")
            os.system("python3.9 -m cProfile -o triangle_packing/result/triangle_packing.prof triangle_packing/triangle_packing_init.py " + dataset)
            os.system("python3.9 -m flameprof triangle_packing/result/triangle_packing.prof > triangle_packing/result/triangle_packing.svg")
            os.system("open -a 'firefox' ./triangle_packing/result/triangle_packing.svg")

            # os.system("python3.9 -m memory_profiler triangle_packing/triangle_packing_init.py " + dataset)
            os.system("mprof run triangle_packing/triangle_packing_init.py " + dataset)
            os.system("mprof plot")

            

        if(operation == "find_triangles"):
            print("select a method")
            print("1: chiba_nishizeki")
            print("2: leapfrog trijoin")
            method = int(input("enter the index of method: "))

            if(method == 1):
                # os.system("python3.9 chiba_nishizeki/chiba_nishizeki.py "+ dataset)

                os.system("python3.9 -m cProfile -o chiba_nishizeki/result/chiba_nishizeki.prof chiba_nishizeki/chiba_nishizeki.py " + dataset)
                os.system("python3.9 -m flameprof chiba_nishizeki/result/chiba_nishizeki.prof > chiba_nishizeki/result/chiba_nishizeki.svg")
                os.system("open -a 'firefox' ./chiba_nishizeki/result/chiba_nishizeki.svg")

                # os.system("python3.9 -m memory_profiler chiba_nishizeki/chiba_nishizeki.py " + dataset)
                os.system("mprof run chiba_nishizeki/chiba_nishizeki.py " + dataset)
                os.system("mprof plot ")

            
            if(method == 2):
                # print("using leapfrog_trijoin")
                os.system("python3.9 -m cProfile -o leapfrog_trijoin/result/leapfrog_trijoin.prof leapfrog_trijoin/leapfrog_init.py " + dataset)
                # os.system("python3.9 -m cProfile -o chiba_nishizeki/result/chiba_nishizeki.prof chiba_nishizeki/chiba_nishizeki.py " + dataset)
                os.system("python3.9 -m flameprof leapfrog_trijoin/result/leapfrog_trijoin.prof > leapfrog_trijoin/result/leapfrog_trijoin.svg")
                os.system("open -a 'firefox' ./leapfrog_trijoin/result/leapfrog_trijoin.svg")

                # os.system("python3.9 -m memory_profiler leapfrog_trijoin/leapfrog_init.py " + dataset)
                os.system("mprof run leapfrog_trijoin/leapfrog_init.py " + dataset)
                os.system("mprof plot")






 
