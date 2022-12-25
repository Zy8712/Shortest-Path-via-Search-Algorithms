import sys # importing this allows us to take in command line arguments
from queue import Queue, PriorityQueue # import priority queue (allowed as stated in course Discord)

###################################
# Course: EECS3401
# Assessment: Project 1
# Student Name: Bryan Li
# Student ID: 216426744
# Professor: Archit Garg
# Due Date: 10/31/2021 11:59pm
###################################

# DISCLAIMER: CERTAIN PARTS OF MY CODE MAY BE INCOMPLETE DUE TO HIGH WORKLOAD FROM OTHER COURSES #

# ******* IMPORTANT NOTES ******** #
# From Prof on course Discord #
# "bfs does not look at the edge cost, same with dfs, so by whatever way you reach the goal #
# through bfs or dfs implementation that will be the path, it need not be the least cost    #
# path, because bfs will find the least edges path and dfs expands the deepest node first,  # 
# so just display that path, no need to implement dijikstra's."                             #
# Submission is find_path.py zipped (having the name firstname_lastname_studentid_project1.zip) #

####################################################################################################
## VERTEX CLASS. Serves as our blueprint for a Vertex object.
####################################################################################################
class Vertex:
    
    # Vertex Class Constructor
    def __init__(self, vertex_new): # reserved function, initializes the state of the Vertex object
        self.id = vertex_new # object field, assign unique id to specific object
        self.adjacent = {} # stores all vertices & weights connected to this particular vertex object

    # Print function. When you try to print out a vertex, you print out the vertex and list of adjacent vertices.
    def __str__(self):
        return str(self.id) # string output

    # Mutator function. Connects an adjacent vertex to this vertex, while also saving the weight
    def add_adjacent_vertex(self, adjacent_vertex, weight):
        self.adjacent[adjacent_vertex] = weight # store weight of edge to adjacent vertex
    
     # Accessor function get_id. Returns a string value which is the name of the vertex.
    def get_id(self):
        return self.id # access object field and return it

    # Accessor function get_weight. Returns a string value which is the weight of the edge.
    def get_weight(self, adjacent_vertex):
        return self.adjacent[adjacent_vertex] # access and return the weight of the adjacent_vertex

    # Accessor function. Returns dictionary keys which can be used to access the vertex fields.
    def get_adjacent_vertices(self):
        return self.adjacent.keys()  # returns keys corresponding to adjacent vertexes
    
    # Accessor function. Returns an int value indicating the number of edges a vertex has.
    def get_adjacent_vertices_num(self):
        count_adj = 0 # initialize counter equal to zero
        for edge in self.get_adjacent_vertices(): # loop through all edges
            count_adj += 1  # increment counter
        return count_adj # return number of adjacent vertices/ connected edges



