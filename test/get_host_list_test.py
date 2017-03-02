#coding:utf-8

from zabbix_api import ZabbixApi
from zabbix_api_setting import *

zabbix = ZabbixApi(ip=ZABBIX_SERVER_IP, user= ZABBIX_USER, password=ZABBIX_PASSWORD)

#get host list
ret = zabbix.get_hosts()

if ret['success']:
    for host in ret['results']:
        print host
else:
    print ret['error']
