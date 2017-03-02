#coding:utf-8

from zabbix_api import ZabbixApi
from zabbix_api_setting import *

zabbix = ZabbixApi(ip=ZABBIX_SERVER_IP, user= ZABBIX_USER, password=ZABBIX_PASSWORD)

#set trigger status
triggerid = 13503

print zabbix.enable_trigger(triggerid)

#print zabbix.disable_trigger(triggerid)
