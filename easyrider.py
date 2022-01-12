# Write your awesome code here
import json
import re
import collections


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
        self.count_bus_id = []
        self.bus_count = []
        self.data_all = []
        self.start_stops = set()
        self.finish_stops = set()
        self.transfer_stops = set()
        self.bus_lines_dict = collections.defaultdict(list)
        self.stops = set()
        self.times = dict()
        self.data_not_sorted = []

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

    def list_sorted(self):
        self.input_save_json()

        try:
            with open('data.json', 'r') as f:
                data_load = json.loads(json.load(f))
                self.data_all = sorted(data_load, key=lambda x: x['stop_name'])
        except FileNotFoundError:
            print('Not file found!')

    def list_not_sorted(self):
        self.input_save_json()

        try:
            with open('data.json', 'r') as f:
                data_load = json.loads(json.load(f))
                self.data_not_sorted = data_load
        except FileNotFoundError:
            print('Not file found!')

    def bus_stops_list(self):
        for b in self.data_all:
            self.bus_lines_dict[b['bus_id']].append(b['stop_type'])
            if b['stop_type'] == 'S':
                self.start_stops.add(b['stop_name'])
            if b['stop_type'] == 'F':
                self.finish_stops.add(b['stop_name'])
            if b['stop_name'] in self.stops:
                self.transfer_stops.add(b['stop_name'])
            self.stops.add(b['stop_name'])

    def invalid_stops(self):
        is_bool = True

        for b in self.bus_lines_dict:
            if ('S' not in self.bus_lines_dict[b] or 'F' not in self.bus_lines_dict[b]) and is_bool:
                print(f'There is no start or end stop for the line: {b}')
                is_bool = False

        return is_bool

    def special_stops(self):
        self.list_sorted()
        self.bus_stops_list()

        invalid_stop = self.invalid_stops()

        if invalid_stop:
            print(f'Start stops: {len(self.start_stops)} {list(sorted(self.start_stops))}')
            print(f'Transfer stops: {len(self.transfer_stops)} {list(sorted(self.transfer_stops))}')
            print(f'Finish stops: {len(self.finish_stops)} {list(sorted(self.finish_stops))}')

    def start(self):
        self.bus_count_result()

        print('Line names and number of stops:')

        for bus in self.bus_count:
            for k, v in bus:
                print(f'bus_id: {k}, stops: {v}')

    def checking_data_type(self):
        self.show_field_json()

        data_num = sum([int(v) for v in self.data_obj.values()])
        print(f'Type and required field validation: {data_num} errors')

        for k, v in self.data_obj.items():
            print(f'{k}: {v}')

    def invalid_times(self):
        val = False

        for b in self.data_not_sorted:
            try:
                self.times[b['bus_id']].append(b)
            except KeyError:
                self.times[b['bus_id']] = [b]

        print('Arrival time test:')

        for b, d in self.times.items():
            current_time = d[0]['a_time']
            for stop in d[1:]:
                next_time = stop['a_time']
                if current_time >= next_time:
                    print(f'bus_id line {b}: wrong time on station {stop["stop_name"]}')
                    val = True
                    break
                current_time = next_time

        if not val:
            print('OK')


if __name__ == '__main__':
    easy_rider = EasyRider()
    easy_rider.list_not_sorted()
    # easy_rider.special_stops()
    easy_rider.invalid_times()
