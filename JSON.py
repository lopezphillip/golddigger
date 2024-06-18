# This is a wrapper for the json class.
#
# Handles both json string and json files.
# Supports pretty output for logging.
# Sanitized file reads of utf-8 data.


import json
import logging


class JSON:
    def __init__(self):
        pass

    @staticmethod
    def loads(json_text):  # takes json string and returns a dict
        return JSON.sanitize(json.loads(json_text))

    @staticmethod
    def dumps(json_data, sort=False, pretty=False):  # takes dict and returns json string
        if pretty:
            return json.dumps(json_data, indent=4, sort_keys=sort)
        else:
            return json.dumps(json_data, sort_keys=sort)

    @staticmethod
    def load(json_data):  # takes fp to a json file.  need?
        return json.load(json_data)

    @staticmethod
    def dump(data, json_file):  # takes dict and saves to file (?)
        return json.dump(data, json_file)

    # OUTPUT
    @staticmethod
    def data_output(data):
        logging.debug('data: %s', JSON.dumps(data, True, True))

    @staticmethod
    def json_output(data):
        JSON.data_output(data)

    @staticmethod
    def sanitize(data):
        # if isinstance(data, dict):
        #     return {JSON.sanitize(key): JSON.sanitize(value)
        #             for key, value in iter(data)}
        # elif isinstance(data, list):
        #     return [JSON.sanitize(element) for element in data]
        # else:
        return data

    @staticmethod
    def read_json(filename):
        try:
            with open(filename, 'r') as json_file:
                logging.debug("Reading JSON File: %s", filename)
                return JSON.load(json_file)  # JSON.loads(JSON.dumps(JSON.load(json_file)))
        except IOError:
            logging.warning("JSON File Read Error.  file:%s", filename)
        return None
