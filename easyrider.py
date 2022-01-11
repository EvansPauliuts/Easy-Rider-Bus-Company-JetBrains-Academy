# Write your awesome code here
import json
import re
import collections


class EasyRider:
    def __init__(self):
        self.data_key = [
            'bus_id',
            'stop_name',
            'stop_type',
            'a_time'
        ]
        self.data_obj = dict.fromkeys(self.data_key, 0)
        self.count_bus_id = []
        self.bus_count = []

    def input_save_json(self):
        name_data = input()

        try:
            with open('data.json', 'w', encoding='utf-8') as f:
                data = json.dumps(name_data)
                f.write(data)
        except FileNotFoundError:
            print('Not file found!')

    def show_field_json(self):
        self.input_save_json()

        try:
            with open('data.json', 'r') as f:
                data_load = json.loads(json.load(f))

                for data in data_load:
                    for v in data:
                        if v in self.data_key:
                            if v in ['a_time']:
                                if not bool(re.match(r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$', data[v])):
                                    self.data_obj[v] += 1
                            if v in ['stop_type']:
                                if isinstance(data[v], str):
                                    if not bool(re.match(r'^(S|F|O|^$)$', data[v])):
                                        self.data_obj[v] += 1
                            if v in ['stop_name']:
                                pattern = r'[A-Z]\w+\s?\w+?\s(Road|Avenue|Boulevard|Street)$'
                                if not bool(re.match(pattern, data[v])):
                                    self.data_obj[v] += 1

        except FileNotFoundError:
            print('Not file found!')

    def find_bus_id_list(self):
        self.input_save_json()

        try:
            with open('data.json', 'r') as f:
                data_load = json.loads(json.load(f))

                for data in data_load:
                    self.count_bus_id.append(data['bus_id'])
        except FileNotFoundError:
            print('Not file found!')

    def bus_count_result(self):
        self.find_bus_id_list()

        self.bus_count.append(
            [(item, count) for item, count in collections.Counter(self.count_bus_id).items() if count > 1]
        )

    def start(self):
        self.bus_count_result()

        print('Line names and number of stops:')

        for bus in self.bus_count:
            for k, v in bus:
                print(f'bus_id: {k}, stops: {v}')


if __name__ == '__main__':
    easy_rider = EasyRider()
    easy_rider.start()
