from csv import reader

def get_data(path):
    csv_list = load_csv(0, path)
    data_list = list()
    for entry in csv_list:
        data_list.append([int(numeric_string) for numeric_string in entry])
    return data_list

def load_csv(start_index, path):
    dataset = list()
    row_number = -1
    counter = 0
    with open(path, 'r') as file:
        csv_reader = reader(file)
        for row in csv_reader:
            row_number += 1
            if not row or start_index > row_number:
                continue
            else:
                counter += 1
                dataset.append(row)
    return dataset