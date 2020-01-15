#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# Weblogic Console
# updated 2019/10/23
# by 0xn0ne

import sys

from stars import Star, universe, target_type
from utils import http

headers = {'User-Agent': 'TestUA/1.0'}


@universe.groups()
class WeblogicConsole(Star):
    info = {
        'NAME': 'weblogic administrator console',
        'CVE': None,
        'TAG': []
    }
    type = target_type.MODULE

    def light_up(self, dip, dport, path='console', *args, **kwargs) -> (bool, dict):
        r, data = http('http://{}:{}/{}/login/LoginForm.jsp'.format(dip, dport, path))
        if r and r.status_code == 200:
            return True, {'url': r.url}
        return False, {}


# def run(dip, dport):
#     res, url = islive(dip, dport)
#     if res:
#         print('[+] Found a module with Weblogic Console at {}:{}!'.format(dip, dport))
#         print('[+] Path is: {}'.format(url))
#         print('[+] Please try weak password blasting!')
#     else:
#         print('[-] Target {}:{} does not detect Weblogic Console vulnerability!'.format(dip, dport))

