from csv import reader
import numpy as np

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

def get_test_data(train_data, mumber_of_tests, distort):
    test_data = []
    for _ in range(mumber_of_tests):
        r_i = np.random.randint(0, len(train_data))
        base_pattern = np.array(train_data[r_i])
        noise = 1 * (np.random.random(base_pattern.shape) > distort)
        np.place(noise, noise == 0, -1)
        noisy_pattern = np.multiply(base_pattern, noise)
        test_data.append((base_pattern, noisy_pattern))
    return test_data;