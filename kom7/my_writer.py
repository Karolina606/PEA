import csv


class my_writer:
    def __init__(self, out_file, tsp_aco_param):
        self.tsp_aco_param = tsp_aco_param
        self.out_file = out_file

    def simple_write_to_csv(self, tsp_result, tsp_opti, tsp_error=0):
        with open(self.out_file, 'a') as f:
            f.write(str(tsp_result[0]) + ';' +
                    str(tsp_result[1]) + ';' +
                    str(tsp_result[2]).replace('.', ',') + ';' +
                    str(tsp_result[3]).replace('.', ',') + ';' +
                    str(tsp_result[4]).replace('.', ',') + ';' +
                    str(tsp_result[5]).replace('.', ',') + ';' +
                    tsp_opti + ';' +
                    str(tsp_error) + ';'
                    + str(self.tsp_aco_param[0]).replace('.', ',') + ';'
                    + str(self.tsp_aco_param[1]).replace('.', ',') + ';'
                    + str(self.tsp_aco_param[2]).replace('.', ',') + ';'
                    + str(self.tsp_aco_param[3]).replace('.', ',') + ';'
                    + str(self.tsp_aco_param[4]).replace('.', ',') + ';'
                    + str(self.tsp_aco_param[5]).replace('.', ',') + ';'
                    + str(self.tsp_aco_param[6]).replace('.', ',') + ';' +
                    '\n')

    def header_write_to_csv(self, tsp_result, tsp_opti):
        with open(self.out_file, 'a') as f:
            f.write(str(tsp_result[0]) + ';' +
                    str(tsp_result[1]) + ';' +
                    str(tsp_result[2]).replace('.', ',') + ';' +
                    str(tsp_result[3]).replace('.', ',') + ';' +
                    str(tsp_result[4]).replace('.', ',') + ';' +
                    str(tsp_result[5]).replace('.', ',') + ';' +
                    tsp_opti + ';'
                    + str('memory') + ';'
                    + str('alfa') + ';'
                    + str('beta') + ';'
                    + str('ro') + ';'
                    + str('m') + ';'
                    + str('pher_distribution') + ';'
                    + str('heuristic') + ';'
                    + str('iterations') +
                    '\n')
