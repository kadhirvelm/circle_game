#!/usr/bin/env python3
import hid


class Controller:

    def __init__(self, path):
        try:
            self.device = hid.device()
            self.device.open_path(path)
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
        letter = data[2]
        if letter == 1:
            return 'A'
        elif letter == 2:
            return 'B'
        elif letter == 4:
            return 'X'
        elif letter == 8:
            return 'Y'
        elif letter == 16:
            return 'LT'
        elif letter == 32:
            return 'RT'
        elif letter == 0:
            return 'Released'
        else:
            return 'Unknown'

    @staticmethod
    def return_microsoft_paths():
        paths = []
        for d in hid.enumerate():
            if d['product_id'] == 39:
                paths.append(d['path'])
        return paths
