#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# CVE-2018-2894
# updated 2019/10/23
# by 0xn0ne

from stars import universe, Star, target_type
from utils import http


@universe.groups()
class CVE_2018_2894(Star):
    info = {
        'NAME': '',
        'CVE': 'CVE-2018-2894',
        'TAG': []
    }
    type = target_type.MODULE

    def light_up(self, dip, dport, force_ssl=None, *args, **kwargs) -> (bool, dict):
        url = 'http://{}:{}/wsutc/begin.do'.format(dip, dport)
        b_res, data = http(url, ssl=force_ssl)
        url = 'http://{}:{}/ws_utc/config.do'.format(dip, dport)
        c_res, data = http(url, ssl=force_ssl)
        if (b_res and b_res.status_code == 200) or (c_res and c_res.status_code == 200):
            return True, {'msg': 'finish.'}
        return False, {'msg': 'finish.'}