####################################################################################################
## GRAPH CLASS. Serves as our blueprint for a Graph object.
####################################################################################################
class Graph:
    
    # Graph Class Constructor
    def __init__(self): # reserved function, initializes the state of the Graph object
        self.vert_dict = {} # stores every vertex in the graph
        self.num_vertices = 0  # stores total number of vertices in the graph

    # Mutator function. Adds new vertexes to the Graph object.
    def add_vertex(self, add_vertex): # parameter add_vertex is vertex to be added
        self.num_vertices = self.num_vertices + 1 # increment counter for number of vertexes in graph
        new_vertex = Vertex(add_vertex) # create a new vertex object using string provided (the location/name of city)
        self.vert_dict[add_vertex] = new_vertex # 
        return new_vertex
    
    # Mutator function. Adds new edges to the Graph object
    def add_edge(self, first_vertex, second_vertex, weight):
        # Following statements adds edges going both ways between the two vertices
        self.vert_dict[first_vertex].add_adjacent_vertex(self.vert_dict[second_vertex], weight) # edge one way
        self.vert_dict[second_vertex].add_adjacent_vertex(self.vert_dict[first_vertex], weight) # edge other way

    # Accessor function. Takes in string name of city, returns string names of adjacent cities.
    def get_vertex(self, name):
        if name in self.vert_dict: # checks to see if vertex with corresponding name is on graph
            return self.vert_dict[name] # returns the vertex if found on graph
        return None

    # Accessor function. Returns the number of vertices on the graph.
    def get_vertices_num(self):
        return self.num_vertices # return vertice counter
    
    # Recursive Helper function. Recursively explores the graph starting from the poing of origin.
    # Returns either an empty list indicating that the destination vertex has been found or it
    # sends a list with all vertices of a part of the disconnected graph.
    def point_connectivity_helper(self, orig, dest, list_check):
        
        # base case
        if str(orig.get_id()) in list_check: # checks to see if the vertex is alrady checked
            return list_check # return the list
       
        # base case
        if str(orig.get_id()) == str(dest.get_id()): # checks to see if we've arrived at the goal
            list_check.clear() # remove all items from the list
            return list_check # return the list
        
        # recursive case
        for adj in orig.get_adjacent_vertices(): # for loop, recurses through adjacent vertices
            adjid = adj.get_id() # get the name/id of the adjacent vertex
            list_check.append(orig.get_id()) # add the vertex to the list
            # recursive call. sends adjacent vertex as the new main vertex being checked
            list_check = map_graph.point_connectivity_helper(map_graph.get_vertex(str(adjid)), dest, list_check) 
            if not list_check: # checks to see whether or not the list is empty
                break # exits the loop
        return list_check # returns the list

    # Checker function. Checks to see if the start and end vertices can ever traverse to one another.
    # Also implicitly gives us a clue as to whether or not the graph is a disconnected graph (which
    # we know it is due to the project instructions).
    def point_connectivity(self, orig, dest, list_check):
        list_check = map_graph.point_connectivity_helper(orig, dest, list_check) # calls recursive helper function
        if not list_check: # checks to see whether or no the list is empty
            return True # returns boolean value of true if list is empty
        return False # returns boolean value of false if list isn't empty
    
    # Printer/output function. Outputs the results from Uniform-Cost-Search.
    # Relies on ucs_algorithm for correct paths and correct optimal cost.
    def print_ucs(self, map_graph, orig, dest, explored, optimal_cost):
        oc_path = [] # declare list of optimal path
        test_path = [] # declare list used for testing/finding optimal path
        test_cost = 0 # test the cost of the path to find the least cost
        first_check = True # boolean used for testing
        #oc_path = explored[explored.index(orig):explored.index(dest)+1]
        #print("optimal")
        #print(optimal_cost)
        #for x in range(len(explored)):
            #print(explored[x])
        
        # for loop. cycles through the list containing all the successful routes
        for x in range(len(explored)):
            #print(explored[x].get_id())
            if explored[x] != dest: # if vertex is equal to destination
                if first_check == True: # check if boolean value is true, if last vertex was destination vertex
                    test_path.append(explored[x]) # add vertex to test list
                    # try exception in case vertexes are not connected
                    try:
                        test_cost += int(explored[x].get_weight(explored[x+1])) # add to cost accumulator
                    except Exception:
                        pass # move on, no error thrown
                else:  # if boolean value is false, last vertex was not a destination vertex
                    first_check = True # set boolean value to true 
                    # try exception in case vertexes are not connected
                    try:
                        test_cost += int(explored[x].get_weight(explored[x+1])) # add to cost accumulator
                    except Exception:
                        pass # move on, no error thrown
                    # try exception in case vertexes are not connected
                    try:
                        test_cost += int(explored[0].get_weight(explored[x])) # add to cost accumulator
                    except Exception:
                        # attempt backtracking
                        find = False # declare boolean variable
                        for y in range(len(explored)-1): # iterate through vertexes on path
                            vertex3 = map_graph.get_vertex(explored[x-y]) # get vertex
                            for adj in explored[x].get_adjacent_vertices(): # iterate through adjacent vertices
                                # check to see if adjacent vertex is the one we shoudl backtrack to
                                if vertex3.get_id() == adj.get_id() and explored.index(vertex3.get_id()) < explored.index(explored[x].get_id()):
                                    test_cost += int(explored[0].get_weight(vertex3)) # add to cost accumulator
                                    find = True # set boolean variable to true
                                    break # exit loop
                            if (find == True): # check if boolean variable is true
                                break # exit loop
                        
            if explored[x] == dest: # if current vertex is the destination vertex
                test_path.append(explored[x]) # add destination vertex to list for test path
                if test_cost == optimal_cost: # check if the cost for this path is equal to 
                    oc_path = test_path.copy() # set the optimal path list equal to the current path
                    test_path.clear() # remove all items from the list
                    break # exit loop
                elif len(oc_path) == 0: # check to see if this is the first path
                    oc_path = test_path.copy() # set current optimal path to current path
                    test_path.clear() # remove all items from the list
                    test_path.append(explored[0]) # add back point of origin to path list
                    test_cost = 0 # reset cost of path to zero
                    first_check = False # set boolean variable to false
                else:
                    test_path.clear() # remove all items from the list
                    test_path.append(explored[0]) # add back point of origin to path list
                    test_cost = 0 # reset cost of path to zero
                    first_check = False # set boolean variable to false
        
        print("distance: " +str(optimal_cost) +" mi\n") # output optimal cost/distance
        print("path:\n") # output labal for path
        
        for x in range(len(oc_path)-1): # for loop cycles through vertices of optimal path
            print(oc_path[x].get_id() +" to " +oc_path[x+1].get_id() +": " +oc_path[x].get_weight(oc_path[x+1]) +" mi\n") # output
        
        print("====================================\n") # output
        return None # return nothing

    # Search Algorithm function. Performs a Uniform-Cost-Search on the graph to find a path.
    def ucs_algorithm(self, map_graph, orig, dest):
        
        ucs_frontier = PriorityQueue() # priority queue acts as frontier for search algorithm
        frontier_checklist = [] # extra list that holds the same vertices as frontier. used for checking if a vertex is on the frontier
        ucs_frontier.put((0, orig)) # add point of origin to frontier
        frontier_checklist.append(orig) # add point of origin to frontier list
        ucs_explored = [] # declare list to hold vertices already visited
        optimal_cost = sys.maxsize # declare variable for optimal cost and set to maximum possible value
        ucs_path = [] # declare list to hold multiple paths to point of destination
        ucs_path.append(orig) # add point of origin to this path list
    
        while True: # loops indefnitely, or at least until a break statement is reached
            if ucs_frontier.empty(): # if the frontier is empty
                break # exit loop
            
            # remove vertex from the frontier
            (ucs_weight, current_vertex) = ucs_frontier.get() # get weight and leading vertex from frontier
            
            if current_vertex != dest: # check if the current vertex is not the destination vertex
                ucs_explored.append(current_vertex) # add the current vertex to the list of explored vertices
                frontier_checklist.remove(current_vertex) # remove the vertex from the frontier list
            
            if current_vertex == dest: # check to see if current vertex is the destination vertex
                if optimal_cost > ucs_weight: # if the optimal cost is more than the weight of the current path
                    optimal_cost = ucs_weight # set new optimal cost/weight for a path on the graph
                else:
                    continue # skip this iteration
            
            # if the weight of the current path is more than a previously determined optimal, the path is abandoned
            if ucs_weight > optimal_cost: 
                continue # skip this iteration
            
            # for loop. iterate through all vertices adjacent this current vertex
            for key in current_vertex.get_adjacent_vertices():
                vertex = map_graph.get_vertex(key.get_id()) # set vertex equal to one of the adjacent vertices
                # check to see if vertex has been visted before or is currently on the frontier
                if vertex not in ucs_explored and vertex not in frontier_checklist: 
                    ucs_frontier.put((ucs_weight + int(current_vertex.get_weight(vertex)), vertex)) # add adjacent vertex to frontier
                    ucs_path.insert(ucs_path.index(current_vertex)+1, vertex) # add vertex to path list
                    if vertex != dest: # if vertex is not the destination vertex
                        frontier_checklist.append(vertex) # add vetex to frontier list

        map_graph.print_ucs(map_graph, orig, dest, ucs_path, optimal_cost) # call printer helper function
        return None # returns nothing
        
    # Printer/output function. Outputs the results from Breadth-First-Search.
    # Relies on bfs_algorithm for correct paths and correct cost.
    def print_bfs(self, map_graph, orig, dest, path):
        cost = 0 # declare accumulator variable
        path = path[path.index(orig):path.index(dest)+1] # cut out the path
        lows_dest_adj = path[-2]  # get second to last vertex in the path list
        
        # in case two paths reach at the same time
        for key in dest.get_adjacent_vertices(): # for loop. iterates through adjacent vertices of destination vertex
            if map_graph.get_vertex(key.get_id()) in path: #check to see if adjacent vertices of destination vertex are on path
                if dest.get_weight(key) < dest.get_weight(lows_dest_adj): # check to see which vertex on path & connected to destination is cheaper
                    path.remove(lows_dest_adj) # removes one vertex from the path, disconneecting it
                 
        for x in range(len(path)-1): # for loop. cycles through edges on path
            cost += int(path[x].get_weight(path[x+1])) # accumutes/calculates cost
        
        print("distance: " +str(cost) +" mi\n") # output distance/cost 
        print("path:\n") # output path label
        
        for x in range(len(path)-1): # for loop, iterates through edges of path
            print(path[x].get_id() +" to " +path[x+1].get_id() +": " +path[x].get_weight(path[x+1]) +" mi\n") # output path
        
        print("====================================\n") # output
        
        return None # return nothing
    
    # implemented by refering to AIMA3e from Breadth-First-Search.md in link...
    # ...provided on Project instructions
    # Search Algorithm function. Performs a Breadth-First-Search on the graph to find a path.
    def bfs_algorithm(self, map_graph, orig, dest): 
        
        bfs_frontier = [] # declare list, use as frontier
        bfs_frontier.append(orig) # add point of origin to frontier
        bfs_explored = [] # declare list to be used to store explored vertices
        bfs_path = [] # declare list to hold vertices on path to destination vertex
        bfs_path.append(orig) # add point of origin to path
        
        while True: # loops indifintely, or at least until a break statement is reached
            if not bfs_frontier: # checks to see if frontier is empty
                break # exits loop
            
            current_vertex = bfs_frontier[0] # set current vertex equal to 
            bfs_frontier.pop(0) # remove vertex from frontier
            bfs_explored.append(current_vertex) # add vertex to list of explored vertices
            
            if current_vertex == dest: # check to see if current vertex is destination vertex
                map_graph.print_bfs(map_graph, orig, dest, bfs_path) # call print helper function
                return # return nothing

            for key in current_vertex.get_adjacent_vertices(): # for loop, iterates through adjacent vertices
                vertex = map_graph.get_vertex(key.get_id()) # get adjacent vertex
                # check if adjacent vertex has been visited yet or is in currently on the frontier
                if vertex not in bfs_explored and vertex not in bfs_frontier:
                    bfs_frontier.append(vertex) # add adjacent vertex to frontier
                    bfs_path.insert(bfs_path.index(current_vertex)+1, vertex) # add adjacent vertex to path list
        return None # return nothing
    
    # Printer/output function. Outputs the results from Depth-First-Search.
    # Relies on dfs_algorithm for correct paths and correct cost.
    def print_dfs(self, map_graph, dfs_dest_found):
        cost = 0 # declare cost accumulator
        
        for x in range(len(dfs_dest_found)-1): # interate through successful path
            vertex = map_graph.get_vertex(dfs_dest_found[x]) # set vertex equal to a vertex on the path
            vertex2 = map_graph.get_vertex(dfs_dest_found[x+1]) # set vertex2 equal to a vertex on the path

            #for y in range(len(dfs_dest_found)-1):
             #  vertex2 = map_graph.get_vertex(dfs_dest_found[x+1-y])
            try:
                cost += int(vertex2.get_weight(vertex2)) # accumulate cost
            except Exception:
                # BACKTRACKING. In cases where we hit a dead end and need to go back.
                find = False # set boolean value equal to false
                for y in range(len(dfs_dest_found)-1): # interate through vertices on path
                    vertex3 = map_graph.get_vertex(dfs_dest_found[x-y]) # set vertex3 equal to a vertex on the path
                    for adj in vertex2.get_adjacent_vertices(): # iterate through all adjacent vertices of vertex2
                        # if statement check to see if vertex3 is an adjacent vertex to vertex, and whether it is the one it backtracks to
                        if vertex3.get_id() == adj.get_id() and dfs_dest_found.index(vertex3.get_id()) < dfs_dest_found.index(vertex2.get_id()):
                            cost += int(vertex2.get_weight(vertex3)) # cost accumualator
                            find = True # set boolean variable to true
                            break # exit loop
                    if (find == True):
                        break # exit loop
                    
        print("distance: " +str(cost) +" mi\n")
        print("path:\n") # output path label
        
        for x in range(len(dfs_dest_found)-1): # iterate through edges
            vertex = map_graph.get_vertex(dfs_dest_found[x]) # set vertex equal to vertex on the path
            vertex2 = map_graph.get_vertex(dfs_dest_found[x+1]) # set vertex equal to vertex on the path
            try:
                print(vertex.get_id() +" to " +vertex2.get_id() +": " +vertex.get_weight(vertex2) +" mi\n") # output path
            except Exception:
                # BACKTRACKING. Again, but this time for printing out the appropriate path details
                find = False # set boolean variable equal to false
                for y in range(len(dfs_dest_found)-1):
                    vertex3 = map_graph.get_vertex(dfs_dest_found[x-y]) # set vertex3 equal to a vertex on the path
                    for adj in vertex2.get_adjacent_vertices(): # iterate through adjacent vertices of vertex2
                        # if statement check to see if vertex3 is an adjacent vertex to vertex, and whether it is the one it backtracks to
                        if vertex3.get_id() == adj.get_id() and dfs_dest_found.index(vertex3.get_id()) < dfs_dest_found.index(vertex2.get_id()):
                            print(vertex3.get_id() +" to " +vertex2.get_id() +": " +vertex3.get_weight(vertex2) +" mi\n") # output path
                            find = True # set boolean variable equal to true
                            break # exit loop
                    if (find == True):
                        break # exit loop
        print("====================================\n") # output
        return None # return nothing
    
    # Recursive Helper Method. Helps Depth-First-Search the graph for dfs_algorithm.
    def dfs_algorithm_helper(self, map_graph, orig, dest, dfs_visited, dfs_dest_found):
        
        dfs_visited.append(orig) # add point orig to visited list
        dfs_dest_found.append(orig.get_id()) # add vertex to path 
        
        # base case
        if orig.get_id() == dest.get_id(): # checks to see if current vertex is the destination vertex
            map_graph.print_dfs(map_graph, dfs_dest_found) # call the printer helper method to output
            return dfs_dest_found # reuturn the list containing the path
        
        # recursive case
        for key in orig.get_adjacent_vertices(): # iterates through adjacent vertices
            vertex = map_graph.get_vertex(key.get_id()) # gets adjacent vertex
            if vertex not in dfs_visited: # check to see if adjacent vertex has already been visited
                dfs_dest_found = map_graph.dfs_algorithm_helper(map_graph, vertex, dest, dfs_visited, dfs_dest_found) #recursive call
        return dfs_dest_found # return the list containing the path
    
    # Search Algorithm function. Performs a Depth-First-Search on the graph to find a path.
    def dfs_algorithm(self, map_graph, orig, dest):
        
        dfs_visited = [] # declare list for visited vertices
        dfs_dest_found = [] # declare list for path
        
        map_graph.dfs_algorithm_helper(map_graph, orig, dest, dfs_visited, dfs_dest_found) # call recursive helper function
        
        return None # returns nothing 
    
    # Printer/output method. Outputs the path and cost from astar_algorithm.
    def print_astar(self):
        
        print("distance: mi\n") # output
        print("path:\n") # output path label
        
        print("====================================\n") # output
        
        # DID NOT COMPLETE DUE TO WORKLOAD

        return None # return nothing
    
    # Search Algorithm. Performs A* Search.
    def astar_algorithm(self, map_graph, orig, dest):
        
        open_list = []
        closed_list = []
        
        open_list.append(orig)
        
        # DID NOT COMPLETE DUE TO WORKLOAD
        
        map_graph.print_astar() # call printer function
        
        return None # return nothing



