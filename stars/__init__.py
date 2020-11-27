import traceback
from typing import List, Mapping, Any, Dict, Tuple, Union
import logging

from logger import APPNAME
from state import BaseState
from utils import http

logger = logging.getLogger(APPNAME)


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
        self.msg_group: Dict[str, List[str]] = {}
        for key in rc:
            code = rc[key]
            self.msg_group[code] = []
            if code == result_code.START:
                self.msg_group[code].append('[*][{call}][{target}] Start...')
            if code == result_code.NOTEXISTS:
                if self.type == target_type.VULNERABILITY:
                    self.msg_group[code].append('[-][{call}][{target}] Not vulnerability.')
                elif self.type == target_type.MODULE:
                    self.msg_group[code].append('[-][{call}][{target}] Not found.')
            if code == result_code.EXISTS:
                if self.type == target_type.VULNERABILITY:
                    self.msg_group[code].append('[+][{call}][{target}] Exists vulnerability!')
                elif self.type == target_type.MODULE:
                    self.msg_group[code].append('[+][{call}][{target}] Found module!')
                    self.msg_group[code].append('[*][{call}][{target}] Please verify manually!')
            if code == result_code.TIMEOUT:
                self.msg_group[code].append('[!][{call}][{target}] Timeout.')
            if code == result_code.ERROR:
                self.msg_group[code].append('[!][{call}][{target}] Connection error.')

    def light_and_msg(self, dip, dport, force_ssl=None, *arg, **kwargs):
        self.print_msg(f'{dip}:{dport}', result_code.START)
        res = False
        data = {}
        try:
            res, data = self.light_up(dip, dport, force_ssl, *arg, **kwargs)
        except Exception as e:
            # ConnectionResetError: 当 socket 连接被重置触发，常见于反序列化的场景
            # ConnectionAbortedError: 当 socket 连接被强制中断触发，常见于存在防火墙的场景
            self.print_msg(f'{dip}:{dport}', result_code.ERROR, {
                'more_detail': ['''The following information output is only used for error tracking, so don't panic''',
                                '以下信息输出仅为错误追踪使用，请勿担心', traceback.format_exc()]}, level=logging.DEBUG)
        if res:
            self.print_msg(f'{dip}:{dport}', result_code.EXISTS)
        else:
            self.print_msg(f'{dip}:{dport}', result_code.NOTEXISTS)
        return res, data

    def light_up(self, dip, dport, force_ssl=None, *arg, **kwargs) -> Tuple[Union[bool, None], dict]:
        self.print_msg(f'{dip}:{dport}', result_code.START)
        return None, {}

    def get_info(self, key: str):
        if key in self.info:
            return self.info[key.upper()]

    def set_info(self, key: str, value: Any):
        if key.upper() == 'CVE':
            self.info[key.upper()] = value.upper()
        else:
            self.info[key.upper()] = value

    def add_msg_group(self, msg, code=result_code.START, sign=msg_sign.STR):
        if code not in self.msg_group:
            return None
        self.msg_group[code] = f'{sign} {msg}'

    def print_msg(self, target, code: int = result_code.START, data: Union[Dict[str, Any], None] = None,
                  level: int = logging.INFO):
        if not data:
            data = {}
        data['target'] = target
        data['call'] = self.get_info("CVE") if self.get_info("CVE") else self.get_info("NAME")

        for msg in self.msg_group[code]:
            logger.info(msg.format(**data))
        if 'more_detail' in data and isinstance(data['more_detail'], List):
            # The 'more_detail' key type is List
            for detail in data['more_detail']:
                self.print_ext_msg(detail, level=level)

    def print_ext_msg(self, msg, sign=msg_sign.STR, level: int = logging.INFO):
        logger.log(level, f'{sign} {msg}')

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
