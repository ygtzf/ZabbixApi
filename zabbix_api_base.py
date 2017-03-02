# coding:utf-8

import sys

import utils
from utils import CustomTime
from http_request import HttpRequest

event_status = ['OK', 'PROBLEM']
event_ack = ['NO', 'YES']
trigger_severity = ['NOT CLASSIFIED', 'INFORMATION', 'WARNING', 'AVERAGE', 'HIGH', 'DISASTER']


class ZabbixApiBase(HttpRequest):
    """
    Zabbix API class, include all the helpful API
    """

    def __init__(self, ip="127.0.0.1", port="80", user="admin", password="zabbix"):
        """
        desc:
            get the auth id, this auth_id will use in all operations
        """

        self.url = "http://" + ip + ":" + port + "/zabbix/api_jsonrpc.php"
        self.auth = None
        self.user = user
        self.password = password
        self.auth = self.login()

    def login(self):
        """
        desc:
            login zabbix server
        param:
            user: zabbix server account
            password: zabbix server password
        return:
            a avaiable auth id
        """

        use_auth = False
        auth = None
        method = 'user.login'
        param ={
            'user' : self.user,
            'password' : self.password,
        }

        auth = self.do_request(method, param)
        return auth['results']

    def _get_event(self,hostid=None, time_from=None, time_to=None):
        """
        desc:
            event list
        param:
            hostid: Zabbix agent hostid (if list event by hostname)
            time_from: start time (if list event by time)
            time_to: stop time (if list event by time)
        return:
            event list
        """

        event_list = []

        method = 'event.get'
        param = {
            'output' : 'extend',
            'hostids': hostid,
            'time_from': time_from,
            'time_till': time_to,
        }

        event = self.do_request(method, param)


        c_time = CustomTime()

        for value in event['results']:
            event_dict = {}
            event_dict['eventid'] = value['eventid']
            event_dict['time'] = c_time.time_format(int(value['clock']))
            event_dict['status'] = event_status[ int(value['value']) ]
            event_dict['ack'] = event_ack[ int(value['acknowledged']) ]
            event_dict['duration'] = c_time.dur_time(int(value['clock']))


            trigger = self.get_trigger_base(triggerid=value['objectid'])

            for var in trigger['results']:
                event_dict['desc'] = var['description']
                event_dict['severity'] = trigger_severity[ int(var['priority']) ]


            host_name = self.get_host_base(triggerids = value['objectid'])

            if not host_name:
                continue

            for key in host_name:
                event_dict['host'] = key['host']
                event_dict['hostid'] = key['hostid']


            event_list.append(event_dict)

        return utils.return_format(event_list)

    def get_trigger_base(self, triggerid=None, hostid=None):
        """
        desc:
            get trigger list
        param:
            triggerid if get trigger name by id
        return:
            trigger description and trigger priority
        """

        method = 'trigger.get'
        param = {
            'triggerids' : triggerid,
            'hostids': hostid,
            'output' : [
                'extend',
                'description',
                'priority',
                'hostid',
                'status',
                'triggerid',
                'expression',
                'functions'
            ],
            'selectFunctions': 'extend',
        }

        return self.do_request(method, param)


    def get_host_base(self, triggerids=None):
        """
        desc:
            get Zabbix agent host info
        param:
            triggerid if get host by triigerid
        return:
            Zabbix agent host name and host id
        """

        method = 'host.get'
        param = {
            'triggerids' : triggerids,
            'output' : [
                'host',
                'hostid',
                'name'
            ],
        }

        host = self.do_request(method, param)
        return host['results']

    def get_hostid(self, hostname):
        if hostname:
            host = self.get_host_base()
            for key in host:
                if hostname == key['host']:
                    return key['hostid']

    def create_host_base(self, hostname, group, templates, ip, port="10050", dns=""):
        """
        desc:
            create Zabbix agent host from Zabbix server
        param:
            hostname: Zabbix agent hostname
            group: Zabbix group name
            templates: template Zabbix agent will load
            ip: agent host's ip
            port: agent host zabbix-agentd service port
        return:
            the host id
        """

        method = "host.create"
        param = {
            "host" : hostname,
            "interfaces" : [
                {
                    "type" : 1,
                    "main" : 1,
                    "useip" :  1,
                    "ip" : ip,
                    "dns" : dns,
                    "port" : port,
                }
            ],
            "groups" : [
                {
                    "groupid" : group,
                }
            ],
            "templates" : [
                {
                    "templateid" : templates,
                }
            ],
        }

        host_id = self.do_request(method, param)
        return host_id['results']


    def get_host_group(self):
        """
        desc:
            Zabbix host group list
        param:
            no
        return:
            host group's id and group name
        """

        method = "hostgroup.get"
        param = {
            "output" : [
                "groupid",
                "name"
            ]
        }

        host_group = self.do_request(method, param)
        return host_group['results']

    def get_hostgroup_id(self, hostgroup_name):
        """
        desc:
            get host group id by hostgroup name
        param:
            host group name
        return:
            the host group id
        """

        host_group = self.get_host_group()

        for key in host_group:
            if key['name'] == hostgroup_name :
                return key['groupid']

        return None

    def get_template(self):
        """
        desc:
            template list
        return:
            template id. template name.
        """

        method = "template.get"
        param = {
            "output" : [
                "host",
                "templateid",
                "name"
            ]
        }

        host_group = self.do_request(method, param)
        return host_group['results']

    def get_template_id(self, template_name):
        """
        desc:
            get template id by template name
        param:
            template name
        return:
            tempalte id
        """

        template = self.get_template()

        for key in template:
            if key['name'] == template_name :
                return key['templateid']

    def del_host(self, hostid):
        """
        desc:
            delete a host by hostid
        """

        method = 'host.delete'
        param = [hostid]

        return self.do_request(method, param)

    def create_host_group(self, host_group_name):
        """
        desc:
            create hostgroup
        """

        method = "hostgroup.create"
        param = {
            "name" : host_group_name,
        }

        self.do_request(method, param)

        return self.get_hostgroup_id(host_group_name)

    def del_host_group(self, hostgroup_id):
        """
        desc:
            delete hostgroup by hostgroup id
        """

        method = "hostgroup.delete"
        param = [hostgroup_id]

        self.do_request(method, param)

    def create_host(self, hostname, groupname, ip):
        """
        desc:
            create host API
        param:
            agent hostname, agent hostgroup name. agent host ip
        """

        templateid = self.get_template_id("Template OS Linux")

        groupid = self.get_hostgroup_id(groupname)
        if groupid is None:
            groupid = self.create_host_group(groupname)

        host = self.get_host_base()
        for var in host:
            if hostname == var['host']:
                print "The host %s is already exists" % hostname
                return

        self.create_host_base(hostname, groupid, templateid, ip)


    def create_mediatype(self, name="post-message", type_num=1):
        """
        desc:
            create mediatype, default create a cunstom mediatype
        """

        method = "mediatype.create"
        param = {
            "description": name,
            "type": type_num,
            "exec_path": "mail.py",
        }

        return self.do_request(method, param)

    def get_mediatype(self, name=None):
        """
        desc:
            get mediatype or get mediatype id by name
        """

        method = "mediatype.get"
        param ={
            "output": "extend",
            "filter": name,
        }

        alist = self.do_request(method, param)
        for key in alist['results']:
            print key

        if name:
            return alist['results']['mediatypeid']

    def _create_action(self, name, subject, message, conditions, operations):
        """
        desc:
            create action base function
        note:
            zabbix server 2.2 diffrent from 2.4, this api for 2.2
            2.4 version: instead the "conditions" by the follow:
            "filter":{
                "evaltype": 2,
                "conditions": conditions,
            },
        """

        method = "action.create"
        param ={
            "name": name,
            "eventsource": 0,
            "esc_period": 61,
            "evaltype": 2,
            "def_shortdata": subject,
            "def_longdata": message,
            "conditions": conditions,
            "operations": operations,
        }

        return self.do_request(method, param)


    def get_actions(self):
        """
        desc:
            get actions list
        """

        method = "action.get"
        param = {
            "output": "extend",
        }

        actions = self.do_request(method, param)
        for var in actions['results']:
            print var

    def add_media(self, userid, mediatypeid):
        """
        desc:
            add media for zabbix server users
        """

        method = "user.addmedia"
        param = {
            "users":[
                {
                    "userid": userid,
                }
            ],
            "medias":{
                "mediatypeid": mediatypeid,
                "sendto": "",
                "active": 0,
                "severity": 63,
                "period": "1-7,00:00-24:00"
            }
        }

        return self.do_request(method, param)

    def get_item_key(self, itemid):
        method = "item.get"
        param = {
            "output": [
                "key_",
            ],
            "itemids": itemid,
        }

        data = self.do_request(method, param)

        for var in data['results']:
            return var['key_']

    def get_itemid(self, hostid, itemname):
        method = "item.get"
        param = {
            "output": [
                "itemid",
                "units",
            ],
            "search": {
                "key_": itemname,
            },
            "filter":{
                "hostid": hostid,
            }
        }

        itemlist = self.do_request(method, param)
        for item in itemlist['results']:
            return item['itemid'], item["units"]


    def get_data(self, hostname, itemid, value_type, unit, time_from=None, time_to=None):
        datalist = []

        hostid = self.get_hostid(hostname)

        if time_from or time_to:
            s_time = CustomTime()

            if time_from:
                time_from = s_time.date_to_secds(time_from)
            if time_to:
                time_to = s_time.date_to_secds(time_to)


        method = "history.get"
        param = {
            "output": "extend",
            "history": value_type,
            "itemids": itemid,
            "time_from": time_from,
            "time_till": time_to,
            "hostid": hostid,
        }

        c_time = CustomTime()

        ret_list = self.do_request(method, param)
        for data in ret_list['results']:
            datadict = {}

            datadict['value'] = data['value']
            datadict['unit'] = unit
            datadict['time'] = c_time.time_format(int(data['clock']))
            datalist.append(datadict)

        return utils.return_format(datalist)

    def get_expression_value(self, expression):
        if '>' in expression:
            operator = '>'
            function,value = expression.split('>')
        elif '<' in expression:
            operator = '<'
            function,value = expression.split('<')
        elif '=' in expression:
            operator = '='
            function,value = expression.split('=')
        elif '#' in expression:
            operator = '#'
            function,value = expression.split('#')

        return operator, value

    def get_trigger(self, hostid, hostname=None):
        trigger_list = []

        ret_list = self.get_trigger_base(hostid=hostid)
        for trigger in ret_list['results']:
            trigger_dict = {}

            trigger_dict['name'] = trigger['description']
            trigger_dict['severity'] = trigger['priority']
            trigger_dict['enabled'] = bool(not int(trigger['status']))
            trigger_dict['triggerid'] = trigger['triggerid']

            if hostname:
                trigger_dict['host'] = hostname
            else:
                trigger_dict['host'] = self.get_host_base(triggerids=trigger['triggerid'])

            trigger_dict['operator'],trigger_dict['threshold'] = self.get_expression_value(trigger['expression'])

            for function in trigger['functions']:
                trigger_dict['function'] = function['function']
                trigger_dict['time_param'] = function['parameter']
                trigger_dict['item_key'] = self.get_item_key(function['itemid'])

            trigger_list.append(trigger_dict)

        return utils.return_format(trigger_list)

    def set_trigger_status(self, triggerid, status):
        method = "trigger.update"
        param = {
            "triggerid": triggerid,
            "status": status,
        }

        return self.do_request(method, param)