####################################################################################################
## PROGRAM BEGINS RUNNING HERE. MAIN METHOD/FUNCTION.
####################################################################################################
if __name__ == "__main__":

###############################################
# Take in command line arguments.
    search_algo = sys.argv[1]   # take in name of search algorithm to be used
    map_file = sys.argv[2]  # take in name of txt file for which map data is taken
    point_of_origin = sys.argv[3]   # take in point of origin
    point_of_destination = sys.argv[4]  # take in point of destination
    heuristics = "" # declare variable for name of heuristic file
    # certain command line entries may or may not have a file name entered for heuristics
    # we catch the exception in the event that no heuristic file name is entered
    # having no entry would normally results in a traceback
    try:
        heuristics = sys.argv[5]    # take in name of txt file for possible heuristic
    except Exception:
        pass
    
    # used to test values stored, values taken from command line (commented out when done)
    print(search_algo +" " +map_file +" " +point_of_origin +" " +point_of_destination +"" +heuristics +"\n")
    
    # Check condition. If point of origin and destination are the same.
    # (distance = zero and path = none in case of origin == destination)
    if point_of_origin == point_of_destination: # in the event that the start and goal vertices are the same
        print("\n======== " +search_algo +" ========\n") # output
        print("distance: zero\n") # output distance of zero since you are already there
        print("path:\nnone\n") # no need to traverse, hence no path
        print("====================") # output
        sys.exit() # stops execution of python program
    
    ## Example ##
    # python find_path.py ucs input_file1.txt Columbia WashingtonDC
    ################# sysargv[1] sysargv[2] sysargv[3] sysargv[4]
    
    
