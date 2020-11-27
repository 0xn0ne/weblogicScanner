#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
# CVE-2020-2551
# updated 2020/03/07
# by 0xn0ne
# 不会 java，该漏洞的分析也没人发，对该 POC 还不是很理解

import socket

from stars import universe, Star, target_type


@universe.groups()
class CVE_2020_2551(Star):
    info = {
        'NAME': '',
        'CVE': 'CVE-2020-2551',
        'TAG': []
    }
    type = target_type.MODULE

    def light_up(self, dip, dport, force_ssl=None, timeout=5, *args, **kwargs) -> (bool, dict):
        # t3 handshake
        dport = int(dport)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            sock.connect((dip, dport))
        except socket.timeout:
            return False, {'msg': 'connection timeout.'}
        except ConnectionRefusedError:
            return False, {'msg': 'connection refuse.'}
        sock.send(bytes.fromhex('47494f50010200030000001700000002000000000000000b4e616d6553657276696365'))
        res = sock.recv(1024)

        return b'GIOP' in res, {'msg': 'finish.'}
