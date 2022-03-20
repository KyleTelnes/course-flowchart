from cProfile import label
import igraph
# re (regular expressions) is used for validation and parsing
import re

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

    while True:
        print(
            "Please select your major: \n 1 -> BA - Computer Science. \n 2 -> BS - Computer Science. \n 3 -> BS - Electrical Engineer. \nInput the corresponding numbers only 1, 2 or 3")
        user_input = 1
        try:
            user_input = int(input())
        except ValueError:
            print("Not a valid value.")
            continue
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
            print("Please Input the corresponding numbers only: 1, 2 or 3.")
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
                "\nInput the corresponding numbers only 0, 1, 2 or 3")
            user_input = int(input())
        except ValueError:
            print("Not a valid input. Input the corresponding numbers only: 0, 1, 2 or 3")
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
            print("Please input the corresponding numbers only: 0, 1, 2 or 3.")
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
        if credits < 5:
            print("The value of credits cannot be below 5.")
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
            dg.add_edge(source, destination)
        i = i + 1
    return dg

'''
Function: Generate_Layering
Description:    
    Generates the layering list to use in the sugiyama layout algorithm.
    Iterates through a topological sorting of the graph. Adds courses 
    offered in the same quarter to a layer until hitting the max_credits.
    after a class is added to a layer, it is popped from the front of the
    list.
Parameters: 
    dg - the directed graph
    max_credits - the user-specified maximum amount of credits per quarter
    start_qtr - the starting quarter specified by the user
    topo_sort - a topological sorting of the graph
Returns: 
    layers - a list filled with layer numbers, the indices of this list
            correspond to the indices of the vertices of the graph
'''
def Generate_Layering(dg, max_credits, start_qtr, topo_sort):
    layers = []
    # Fill layer list with 0s
    for x in range(len(dg.vs)):
        layers.append(0)

    curr_cred = 0
    curr_quarter = start_qtr
    curr_layer = 1

    classes_in_quarter = []
    curr_year = 1

    print("Year: ", curr_year)

    while len(topo_sort) != 0:
        # iterate through topo_sort
        i = 0
        while curr_cred < max_credits and i < len(topo_sort):
            curr_class = dg.vs[topo_sort[i]]
            course_code = re.search("\d\d\d\d", curr_class["name"]).group()
            # because pre reqs are being removed when they are fulfilled, an
            # available class will have no pre reqs
            if curr_class["pre_reqs"] == "[]" \
                and re.search(str(curr_quarter), curr_class["quarters"]) \
                and int(course_code[0]) <= curr_year: # This condition makes it so that junior and senior courses are not assigned in the first year
                layers[topo_sort[i]] = curr_layer
                if curr_cred + int(dg.vs[topo_sort[i]]["credits"]) > max_credits:
                    break
                else:
                    curr_cred = curr_cred + int(dg.vs[topo_sort[i]]["credits"])
                    # Add the current class to the list of classes in this quarter
                    classes_in_quarter.append(curr_class)
                    topo_sort.pop(i)
            else:
                i = i + 1
        # For text representation of course sequence
        print("\tQuarter: ", curr_quarter)
        # Remove the names of the classes in the quarter from the
        # other classes prerequisite list
        for x in classes_in_quarter:
            # For text representation of course sequence
            print("\t\t", x["name"])
            Update_Prereq(x, dg)
        classes_in_quarter.clear()

        curr_layer = curr_layer + 1
        curr_cred = 0
        curr_quarter = Change_Quarter(curr_quarter)
        # Every 4 quarters, the year changes
        if curr_layer % 4 == 0:
            curr_year = curr_year + 1
            print("Year: ", curr_year)
    return layers

'''
Function: Change_Quarter
Description:    
    Helps the Generate Layout function by changing the quarter after
    the capacity of classes has been reached for a layer
Parameters: 
    current_quarter - the current value of the quarter:
        0 for summer, 1 for autumn, 2 for winter, 3 for spring
Returns: 
    the next value of quarter going in this pattern: 0->1->2->3->0->1->...
'''
def Change_Quarter(current_quarter):
    if current_quarter == 0:
        return current_quarter + 1
    if current_quarter == 1:
        return current_quarter + 1
    if current_quarter == 2:
        return current_quarter + 1
    if current_quarter == 3:
        return 0

'''
Function: Update_Prereq
Description:    
    Helps the Generate Layout Function by removing prereqs that have
    been added to a layer
Parameters: 
    class_removed - a vertex object representing the name of the class 
                    to remove
    dg - the directed graph
Returns: 
    nothing
'''
def Update_Prereq(class_removed, dg):
    for x in dg.vs:
        if re.search(class_removed["name"], x["pre_reqs"]) != None:
            # Remove comma and whitespace
            x["pre_reqs"] = re.sub(", ", "", x["pre_reqs"])
            # Remove class
            x["pre_reqs"] = re.sub(class_removed["name"], "", x["pre_reqs"])
            

def main():
    # Select file (major1.txt or major2.txt)
    filename = get_file_name()

    # Validate Input
    if Validate_Input(filename) != False:
        print("File Format is Valid!")
    else:
        print("File Format is Not Valid!")

    # Get the maximum credits
    max_credits = Get_Max_Credits()

    # Ask User for starting quarter
    starting = get_starting_qtr()

    # Build Graph in Memory
    dg = Generate_Graph(filename)

    # Generate the layer list used in the sugiyama layout
    list_of_layers = Generate_Layering(dg, max_credits, starting, dg.topological_sorting())

    # Output visual representation of course sequence

    layout = dg.layout_sugiyama(layers=list_of_layers, vgap=200)
    layout.rotate(-90, 0, 1)
    igraph.plot(dg, layout=layout, margin=(60, 60, 60, 80),
                bbox=(3000, 2000), vertex_label=dg.vs["name"],
                vertex_label_size=20, vertex_shape="rectangle",
                vertex_size= 50, vertex_label_dist=2) 


if __name__ == "__main__":
    main()
