#!/usr/bin/env python3
import hid
import math


class Controller:
    def __init__(self, path):
        try:
            self.device = hid.device()
            self.device.open_path(path)
            self.last_thumpad_NS = None
            self.last_thumpad_WE = None
            self.last_button = None
        except IOError as ex:
            print(ex)
            print("Error initializing the microsoft device")

    def close(self):
        self.device.close()

    def read(self):
        return self.__input_translate(self.device.read(64))

    @staticmethod
    def __input_translate(data):
        """Given input data, should return some array of buttons currently pressed."""
        values = {0: 'Released', 1: 'A', 2: 'B', 4: 'X', 8: 'Y', 16: 'LT', 32: 'RT'}

        def return_button_value():
            if 'buttons' in output.keys():
                output["buttons"].append(values[int(math.pow(2, curr_number))])
            else:
                output['buttons'] = [values[int(math.pow(2, curr_number))]]

        def return_we(value):
            if value > 63:
                return 'E'
            elif value < 63:
                return 'W'
            else:
                return ''

        def return_ns(value):
            if value > 63:
                return 'S'
            elif value < 63:
                return 'N'
            else:
                return ''

        output = {}
        binary_buttons = bin(data[2])[2:]
        curr_number = 0
        for integer in binary_buttons[::-1]:
            if int(integer) == 1:
                return_button_value()
            curr_number += 1
        if 'buttons' not in output.keys():
            output['buttons'] = values[0]

        output['thumpad'] = [return_we(data[0]), return_ns(data[1])]
        return output

    @staticmethod
    def return_microsoft_paths():
        paths = []
        for d in hid.enumerate():
            if d['product_id'] == 39:
                paths.append(d['path'])
        return paths
