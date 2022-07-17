#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# Weblogic Console
# updated 2019/10/23
# by 0xn0ne

import sys
from multiprocessing.managers import SyncManager
from typing import Any, Dict, List, Mapping, Tuple, Union

from utils import http

from stars import target_type, Star

headers = {'User-Agent': 'TestUA/1.0'}


# @universe.groups()
class WeblogicConsole(Star):
    info = {
        'NAME': 'Weblogic Console',
        'CVE': None,
        'TAG': []
    }
    type = target_type.MODULE

    def light_up(self, dip, dport, force_ssl=None, path='console', *args, **kwargs) -> (bool, dict):
        r, data = http(
            'http://{}:{}/{}/login/LoginForm.jsp'.format(dip, dport, path), ssl=force_ssl)
        if r and r.status_code == 200:
            return True, {'url': r.url}
        return False, {}


def run(queue: SyncManager.Queue, data: Dict):
    obj = WeblogicConsole()
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
