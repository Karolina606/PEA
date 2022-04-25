import sys
import time
from configparser import ConfigParser
import my_writer

visited = []
min_way = 10000000000000
current_path = 0
path = []


def visit_neighbor(ver, matrix):
    global min_way
    global path
    # przechodzi przez każdy wierzchołek
    for i in range(len(matrix)):
        # zostaje w wierzchołku jeśli to inny wierzchołek niż przed chwilą i nie odwiedziliśmy go wcześniej
        if i != ver and i not in visited and matrix[ver][i] != 0:
            print(visited)
            # dodaje wierzchołek do odwiedzonych
            visited.append(i)
            # odwiedza sąsiadów tego wierzchołka
            visit_neighbor(i, matrix)
            print(visited)

            # jeśli odwiedziliśmy już wszystkie wierzchołki
            if len(visited) == len(matrix):
                # sprawdź drogę
                current_way = 0
                for j in range(len(visited) - 1):
                    # dodaje wszystkie wagi dróg na trasie
                    current_way = current_way + int(matrix[visited[j]][visited[j + 1]])
                # dodaje powrót do początku
                current_way = current_way + int(matrix[visited[len(visited)-1]][visited[0]])
                # sprawdza czy ta droga jest krótsza niż wcześniej zapisana
                if current_way < min_way:
                    min_way = current_way
                    path = visited.copy()
                    print('path: '+ str(path))

            visited.remove(i)

    return min_way


def work(matrix):
    global min_way
    global visited
    global current_path
    global path
    visited = []
    min_way = 10000000000000
    current_path = 0

    start_time = time.time()

    visited.append(0)
    result = visit_neighbor (0, matrix)

    end_time1 = time.time() - start_time
    print("Path: " + str(path))
    return [len(matrix), result, end_time1, path + [0]]


def from_txt_to_matrix(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        n = int(lines[0])

        matrix = []
        for each in lines[1:]:
            matrix.append(each.split())

    return matrix


def main():
    try:
        # Otworzenie pliku .ini i wczytanie jego parametrów
        file = 'config.ini'
        config = ConfigParser()
        config.read(file)

        # Zczytanie parametrów
        result_out_file = config['result']['tsp_bf']
        data0 = config['data']['file0']
        data1 = config['data']['file1']
        data2 = config['data']['file2']
        data3 = config['data']['file3']
        data4 = config['data']['file4']
        data5 = config['data']['file5']
        data6 = config['data']['file6']
        data7 = config['data']['file7']

        matrix0_1 = from_txt_to_matrix(data7)
        matrix1 = from_txt_to_matrix(data1)
        matrix2 = from_txt_to_matrix(data2)
        matrix3 = from_txt_to_matrix(data3)
        matrix4 = from_txt_to_matrix(data4)
        matrix5 = from_txt_to_matrix(data5)
        matrix6 = from_txt_to_matrix(data6)
        matrix0_2 = from_txt_to_matrix(data0)


        # Make analysis
        # tsp_result = [0, 0, 0, []] # wielkość instancji, wynik tsp, czas
        tsp_result = work(matrix7)
        my_writer.simple_write_to_csv(result_out_file, tsp_result)
        tsp_result = work(matrix8)
        my_writer.simple_write_to_csv(result_out_file, tsp_result)
        tsp_result = work(matrix9)
        my_writer.simple_write_to_csv(result_out_file, tsp_result)
        tsp_result = work(matrix0_1)
        my_writer.simple_write_to_csv(result_out_file, tsp_result)
        tsp_result = work(matrix0_2)
        my_writer.simple_write_to_csv(result_out_file, tsp_result)
        tsp_result = work(matrix11)
        my_writer.simple_write_to_csv(result_out_file, tsp_result)
        tsp_result = work(matrix12)
        my_writer.simple_write_to_csv(result_out_file, tsp_result)
        tsp_result = work(matrix13)
        my_writer.simple_write_to_csv(result_out_file, tsp_result)
        tsp_result = work(matrix1)
        my_writer.simple_write_to_csv(result_out_file, tsp_result)
        tsp_result = work(matrix14)
        my_writer.simple_write_to_csv(result_out_file, tsp_result)
        tsp_result = work(matrix2)
        my_writer.simple_write_to_csv(result_out_file, tsp_result)

        input('Skończyłem, wciśnij cokolwiek, aby mnie wyłączyć...')
        sys.exit(0)

    except OSError:
        print("Coś poszło nie tak, sprawdź czy plik inicjujący")


matrix7 = [
    [0, 10],
    [10, 0]
]

matrix8 = [
    [0, 10, 12, 8],
    [10, 0, 15, 18],
    [12, 15, 0, 5],
    [8, 18, 5, 0]
]

matrix9 = [
    [0, 10, 12, 8, 9],
    [10, 0, 15, 18, 10],
    [12, 15, 0, 5, 11],
    [8, 18, 5, 0, 5],
    [9, 10, 11, 5, 0]
]

matrix10 = [
    [0, 10, 12, 8, 9, 31],
    [10, 0, 15, 18, 10, 50],
    [12, 15, 0, 5, 11, 4],
    [8, 18, 5, 0, 5, 19],
    [9, 10, 11, 5, 0, 21],
    [31, 50, 4, 19, 21, 0]
]

matrix11 = [
    [0, 10, 12, 8, 9, 31, 2],
    [10, 0, 15, 18, 10, 50, 4],
    [12, 15, 0, 5, 11, 4, 8],
    [8, 18, 5, 0, 5, 19, 16],
    [9, 10, 11, 5, 0, 21, 20],
    [31, 50, 4, 19, 21, 0, 30],
    [2, 4, 8, 16, 20, 30, 0]
]

matrix12 = [
    [0, 20, 30, 31, 28, 40, 8, 21],
    [20, 0, 10, 14, 20, 44, 9, 20],
    [30, 10, 0, 10, 22, 50, 5, 31],
    [31, 14, 10, 0, 14, 42, 3, 22],
    [28, 20, 22, 14, 0, 28, 11, 20],
    [40, 44, 50, 42, 28, 0, 14, 3],
    [8, 9, 5, 3, 11, 14, 0, 3],
    [21, 20, 31, 22, 20, 3, 3, 0]
]

matrix13 = [
    [0, 20, 30, 31, 28, 40, 8, 21, 50],
    [20, 0, 10, 14, 20, 44, 9, 20, 3],
    [30, 10, 0, 10, 22, 50, 5, 31, 10],
    [31, 14, 10, 0, 14, 42, 3, 22, 4],
    [28, 20, 22, 14, 0, 28, 11, 20, 9],
    [40, 44, 50, 42, 28, 0, 14, 3, 2],
    [28, 9, 5, 3, 11, 14, 0, 3, 10],
    [21, 20, 31, 22, 20, 3, 3, 0, 11],
    [50, 3, 10, 4, 9, 2, 10, 11, 0]
]

matrix14 = [
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


if __name__ == '__main__':
    main()
