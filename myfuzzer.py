__author__ = 'sf'

import argparse
'''
from Mutators import mutator
from Coverager import coverager
from Support import basic_operation
from Support import db_operation
from Support import logger
'''
parser = argparse.ArgumentParser(description="process some arguments")

parser.add_argument('-r', '--run_model', choices=['online', 'offline'],
                    default='online', help='run task model: online or offline')

group_online = parser.add_argument_group("Arguments of online model")
group_online.add_argument('-u', '--user_id', type=int, default=15, help='identify which user')
group_online.add_argument('-t', '--task_id', type=int, help='identify which task')
group_online.add_argument('-v', '--vm_id', type=int, help='identify the vm id')
group_online.add_argument('-m', '--master_ip', help='master ip')
group_online.add_argument('-d', '--db', action='store_true', help='whether db')

parser.add_argument('-skip', '--skip_deterministic', action='store_true',
                    help='to skip the deterministic fuzzing like BITFLIP or ARITHMETIC INC/DEC')
parser.add_argument('-p', '--parallel', action='store_true', default=True, help='run task parallel')
parser.add_argument('-s', '--sync', action="store_true", help="identify if support sync")

args = parser.parse_args()
print parser.parse_args()

def parse_options():
    """
    Read options from config file or input arguments
    :return:
    """

def parse_config_file():
    """
    Initialize arguments from config file.
    :return:
    """

def set_modules():
    """
    Set fuzzing modules according config file or input arguments.
    set mutators/guider models/coverage type/analyzer
    :return:
    """