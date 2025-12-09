#https://adventofcode.com/2025/day/8
INPUT_FILENAME = "inputs/inputs_08.txt"

import math

class DisjointSets: #union find datastructure

    def __init__(self, n : int):
        self.parent = [i for i in range(n)]

    def find(self, i: int) -> int:
        if self.parent[i] == i:
            return i
        else:
            return self.find(self.parent[i])

    def union(self, i: int, j: int) -> None:
        i_head = self.find(i)
        j_head = self.find(j)
        self.parent[i_head] = j_head

    def get_sets(self) -> list[set]:
        sets = [set() for _ in range(len(self.parent))]
        for i in range(len(self.parent)):
            i_head = self.find(i)
            sets[i_head].add(i)

        sets = list(filter(lambda x: x, sets))
        sets = sorted(sets, key=lambda x: len(x))

        return sets





def get_cycle_counts(data):
    CONNECTIONS_MADE = 1000

    #construct list of connections of the form (distance, idx of 1st box, idx of 2nd box)
    connection_distances = []
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            a_0, a_1, a_2 = data[i]
            b_0, b_1, b_2 = data[j]
            dist = ((a_0-b_0)**2 + (a_1-b_1)**2 + (a_2-b_2)**2)**(1/2)
            connection_distances.append((dist, i, j))
    
    connection_distances.sort()
    chosen_connections = connection_distances[:CONNECTIONS_MADE]

    #form sets based on graph via connections. 
    dis_sets = DisjointSets(len(data))
    for connection in chosen_connections:
        dist, i, j = connection
        dis_sets.union(i, j)
    
    return [len(s) for s in dis_sets.get_sets()]




def get_prod_of_3_largest(cycle_counts):
    cycle_counts = sorted(cycle_counts, reverse=True)
    return math.prod(cycle_counts[:3])


def get_data():
    with open(INPUT_FILENAME) as f:
        lines = f.readlines()
        data = [tuple([int(a.strip()) for a in line.split(',')]) for line in lines]

    return data


def main():
    data = get_data()
    cycle_counts = get_cycle_counts(data)
    p1_sol = get_prod_of_3_largest(cycle_counts)

    print("product of 3 largest cycle counts: {}".format(p1_sol))

if __name__ == "__main__":
    main()