###############################################
# Some variable declarations/file opening.
    copy_map_info = [] # declare empty list used for copying values from lines of the file
    map_graph = Graph() # declare a new graph object which'll be used to map the data in the txt file
    counter = 0 # declare a counter, used to count the number of lines in the txt file
    added_vertexes = [] # declare empty list used for storing the strings of vertexes already added
    
    # open the file specified in the command lines, this contains the data to build the graph/map
    mapInfo = open(map_file, "r")   # data in this file is for paths between cities 
    
###############################################
# Find file size (number of lines in text file)
    file_content = mapInfo.read()   # take in all lines of data from txt file
    file_lines_list = file_content.split("\n") # split lines of data into separate indexes to be stored in list
    
    # for loop, loops through to every line in the txt file
    for i in file_lines_list: # loops from i = 0, up to the length of the file
        if i:   # used to ensure that there is content in the text file (0 if empty)
            counter += 1    # increment counter, used to count number of lines in txt file

###############################################
# Begin building graph/map using data from text file.
    mapInfo.seek(0) # reset back to the top of the text file
    origin_pointer = Vertex("") # create a pointer to point at the Vertex object which is our origin
    destination_pointer = Vertex("") # create a point to point at the Vertex object which is our destination
    temp = Vertex("") # create a temporary pointer
    pointer_list = [] # create a list of pointers to all vertices on graph for easy access
    
    j = 1 # declare a counter used for a loop
    while j < counter: # loop
        # splits the line it into parts, storing it into a list
        copy_map_info = mapInfo.readline().split() # two locations and weight now in list
        
        # check to see if first location is already added onto the graph
        if copy_map_info[0] not in added_vertexes: # if not added yet, then execute the code
            if copy_map_info[0] == point_of_origin: # checks strings to see if it is point of origin
                origin_pointer = map_graph.add_vertex(copy_map_info[0]) # add the location as a vertex on the graph
                added_vertexes.append(copy_map_info[0]) # add to list which keeps track of added locations
                pointer_list.append(origin_pointer) # add to list of pointers
            elif copy_map_info[0] == point_of_destination: # check strings to see if it is point of destination
                destination_pointer = map_graph.add_vertex(copy_map_info[0]) # add the location as a vertex on the graph
                added_vertexes.append(copy_map_info[0]) # add to list which keeps track of added locations
                pointer_list.append(destination_pointer) # add to list of pointers
            else:
                temp = map_graph.add_vertex(copy_map_info[0]) # add the location as a vertex on the graph
                added_vertexes.append(copy_map_info[0]) # add to list which keeps track of added locations
                pointer_list.append(temp) # add to list of pointers
        
        # check to see if second location is already added onto the graph    
        if copy_map_info[1] not in added_vertexes: # if not added yet, the execute the code
            if copy_map_info[1] == point_of_origin: # checks strings to see if it is point of origin
                origin_pointer = map_graph.add_vertex(copy_map_info[1]) # add the location as a vertex on the graph
                added_vertexes.append(copy_map_info[1]) # add to list which keeps track of added locations
                pointer_list.append(origin_pointer)
            elif copy_map_info[1] == point_of_destination: # check strings to see if it is point of destination
                destination_pointer = map_graph.add_vertex(copy_map_info[1]) # add the location as a vertex on the graph
                added_vertexes.append(copy_map_info[1]) # add to list which keeps track of added locations
                pointer_list.append(destination_pointer)
            else:
                temp = map_graph.add_vertex(copy_map_info[1]) # add the location as a vertex on the graph
                added_vertexes.append(copy_map_info[1]) # add to list which keeps track of added locations
                pointer_list.append(temp)
            
        # adds edge to graph, sends the two locations and the weight of their path as parameters
        map_graph.add_edge(copy_map_info[0], copy_map_info[1], copy_map_info[2])
        
        copy_map_info.clear() # reset list to empty
        j += 1 # increment counter by 1
    
    mapInfo.close() # close the file associated with mapInfo (which is the text file)


