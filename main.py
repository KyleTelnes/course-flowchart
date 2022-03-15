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
        x = re.search("^[A-Z][A-Z][A-Z]?\s\d\d\d\d,(\s\w+)*,\s\d,\s\[([A-Z][A-Z][A-Z]?\s\d\d\d\d)?(,\s([A-Z][A-Z][A-Z]?\s\d\d\d\d))*\],\s\[(\d)?(,\d)*\]$", line)
        if x == None or x.start() != 0:
            return False
    return True

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
    dg = igraph.Graph(directed= True)

    f = open(filename, "r")

    # add all vertices
    i = 0
    for line in f:
        # re is used to get the attributes of the course
        course_code = re.search("^[A-Z][A-Z][A-Z]?\s\d\d\d\d", line).group()
        course_name = re.search(",(\s\w+)*", line).group()[2:] # [2:] slices off the comma and the space
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
            source = dg.vs.find(name= y)
            destination = dg.vs[i]
            dg.add_edge(source, destination)
        i = i + 1
    return dg

def main():
    # Step 1: Select file (major1.txt or major2.txt)
    default_major = "major1.txt"
    selected_major = default_major
    starting_qtr = 1
    print("Please select your major: \n 1 -> BA - Computer Science. \n 1 -> BS - Computer Science. \n 3 -> BS - Electrical Engineer. \n Input the corsponding numbers only 1,2 or 3")
    user_input = input()
    if user_input == "1":
        print("\nSelected major = BA - Computer Science.\n")
        selected_major = default_major
    elif user_input == "2":
        print("\nSelected major = BS - Computer Science.\n")
        selected_major = "major2.txt"
    elif user_input == "3":
        print("\nSelected major = BS - Electrical Engineer.\n")
        selected_major = "major3.txt"
    else:
        print("The major you selected doesn't match the options. Please try again.")
        exit()




    # Step 2: Validate Input
    if Validate_Input(selected_major) != False:
        print("File Format is Valid!")
    else:
        print("File Format is Not Valid!")

    # Step 3: Build Graph in Memory

    dg = Generate_Graph(selected_major)
        
    igraph.summary(dg)
    # Step 4: Ask User for Maximum Credits
    max_credits = Get_Max_Credits()

    # Step 5: Ask User for starting quarter
    print("Which quarter will you be starting this major? \n 0 -> Summer \n 1 -> Fall or Autumn \n 2 -> Winter \n 3 -> Spring. \n Input the corsponding numbers only 0, 1,2 or 3")
    user_input = input()

    if user_input == "0":
        starting_qtr = 0
        print("Starting in Summer")
    elif user_input == "1":
        starting_qtr = 1
        print("Starting in Fall/Autumn")
    elif user_input == "2":
        starting_qtr = 2
        print("Starting in Winter")
    elif user_input == "3":
        starting_qtr = 3
        print("Starting in Spring")
    else:
        print("Please select from the available options.")
        exit()
    # Step 6: Output text representation of course sequence
    
    layout = dg.layout_reingold_tilford(root=[1,3])
    layout.rotate(-90, 0, 1)
    igraph.plot(dg, layout=layout, vertex_label=dg.vs["name"])



if __name__ == "__main__":
    main()
    print("Name = ", __name__)


# with open(selected_major, "r") as file:
#     print(file.read())
#
# print(selected_major)

