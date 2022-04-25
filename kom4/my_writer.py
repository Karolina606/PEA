import csv


class my_writer:
    def __init__(self, out_file, tsp_sa_param):
        self.tsp_sa_param = tsp_sa_param
        self.out_file = out_file

    def simple_write_to_csv(self, tsp_result, tsp_opti, tsp_error=0):
        with open(self.out_file, 'a') as f:
            f.write(str(tsp_result[0]) + ';' +
                    str(tsp_result[1]) + ';' +
                    str(tsp_result[2]).replace('.', ',') + ';' +
                    str(tsp_result[3]).replace('.', ',') + ';' +
                    str(tsp_result[4]).replace('.', ',') + ';' +
                    tsp_opti + ';' +
                    str(tsp_error) + ';'
                    + str(self.tsp_sa_param[0]) + ';'
                    + str(self.tsp_sa_param[1]) + ';'
                    + str(self.tsp_sa_param[2]) + ';'
                    + str(self.tsp_sa_param[3]) + ';'
                    + str(self.tsp_sa_param[4]) + ';'
                    + str(self.tsp_sa_param[5]) + ';' +
                    '\n')
