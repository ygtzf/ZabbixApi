#coding:utf-8

from zabbix_api import ZabbixApi
from zabbix_api_setting import *

zabbix = ZabbixApi(ip=ZABBIX_SERVER_IP, user= ZABBIX_USER, password=ZABBIX_PASSWORD)

host = "zhanghui-0003"
template = "eonfabric"
time_from = "2015-12-11 13:00:00"
time_to = "2015-12-11 13:10:00"

#ret = zabbix.list_items(hostname="ygt")
ret = zabbix.list_items(hostname=host)
#ret = zabbix.list_items(hostname=host,templatename=template)
#ret = zabbix.list_items(templatename=template)
if ret['success']:
    for item in ret['results']:
        print item
else:
    print ret['error']

itemid = 23707

#get history data
ret = zabbix.get_item_data(host, itemid, time_from, time_to)

if ret['success']:
    for var in ret['results']:
        print var
else:
    print ret['error']
