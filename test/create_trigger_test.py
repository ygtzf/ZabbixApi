#coding:utf-8

from zabbix_api import ZabbixApi
from zabbix_api_setting import *

zabbix = ZabbixApi(ip=ZABBIX_SERVER_IP, user= ZABBIX_USER, password=ZABBIX_PASSWORD)

host = "ubuntu-zabbix-test"

ret = zabbix.list_items(hostname=host)
if ret['success']:
    for item in ret['results']:
        print item
else:
    print ret['error']


expression = "{ubuntu-zabbix-test:system.cpu.util[,iowait].avg(5m)}>20"
trigger_name = "CPU load too high"

"""
Severity possible values are:
    0 - (default) not classified;
    1 - information;
    2 - warning;
    3 - average;
    4 - high;
    5 - disaster.
"""
severity = 4

ret = zabbix.create_trigger(trigger_name, severity, expression)

if ret['success']:
    print ret['results']['triggerids']
else:
    print ret['error']
