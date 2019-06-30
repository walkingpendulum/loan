import argparse

import yaml
import models


def arg_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', dest='config_path', help='path to configuration file', required=True)

    return parser


def parse_config(config_path):
    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.BaseLoader)

    return config


def parse_period(period_str):
    """Parses period in months (m, y modifiers allowed) and returns value in months"""
    translations = str.maketrans({'m': '*1+', 'y': '*12+'})
    allowed = '0123456789+-*/.'
    period_str = ''.join(filter(allowed.__contains__, str.translate(period_str + '+0', translations)))
    return eval(period_str)


def parse_extra_payments(payments):
    return [models.Payment(**params) for params in payments]
