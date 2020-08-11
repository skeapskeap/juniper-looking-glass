#https://www.juniper.net/documentation/en_US/junos-pyez/topics/task/program/junos-pyez-rpcs-executing.html
#https://blog.maxgraph.ru/2019/04/12/vyvod-xml-v-html-xml-to-html/ xml-to-html
from jnpr.junos import Device
from lxml import etree
from settings import JUN_IP, JUN_PORT, USERNAME, PASSWORD
from ncclient import manager  # https://ncclient.readthedocs.io/en/latest/

# command = 'show route protocol bgp detail 8.8.8.8'
# command = 'show route protocol bgp terse 8.8.8.8'
# command = 'show version'
# command = 'show bgp summary'


def connect(command):
    print(command)
    conn = manager.connect(host=JUN_IP,
                           port=JUN_PORT,
                           username=USERNAME,
                           password=PASSWORD,
                           timeout=10,
                           device_params={'name': 'junos'},
                           hostkey_verify=False)

    reply = conn.command(command, format='text')
    reply = reply.xpath('output')[0].text
    reply = reply.split('\n')
    return reply


def reply_to_query(command, ip):
    if command in ['udp traceroute', 'icmp-traceroute', 'ping']:
        if ip:
            return run_ping(ip)
        else:
            return("there's no ip")
    if command in ['show route protocol bgp detail', 'show route protocol bgp terse']:
        if ip:
            command = ' '.join([command, ip])
        else:
            return("there's no ip")
    return connect(command)


def run_ping(ping_IP, ping_count='4'):
    with Device(host=JUN_IP, user=USERNAME, password=PASSWORD, port=23) as dev:
        ping = dev.rpc.ping(count=ping_count, host=ping_IP)
        # ping = ping.xpath('target-host')[0].text  # возвращает кусок из xml
        ping = etree.tostring(ping, encoding='unicode')  # возвращает xml в виде строки
        print(type(ping))
    return ping


if __name__ == '__main__':
    #print(connect(command))
    print(run_ping('8.8.8.8', '2'))
