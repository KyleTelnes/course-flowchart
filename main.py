import igraph
# re is used for validation
import re

def Validate_Input(filename):
    f = open(filename, "r")
    for line in f:
        # Validate the format with a regular expression
        x = re.search("[A-Z][A-Z][A-Z]\s\d\d\d\d,(\s\w+)*,\s\d,\s\[([A-Z][A-Z][A-Z]\s\d\d\d\d)?(,\s([A-Z][A-Z][A-Z]\s\d\d\d\d))*\],\s\[(\d)?(,\d)*\]", line)
        if x == None or x.start() != 0:
            return False
    return True
            

def main():
    if Validate_Input("test.txt") != False:
        print("File Format is Valid!")
    else:
        print("File Format is Not Valid!")
    #dg = igraph.Graph(directed=True)
    
    #dg.add_vertices(5)
    #dg.add_edge(1, 2)
    #dg.add_edge(3, 1)
    #dg.add_edge(4, 0)
    #dg.add_edge(2, 0)
    #dg.vs["name"] = ["CSC 3430", "CSC 2430", "CSC 2431", "CSC 1230", "MAT 2200"]
    #dg.vs["class_name"] = ["Algorithms Analysis and Design", "Data Structures I", "Data Structures II", "Problem Solving and Programming", "Statistics"]
    #dg.vs["credit"] = [4, 5, 5, 5, 5]
    #dg.vs["pre_req"] = [["CSC 2431", "MAT 2200"], ["CSC 1230"], ["CSC 2430"], [], []]
    #dg.vs["quarter_offered"] = [[2], [2,3], [1,3], [], []]

    #starting_quarter = input()
    #print(starting_quarter)

    #layout = dg.layout("kk")
    #igraph.plot(dg, layout=layout)
    #print(dg.is_dag())


if __name__ == "__main__":
    main()