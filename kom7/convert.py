import math


def main():
    file = "pr1002.txt"
    out_file = "pr1002.tsp"
    n = 1002
    vertexes = {}
    matrix = []
    with open(file) as f:
        lines = f.readlines()

        i = 0
        for line in lines:
            sklad = line.split(' ')
            vertexes[i] = (float(sklad[1]), float(sklad[2]))
            i += 1

        for line in range(n):
            wiersz = []
            for column in range(n):
                distance = math.sqrt( (vertexes[line][0] - vertexes[column][0])**2 + (vertexes[line][1] - vertexes[column][1])**2 )
                wiersz.append(distance)
            matrix.append(wiersz)

        with open(out_file, 'a') as f:
            for line in matrix:
                f.write(list_to_line(line))


def list_to_line(list):
    line = ""
    for element in list:
        line += str(int(element))
        line += " "

    line += '\n'
    return line


if __name__ == '__main__':
    main()