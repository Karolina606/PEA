# Python3 program to solve
# Traveling Salesman Problem using
# Branch and Bound.
import math
import os
import sys
import time
from configparser import ConfigParser

from wmi import WMI

import my_writer

maxsize = float('inf')
# Adjacency matrix for the given graph
adj = [[0, 10, 15, 20],
       [10, 0, 35, 25],
       [15, 35, 0, 30],
       [20, 25, 30, 0]]

N = 4

# final_path[] stores the final solution
# i.e. the // path of the salesman.
final_path = [None] * (N + 1)

# visited[] keeps track of the already
# visited nodes in a particular path
visited = [False] * N

# Stores the final minimum weight
# of shortest tour.
final_res = maxsize


# Function to copy temporary solution
# to the final solution
def copyToFinal(curr_path):
    final_path[:N + 1] = curr_path[:]
    final_path[N] = curr_path[0]


# Function to find the minimum edge cost
# having an end at the vertex i
def firstMin(adj, i):
    min = maxsize
    for k in range(N):
        if adj[i][k] < min and i != k:
            min = adj[i][k]

    return min


# function to find the second minimum edge
# cost having an end at the vertex i
def secondMin(adj, i):
    first, second = maxsize, maxsize
    for j in range(N):
        if i == j:
            continue
        if adj[i][j] <= first:
            second = first
            first = adj[i][j]

        elif (adj[i][j] <= second and
              adj[i][j] != first):
            second = adj[i][j]

    return second


# function that takes as arguments:
# curr_bound -> lower bound of the root node
# curr_weight-> stores the weight of the path so far
# level-> current level while moving
# in the search space tree
# curr_path[] -> where the solution is being stored
# which would later be copied to final_path[]
def TSPRec(adj, curr_bound, curr_weight,
           level, curr_path, visited):
    global final_res

    # base case is when we have reached level N
    # which means we have covered all the nodes once
    if level == N:

        # check if there is an edge from
        # last vertex in path back to the first vertex
        if adj[curr_path[level - 1]][curr_path[0]] != 0:

            # curr_res has the total weight
            # of the solution we got
            curr_res = curr_weight + adj[curr_path[level - 1]] \
                [curr_path[0]]
            if curr_res < final_res:
                copyToFinal(curr_path)
                final_res = curr_res
        return

    # for any other level iterate for all vertices
    # to build the search space tree recursively
    for i in range(N):

        # Consider next vertex if it is not same
        # (diagonal entry in adjacency matrix and
        # not visited already)
        if (adj[curr_path[level - 1]][i] != 0 and
                visited[i] == False):
            temp = curr_bound
            curr_weight += adj[curr_path[level - 1]][i]

            # different computation of curr_bound
            # for level 2 from the other levels
            if level == 1:
                curr_bound -= ((firstMin(adj, curr_path[level - 1]) +
                                firstMin(adj, i)) / 2)
            else:
                curr_bound -= ((secondMin(adj, curr_path[level - 1]) +
                                firstMin(adj, i)) / 2)

            # curr_bound + curr_weight is the actual lower bound
            # for the node that we have arrived on.
            # If current lower bound < final_res,
            # we need to explore the node further
            if curr_bound + curr_weight < final_res:
                curr_path[level] = i
                visited[i] = True

                # call TSPRec for the next level
                TSPRec(adj, curr_bound, curr_weight,
                       level + 1, curr_path, visited)

            # Else we have to prune the node by resetting
            # all changes to curr_weight and curr_bound
            curr_weight -= adj[curr_path[level - 1]][i]
            curr_bound = temp

            # Also reset the visited array
            visited = [False] * len(visited)
            for j in range(level):
                if curr_path[j] != -1:
                    visited[curr_path[j]] = True


