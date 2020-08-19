#https://www.juniper.net/documentation/en_US/junos-pyez/topics/task/program/junos-pyez-rpcs-executing.html
#https://blog.maxgraph.ru/2019/04/12/vyvod-xml-v-html-xml-to-html/ xml-to-html
from lg_app.config import COMMAND_MAPPING, IGNORE_TARGET, ANY_TARGET, LINUX_COMMAND
from ncclient import manager  # https://ncclient.readthedocs.io/en/latest/
from ncclient import operations
from lg_app.jun_params import JUN_IP, JUN_PORT, USERNAME, PASSWORD
import socket
import subprocess


def reply_to_query(command, target):
    input = Input(command, target)

    if not input.validate():
        return False, input.error_message
    if input.command in LINUX_COMMAND:
        query = input.linux_command()
        return linux_cli(query), ' '.join(query)
    else:
        query = input.jun_query()
        return connect(query), query


def linux_cli(command: list) -> list:
    try:
        result = subprocess.check_output(command, universal_newlines=True, stderr=subprocess.STDOUT)
    except FileNotFoundError as no_file:
        result = f'{no_file.filename}: {no_file.strerror}'
    except subprocess.CalledProcessError as proc_err:
        result = proc_err.output

    return [result]


def connect(command: str) -> list:
    try:
        connect = manager.connect(host=JUN_IP,
                                  port=JUN_PORT,
                                  username=USERNAME,
                                  password=PASSWORD,
                                  timeout=10,
                                  device_params={'name': 'junos'},
                                  hostkey_verify=False)
    except OSError as os_error:                                                 # Когда не подключается к джуниперу =\
        reply = f'[Errno {os_error.errno}] {os_error.strerror}'
        return [reply]

    try:
        reply = connect.command(command, format='text')
        reply = reply.xpath('output')[0].text
        reply = reply.split('\n')
    except operations.rpc.RPCError as rpc_error:                    # Когда джуниперу не нравится кривой запрос
        reply = [rpc_error.message]
    except (IndexError, operations.errors.TimeoutExpiredError):     # Когда джунипер ответил "ничего" или не ответил
        reply = ['Something went wrong. Try another prefix']
    return reply


class Input:

    def __init__(self, command, target=''):
        self.command = COMMAND_MAPPING.get(command)
        self.target = target

    def validate(self):
        if self.command in IGNORE_TARGET:                       # для bgp summary не нужен target
            self.target = ''
            return True
        if not self.target:
            self.error_message = 'Please specify destination'
            return False
        if self.command in ANY_TARGET:                          # для команд, которым нужен хоть какой-то target
            return True
        if self.valid_target():                                 # для команд, которым нужен корректный target
            return True
        else:
            self.error_message = 'Incorrect IP or hostname'
            return False

    def valid_target(self):
        try:
            self.target = socket.gethostbyname(self.target)     # если указан домен, проверяет резолвинг его в IP
            return True                                         # если указан ip, проверяет его корректность
        except socket.error:
            return False

    def jun_query(self) -> str:
        return f'{self.command} {self.target}'

    def linux_command(self) -> list:
        return self.command + [self.target]

    def __repr__(self):
        return f'<Input: {self.command} {self.target}>'


if __name__ == '__main__':
    print(connect('show version'))
