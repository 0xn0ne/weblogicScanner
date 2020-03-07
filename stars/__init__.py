from typing import List, Mapping, Any, Dict, Tuple, Union

from state import BaseState
from utils import http


class MessageSign(BaseState):
    EXC = '[!]'
    STR = '[*]'
    PLS = '[+]'
    MIN = '[-]'


class TargetType(BaseState):
    VULNERABILITY = 40
    MODULE = 20


class ResultCode(BaseState):
    # start checking
    START = 10
    # exists vulnerability
    EXISTS = 20
    # not exists anything
    NOTEXISTS = 40
    # timeout
    TIMEOUT = 50
    # error
    ERROR = 60
    # detect finish
    FINISH = 100


msg_sign = MessageSign()
result_code = ResultCode()
target_type = TargetType()


class Star:
    info = {
        'NAME': '',
        'CVE': '',
        'TAG': []
    }

    type: target_type.VULNERABILITY

    def __init__(self):
        rc = result_code.to_dict()
        self.ext_msg: Dict[str, List[str]] = {}
        for key in rc:
            code = rc[key]
            self.ext_msg[code] = []
            if code == result_code.START:
                self.ext_msg[code].append('[*] Start detect {call} for {target}.')
            if code == result_code.NOTEXISTS:
                if self.type == target_type.VULNERABILITY:
                    self.ext_msg[code].append('[-] Target {target} does not detect {call} vulnerability!')
                elif self.type== target_type.MODULE:
                    self.ext_msg[code].append('[-] Target {target} does not detect {call}!')
            if code == result_code.EXISTS:
                if self.type == target_type.VULNERABILITY:
                    self.ext_msg[code].append('[+] Target {target} has a {call} vulnerability!')
                elif self.type == target_type.MODULE:
                    self.ext_msg[code].append('[+] Found a module with {call} at {target}!')
                    self.ext_msg[code].append('[*] Please verify {call} vulnerability manually!')
            if code == result_code.TIMEOUT:
                self.ext_msg[code].append('[!] Target {target} detect timeout!')
            if code == result_code.ERROR:
                self.ext_msg[code].append('[!] Target {target} connection error!')
            if code == result_code.FINISH:
                self.ext_msg[code].append('---------------- Heartless Split Line ----------------')

    def light_and_msg(self, dip, dport, *arg, **kwargs):
        self.msg(f'{dip}:{dport}', result_code.START)
        res = False
        data = {}
        try:
            res, data = self.light_up(dip, dport, *arg, **kwargs)
        except ConnectionAbortedError:
            self.msg(f'{dip}:{dport}', result_code.ERROR)
        if res:
            self.msg(f'{dip}:{dport}', result_code.EXISTS)
        else:
            self.msg(f'{dip}:{dport}', result_code.NOTEXISTS)
        self.msg(f'{dip}:{dport}', result_code.FINISH)
        return res, data

    def light_up(self, dip, dport, *arg, **kwargs) -> Tuple[Union[bool, None], dict]:
        self.msg(f'{dip}:{dport}', result_code.START)
        return None, {}

    def get_info(self, key: str):
        if key in self.info:
            return self.info[key.upper()]

    def set_info(self, key: str, value: Any):
        if key.upper() == 'CVE':
            self.info[key.upper()] = value.upper()
        else:
            self.info[key.upper()] = value

    def add_ext_msg(self, msg, code=result_code.START, sign=msg_sign):
        if code not in self.ext_msg:
            return None
        self.ext_msg[code] = f'{sign} {msg}'

    def msg(self, target, code: int = result_code.START, data: Union[Dict[str, str], None] = None):
        if not data:
            data = {}
        data['target'] = target
        data['call'] = self.get_info("CVE") if self.get_info("CVE") else self.get_info("NAME")

        for msg in self.ext_msg[code]:
            print(msg.format(**data))

    def http(self, url, method='GET', *arg, **kwargs):
        return http(url, method, *arg, **kwargs)


class Universe:
    actived: Dict[str, List[Star]] = {}

    def groups(self, gname=''):
        def decorator(cls: Star):
            nonlocal gname
            if not gname:
                gname = 'default'
            if gname not in self.actived:
                self.actived[gname] = []
            # instance = cls
            # if instance
            self.actived[gname].append(cls)

        return decorator


universe = Universe()
