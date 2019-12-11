import yaml
import logging
import json
import os
import sys
import xmltodict
import requests

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)


def load_rss(url):
    logging.info('Request URL: {}'.format(url))
    try:
        r = requests.request('GET', url)
        data = r.content
        logging.debug('Response data: {}'.format(data))
        if r.status_code is 200:
            logging.info('successful: {}'.format(url))
        else:
            logging.error('Error message: {}'.format(data['error']['title']))
            sys.exit()
        return xmltodict.parse(data)
    except requests.exceptions.RequestException as e:
        logging.error(e)
        sys.exit()

def load_configure(file):
    logging.info('Loading {} configuration...'.format(file))
    return parse_yaml('configure/{}.yaml'.format(file))

def parse_yaml(file):
    try:
        return yaml.load(open(file, 'r'))
    except yaml.YAMLError as exc:
        logging.exception('Error while parsing YAML file:')
        if hasattr(exc, 'problem_mark'):
            if exc.context is not None:
                logging.warning('  parser says\n' + str(exc.problem_mark) + '\n  ' +
                                str(exc.problem) + ' ' + str(exc.context) +
                                '\nPlease correct data and retry.')
            else:
                logging.warning('  parser says\n' + str(exc.problem_mark) + '\n  ' +
                                str(exc.problem) + '\nPlease correct data and retry.')
        else:
            logging.warning('Something went wrong while parsing yaml file')
        return


def save_to_json(folder, filename, data):
    with open('{}/{}.json'.format(folder, filename), 'w') as f:
        f.write(json_dump(data))
        f.close()
    logging.info('Saved file: {}.json'.format(filename))


def json_dump(data):
    return json.dumps(data, indent=4, sort_keys=True)
