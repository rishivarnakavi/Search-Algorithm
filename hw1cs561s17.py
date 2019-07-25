import sys
import re
import collections
from collections import deque
import Queue as q

def main():
    file1 = open("input5.txt", "r")
    file2 = open("output.txt", "w")
    num_lines = sum(1 for line in open("input5.txt"))
    Algo = file1.readline().rstrip()
    Fuel = file1.readline().rstrip()
    Start_State = file1.readline().rstrip()
    Goal_State = file1.readline().rstrip()
    Node_List = {}
    Node_List_temp = {}
    for i in range(3, num_lines - 1):
        temparray = file1.readline().rstrip()
        temparray2 = re.findall(r"[\w']+", temparray)
        if temparray2[0] not in Node_List_temp.keys():
            Node_List_temp[temparray2[0]] = {}
            for j in range(1, len(temparray2) - 1):
                if j%2 == 0:
                    continue
                else:
                    Node_List_temp[temparray2[0]][temparray2[j]] = temparray2[j + 1]

    val = {}
    if (Algo == 'BFS'):
        for key in Node_List_temp.keys():
            val = collections.OrderedDict(sorted(Node_List_temp[key].items()))
            Node_List[key] = val
        (p, f) = implementBFSAlgo(Node_List, Start_State, Goal_State, Fuel)
        if len(p) == 0:
            file2.write("No Path")
        else:
            for i in range(len(p)):
                file2.write(p[i])
                if i != len(p)-1:
                    file2.write('-')
                else:
                    file2.write(' ')
            file2.write(str(f))
    elif (Algo == 'DFS'):
        for key in Node_List_temp.keys():
            val = collections.OrderedDict(reversed(sorted(Node_List_temp[key].items())))
            Node_List[key] = val
        (p,f) = implementDFSAlgo(Node_List, Start_State, Goal_State, Fuel)
        if len(p) == 0:
            file2.write("No Path")
        else:
            for i in range(len(p)):
                file2.write(p[i])
                if i != len(p)-1:
                    file2.write('-')
                else:
                    file2.write(' ')
            file2.write(str(f))
    else:
        for key in Node_List_temp.keys():
            val = collections.OrderedDict(sorted(Node_List_temp[key].items()))
            Node_List[key] = val
        (p, f) = implementUCSAlgo(Node_List, Start_State, Goal_State, Fuel)
        if len(p) == 0:
            file2.write("No Path")
        else:
            for i in range(len(p)):
                file2.write(p[i])
                if i != len(p)-1:
                    file2.write('-')
                else:
                    file2.write(' ')
            file2.write(str(f))


def implementBFSAlgo(Node_List, Start_State, Goal_State, Fuel):
    queue = []
    visited = []
    explored = []
    path =[]
    queue.append(Start_State)
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node not in explored:
            explored.append(node)
        if node != Goal_State:
            for i in Node_List[node].keys():
                node1 = i
                if node1 not in visited:
                    visited.append(node1)
                    if node1 not in explored:
                        path1 = list(path)
                        path1.append(node1)
                        queue.append(path1)
                if node1 == Goal_State:
                    if node1 not in explored:
                        path1 = list(path)
                        path1.append(node1)
                        queue.append(path1)
        else:
            fuel_remaining = Fuel
            for j in range(len(path) - 1):
                if fuel_remaining != 0:
                    val1 = path[j]
                    val2 = path[j + 1]
                    path_fuel = Node_List[val1][val2]
                    fuel_remaining = int(fuel_remaining) - int(path_fuel)
            if fuel_remaining < 0:
                continue
            else:
                return (path, fuel_remaining)
    return (queue, fuel_remaining)



def implementDFSAlgo(Node_List, Start_State, Goal_State, Fuel):
    queue = []
    visited = []
    path = []
    queue.append(Start_State)
    while queue:
        path = queue.pop()
        node = path[-1]
        if node not in visited:
            visited.append(node)
        if node != Goal_State:
            for i in Node_List[node].keys():
                node1 = i
                if node1 not in visited:
                    path1 = list(path)
                    path1.append(node1)
                    queue.append(path1)
        else:
            fuel_remaining = Fuel
            for j in range(len(path) - 1):
                if fuel_remaining != 0:
                    val1 = path[j]
                    val2 = path[j + 1]
                    path_fuel = Node_List[val1][val2]
                    fuel_remaining = int(fuel_remaining) - int(path_fuel)
            if fuel_remaining < 0:
                continue
            else:
                return (path, fuel_remaining)
    return (queue, fuel_remaining)

def implementUCSAlgo(Node_List, Start_State, Goal_State, Fuel):
    queue = q.PriorityQueue()
    visited = []
    explored = []
    path = []
    rates = {}
    queue.put((0,[Start_State]))
    while queue:
        cumulative_cost, path = queue.get()
        node = path[-1]
        if node not in explored:
            explored.append(node)
        if node != Goal_State:
            for i in Node_List[node].keys():
                node1 = i
                if node1 not in explored:
                    if node1 not in visited:
                        visited.append(node1)
                        path1 = list(path)
                        path1.append(node1)
                        edge_cost = Node_List[node][node1]
                        total_cost = int(cumulative_cost) + int(edge_cost)
                        rates[node1] = total_cost
                        queue.put((total_cost,path1))
                    else:
                        path1 = list(path)
                        path1.append(node1)
                        edge_cost = Node_List[node][node1]
                        total_cost = int(cumulative_cost) + int(edge_cost)
                        if total_cost < rates[node1]:
                            rates[node1] = total_cost
                            queue.put((total_cost, path1))
        else:
            fuel_remaining = Fuel
            for j in range(len(path) - 1):
                if fuel_remaining != 0:
                    val1 = path[j]
                    val2 = path[j + 1]
                    path_fuel = Node_List[val1][val2]
                    fuel_remaining = int(fuel_remaining) - int(path_fuel)
            if fuel_remaining < 0:
                continue
            else:
                return (path, fuel_remaining)
    return (queue, fuel_remaining)

main()