# This function sets up final_path
def TSP(adj):
    global N
    global final_res
    global final_path
    global visited

    N = len(adj)
    # Calculate initial lower bound for the root node
    # using the formula 1/2 * (sum of first min +
    # second min) for all edges. Also initialize the
    # curr_path and visited array
    curr_bound = 0
    curr_path = [-1] * (N + 1)
    visited = [False] * N

    # Compute initial bound
    for i in range(N):
        curr_bound += (firstMin(adj, i) +
                       secondMin(adj, i))

    # Rounding off the lower bound to an integer
    curr_bound = math.ceil(curr_bound / 2)

    # We start at vertex 1 so the first vertex
    # in curr_path[] is 0
    visited[0] = True
    curr_path[0] = 0

    # Call to TSPRec for curr_weight
    # equal to 0 and level 1
    TSPRec(adj, curr_bound, 0, 1, curr_path, visited)


def best_search_init(matrix):
    global N
    global final_res
    global final_path
    global visited
    global adj
    adj = matrix
    N = len(adj)
    final_path = [None] * (N + 1)
    visited = [False] * N
    final_res = maxsize


def memory():
    w = WMI('.')
    result = w.query("SELECT WorkingSet FROM Win32_PerfRawData_PerfProc_Process WHERE IDProcess=%d" % os.getpid())
    return int(result[0].WorkingSet)


def work(name, matrix):
    global N
    global final_res
    global final_path
    global visited

    print("Liczę dla: " + name)

    start_time = time.time()
    best_search_init(matrix)
    TSP(matrix)
    end_time = time.time() - start_time

    tsp_result = [name, len(matrix), end_time, memory(), final_res, final_path]
    # tsp_result = [name, len(matrix), end_time, min(paths_costs), paths[low_cost_index]]
    return tsp_result


def from_txt_to_matrix(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        n = int(lines[0])

        matrix = []
        for each in lines[1:]:
            matrix.append(each.split())

        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j] = int(matrix[i][j])

    return matrix


