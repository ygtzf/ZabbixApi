ZabbixApi
####################

介绍
____________________
ZabbixApi封装了Zabbix server提供的部分API。

使用说明
___________________
1. 实例化类
   zabbix = ZabbixApi()

2. 调用相应方法
   列出所有事件:

::

    from ZabbixApi import ZabbixApi

    zabbix = ZabbixApi()

    time_from = "2015-11-25 17:00:00"
    time_to = "2015-12-02 00:00:00"

    eventlist = zabbix.get_event(hostname="ubuntu-zabbix-test", time_from=time_from, time_to=time_to)
    for value in eventlist:
    print value

    结果：
    {'eventid': u'551', 'status': 'OK', 'hostid': u'10139', 'severity': 'WARNING', 'ack': 'NO', 'duration': 174390.0362920761, 'host': u'ubuntu-zabbix-test', 'time': '2015-12-01 15:59:33', 'desc': u'Free disk space is less than 20% on volume /'}


接口说明
____________________

* get_event(hostname=None, time_from=None, time_to=None)

::

  hostname,time_from,time_to都为空时，列出所有host，所有时间的事件(具体能保存多长时间的事件还不太清楚);
  hostname参数为空时，输出某一时间段的所有host的事件;
  time_from,time_to为空时，列出某个host上的所有事件;
  返回值：
  返回列表，列表的每个元素是字典，字典包含如下key：
  eventid: 事件ID
  status： 事件的状态（OK/Problem)
  severity: 严重级别（Information/Warning/Average/High）
  ack: 是否被确认(Yes/No)
  duration: 持续时间(秒)
  host: 事件所在的主机名
  time: 发生时间
  desc: 事件描述


* set_host_status(hostname, status=1)

  设置某台主机是否被监控
  参数：status 0：监控 1：不监控(此函数参数默认为不监控，因为主机加入zabbix server的时候，默认是监控状态)

* event_ack(eventid)

  对某事件进行确认
  参数：eventid

* get_cpu(hostname, time_from=None, time_to=None)

  获取某台主机的CPU的负载
  time_from,time_to为空时，返回7天内的历史数据(历史数据默认保存90天)
  返回值：
  返回列表，列表的每个元素是字典，字典包含如下key：
  unit: 单位
  value: 监控数据
  time: 监控数据获取到的时间点

* get_memory(hostname, time_from=None, time_to=None)

  获取某台主机的可用内存
  time_from,time_to为空时，返回7天内的历史数据(历史数据默认保存90天)
  返回值同get_cpu()

* get_network_traffic_in(hostname, time_from=None, time_to=None)

  获取某台主机的入口流量(目前只检测eth0)
  time_from,time_to为空时，返回7天内的历史数据(历史数据默认保存90天)
  返回值同get_cpu()

* get_network_traffic_out(hostname, time_from=None, time_to=None)

  获取某台主机的出口流量(目前只检测eth0)
  time_from,time_to为空时，返回7天内的历史数据(历史数据默认保存90天)
  返回值同get_cpu()
