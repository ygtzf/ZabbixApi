ZabbixApi
####################

介绍
____________________
ZabbixApi封装了Zabbix server提供的部分API。

使用说明
___________________
1. 实例化类
   zabbix = ZabbixApi()

2. 调用相应方法:

::

   列出所有事件:

    from ZabbixApi import ZabbixApi
    url = http://10.6.14.212/zabbix
    zabbix = ZabbixApi(url, user="admin", password="zabbix")

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

::

  设置某台主机是否被监控
  参数：status 0：监控 1：不监控(此函数参数默认为不监控，因为主机加入zabbix server的时候，默认是监控状态)

* event_ack(eventid)

::

  对某事件进行确认
  参数：eventid

* get_cpu(hostname, time_from=None, time_to=None)

::

  获取某台主机的CPU的负载
  time_from,time_to为空时，返回7天内的历史数据(历史数据默认保存90天)
  返回值：
  返回列表，列表的每个元素是字典，字典包含如下key：
  unit: 单位
  value: 监控数据
  time: 监控数据获取到的时间点

* get_memory(hostname, time_from=None, time_to=None)

::

  获取某台主机的可用内存
  time_from,time_to为空时，返回7天内的历史数据(历史数据默认保存90天)
  返回值同get_cpu()

* get_network_traffic_in(hostname, time_from=None, time_to=None)

::

  获取某台主机的入口流量(目前只检测eth0)
  time_from,time_to为空时，返回7天内的历史数据(历史数据默认保存90天)
  返回值同get_cpu()

* get_network_traffic_out(hostname, time_from=None, time_to=None)

::

  获取某台主机的出口流量(目前只检测eth0)
  time_from,time_to为空时，返回7天内的历史数据(历史数据默认保存90天)
  返回值同get_cpu()

* create_trigger(trigger_name, severity, **expression_kwargs)

::

  创建一个trigger
  trigger_name: 自定义trigger的名称
  severity: trigger的严重级别，包括以下值：
    0 - (default) not classified;
    1 - information;
    2 - warning;
    3 - average;
    4 - high;
    5 - disaster
  expression_kwargs: 表达式的字典,有以下key：
    "hostname"
    "function_name": 函数名称（last、avg、diff、nodata）
    "item_key":  从get_items接口的返回值中取的。
    "param":  时间值，作为function的参数
    "operator":  比较符（>/</=/#(不等于)）
    "threshold": 阈值
  返回值：
  返回triggerid


* update_trigger(triggerid, **expression_kwargs)

::
  更新某个trigger
  参数需要triggerid和表达式，表达式同create_trigger中的参数expression
  返回值：
  返回triggerid

* list_trigger(hostname)

::

  获取某台主机的trigger列表
  返回值:
  返回列表，列表的每个元素是字典，字典包含如下key：
  "function" : 函数名
  "name" : trigger 名称
  "enabled" : trigger状态（bool值）
  "triggerid" : triggerid
  "threshold" : 阈值
  "time_param" : function函数的参数
  "item_key" : item key
  "host" : hostname
  "severity" : 严重级别

* list_items(hostname)

::

  获取某台主机上的item列表
  返回值：
  "itemid" : itemid
  "units" : 单位
  "key_" : item key (这个将在创建triiger的时候用到)
  "name" : item 名称
