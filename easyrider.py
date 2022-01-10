# Write your awesome code here
import json


class EasyRider:
    def __init__(self):
        self.data_key = [
            'bus_id',
            'stop_id',
            'stop_name',
            'next_stop',
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
                            if v in ['bus_id', 'stop_id']:
                                if not isinstance(data[v], int):
                                    self.data_obj[v] += 1
                            if v in ['stop_name', 'next_stop', 'a_time']:
                                if isinstance(data[v], str):
                                    if len(data[v]) == 0:
                                        self.data_obj[v] += 1
                            if v in ['next_stop']:
                                if isinstance(data[v], str):
                                    self.data_obj[v] += 1
                            if v in ['stop_type', 'a_time', 'stop_name']:
                                if isinstance(data[v], (int, float)):
                                    self.data_obj[v] += 1
                            if v in ['stop_type']:
                                if isinstance(data[v], str):
                                    if len(data[v]) == 2:
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
