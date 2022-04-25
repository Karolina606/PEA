

class instance:
    def __init__(self, paramters_as_string: str):
        params = paramters_as_string.split(';')
        self.name = params[0]
        self.opti_result = int(params[1])
        self.opti_path = params[2]
        self.matrix = self.from_txt_to_matrix(self.name)
        self.length = len(self.matrix)

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
