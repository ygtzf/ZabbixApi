#coding:utf-8

from zabbix_api import ZabbixApi
from zabbix_api_setting import *

zabbix = ZabbixApi(ip=ZABBIX_SERVER_IP, user= ZABBIX_USER, password=ZABBIX_PASSWORD)

host = "ubuntu-zabbix-test"

ret = zabbix.list_triggers(hostname=host)

if ret['success']:
    for var in ret['results']:
        print var
else:
    print ret['error']
