from pysnmp.hlapi import *
from pysnmp.proto.rfc1155 import ObjectName
from rich.console import Console
from rich.table import Table
from main import *


def get_port_state():
    oid = '.1.3.6.1.2.1.2.2.1.8'
    target = '10.91.0.27'
    return walk_snmp(target, oid)


def get_port_expect_state():
    oid = '.1.3.6.1.2.1.2.2.1.7'
    target = '10.91.0.27'
    return walk_snmp(target, oid)


def port_error():
    port_expect = get_port_expect_state()
    port_operate = get_port_state()
    port_status = []
    for i in range(len(port_expect)):
        port_info = {}
        port_info['port'] = i + 1
        if port_expect[i]['value'] != port_operate[i]['value']:
            port_info["status"] = "warning"
        else:
            port_info["status"] = "safe"

        port_status.append(port_info)

    return port_status


if __name__ == "__main__":
    print(get_port_state())
    print(get_port_expect_state())
    print(port_error())