###############################################
# Check for valid origin and destination points.
    if point_of_origin not in added_vertexes and point_of_destination not in added_vertexes:
        print("Invalid point of origin and point of destination.") # output error message
        print("Both points entered are not on the map/graph of " +map_file) # output error message
        sys.exit() # stops execution of python program

    elif point_of_origin not in added_vertexes:
        print("Invalid point of origin.") # output error message
        print("Origin point entered are not on the map/graph of " +map_file) # output error message
        sys.exit() # stops execution of python program
    
    elif point_of_destination not in added_vertexes:
        print("Invalid point of destination.") # output error message
        print("Destination point entered are not on the map/graph of " +map_file) # output error message
        sys.exit() # stops execution of python program

###############################################
# Check for Graph connectivity.
    connect = True # declare boolean variable used for checking if graph is connected (for the two points)
    list_check = [] # declare list used to store vertices visited to see if graph is connected (for the two points)
    connect = map_graph.point_connectivity(origin_pointer, destination_pointer, list_check) # call function

###############################################
# Begin searching using search algorithm requested#
    if connect == True: # if graph is disconnected, but origin and destination can still reach each other
        if search_algo == "ucs": # if the algorithm requested in the command line is ucs
            #print(str(origin_pointer.get_id()), str(destination_pointer.get_id()))
            print("\n================ " +search_algo +" ================\n") # output 
            map_graph.ucs_algorithm(map_graph, origin_pointer, destination_pointer) # invoke the search algorithm
            #print("ucs algorithm selected") # test selection
    
        elif search_algo == "bfs": # if the algorithm requested in the command line is bfs
            print("\n================ " +search_algo +" ================\n") #output
            map_graph.bfs_algorithm(map_graph, origin_pointer, destination_pointer) # invoke the search algorithm
            #print("bfs algorithm selected") # test selection
    
        elif search_algo == "dfs": # if the algorithm requested in the command line is dfs
            print("\n================ " +search_algo +" ================\n") #output
            map_graph.dfs_algorithm(map_graph, origin_pointer, destination_pointer) # invoke the search algorithm
            #print("dfs algorithm selected") # test selection
    
        elif search_algo == "astar": # if the algorithm requested in the command line is astar
            if heuristics == "": # user tries to use astar but didn't include heuristic file
                print("Heuristics source file missing from command line input.") # output error message
            else: # heuristic file included by user in command line
                heuristicInfo = open(heuristics, "r") # open heuristic file
                file_content2 = heuristicInfo.read()   # take in all lines of data from txt file
                file_lines_list2 = file_content2.split("\n") # split lines of data into separate indexes to be stored in list
                counter2 = 0 # declare a counter
                # for loop, loops through to every line in the txt file
                for z in file_lines_list: # loops from z = 0, up to the length of the file
                    if z:   # used to ensure that there is content in the text file (0 if empty)
                        counter2 += 1    # increment counter, used to count number of lines in txt file
                
                heuristicInfo.seek(0) # reset back to the top of the text file
                copy_heuristic_info = [] # declare copy list
                heuristicLocation = [] # declare list for heuristic locations
                heuristicLocationWeight = [] # declare list for corresponding weights to those locations
                
                while y < counter2: # loop
                    # splits the line it into parts, storing it into a list
                    copy_heuristic_info = heuristicInfo.readline().split() # two locations and weight now in list
                    heuristicLocation.append(copy_heuristic_info_info[0]) # add location data to list
                    heuristicLocationWeight(copy_heuristic_info_info[1]) # add weight data to list
                    copy_heuristic_info.clear() # reset list to empty
                    y += 1 # increment counter by 1
                
                heuristicInfo.close() # close heuristic text file
                
                print("\n================ " +search_algo +" ================\n")
                map_graph.astar_algorithm(origin_pointer, destination_pointer) # invoke the search algorithm
                #print("astar algorithm selected") # test selection

        else:   # if the algorithm entered is not one of the four valid options
            print("Search algorithm entered in command line is not a valid option.") # error message
            print("The four accepted search algorithms are:") # inform user
            print("ucs (Uniform-Cost Search)") # inform user
            print("bfs (Breadth-First Search)") # inform user
            print("dfs (Depth-First Search)") # inform user
            print("astar (A-Star Search)") # inform user
            sys.exit() # stops execution of python program
    else: # in cases where: graph is disconected, origin and destination have no path between them
        print("\n======== " +search_algo +" ========\n") # output
        print("distance: infinity\n") # output an infinite amount of distance between the two
        print("path:\nnone\n") # output no path message
        print("====================") # output






