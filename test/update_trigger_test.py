#coding:utf-8

from zabbix_api import ZabbixApi
from zabbix_api_setting import *

zabbix = ZabbixApi(ip=ZABBIX_SERVER_IP, user= ZABBIX_USER, password=ZABBIX_PASSWORD)

triggerid = 13563

expression = "{zhanghui-0003:cpu_wait.avg(5m)}>55"
#ret = zabbix.update_trigger(triggerid, expression=expression, trigger_name="CPU-test", severity=2)
#ret = zabbix.update_trigger(triggerid)
ret = zabbix.update_trigger(triggerid, severity=1)

print ret['results']['triggerids']
