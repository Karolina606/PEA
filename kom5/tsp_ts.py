import itertools
import math
import sys
import time
from configparser import ConfigParser
import random

import gc
import os
import wmi
from itertools import permutations

from my_writer import my_writer
from instance_class import instance

fitness_list = []

maxTabuSize = 10000
neighborhood_size = 500
stoppingTurn = 500
swap_way = 0
cadence = 15
tsp_ts_param = []

def memory():
    w = wmi.WMI('.')
    result = w.query("SELECT WorkingSet FROM Win32_PerfRawData_PerfProc_Process WHERE IDProcess=%d" % os.getpid())
    return int(result[0].WorkingSet)


def random_initial(matrix):
    nodes = list(range(len(matrix)))
    first_node = current_node = random.choice(nodes)
    solution = [current_node]
    nodes.remove(current_node)

    while nodes:
        next_node = random.choice(nodes)
        if next_node in nodes:
            nodes.remove(next_node)
            solution.append(next_node)
            current_node = next_node
            # print("Nodes: " + str(nodes) + " Solution: " + str(solution))

    solution.append(first_node)
    fitness_list.append(solution)

    return solution


def initial(matrix):
    global fitness_list
    nodes = list(range(len(matrix)))
    first_node = current_node = random.choice(nodes)
    solution = [current_node]
    nodes.remove(current_node)

    while nodes:
        next_node = min(nodes, key=lambda x: matrix[current_node][x])
        nodes.remove(next_node)
        solution.append(next_node)
        current_node = next_node
        # print("Nodes: " + str(nodes) + " Solution: " + str(solution))

    solution.append(first_node)
    fitness_list.append(solution)

    return solution


def get_neighbors(state, matrix):
    # return hill_climbing(state)
    # return two_opt_swap(state)

    # dwuzmiana
    if swap_way == 0:
        # current_perm = state.copy()
        # tmp_best = state.copy()
        # node1 = random.randint(1, len(matrix)-2)
        # node2 = random.randint(1, len(matrix)-2)
        #
        # current_perm[node1] = tmp_best[node2]
        # current_perm[node2] = tmp_best[node1]
        # return [current_perm]
        return two_opt_swap(state)

    # zamiana dwóch części tablicy
    if swap_way == 1:
        tmp_best = state.copy()
        divide_index = random.randint(1, len(matrix) - 2)
        first_part = tmp_best[divide_index:len(matrix) - 2]
        second_part = tmp_best[1:divide_index]
        current_perm = [tmp_best[0]] + first_part + second_part + [tmp_best[len(matrix) - 2]]
        return [current_perm]

    # odwrocenie czesci
    if swap_way == 2:
        tmp_best = state.copy()
        index1 = random.randint(1, len(state) - 2)
        index2 = random.randint(1, len(state) - 2)
        while index1 == index2:
            index2 = random.randint(1, len(state) - 2)
        if index1 > index2:
            swap = index1
            index1 = index2
            index2 = swap
        tmp_best = tmp_best[:index1] + tmp_best[index1:index2:-1] + tmp_best[:index2]
        return [tmp_best]

    # hill climbing
    if swap_way == 3:
        return hill_climbing(state)


def hill_climbing(state):
    node = random.randint(1, len(state) - 2)
    neighbors = []

    for i in range(len(state)-1):
        if i != node and i != 0:
            tmp_state = state.copy()
            tmp = tmp_state[i]
            tmp_state[i] = tmp_state[node]
            tmp_state[node] = tmp
            neighbors.append(tmp_state)

    return neighbors


def two_opt_swap(state):
    global neighborhood_size
    neighbors = []

    for i in range(neighborhood_size):
        node1 = 0
        node2 = 0

        while node1 == node2:
            node1 = random.randint(1, len(state) - 1)
            node2 = random.randint(1, len(state) - 1)

        if node1 > node2:
            swap = node1
            node1 = node2
            node2 = swap

        tmp = state[node1:node2]
        tmp_state = state[:node1] + tmp[::-1] + state[node2:]
        neighbors.append(tmp_state)

    return neighbors


def weight_distance(city1, city2, matrix):
    global max_fitness

    if matrix[city1][city2] != 0 and matrix[city1][city2] != -1:
        return matrix[city1][city2]

    return -1  # there can't be minus distance, so -1 means there is not any city found in graph or there is not such edge


def calculate_way_cost(way, matrix):
    cost = 0
    for i in range(len(way)-1):
        cost += matrix[way[i]][way[i+1]]

    return cost


