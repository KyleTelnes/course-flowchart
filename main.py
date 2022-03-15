import igraph
from igraph import *



def main():
    dg = igraph.Graph(directed=True)
    
    dg.add_vertices(5)
    dg.add_edge(1, 2)
    dg.add_edge(3, 1)
    dg.add_edge(4, 0)
    dg.add_edge(2, 0)
    dg.vs["name"] = ["CSC 3430", "CSC 2430", "CSC 2431", "CSC 1230", "MAT 2200"]

    layout = dg.layout("kk")
    igraph.plot(dg, layout=layout)
    print(dg.is_dag())

if __name__ == "__main__":
    # main()
    print("Name = ", __name__)

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
with open(selected_major, "r") as file:
    print(file.read())

print(selected_major)

