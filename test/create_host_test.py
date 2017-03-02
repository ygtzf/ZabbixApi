#coding:utf-8
from zabbix_api import ZabbixApi
from zabbix_api_setting import *

zabbix = ZabbixApi(ip=ZABBIX_SERVER_IP, user= ZABBIX_USER, password=ZABBIX_PASSWORD)

#create host  test
print zabbix.create_host("ubuntu-zabbix-test", "zabbix-test-group", "14.14.14.165")
