

class instance:
    def __init__(self, parameters_as_string: str):
        params = parameters_as_string.split(';')
        self.name = params[0]
        self.opti_result = int(params[1])
        self.opti_path = params[2]
        self.matrix = self.from_txt_to_matrix(self.name)
        self.length = len(self.matrix)
        self.pheromone_matrix = []

    def init_pheromone_matrix(self, pheromone_level):
        for i in range(self.length):
            next_line = []
            for j in range(self.length):
                next_line.append(pheromone_level)
            self.pheromone_matrix.append(next_line)

    def decrease_pheromone(self, ro):
        # DAS
        for i in range(self.length):
            for j in range(self.length):
                self.pheromone_matrix[i][j] = ro * self.pheromone_matrix[i][j]

    def print_pheromone_matrix(self):
        print("####################################### Pheromone matrix #######################################")
        for i in range(self.length):
            print(self.pheromone_matrix[i])

    @staticmethod
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
