#coding:utf-8

from zabbix_api import ZabbixApi
from zabbix_api_setting import *

zabbix = ZabbixApi(ip=ZABBIX_SERVER_IP, user= ZABBIX_USER, password=ZABBIX_PASSWORD)

#set zabbix agent host status, 0:enable 1:disable
print zabbix.set_host_status("ubuntu-zabbix-test", 0)
