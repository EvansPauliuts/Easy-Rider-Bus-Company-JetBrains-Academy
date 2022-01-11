# Write your awesome code here
import json
import re


class EasyRider:
    def __init__(self):
        self.data_key = [
            'stop_name',
            'stop_type',
            'a_time'
        ]
        self.data_obj = dict.fromkeys(self.data_key, 0)

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

    def start(self):
        self.show_field_json()

        data_num = sum([int(v) for v in self.data_obj.values()])
        print(f'Type and required field validation: {data_num} errors')

        for k, v in self.data_obj.items():
            print(f'{k}: {v}')


if __name__ == '__main__':
    easy_rider = EasyRider()
    easy_rider.start()
