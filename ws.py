#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import json
import os
import re
import time

import stars
import stars._import

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--targets', required=True, nargs='+',
                        help='target, or targets file(default port 7001). eg. 127.0.0.1:7001')
    parser.add_argument('-v', '--vulnerability', nargs='+',
                        help='vulnerability name. eg. "weblogic administrator console"')
    parser.add_argument('-o', '--output', type=str, help='Path to json output(default without output).')
    args = parser.parse_args()

    if args.output and not os.path.isdir(args.output):
        os.makedirs(args.output)

    vulnerability_list = []
    if args.vulnerability:
        for item in args.vulnerability:
            item: str
            vulnerability_list.append(item.lower())

    m_target = {}
    for target in args.targets:
        t_list = []
        if os.path.isfile(target):
            with open(target) as _f:
                for it in _f.read().split('\n'):
                    res = re.search(r'^(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})([ :](\d{,5}))?$', it)
                    if res:
                        port = res.group(3) if res.group(3) else '7001'
                        id = res.group(1) + ':' + port
                        m_target[id] = {'ip': res.group(1), 'port': port}
        else:
            res = re.search(r'^(\d{,3}\.\d{,3}\.\d{,3}\.\d{,3})([ :](\d{,5}))?$', target)
            if res:
                port = res.group(3) if res.group(3) else '7001'
                id = res.group(1) + ':' + port
                m_target[id] = {'ip': res.group(1), 'port': port}

    for key in m_target:
        for group_name in stars.universe.actived:
            for star in stars.universe.actived[group_name]:
                instance = star()
                if vulnerability_list and ((instance.info['CVE'] and instance.info['CVE'].lower() not in vulnerability_list) or (
                        instance.info['NAME'] and instance.info['NAME'].lower() not in vulnerability_list)):
                    continue
                res, msg = instance.light_and_msg(m_target[key]['ip'], m_target[key]['port'])
                ikey = instance.info['CVE'] if instance.info['CVE'] else instance.info['NAME']
                m_target[key][ikey] = res

    if args.output:
        with open(os.path.join(args.output, f'res_{time.strftime("%Y%m%d_%H.%M.%S", time.localtime(time.time()))}.json'), 'w') as _f:
            _f.write(json.dumps(m_target))
