#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import json
import os
import re
import time
import importlib
import traceback


import stars
# import stars._import
from utils.process import AutoProcess


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--targets', required=True, nargs='+',
                        help='target, or targets file(default port 7001). eg. 127.0.0.1:7001')
    parser.add_argument('-v', '--vulnerability', nargs='+',
                        help='vulnerability name. eg. "weblogic administrator console"')
    parser.add_argument('-p', '--process_number', default=8,
                        type=int, help='Number of program processes(default number 8).')
    parser.add_argument('-o', '--output', required=False, type=str,
                        help='Path to json output(default without output).')
    parser.add_argument('-s', '--ssl', action='store_true',
                        help='Forcing the use of the https protocol.')
    args = parser.parse_args()

    s_time = time.time()
    if args.output and not os.path.isdir(args.output):
        os.makedirs(args.output)
    if not args.ssl:
        args.ssl = None

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
                    res = re.search(r'^([\w.\-]{,80})([ :](\d{,5}))?$', it)
                    if res:
                        port = res.group(3) if res.group(3) else '7001'
                        id = res.group(1) + ':' + port
                        m_target[id] = {'ip': res.group(1), 'port': port}
        else:
            res = re.search(r'^([\w.\-]{,80})([ :](\d{,5}))?$', target)
            if res:
                port = res.group(3) if res.group(3) else '7001'
                id = res.group(1) + ':' + port
                m_target[id] = {'ip': res.group(1), 'port': port}

    autopro = AutoProcess(args.process_number)
    autopro.run()
    for filename in os.listdir('./stars'):
        re_data = re.search(r'([^\.\/\\]+)\.py', filename)
        if not re_data or filename.startswith('_'):
            continue
        script_name = re_data.group(1)
        try:
            module = importlib.import_module('.{}'.format(script_name),
                                             'stars')
            if 'run' not in module.__dir__():
                continue
            for key in m_target:
                data = {
                    'IP': m_target[key]['ip'], 'PORT': m_target[key]['port'], 'IS_SSL': args.ssl}
                autopro.put_task(module.run, [data], queue=True)
        except:
            print('ERROR:\n' + traceback.format_exc())

    # for key in m_target:
    #     for group_name in stars.universe.actived:
    #         for star in stars.universe.actived[group_name]:
    #             instance = star()
    #             if vulnerability_list and not (
    #                     (instance.info['CVE'] and instance.info['CVE'].lower() in vulnerability_list) or (
    #                     instance.info['NAME'] and instance.info['NAME'].lower() in vulnerability_list)):
    #                 continue
    #             res, msg = instance.light_and_msg(
    #                 m_target[key]['ip'], m_target[key]['port'], args.ssl)
    #             ikey = instance.info['CVE'] if instance.info['CVE'] else instance.info['NAME']
    #             m_target[key][ikey] = res

    #             autopro.put_task(instance.light_and_msg, [
    #                              m_target[key]['ip'], m_target[key]['port'], args.ssl], queue=True)

    while autopro.signal > 0:
        for ret in autopro.get_return():
            for key in m_target:
                if m_target[key]['ip'] == ret['IP'] and m_target[key]['port'] == ret['PORT']:
                    name = ret['NAME']
                    m_target[key][name] = ret['STATE']
        time.sleep(1)

    result = {}
    for target in m_target:
        result[target] = {}
        for key in sorted(m_target[target].keys()):
            result[target][key] = m_target[target][key]

    if args.output:
        with open(
                os.path.join(
                    args.output, f'result_{time.strftime("%m%d_%H%M%S", time.localtime(time.time()))}.json'),
                'w') as _f:
            _f.write(json.dumps(result))
    print('Run completed, {} seconds total.'.format(int(time.time() - s_time)))
