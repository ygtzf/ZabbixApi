# coding:utf-8

import utils
from utils import CustomTime
from zabbix_api_base import ZabbixApiBase

class ZabbixApi(ZabbixApiBase):
    def get_events(self, hostname=None, time_from=None, time_to=None):
        """
        desc:
            get all event list; or get event list by hostname, or by time
        param:
            hostname: must when get event list by hostname
            time_from, time_to: must  when get event by time
        example:
            time format: "2015-11-25 10:00:00"
        """
        if time_from or time_to:
            s_time = CustomTime()

            if time_from:
                time_from = s_time.date_to_secds(time_from)
            if time_to:
                time_to = s_time.date_to_secds(time_to)

        hostid = None
        if hostname:
            hostid = self.get_hostid(hostname)

            if not hostid:
                return utils.return_format(hostid)

        return self._get_event(hostid=hostid, time_from=time_from, time_to=time_to)



    def set_host_status(self, hostname, status=1):
        """
        desc:
            set host whether is monitored
        param:
            status: 0:enable (monitor) 1:disable (no monitor)
        """
        hostid = None
        if hostname:
            hostid = self.get_hostid(hostname)

            if not hostid:
                return utils.return_format(hostid)

        method = "host.update"
        param = {
            "hostid": hostid,
            "status": status,
        }

        return self.do_request(method, param)

    def event_ack(self, eventid):
        """
        desc:
            ack event
        param:
            event id
        """

        method = "event.acknowledge"
        param = {
            "eventids": eventid,
            "message" : "Problem ack"
        }

        return self.do_request(method, param)

    def create_action(self, host_groupid, user_groupid, userid, mediatypeid):
        """
        desc:
            create action API
        pram:
            host_groupid: host grooup id,
            user_groupid: user group id,
            userid: zabbix server user id,
            mediatypeid: mediatype id will used by action for post or send mail
        """

        name = "default-action"
        subject = "{TRIGGER.NAME}:{TRIGGER.STATUS}"
        message = '''Trigger: {TRIGGER.NAME}\r\nTrigger status: {TRIGGER.STATUS}\r\n
        Trigger serverity: {TRIGGER.SEVERITY}\r\nItem:({HOST.NAME1}:{ITEM.KEY1})\r\n
        Event id : {EVENT.ID}\r\nEvent status: {EVENT.STATUS}\r\n
        Event time: {EVENT.TIME}\r\nEvent.date: {EVENT.DATE}\r\n
        Event ack: {EVENT.ACK.STATUS}
        '''

        conditions = [
            {
                "conditiontype": 0,
                "operator": 0,
                "value": host_groupid
            },
        ]

        operations = [
            {
                "operationtype": 0,
                "esc_period": 61,
                "esc_step_from" : 1,
                "esc_step_to": 2,
                "evaltype": 2,
                "opmessage_grp":[
                    {
                        "usrgrpid": user_groupid,
                    },
                ],
                "opmessage_usr":[
                    {
                        "userid": userid,
                    },
                ],
                "opmessage":{
                    "default_msg": 1,
                    "mediatype": mediatypeid,
                }
            }
        ]


        return self._create_action(name, subject, message, conditions, operations)

    def get_item_data(self, hostname, itemid, time_from=None, time_to=None):
        method = "item.get"
        param = {
            "output": [
                "name",
                "units",
                "value_type",
            ],
            "itemids": itemid,
        }

        ret = self.do_request(method, param)
        if ret['success']:
            if ret['results']:
                for var in ret['results']:
                    item_dict = var
            else:
                return ret
        else:
            return ret

        return self.get_data(hostname, item_dict['itemid'], item_dict['value_type'], item_dict['units'], time_from, time_to)

    def update_trigger(self, triggerid, expression=None, trigger_name=None, severity=None):
        method = "trigger.update"
        param = {
            "triggerid": triggerid,
            "expression": expression,
            "description": trigger_name,
        }

        if severity:
            param["priority"] = severity

        return self.do_request(method, param)

    def list_triggers(self, hostname=None):
        hostid = None

        if hostname:
            hostid = self.get_hostid(hostname)

            if not hostid:
                return utils.return_format(hostid)

        return self.get_trigger(hostid, hostname=hostname)

    def create_trigger(self, trigger_name, severity, expression):
        method = "trigger.create"
        param = {
            'description': trigger_name,
            'expression': expression,
            'priority': severity,
        }

        return self.do_request(method, param)

    def delete_trigger(self, triggerids):
        method = "trigger.delete"

        if type(triggerids) != type([]):
            param = [triggerids]
        else:
            param = triggerids

        return self.do_request(method, param)

    def list_items(self, hostname=None, templatename=None):
        hostid = None
        hostid = self.get_hostid(hostname)

        templateid = None
        templateid = self.get_template_id(templatename)

        if not (hostid or templateid):
           return utils.return_format(hostid)

        method = "item.get"
        param = {
            "output": [
                "itemid",
                "name",
                "key_",
                "units",
                "value_type",
            ],
            "hostids": hostid,
            "templateids": templateid,
        }

        return self.do_request(method, param)

    def get_hosts(self):
        method = "host.get"
        param = {
            'output' : [
                'host',
                'hostid',
                'name'
            ],
        }

        return self.do_request(method, param)

    def enable_trigger(self, triggerid):
        return self.set_trigger_status(triggerid, 0)

    def disable_trigger(self, triggerid):
        return self.set_trigger_status(triggerid, 1)