def main():
    # tab = [(4, 0), (6, 1), (7, 2), (8, 3), (2, 4), (12, 5), (231, 6), (1, 7)]
    # mini, parent = min(tab)
    # print("min: " + str(mini))
    # print("parent: " + str(parent))

    try:
        # Otworzenie pliku .ini i wczytanie jego parametrów
        file = 'config.ini'
        config = ConfigParser()
        config.read(file)

        # Zczytanie parametrów
        result_out_file_bs = 'tsp_bs3.csv'
        data0 = config['data']['tsp_6_1']
        data1 = config['data']['tsp_6_2']
        data2 = config['data']['tsp_10']
        data3 = config['data']['tsp_12']
        data4 = config['data']['tsp_13']
        data5 = config['data']['tsp_14']
        data6 = config['data']['tsp_15']
        data7 = config['data']['tsp_17']
        data8 = config['data']['gr24']
        data9 = config['data']['bays29']
        # data10 = config['data']['att48']
        # data11 = config['data']['eil51']
        # data12 = config['data']['berlin52']
        data13 = config['data']['br17']
        data14 = config['data']['ftv33']
        data15 = config['data']['ftv35']
        data16 = config['data']['ftv38']
        data17 = config['data']['p43']
        data18 = config['data']['gr21']
        data19 = config['data']['ulysses22']
        data20 = config['data']['fri26']

        matrix6_1_opti = config['data']['tsp_6_1_opti']
        matrix6_2_opti = config['data']['tsp_6_2_opti']
        matrix10_opti = config['data']['tsp_10_opti']
        matrix12_opti = config['data']['tsp_12_opti']
        matrix13_opti = config['data']['tsp_13_opti']
        matrix14_opti = config['data']['tsp_14_opti']
        matrix15_opti = config['data']['tsp_15_opti']
        matrix17_opti = config['data']['tsp_17_opti']
        matrix_gr24_opti = config['data']['gr24_opti']
        matrix_bays29_opti = config['data']['bays29_opti']
        # matrix_att48_opti = config['data']['att48_opti']
        # matrix_eil51_opti = config['data']['eil51_opti']
        # matrix_berlin52_opti = config['data']['berlin52_opti']
        matrix_br17_opti = config['data']['br17_opti']
        matrix_ftv33_opti = config['data']['ftv33_opti']
        matrix_ftv35_opti = config['data']['ftv35_opti']
        matrix_ftv38_opti = config['data']['ftv38_opti']
        matrix_p43_opti = config['data']['p43_opti']
        matrix_gr21_opti = config['data']['gr21_opti']
        matrix_ulysses22_opti = config['data']['ulysses22_opti']
        matrix_fri26_opti = config['data']['fri26_opti']

        matrix6_1 = from_txt_to_matrix(data0)
        matrix6_2 = from_txt_to_matrix(data1)
        matrix10 = from_txt_to_matrix(data2)
        matrix12 = from_txt_to_matrix(data3)
        matrix13 = from_txt_to_matrix(data4)
        matrix14 = from_txt_to_matrix(data5)
        matrix15 = from_txt_to_matrix(data6)
        matrix17 = from_txt_to_matrix(data7)
        matrix_gr24 = from_txt_to_matrix(data8)
        matrix_bays29 = from_txt_to_matrix(data9)
        # matrix_att48 = from_txt_to_matrix(data10)
        # matrix_eil51 = from_txt_to_matrix(data11)
        # matrix_berlin52 = from_txt_to_matrix(data12)
        matrix_br17 = from_txt_to_matrix(data13)
        matrix_ftv33 = from_txt_to_matrix(data14)
        matrix_ftv35 = from_txt_to_matrix(data15)
        matrix_ftv38 = from_txt_to_matrix(data16)
        matrix_p43 = from_txt_to_matrix(data17)
        matrix_gr21 = from_txt_to_matrix(data18)
        matrix_ulysses22 = from_txt_to_matrix(data19)
        matrix_fri26 = from_txt_to_matrix(data20)

        # Make analysis
        result_out_file = result_out_file_bs
        # tsp_result = work("matrix_my_2", matrix_my_2)
        # my_writer.simple_write_to_csv(result_out_file, tsp_result)
        my_writer.simple_write_to_csv(result_out_file, ['', '', '', '', '', ''], '')

        tsp_result = work("matrix_my_4", matrix_my_4)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, tsp_my_4_opti)

        tsp_result = work("matrix_my_5", matrix_my_5)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, tsp_my_5_opti)

        tsp_result = work("matrix6_1", matrix6_1)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix6_1_opti)

        tsp_result = work("matrix6_2", matrix6_2)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix6_2_opti)

        tsp_result = work("matrix10", matrix10)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix10_opti)
        #
        # tsp_result = work("matrix_my_11", matrix_my_11)
        # my_writer.simple_write_to_csv(result_out_file, tsp_result, tsp_my_11_opti)

        tsp_result = work("matrix12", matrix12)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix12_opti)

        tsp_result = work("matrix13", matrix13)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix13_opti)

        tsp_result = work("matrix14", matrix14)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix14_opti)

        tsp_result = work("matrix15", matrix15)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix15_opti)

        # tsp_result = work("matrix17", matrix17)
        # my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix17_opti)

        # ==========================================================================
        tsp_result = work("gr21", matrix_gr21)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix_gr21_opti)

        tsp_result = work("ulysses22", matrix_ulysses22)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix_ulysses22_opti)

        tsp_result = work("gr24", matrix_gr24)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix_gr24_opti)

        tsp_result = work("fri26", matrix_fri26)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix_fri26_opti)

        tsp_result = work("bays29", matrix_bays29)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix_bays29_opti)

        # tsp_result = work("att48", matrix_att48)
        # my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix_att48_opti)
        #
        # tsp_result = work("eil51", matrix_eil51)
        # my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix_eil51_opti)
        #
        # tsp_result = work("berlin52", matrix_berlin52)
        # my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix_berlin52_opti)

        tsp_result = work("br17", matrix_br17)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix_br17_opti)

        tsp_result = work("ftv33", matrix_ftv33)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix_ftv33_opti)

        tsp_result = work("ftv35", matrix_ftv35)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix_ftv35_opti)

        tsp_result = work("ftv38", matrix_ftv38)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix_ftv38_opti)

        tsp_result = work("p43", matrix_p43)
        my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix_p43_opti)

        input('Skończyłem, wciśnij cokolwiek, aby mnie wyłączyć...')
        sys.exit(0)

    except OSError:
        print("Coś poszło nie tak, sprawdź czy plik inicjujący")



