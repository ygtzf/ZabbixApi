#coding:utf-8

from zabbix_api import ZabbixApi
from zabbix_api_setting import *

zabbix = ZabbixApi(ip=ZABBIX_SERVER_IP, user= ZABBIX_USER, password=ZABBIX_PASSWORD)

#delete trigger
triggerid = [13569,13568]
#triggerid = 13567

print zabbix.delete_trigger(triggerid)
