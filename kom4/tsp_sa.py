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


def simul_annealing(matrix, tsp_sa_params):
    # Deafult
    a = 0.98
    b = 0.01
    T = 1000
    T_min = 0.001
    # 0 - dwuzmiana, 1 - podział tablicy na dwie części i ich zamiana, 2 - losowanie czesci tablicy i revers na niej
    swap_way = 0

    # Z tsp_sa_params
    T0 = tsp_sa_params[0]
    cooling = tsp_sa_params[1]
    walking = tsp_sa_params[2]
    era = tsp_sa_params[3]
    a = tsp_sa_params[4]

    T = T0
    best = []
    tmp_best = []

    # ustalenie ery
    # era = len(matrix) * 3
    # tsp_sa_params[3] = era


    # losujemy rozwiązanie początkowe:
    best = tmp_best = random_initial(matrix)
    # print(best)
    # T = calculate_way_cost(matrix, list(best)) * len(matrix) / 10
    # tsp_sa_params[0] = T

    # epoka
    epoka = 0
    current_perm = []
    stagnation_counter = 0

    while T > T_min:
        epoka = 0
        stagnation_counter = 0
        while epoka < era:

            current_perm = tmp_best.copy()
            # dwuzmiana
            if swap_way == 0:
                node1 = random.randint(1, len(matrix)-2)
                node2 = random.randint(1, len(matrix)-2)

                current_perm[node1] = tmp_best[node2]
                current_perm[node2] = tmp_best[node1]

            # zamiana dwóch części tablicy
            if swap_way == 1:
                divide_index = random.randint(1, len(matrix) - 2)
                first_part = tmp_best[divide_index:len(matrix)-2]
                second_part = tmp_best[1:divide_index]
                current_perm = current_perm[0] + first_part + second_part + current_perm[len(matrix)-1]

            # odwrocenie czesci
            if swap_way == 2:
                index1 = random.randint(1, len(matrix) - 2)
                index2 = random.randint(1, len(matrix) - 2)
                while index1 == index2:
                    index2 = random.randint(1, len(matrix) - 2)
                current_perm[index1:index2] = current_perm[index1:index2].reverse()

            delta_dist = calculate_way_cost(matrix, list(current_perm)) - calculate_way_cost(matrix, list(best))
            if delta_dist < 0:
                best = current_perm
                tmp_best = current_perm
                stagnation_counter = 0
            else:
                random_number = random.randint(0, 100)/100.0
                if random_number < math.exp(-delta_dist/T):
                    tmp_best = current_perm
                    stagnation_counter = 0
                else:
                    stagnation_counter += 1
                    if stagnation_counter == era:
                        tmp_best = initial(matrix)
                        if calculate_way_cost(matrix, tmp_best) < calculate_way_cost(matrix, best):
                            best = tmp_best

            # print(current_perm)
            # print("T: " + str(T) + " era: " + str(epoka))

            epoka += 1
        T = cool(cooling, T, a, T_min, epoka)

    return best, calculate_way_cost(matrix, list(best)), tsp_sa_params


def cool(cooling_way, T, a, T_min, epoka):
    if cooling_way == "log":
        T = log_cooldown(T, a, epoka)
    if cooling_way == "cauchy":
        T = cauchy_cooldown(T, T_min, epoka)
    else:
        T = geo_cooldown(T, a)

    return T


def log_cooldown(T, a, epoka):
   return T / (math.log10(epoka))


def cauchy_cooldown(T, T_min, epoka):
    return T - ((T_min - 1) / epoka)


def geo_cooldown(T, a):
    return a * T


def calculate_way_cost(matrix, way):
    cost = 0
    for i in range(len(way)-1):
        cost += matrix[way[i]][way[i+1]]

    return cost


def work(matrix: instance, tsp_sa_params):
    print("Liczę dla: " + matrix.name)

    start_time = time.time()
    path, cost, tsp_sa_params = simul_annealing(matrix.matrix, tsp_sa_params)
    end_time = time.time() - start_time

    tsp_result = [str(matrix.name), int(matrix.length), end_time, cost, path]
    print("Name: " + str(tsp_result[0]) + ", size: " + str(tsp_result[1]) + ", time: " + str(end_time) +
          ", cost: " + str(cost))

    return tsp_result, tsp_sa_params


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

        #Zczytanie parametrów
        T0 = int(config['param']['T0'])
        cooling = config['param']['cooling']
        walking = config['param']['walking']
        era = int(config['param']['era'])
        a = float(config['param']['a'])
        swap_way = int(config['param']['swap_way'])

        tsp_sa_param = [T0, cooling, walking, era, a, swap_way]
        result_out_file = str(config['result']['tsp_sa'])
        writer = my_writer(result_out_file, tsp_sa_param)

        matrixes = []
        data = config['data']
        for each in data:
            # print(each)
            unit = config['data'][each]
            # print(unit)
            matrix = instance(unit)
            matrixes.append(matrix)


        # Make analysis
        writer.simple_write_to_csv(['', '', '', '', '', ''], '', '')

        for matrix in matrixes:
            tsp_result, tsp_sa_param = work(matrix, tsp_sa_param)
            tsp_opti = str([matrix.opti_result, matrix.opti_path])
            tsp_error = (tsp_result[3] - matrix.opti_result) / float(matrix.opti_result) * 100.0
            writer.tsp_sa_param = tsp_sa_param
            writer.simple_write_to_csv(tsp_result, tsp_opti, tsp_error)
            print("Opti: cost: " + tsp_opti)
            print("Error: " + str(tsp_error) + "%")

        input('Skończyłem, wciśnij cokolwiek, aby mnie wyłączyć...')
        sys.exit(0)

    except OSError:
        print("Coś poszło nie tak, sprawdź czy plik inicjujący")


if __name__ == '__main__':
    main()