matrix_my_2 = [
    [0, 10],
    [10, 0]
]
tsp_my_2_opti = '20; [0, 1, 0]'

matrix_my_4 = [
    [0, 10, 12, 8],
    [10, 0, 15, 18],
    [12, 15, 0, 5],
    [8, 18, 5, 0]
]
tsp_my_4_opti = '38; [0, 1, 2, 3, 0]'

matrix_my_5 = [
    [0, 10, 12, 8, 9],
    [10, 0, 15, 18, 10],
    [12, 15, 0, 5, 11],
    [8, 18, 5, 0, 5],
    [9, 10, 11, 5, 0]
]
tsp_my_5_opti = '42; [0, 1, 4, 3, 2, 0]'

# matrix10 = [
#     [0, 10, 12, 8, 9, 31],
#     [10, 0, 15, 18, 10, 50],
#     [12, 15, 0, 5, 11, 4],
#     [8, 18, 5, 0, 5, 19],
#     [9, 10, 11, 5, 0, 21],
#     [31, 50, 4, 19, 21, 0]
# ]
#
# matrix11 = [
#     [0, 10, 12, 8, 9, 31, 2],
#     [10, 0, 15, 18, 10, 50, 4],
#     [12, 15, 0, 5, 11, 4, 8],
#     [8, 18, 5, 0, 5, 19, 16],
#     [9, 10, 11, 5, 0, 21, 20],
#     [31, 50, 4, 19, 21, 0, 30],
#     [2, 4, 8, 16, 20, 30, 0]
# ]
#
# matrix12 = [
#     [0, 20, 30, 31, 28, 40, 8, 21],
#     [20, 0, 10, 14, 20, 44, 9, 20],
#     [30, 10, 0, 10, 22, 50, 5, 31],
#     [31, 14, 10, 0, 14, 42, 3, 22],
#     [28, 20, 22, 14, 0, 28, 11, 20],
#     [40, 44, 50, 42, 28, 0, 14, 3],
#     [8, 9, 5, 3, 11, 14, 0, 3],
#     [21, 20, 31, 22, 20, 3, 3, 0]
# ]
#
# matrix13 = [
#     [0, 20, 30, 31, 28, 40, 8, 21, 50],
#     [20, 0, 10, 14, 20, 44, 9, 20, 3],
#     [30, 10, 0, 10, 22, 50, 5, 31, 10],
#     [31, 14, 10, 0, 14, 42, 3, 22, 4],
#     [28, 20, 22, 14, 0, 28, 11, 20, 9],
#     [40, 44, 50, 42, 28, 0, 14, 3, 2],
#     [28, 9, 5, 3, 11, 14, 0, 3, 10],
#     [21, 20, 31, 22, 20, 3, 3, 0, 11],
#     [50, 3, 10, 4, 9, 2, 10, 11, 0]
# ]
#
matrix_my_11 = [
    [-1, 29, 82, 46, 68, 52, 72, 42, 51, 55, 29],
    [29, -1, 55, 46, 42, 43, 43, 23, 23, 31, 41],
    [82, 55, -1, 68, 46, 55, 23, 43, 41, 29, 79],
    [46, 46, 68, -1, 82, 15, 72, 31, 62, 42, 21],
    [68, 42, 46, 82, -1, 74, 23, 52, 21, 46, 82],
    [52, 43, 55, 15, 74, -1, 61, 23, 55, 31, 33],
    [72, 43, 23, 72, 23, 61, -1, 42, 23, 31, 77],
    [42, 23, 43, 31, 52, 23, 42, -1, 33, 15, 37],
    [51, 23, 41, 62, 21, 55, 23, 33, -1, 29, 62],
    [55, 31, 29, 42, 46, 31, 31, 15, 29, -1, 51],
    [29, 41, 79, 21, 82, 33, 77, 37, 62, 51, -1]
]
tsp_my_11_opti = '251; [0, 1, 8, 4, 6, 2, 9, 7, 5, 3, 10, 0]'

if __name__ == '__main__':
    main()
