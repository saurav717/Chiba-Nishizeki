import getopt, sys
import os 
 
argumentList = sys.argv[1:]

print("args: ", argumentList)
if(len(argumentList) != 2 ):
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
            os.system("python3.9 triangle_packing_init.py "+ dataset )#+ ".txt")
            

        # if(operation == "find_triangles"):
        #     print("select a method")
        #     print("1: chiba_nishizeki")
        #     print("2: leapfrog trijoin")
        #     method = input("enter the index of method")

        #     if(method == 1):
            
        #     if(method == 2):






 
