from csv import reader

def get_data(path):
    csv_list = load_csv(0, path)
    data_list = list()
    prev_entry_len = 0
    for entry in csv_list:
        if(prev_entry_len != 0 and len(entry) != prev_entry_len):
            raise ValueError('Wrong image data size in {0}. Was: {1}, Expected: {2}'.format(path, len(entry), prev_entry_len))
        data_list.append([int(numeric_string) for numeric_string in entry])
        prev_entry_len = len(entry)
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