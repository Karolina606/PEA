import csv


def simple_write_to_csv(out_file_name, tsp_result):
    with open(out_file_name, 'a') as f:
        f.write(str(tsp_result[0]) + ';' + str(tsp_result[1]) + ';' + str(tsp_result[2]).replace('.', ',') + ';'
                + str(tsp_result[3]) + ';\n')


def write_to_csv(out_file_name, tsp_result):
    out_file = open(out_file_name, 'w', newline='')
    headers = ['instance_size', 'result', 'time', 'path']
    writer = csv.DictWriter(out_file, delimiter=';', lineterminator='\n', fieldnames=headers)

    writer.writeheader()

    for i in range(len(tsp_result)):
        writer.writerow({'instance_size': tsp_result[0],
                         'result': tsp_result[1],
                         'time': str(tsp_result[2]).replace('.', ','),
                         'path': str(tsp_result[3])})

    out_file.close()


def write_to_csv2(out_file_name, times, memory):
    out_file = open(out_file_name, 'w', newline='')
    headers = ['instance_size', 'time', 'memory']
    writer = csv.DictWriter(out_file, delimiter=';', lineterminator='\n', fieldnames=headers)

    writer.writeheader()

    for i in range(len(times)):
        writer.writerow({'instance_size': list(times.keys())[i],
                         'time': str(list(times.values())[i]).replace('.', ','),
                         'memory': str(list(memory.values())[i]).replace('.', ',')})

    out_file.close()

