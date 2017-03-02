# coding:utf-8

import sys

import json
import urllib2

header = {'Content-Type' : 'application/json-rpc'}


class HttpRequestException(Exception):
    """
    Zabbix Exception calss
    """
    pass

def response_format(successed, response):
    response_dict = {}
    response_dict['success'] = bool(successed)

    if successed:
        response_dict['results'] = response['result']
    else:
        response_dict['error'] = response['error']

    return response_dict

class HttpRequest(object):
    def do_request(self, method, param=None):
        """
        desc:
            make http request to Zabbix API
        param:
            method: Zabbix API method
            param: param by Zabbix API method required
        return:
            Zabbix API exec result
        """

        request = {
            'jsonrpc' : '2.0',
            'method' : method,
            'params' : param,
            'id' : 1,
            'auth' : self.auth,
        }

        req = urllib2.Request(self.url, json.dumps(request))
        req.get_method = lambda: 'POST'


        for key in header:
            req.add_header(key, header[key])

        res = urllib2.urlopen(req)
        response = json.load(res)

        res.close()

        if 'error' in response:
            return response_format(0, response)
            #msg = "\nError: {message}, {data} while sending:\n {json}".format(
            #    message=reponse['error']['message'],
            #    data=reponse['error']['data'],
            #    json=str(request))
            #raise HttpRequestException(msg)
        else:
            return response_format(1, response)
