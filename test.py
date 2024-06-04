from pysnmp.hlapi import *
from main import *


# 使用示例
switch_ip = '10.91.0.27'
community = 'public'

traffic_data = walk_snmp(switch_ip, '1.3.6.1.2.1.1.3')
print(traffic_data)
