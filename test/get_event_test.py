#coding:utf-8

from zabbix_api import ZabbixApi
from zabbix_api_setting import *

zabbix = ZabbixApi(ip=ZABBIX_SERVER_IP, user= ZABBIX_USER, password=ZABBIX_PASSWORD)

#get evetn test
time_from = "2015-11-25 17:00:00"
time_to = "2015-12-09 00:00:00"

#get evetn no condition
#zabbix.get_event()

#get event by time
#zabbix.get_event(time_from=time_from, time_to=time_to)

#get event by hostname and time
ret = zabbix.get_events(hostname="ubuntu-zabbix-test", time_from=time_from, time_to=time_to)

if ret['success']:
    for value in ret['results']:
        print value
else:
    print ret['error']
