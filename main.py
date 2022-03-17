from cProfile import label
import igraph
# re (regular expressions) is used for validation and parsing
import re
import matplotlib.pyplot as plt

'''
Function: Validate_Input
Description:    
    Checks the contents of the file line by line using a
    regular expression to make sure that each line is formatted correctly.
Parameters: 
    filename - the name of the file to validate
Returns: 
    True - if each line has the correct format
    False - if there is a line with incorrect formatting
'''


def Validate_Input(filename):
    f = open(filename, "r")
    for line in f:
        # Validate the format with a regular expression
        x = re.search(
            "^[A-Z][A-Z][A-Z]?\s\d\d\d\d,(\s\w+)*,\s\d,\s\[([A-Z][A-Z][A-Z]?\s\d\d\d\d)?(,\s([A-Z][A-Z][A-Z]?\s\d\d\d\d))*\],\s\[(\d)?(,\d)*\]$",
            line)
        if x == None or x.start() != 0:
            return False
    return True


'''
Function: get_file_name
Description:    
    Asks the user which major they are enrolled in
Parameters: 
    None
Returns: 
    filename that corresponds to the major selected
'''


def get_file_name():
    default_major = "major1.txt"
    selected_major = default_major
    starting_qtr = 1

    while True:
        print(
            "Please select your major: \n 1 -> BA - Computer Science. \n 2 -> BS - Computer Science. \n 3 -> BS - Electrical Engineer. \nInput the corresponding numbers only 1,2 or 3")
        user_input = 1
        try:
            user_input = int(input())
        except ValueError:
            print("Not a valid value.")

        if user_input == 1:
            print("\nSelected major = BA - Computer Science.\n")
            selected_major = default_major
            break
        elif user_input == 2:
            print("\nSelected major = BS - Computer Science.\n")
            selected_major = "major2.txt"
            break
        elif user_input == 3:
            print("\nSelected major = BS - Electrical Engineer.\n")
            selected_major = "major3.txt"
            break
        else:
            print("The major you selected doesn't match the options. Please try again.")
            continue
    return selected_major


'''
Function: get_starting_qtr
Description:    
    Asks the user for the quarter they would like to start in
Parameters: 
    None
Returns: 
    starting_qtr - the quarter the user will be starting in.
'''


def get_starting_qtr():
    # default starting quarter is 1 fall.
    user_input = 1
    starting_qtr = user_input

    while True:
        try:
            print(
                "Which quarter will you be starting this major? \n 0 -> Summer "
                "\n 1 -> Fall or Autumn \n 2 -> Winter \n 3 -> Spring. "
                "\n Input the corresponding numbers only 0, 1,2 or 3")
            user_input = int(input())
        except ValueError:
            print("Not a valid input. Input the corresponding numbers only 0, 1, 2 or 3")
        if user_input == 0:
            starting_qtr = 0
            print("Starting in Summer")
            break
        elif user_input == 1:
            starting_qtr = 1
            print("Starting in Fall/Autumn")
            break
        elif user_input == 2:
            starting_qtr = 2
            print("Starting in Winter")
            break
        elif user_input == 3:
            starting_qtr = 3
            print("Starting in Spring")
            break
        else:
            print("Please input the corresponding numbers only 0, 1, 2 or 3.")
            continue

    return starting_qtr


'''
Function: Get_Max_Credits
Description:    
    Asks the user for the maximum amount of credits that they
    desire per quarter
Parameters: 
    None
Returns: 
    max_credits - the maximum number of credits
'''


def Get_Max_Credits():
    credits = 18
    while True:
        try:
            credits = int(input("Please enter the maximum number of credits per quarter: "))
        # Make sure that the input is a number
        except ValueError:
            print("Not a valid value.")
            continue
        # Validate the input
        if credits < 0:
            print("The value of credits cannot be negative.")
            continue
        if credits > 18:
            print("The value of credits cannot exceed 18.")
            continue
        else:
            break
    return credits


'''
Function: Generate_Graph
Description:    
    Builds Graph from the file specified by the user
Parameters: 
    filename - the name of the file
Returns: 
    dg - the directed graph generated from the file
'''


def Generate_Graph(filename):
    dg = igraph.Graph(directed=True)

    f = open(filename, "r")

    # add all vertices
    i = 0
    for line in f:
        # re is used to get the attributes of the course
        course_code = re.search("^[A-Z][A-Z][A-Z]?\s\d\d\d\d", line).group()
        course_name = re.search(",(\s\w+)*", line).group()[2:]  # [2:] slices off the comma and the space
        credits = re.search(",\s\d", line).group()[2:]
        pre_reqs = re.search(",\s\[([A-Z][A-Z][A-Z]?\s\d\d\d\d)?(,\s([A-Z][A-Z][A-Z]?\s\d\d\d\d))*\]", line).group()[2:]
        quarters = re.search(",\s\[(\d)?(,\d)*\]$", line).group()[2:]

        dg.add_vertex(course_code)
        dg.vs[i]["course_name"] = course_name
        dg.vs[i]["credits"] = credits
        dg.vs[i]["pre_reqs"] = pre_reqs
        dg.vs[i]["quarters"] = quarters
        dg.vs[i]["location"] = 1
        i = i + 1

    # Add Edges
    i = 0
    # iterate through the pre_reqs to create edges
    for x in dg.vs.select(_degree=dg.maxdegree())["pre_reqs"]:
        # iterate through a list of course codes created by a re search for the
        # pattern of the course code (3 letters, a space, and 3 digits)
        for y in re.findall("[A-Z][A-Z][A-Z]?\s\d\d\d\d", x):
            source = dg.vs.find(name=y)
            destination = dg.vs[i]
            destination["location"] = source["location"] + 1
            dg.add_edge(source, destination)
        i = i + 1
    dg.spanning_tree()
    for i in range(0,20):
        print( "name",dg.vs[i]["name"], "Name =", dg.vs[i]["course_name"], " Location =", dg.vs[i]["location"])
    return dg


def main():
    # Select file (major1.txt or major2.txt)
    filename = get_file_name()

    # Get the maxium credits
    max_credits = Get_Max_Credits()

    # Validate Input
    if Validate_Input(filename) != False:
        print("File Format is Valid!")
    else:
        print("File Format is Not Valid!")

    # Ask User for starting quarter
    starting = get_starting_qtr()

    # Build Graph in Memory
    dg = Generate_Graph(filename)
    igraph.summary(dg)

    # Ask User for Maximum Credits
    max_credits = Get_Max_Credits()
    list_of_layers = []
    for i in range(0,20):
        list_of_layers.append(dg.vs[i]["location"])

    print(list_of_layers)
    #  Output text representation of course sequence

    # layout = dg.layout_reingold_tilford_circular(mode="in", root=[1, 5])
    layout = dg.layout_sugiyama(layers=[1, 2, 3, 2, 3, 4, 2, 3, 1, 2, 3, 3, 4, 1, 2, 3, 4, 3, 4, 5], vgap=200)
    layout.rotate(-90, 0, 1)
    igraph.plot(dg, layout=layout, margin=(60, 60, 60, 80), bbox=(1000, 1000), vertex_label=dg.vs["name"],
                vertex_label_size=20, vertex_label_dist=2, vertex_shape="rectangle", vertex_size=50)


if __name__ == "__main__":
    main()
