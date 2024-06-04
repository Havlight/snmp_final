import time
from main import *
# 定义交换机的IP地址和SNMP社区字符串
SWITCH_IP = '10.91.0.27'
COMMUNITY_STRING = 'public'
POLL_INTERVAL = 60  # 轮询间隔时间（秒）

# 定义用于获取接口流量数据的OID
IF_IN_OCTETS_OID = '1.3.6.1.2.1.2.2.1.10'
IF_OUT_OCTETS_OID = '1.3.6.1.2.1.2.2.1.16'


# 定义函数以获取当前时间戳
def get_timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 初始化流量数据存储字典
traffic_data = {}

# 轮询交换机端口流量数据
while True:
    timestamp = get_timestamp()
    print(f"Polling at {timestamp}")

    # 获取输入字节数
    in_octets = walk_snmp(SWITCH_IP, IF_IN_OCTETS_OID)
    # 获取输出字节数
    out_octets = walk_snmp(SWITCH_IP, IF_OUT_OCTETS_OID)

    for entry in in_octets:
        port = entry['oid'].split('.')[-1]
        in_value = int(entry['value'])
        out_value = int(next(item for item in out_octets if item['oid'].endswith(port))['value'])

        if port not in traffic_data:
            traffic_data[port] = {'in': in_value, 'out': out_value, 'last_timestamp': timestamp}
        else:
            last_in = traffic_data[port]['in']
            last_out = traffic_data[port]['out']
            last_timestamp = traffic_data[port]['last_timestamp']

            # 计算流量变化
            in_diff = in_value - last_in
            out_diff = out_value - last_out
            interval = (time.mktime(time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")) -
                        time.mktime(time.strptime(last_timestamp, "%Y-%m-%d %H:%M:%S")))

            in_rate = in_diff / interval
            out_rate = out_diff / interval

            print(f"Port {port} - In: {in_rate} bytes/sec, Out: {out_rate} bytes/sec")

            # 更新流量数据
            traffic_data[port] = {'in': in_value, 'out': out_value, 'last_timestamp': timestamp}

    # 等待下一个轮询周期
    time.sleep(POLL_INTERVAL)
