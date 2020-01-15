from typing import Tuple, Dict

import requests

import re
from urllib.parse import quote

__SCHEME_TO_PORT__ = {
    'ftp': '21',
    'ssh': '22',
    'telnet': '23',
    'tftp': '69',
    'socks4': '1080',
    'socks5': '1080',
    'http': '80',
    'pop2': '109',
    'pop3': '110',
    'sftp': '115',
    'https': '443',
    'sqlserver': '1433',
    'mysql': '3306',
    'postgresql': '5432',
    'redis': '6379',
}


class DictString(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, str(value))


class Url:
    def __init__(self, url: str):
        '''
        :param url: 需要解析的url
        https://example.com:8952/nothing.py;param1=v1;param2=v2?query1=v1&query2=v2#frag
        scheme=>https, netloc=>example.com:8952, path=>/nothing.py, params=>param1=v1;param2=v2,
        query=>query1=v1&query2=v2, fragment=>frag, hostname=>example.com, port=>8952
        '''
        self.scheme, self.netloc, self.path, self.params, self.query = '', '', '', DictString(), DictString()
        self.fragment, self.hostname, self.port, self.username, self.password = '', '', '', '', ''

        try:
            self.scheme, user_pass, self.netloc, self.path = re.search(
                r'(.+)://([^\\/]*:[^\\/]*@)?([^\\/]+)(/[^;?#]*)?', url).groups()
            if not self.path:
                self.path = '/'
            if user_pass:
                self.username, self.password = re.search(r'([^@:]+):([^@:]+)', user_pass).groups()

            self.hostname, self.port = re.search(r'([^:]+):?(\d+)?', self.netloc).groups()
            if not self.port:
                self.port = self.get_default_port(self.scheme)
        except AttributeError:
            raise ValueError('Incorrect URL')

        r = re.findall(r';([^?#]+?)=([^?#;]+)', url)
        if r:
            self.params = DictString(r)
        else:
            self.params = DictString()

        r = re.findall(r'[?&]([^;?#]+?)=([^;?#&]+)', url)
        if r:
            self.query = DictString(r)
        else:
            self.query = DictString()

        r = re.search(r'#([^;?#]+)', url)
        if r:
            self.fragment = r.group(1)

    @classmethod
    def get_default_port(cls, scheme):
        return __SCHEME_TO_PORT__[scheme]

    def url_index(self):
        base = f'{self.scheme}://'
        if self.username:
            base += f'{self.username}:{self.password}@'
        base += self.netloc
        return base

    def url_path(self, encoded=True):
        base = self.path
        if self.params:
            for k in self.params:
                base += f';{k}={quote(self.params[k]) if encoded else self.params[k]}'
        if self.query:
            first = True
            for k in self.query:
                if first:
                    base += '?'
                    first = False
                else:
                    base += f'&'
                base += f'{k}={quote(self.query[k]) if encoded else self.query[k]}'
        if self.fragment:
            base += f'#{self.fragment}'
        return base

    def url_full(self, encoded=True):
        return self.url_index() + self.url_path(encoded)

    def __str__(self):
        return f"URL(scheme={self.scheme}, netloc={self.netloc}, path={self.path}, params={self.params}, query={self.query}, fragment={self.fragment}, hostname={self.hostname}, port={self.port}, username={self.username}, password={self.password})"


def http(url, method='GET', headers=None, params=None, data=None, timeout=10, verify=True) -> (Tuple[requests.Response, None], Dict):
    if not headers:
        headers = {}
    headers.update({'User-Agent': 'TestUA/1.0'})
    nurl = Url(url)
    try:
        nurl.scheme = 'http'
        return requests.request(method, nurl.url_full(), headers=headers, params=params, data=data, timeout=timeout,
                                verify=verify), {'code': 0, 'message': 'request success'}
    except requests.exceptions.RequestException:
        try:
            nurl.scheme = 'https'
            return requests.request(method, nurl.url_full(), headers=headers, params=params, data=data, timeout=timeout,
                                    verify=verify),{'code': 0, 'message': 'request success'}
        except requests.exceptions.RequestException as e:
            return None, {'code': -10, 'message': e.__str__()}

