#coding:utf-8

from zabbix_api import ZabbixApi
from zabbix_api_setting import *

zabbix = ZabbixApi(ip=ZABBIX_SERVER_IP, user= ZABBIX_USER, password=ZABBIX_PASSWORD)

#create a mediatype and get mediatype list
print zabbix.create_mediatype()

#add media
print zabbix.add_media(1, 6)

#create a action
print zabbix.create_action("12", "7", "1", "6")
