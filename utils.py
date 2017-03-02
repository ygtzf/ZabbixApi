# coding:utf-8


from optparse import OptionParser
import time

def return_format(ret):
    return_dict = {}
    return_dict['success'] = True
    if not ret:
        ret = []

    return_dict['results'] = ret

    return return_dict

def get_options():
    """
    Handle the arguments.
    """
    usage = "usage: %prog [option]"

    parser = OptionParser(usage)

    parser.add_option("-s", "--server", action="store", type="string", dest="url", help="Zabbix server URL")
    parser.add_option("-g", "--groupname", action="store", type="string", dest="groupname", help="Host groups to add the host")
    parser.add_option("-n", "--hostname", action="store", type="string", dest="hostname", help="The host's hostname")
    parser.add_option("-u", "--user", action="store", type="string", dest="user", help="Zabbix server user name")
    parser.add_option("-p", "--password", action="store", type="string", dest="password", help="Zabbix server user password")
    parser.add_option("-i", "--ip", action="store", type="string", dest="ip", help="The host's IP")

    options, args = parser.parse_args()

    return options, args

class CustomTime(object):
    """
    Time format calss
    """
    def __init__(self):
        pass

    def time_format(self, seconds):
        """
        desc:
            Show time from seconds to normal format time.
        param:
            time seconds
        return:
            normal format time
            format like "2015-11-25 09:10:00"
        """
        tuple_time = time.localtime(seconds)

        #format_time = time.strftime("%Y-%m-%d %H:%M:%S %p", tuple_time)
        format_time = time.strftime("%Y-%m-%d %H:%M:%S", tuple_time)

        return format_time

    def dur_time(self, atime):
        """
        desc:
            calc during time from lastchange till now
        param:
            atime: last chane time
        return:
            during time
        """
        return time.time() - float(atime)

    def date_to_secds(self, format_time):
        """
        desc:
            show time from normal format time to seconds
        param:
            format_time: normal format time
        return:
            seconds time
        """

        tup_time = time.strptime(format_time, "%Y-%m-%d %H:%M:%S")
        time_secds = time.mktime(tup_time)
        return time_secds
