from ncclient import manager  # https://ncclient.readthedocs.io/en/latest/
from settings import TRG_IP, TRG_PORT, USERNAME, PASSWORD


command = 'show bgp summary'


def connect(command):
    conn = manager.connect(host=TRG_IP,
            port=TRG_PORT,
            username=USERNAME,
            password=PASSWORD,
            timeout=10,
            device_params = {'name':'junos'},
            hostkey_verify=False)

    reply = conn.command(command, format='text')
    reply = reply .xpath('output')[0].text
    reply = reply.split('\n')
    return reply


if __name__ == '__main__':
    print(connect(command))
