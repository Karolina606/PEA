import itertools
import math
import sys
import time
from configparser import ConfigParser
import random

import gc
import os

import numpy.random
import wmi
from itertools import permutations

from Ant import Ant
from my_writer import my_writer
from graph_instance_class import instance

fitness_list = []

alpha = 1
beta = 5
ro = 0.5
m = 1
pher_distribution = 'DAS'
heuristic = 'vis'
iterations = 0
tsp_aco_param = []


def memory():
    w = wmi.WMI('.')
    result = w.query("SELECT WorkingSet FROM Win32_PerfRawData_PerfProc_Process "
                     "WHERE IDProcess=%d" % os.getpid())
    return int(result[0].WorkingSet)


def calculate_way_cost(way, matrix):
    cost = 0
    for i in range(len(way)-1):
        cost += matrix[way[i]][way[i+1]]

    return cost


def aco(matrix: instance):
    global alpha, beta, ro, m, pher_distribution, heuristic, iterations
    global tsp_aco_param
    best_path = []
    best_cost = 9999999999
    ants = []
    m = matrix.length

    print()

    # stwórz potrzebne mrówki i umieść w miastach początkowych
    for i in range(m):
        ant = Ant(i)
        # print("Ant " + str(i) + " tabu " + str(ant.tabu_list))
        ants.append(ant)
        # print("Tworzę " + str(i) + " mrówkę")

    C_nn = 10
    ro_0 = m/C_nn

    matrix.init_pheromone_matrix(ro_0)

    # iterations = range(1)
    if matrix.length <= 50:
        iterations = range(int(matrix.length))
    if matrix.length > 50 and matrix.length <= 80:
        iterations = range(int(matrix.length / 3))
    if matrix.length > 80:
        iterations = range(3)
    # iterations = range(m)
    #iterations = range(int(matrix.length / 4))

    for iteration in iterations:
        # print("Iteracja " + str(iteration))
        # (1, 2) = Q_das ----> słownik krawędzi z wartością dodanego feromonu
        delta_tau = {}

        for i in range(matrix.length-1):

            if pher_distribution == 'DAS' or pher_distribution == 'QAS':
                delta_tau = {}

            # dla każdej mrówki
            for j in range(len(ants)):
                current_ant = ants[j]
                # wybór kolejnego kroku dla mrówki

                p_ij = 0
                city_with_best_probability = -1
                p_sum = 0
                choosen_city = -1

                # print("Mrowka " + str(j) + " tabu: " + str(current_ant.tabu_list))
                # print(set(range(matrix.length)))
                # print(set(current_ant.tabu_list))
                # print(set(range(matrix.length)) - set(current_ant.tabu_list))
                # dla obliczebia mianownika prawdopodobieństwa

                possible_cities = {}

                # Liczymy licznik prawdopodobieństwa dla każdego miasta, a także wspólną sume mianownikia
                for possible_city in range(matrix.length):
                    if possible_city in current_ant.tabu_list:
                        continue
                    # print("Pos city " + str(possible_city))
                    # print(len(matrix.matrix))
                    # print(len(matrix.matrix[1]))
                    if matrix.matrix[current_ant.current_vertex][possible_city] == 0 or \
                            matrix.matrix[current_ant.current_vertex][possible_city] == -1:
                        continue

                    if matrix.matrix[current_ant.current_vertex][possible_city] == 0 or \
                            matrix.matrix[current_ant.current_vertex][possible_city] == -1:
                         p = 0
                    else:
                        # Jaka heurystyka wyboru
                        n_ij = 1.0 / matrix.matrix[current_ant.current_vertex][possible_city]
                        if heuristic == 'vis2':
                            n_ij = n_ij / matrix.matrix[current_ant.current_vertex][possible_city]
                        p = matrix.pheromone_matrix[current_ant.current_vertex][possible_city] ** alpha \
                            * n_ij ** beta

                    possible_cities[possible_city] = p
                    p_sum += p

                # Podział wszystkich elementów aby usyzkać pop. prawdopodobieństwo
                if p_sum == 0:
                    continue
                possibilities = [x/p_sum for x in possible_cities.values()]


                # choosen_city = numpy.random.choice(list(possible_cities.keys()), 1, False, possibilities)[0]
                choosen_city = random.choices(list(possible_cities.keys()), possibilities, k=1)[0]

                # print("choosen " + str(choosen_city))

                pheromone_to_add = 1
                # obliczenie wartości fermonu
                if pher_distribution == 'DAS':
                    pheromone_to_add = 10
                elif pher_distribution == 'QAS':
                    pheromone_to_add = 10 / (matrix.matrix[current_ant.current_vertex][choosen_city])
                elif pher_distribution == 'CAS':
                    pheromone_to_add = 10 / calculate_way_cost(current_ant.tabu_list, matrix.matrix)

                # zapisanie wartości feromonu
                if (current_ant.current_vertex, choosen_city) in delta_tau.keys():
                    delta_tau[(current_ant.current_vertex, choosen_city)] += pheromone_to_add
                else:
                    delta_tau[(current_ant.current_vertex, choosen_city)] = pheromone_to_add

                # dodanie feromonu jeśli DAS lub QAS
                if pher_distribution == 'DAS' or pher_distribution == 'QAS':
                    # Dodanie feromonu od razu po przejściu mrówki DAS / QAS
                    matrix.pheromone_matrix[current_ant.current_vertex][choosen_city] += pheromone_to_add

                # przejście do nowego miasta
                current_ant.change_city(choosen_city)

            if pher_distribution == 'DAS' or pher_distribution == 'QAS':
                # wyparowanie feromonu po przejsciu wszystkich mrowek DAS / QAS
                matrix.decrease_pheromone(ro)
                # dodanie feromonów po wszystkich mrówkach
                for key in delta_tau.keys():
                    matrix.pheromone_matrix[key[0]][key[1]] += delta_tau.get(key)

        # aktualizacja feromonu przy CAS
        if pher_distribution == 'CAS':
            cas_pheromone_update(matrix, delta_tau)

        # obliczanie znalezionych tras przez mrówki, zapamiętana najkrótsza:
        the_same_way_counter = 0
        for ant in ants:
            way = ant.tabu_list
            way.append(ant.tabu_list[0])
            cost = calculate_way_cost(way, matrix.matrix)

            # jeśli ścieżka lepsza od dotychczasowej
            if cost < best_cost:
                best_path = way
                best_cost = cost
            elif cost == best_cost:
                the_same_way_counter += 1

            ant.tabu_list = [ant.tabu_list[0]]
            ant.current_vertex = ant.tabu_list[0]

        # jeśli wszystkie mrówki wskazały tą samą trasę
        if the_same_way_counter == m:
            return best_path, best_cost

    return best_path, best_cost


