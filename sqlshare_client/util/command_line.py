import argparse
import re
import os


def get_oauth_values():
    parser = argparse.ArgumentParser()
    parser.add_argument('--credentials')

    values = vars(parser.parse_args())

    data = {}
    if values["credentials"]:
        with open(values['credentials']) as config_file:
            for line in config_file:
                if re.match('^#', line):
                    continue

                key, value = re.match('(.*?)\s*:\s*(.*)\n*', line).groups()
                data[key] = value

    keys = data.keys()
    for key in keys:
        data[key.lower()] = data[key]

    data['id'] = data['oauth_id']
    data['secret'] = data['oauth_secret']

    return data
