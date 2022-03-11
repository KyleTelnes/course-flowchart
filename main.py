import igraph

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
    main()