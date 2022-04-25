import itertools
import sys
import time
from configparser import ConfigParser

import my_writer
import gc
import os
from wmi import WMI
from queue import PriorityQueue
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree

actual_node = None


def memory():
    w = WMI('.')
    result = w.query("SELECT WorkingSet FROM Win32_PerfRawData_PerfProc_Process WHERE IDProcess=%d" % os.getpid())
    return int(result[0].WorkingSet)


def mst_find(matrix):
    X = csr_matrix(matrix)

    tcsr = minimum_spanning_tree(X)
    tcsr = tcsr.toarray().astype(int)

    c = 0
    for x in tcsr:
        for y in x:
            c += y
    return c


class tsp_lc_node:
    def __init__(self, parent, number, nodes_in_trace=None, cost=0):
        if nodes_in_trace is None:
            nodes_in_trace = []
        self.parent = parent
        self.number = number
        self.nodes_in_trace = nodes_in_trace
        self.cost = cost

    def __eq__(self, other):
        comp = True
        if self.cost != other.cost:
            comp = False
        return comp

    def __gt__(self, other):
        comp = False
        if self.cost > other.cost:
            comp = True
        return comp

    def __le__(self, other):
        comp = False
        if self.cost < other.cost:
            comp = True
        return comp


def low_cost(matrix):
    global actual_node
    priority_queue = PriorityQueue()
    # priority_queue = []
    n = len(matrix)
    bool_nodes_tab = [False] * n
    mini = 100000
    mini_node = None
    mst = mst_find(matrix)
    print("mst dla: " + str(n) + "mst: " + str(mst))

    # inicjowanie pierwszego węzła
    bool_nodes_tab[0] = True
    first_node = tsp_lc_node(None, 0, bool_nodes_tab, 0)

    for i in range(len(matrix[0])):
        if i != first_node.number:
            new_bool_nodes_tab = first_node.nodes_in_trace.copy()
            new_bool_nodes_tab[i] = True
            new_node = tsp_lc_node(first_node, i, new_bool_nodes_tab, first_node.cost + matrix[first_node.number][i])
            # print(new_node.nodes_in_trace)
            priority_queue.put(new_node)

    actual_node = priority_queue.get()
    # priority_queue.remove((_, actual_node))

    while not priority_queue.empty():
        # print("hallo: " + str(actual_node))
        # print("Wybrałem: " + str(actual_node.number) + ";" + str(actual_node.cost) + ";" + str(actual_node.nodes_in_trace))
        for i in range(1, len(matrix[actual_node.number])):
            new_node = None
            if i != actual_node.number and actual_node.nodes_in_trace[i] is False:
                if actual_node.cost + matrix[actual_node.number][i] < 2 * mst and actual_node.cost + matrix[actual_node.number][i] < mini:
                    new_bool_nodes_tab = actual_node.nodes_in_trace.copy()
                    new_bool_nodes_tab[i] = True
                    new_node = tsp_lc_node(actual_node, i, new_bool_nodes_tab,
                                           actual_node.cost + matrix[actual_node.number][i])

                    if False in new_bool_nodes_tab:
                        priority_queue.put(new_node)

                    if False not in new_node.nodes_in_trace:
                        if new_node.cost + matrix[new_node.number][0] < mini:
                            mini = new_node.cost + matrix[new_node.number][0]
                            mini_node = new_node
                            print(mini)
                            if (mini - mst)/mst < 0.14:
                                break
        if (mini - mst) / mst < 0.14:
            break
        actual_node = priority_queue.get()
        #priority_queue.remove((_, actual_node))

    path = []
    path.append(mini_node.number)
    while mini_node.parent is not None:
        mini_node = mini_node.parent
        path.append(mini_node.number)

    path = list(reversed(path)) + [0]
    return path, mini


def work(name, matrix):

    print("Liczę dla: " + name)

    start_time = time.time()
    path, cost = low_cost(matrix)
    end_time = time.time() - start_time

    tsp_result = [name, len(matrix), end_time, memory(), cost, path]
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
        result_out_file_bs = config['result']['tsp_bs']
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

        # tsp_result = work("matrix_my_4", matrix_my_4)
        # my_writer.simple_write_to_csv(result_out_file, tsp_result, tsp_my_4_opti)
        #
        # tsp_result = work("matrix_my_5", matrix_my_5)
        # my_writer.simple_write_to_csv(result_out_file, tsp_result, tsp_my_5_opti)
        #
        # tsp_result = work("matrix6_1", matrix6_1)
        # my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix6_1_opti)
        #
        # tsp_result = work("matrix6_2", matrix6_2)
        # my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix6_2_opti)
        #
        # tsp_result = work("matrix10", matrix10)
        # my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix10_opti)
        # #
        # # tsp_result = work("matrix_my_11", matrix_my_11)
        # # my_writer.simple_write_to_csv(result_out_file, tsp_result, tsp_my_11_opti)
        #
        # tsp_result = work("matrix12", matrix12)
        # my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix12_opti)
        #
        # tsp_result = work("matrix13", matrix13)
        # my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix13_opti)
        #
        # tsp_result = work("matrix14", matrix14)
        # my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix14_opti)
        #
        # tsp_result = work("matrix15", matrix15)
        # my_writer.simple_write_to_csv(result_out_file, tsp_result, matrix15_opti)
        #
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
