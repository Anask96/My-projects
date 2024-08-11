from collections import defaultdict
import threading
import csv
import queue

class Storage:
    
    lock = threading.Lock()
    lock_group = threading.Lock()
    lock_group_number = threading.Lock()
    Lock_alarm = threading.Lock()

    tokens = defaultdict(list)
    group = defaultdict(list)
    alarm = defaultdict(str)

    group_number = 0
    group_num_used = False

    output_buffer = queue.Queue()
    data_queue = queue.Queue()

    headers_csv = ["tokenId", "Bat", "Company", "Roll", "Group", "Time", "Missing information", "Latest Rssi"]
    headers_gui = ["ID", "Battery", "Company", "Roll", "Group", "Problems"]

    def __init__(self):
        pass

    def store_token(self, token, data):
        with self.lock:
            self.tokens[token] = data

    def update_stored_token(self, token, index, data):
        with self.lock:
            self.tokens[token][index] = data

    def check_token_exist(self, token):
        with self.lock:
            if token in self.tokens:
                return True
            return False
    
    def get_total_tokens(self):
        with self.lock:
            return len(self.tokens)

    def get_value_of_key(self, token):
        with self.lock:
            return self.tokens[token]

    def falg_token(self, token):
        with self.lock:
            self.tokens[token][5] = 1

    def store_group_token(self, token, data):
        with self.lock_group:
            self.group[token] = data


    def get_total_group_tokens(self):
        with self.lock_group:
            return len(self.group)

    def update_stored_token_in_group(self, token, index, data):
        with self.lock_group:
            self.group[token][index] = data

    def reset_group(self):
        with self.lock_group:
            with self.lock:
                for key, value in self.group.items():
                    self.tokens[key][3] = value[3]
            self.group.clear()
            self.increment_group_number()

    def group_number_already_assigned(self, token):
        with self.lock:
            if self.tokens[token][3] != -1: 
                return True
            return False

    def get_group_number(self):
        with self.lock_group_number:
            self.group_num_used = True
            return self.group_number

    def increment_group_number(self):
        with self.lock_group_number:
            if self.group_num_used == True:
                self.group_number += 1
                self.group_num_used = False

    def add_alarm(self, id, message):
        with self.Lock_alarm:
            self.alarm[id] = message

    def remove_alarm(self, id):
        with self.Lock_alarm:
            if id in self.alarm:
                del self.alarm[id]


    def download_data(self):
        regular_dict = dict(self.tokens)
        # Step 2: Write to CSV
        with open('output.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            
            # Write the header row
            writer.writerow(self.headers_csv)

            # Write the data rows
            for key, token_set in regular_dict.items():
                row = [key] + list(token_set)
                writer.writerow(row)

        print("CSV file 'output.csv' created successfully.")