def cas_pheromone_update(matrix: instance, delta_tau):
    matrix.decrease_pheromone(ro)
    for key in delta_tau.keys():
        matrix.pheromone_matrix[key[0]][key[1]] += delta_tau.get(key)


def work(matrix: instance):
    print("Liczę dla: " + matrix.name)

    start_time = time.time()
    path, cost = aco(matrix)
    end_time = time.time() - start_time

    tsp_result = [str(matrix.name), int(matrix.length), end_time, cost, path, memory()]
    print("Name: " + str(tsp_result[0]) + ", size: " + str(tsp_result[1]) + ", time: " + str(end_time) +
          ", cost: " + str(cost) + ", memory: " + str(memory()))

    # return tsp_result, tsp_ts_params
    return tsp_result


def main():
    # tab = [(4, 0), (6, 1), (7, 2), (8, 3), (2, 4), (12, 5), (231, 6), (1, 7)]
    # mini, parent = min(tab)
    # print("min: " + str(mini))
    # print("parent: " + str(parent))
    global alpha, beta, ro, m, pher_distribution, heuristic, iterations
    global tsp_aco_param

    try:
        # Otworzenie pliku .ini i wczytanie jego parametrów
        file = 'config.ini'
        config = ConfigParser()
        config.read(file)

        #Zczytanie parametrów
        alpha = float(config['param']['alpha'])
        beta = int(config['param']['beta'])
        ro = float(config['param']['ro'])
        m = int(int(config['param']['m']))
        pher_distribution = str(config['param']['pher_distribution'])
        heuristic = str(config['param']['heuristic'])

        tsp_aco_param = [alpha, beta, ro, m, pher_distribution, heuristic]
        result_out_file = str(config['result']['tsp_aco'])
        writer = my_writer(result_out_file, tsp_aco_param)

        matrixes = []
        data = config['data']
        for each in data:
            #print(each)
            unit = config['data'][each]
            #print(unit)
            matrix = instance(unit)
            matrixes.append(matrix)


        # Make analysis
        writer.header_write_to_csv(['nazwa', 'wielkosc', 'czas', 'wynik', 'sciezka', 'wynik pop.', 'pamiec'], 'blad %')

        for matrix in matrixes:
            tsp_result = work(matrix)
            tsp_opti = str([matrix.opti_result, matrix.opti_path])
            tsp_error = (tsp_result[3] - matrix.opti_result) / float(matrix.opti_result) * 100.0
            tsp_aco_param = [alpha, beta, ro, m, pher_distribution, heuristic, iterations]
            writer.tsp_aco_param = tsp_aco_param
            writer.simple_write_to_csv(tsp_result, tsp_opti, tsp_error)
            print("Opti: cost: " + tsp_opti)
            print("Error: " + str(tsp_error) + "%")

        input('Skończyłem, wciśnij cokolwiek, aby mnie wyłączyć...')
        sys.exit(0)

    except OSError:
        print("Coś poszło nie tak, sprawdź czy plik inicjujący")


if __name__ == '__main__':
    main()