def tabu_search(matrix):
    global maxTabuSize, neighborhood_size, stoppingTurn, cadence
    global tsp_ts_param

    # czy chcemy wczytać z pliku, czy żeby policzyło
    if_maxTabuSize_auto = True
    if_neighborhood_size_auto = True
    if_stoppingTurn_auto = False
    if_cadence_auto = True

    if if_maxTabuSize_auto:
        maxTabuSize = 3 * len(matrix)
    if if_neighborhood_size_auto:
        neighborhood_size = int((len(matrix) * (len(matrix)-1))/2)
    if if_stoppingTurn_auto:
        stoppingTurn = len(matrix) * 10
    if if_cadence_auto:
        cadence = int(len(matrix) * 0.20)

    iterations = 0

    # zainicjuj rozw. poczatkowe
    s0 = initial(matrix)

    # max_fitness will act like infinite fitness
    sBest = s0
    vBest = calculate_way_cost(s0, matrix)
    bestCandidate = s0
    tabuList = {tuple(s0): cadence}
    # [0, 1] - 0 ścieżka, 1 ilość cadence
    stop = False
    best_keep_turn = 0

    # start_time = time.time()
    while not stop:
        sNeighborhood = get_neighbors(bestCandidate, matrix)
        bestCandidate = sNeighborhood[0]
        for sCandidate in sNeighborhood:
            if (tuple(sCandidate) in tabuList.keys() and calculate_way_cost(sCandidate, matrix) < calculate_way_cost(bestCandidate, matrix)) * 0.3 and len(matrix) > 20:
                tabuList.pop(tuple(sCandidate))
                bestCandidate = sCandidate

            elif (tuple(sCandidate) not in tabuList.keys() and calculate_way_cost(sCandidate, matrix) < calculate_way_cost(bestCandidate, matrix)):
                bestCandidate = sCandidate

        if calculate_way_cost(bestCandidate, matrix) < calculate_way_cost(sBest, matrix):
            sBest = bestCandidate
            vBest = calculate_way_cost(sBest, matrix)
            best_keep_turn = 0

        newTabuList = {}
        # zmniejszenie cadence każdego
        for key in tabuList.keys():
            tabuList[key] -= 1
            if tabuList[key] >= 0:
                newTabuList[key] = tabuList[key]

        tabuList = newTabuList

        tabuList[tuple(bestCandidate)] = cadence

        if len(tabuList) > maxTabuSize:
            tabuList.pop(0)

        if best_keep_turn == stoppingTurn:
            if iterations % 2 == 0:
                iterations += 1
                bestCandidate = initial(matrix)
                tabuList = {tuple(s0): cadence}
                # [0, 1] - 0 ścieżka, 1 ilość cadence
                stop = False
            else:
                stop = True
            best_keep_turn = 0

        # if best_keep_turn == stoppingTurn:
        #     stop = True
        #     best_keep_turn = 0

        if iterations == stoppingTurn:
            stop = True

        best_keep_turn += 1

    # exec_time = time.time() - start_time
    cost = calculate_way_cost(sBest, matrix)
    return sBest, cost


def work(matrix: instance):
    print("Liczę dla: " + matrix.name)

    start_time = time.time()
    path, cost = tabu_search(matrix.matrix)
    end_time = time.time() - start_time

    tsp_result = [str(matrix.name), int(matrix.length), end_time, cost, path]
    print("Name: " + str(tsp_result[0]) + ", size: " + str(tsp_result[1]) + ", time: " + str(end_time) +
          ", cost: " + str(cost))

    # return tsp_result, tsp_ts_params
    return tsp_result


def main():
    # tab = [(4, 0), (6, 1), (7, 2), (8, 3), (2, 4), (12, 5), (231, 6), (1, 7)]
    # mini, parent = min(tab)
    # print("min: " + str(mini))
    # print("parent: " + str(parent))
    global maxTabuSize, neighborhood_size, stoppingTurn, swap_way, cadence
    global tsp_ts_param

    try:
        # Otworzenie pliku .ini i wczytanie jego parametrów
        file = 'config.ini'
        config = ConfigParser()
        config.read(file)

        #Zczytanie parametrów
        maxTabuSize = int(config['param']['maxTabuSize'])
        neighborhood_size = int(config['param']['neighborhood_size'])
        stoppingTurn = int(config['param']['stoppingTurn'])
        swap_way = int(config['param']['swap_way'])
        cadence = int(config['param']['cadence'])

        tsp_ts_param = [maxTabuSize, neighborhood_size, stoppingTurn, swap_way, cadence]
        result_out_file = str(config['result']['tsp_ts'])
        writer = my_writer(result_out_file, tsp_ts_param)

        matrixes = []
        data = config['data']
        for each in data:
            #print(each)
            unit = config['data'][each]
            #print(unit)
            matrix = instance(unit)
            matrixes.append(matrix)


        # Make analysis
        writer.simple_write_to_csv(['', '', '', '', '', ''], '', '')

        for matrix in matrixes:
            tsp_result = work(matrix)
            tsp_opti = str([matrix.opti_result, matrix.opti_path])
            tsp_error = (tsp_result[3] - matrix.opti_result) / float(matrix.opti_result) * 100.0
            tsp_ts_param = [maxTabuSize, neighborhood_size, stoppingTurn, swap_way, cadence]
            writer.tsp_ts_param = tsp_ts_param
            writer.simple_write_to_csv(tsp_result, tsp_opti, tsp_error)
            print("Opti: cost: " + tsp_opti)
            print("Error: " + str(tsp_error) + "%")

        input('Skończyłem, wciśnij cokolwiek, aby mnie wyłączyć...')
        sys.exit(0)

    except OSError:
        print("Coś poszło nie tak, sprawdź czy plik inicjujący")


if __name__ == '__main__':
    main()
