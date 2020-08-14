#https://www.juniper.net/documentation/en_US/junos-pyez/topics/task/program/junos-pyez-rpcs-executing.html
#https://blog.maxgraph.ru/2019/04/12/vyvod-xml-v-html-xml-to-html/ xml-to-html
from ncclient import manager  # https://ncclient.readthedocs.io/en/latest/
from ncclient import operations
from settings import JUN_IP, JUN_PORT, USERNAME, PASSWORD
import socket
import subprocess

COMMAND_LIST    = [('show bgp summary', 'bgp summary'),
                   ('show route terse protocol bgp', 'bgp route terse'),
                   ('show route detail protocol bgp', 'bgp route detail'),
                   ('mtr', 'mtr'),
                   ('ping', 'ping')]

NO_TARGET       = ['show bgp summary']
ANY_TARGET      = ['show route terse protocol bgp', 'show route detail protocol bgp']


class Input:

    def __init__(self, command, target=''):
        self.command = command
        self.target = target

    def validate(self):
        if self.command in NO_TARGET:  # для bgp summary не нужен target
            self.target = ''
            return True
        if not self.target:
            self.error_message = 'Please specify destination'
            return False
        if self.command in ANY_TARGET:  # для команд, которым нужен хоть какой-то target
            return True
        if self.valid_target():  # для команд, которым нужен корректный target
            return True
        else:
            self.error_message = 'Incorrect IP or hostname'
            return False

    def valid_target(self):
        try:
            self.target = socket.gethostbyname(self.target)  # если указан домен, проверяет резолвинг его в IP
            return True                                      # если указан ip, проверяет его корректность
        except socket.error:
            return False

    def query(self):
        return f'{self.command} {self.target}'

    def __repr__(self):
        return f'<Input: {self.command} {self.target}>'


def connect(command: str) -> list:
    conn = manager.connect(host=JUN_IP,
                           port=JUN_PORT,
                           username=USERNAME,
                           password=PASSWORD,
                           timeout=10,
                           device_params={'name': 'junos'},
                           hostkey_verify=False)

    try:
        reply = conn.command(command, format='text')
        reply = reply.xpath('output')[0].text
        reply = reply.split('\n')
    except operations.rpc.RPCError as rpc_error:
        reply = [rpc_error.message]
    except (IndexError, operations.errors.TimeoutExpiredError):
        reply = ['Something went wrong. Try another prefix']
    return reply


def reply_to_query(command, target):
    input = Input(command, target)
    if not input.validate():
        return False, input.error_message

    query = input.query()
    if command == 'ping':
        return ping(target), query
    elif command == 'mtr':
        return mtr(target), query
    else:
        return connect(query), query


def mtr(target_host: str) -> str:
    try:
        result = subprocess.check_output(['mtr', '-oLSDW', target_host, '-r', '-c 10'], universal_newlines=True)
        return result
    except FileNotFoundError:
        return False


def ping(target_host: str) -> str:
    try:
        result = subprocess.check_output(['ping', target_host, '-c 4', '-n'], universal_newlines=True, stderr=subprocess.STDOUT)
        return result
    except subprocess.CalledProcessError:
        return False


if __name__ == '__main__':
    print(connect('show version'))
