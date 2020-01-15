DEFAULT_LANG = '_lang_cn'


class BaseState:
    @classmethod
    def to_dict(cls):
        obj_dict = {}
        for n in dir(cls):
            v = getattr(cls, n)
            if n.startswith('_') or callable(v):
                continue
            obj_dict[n] = v
        return obj_dict

    @classmethod
    def text(cls, value: int, lang=DEFAULT_LANG):
        if value not in cls.__dict__[lang]:
            return 'error code'
        return cls.__dict__[lang][value]

    @classmethod
    def group_to_dict(cls, value: int, lang=DEFAULT_LANG):
        return {'code': value, 'msg': cls.text(value, lang)}

    @classmethod
    def group_to_list(cls, value: int, lang=DEFAULT_LANG):
        return [value, cls.text(value, lang)]


class R(BaseState):
    '''Response Content'''
    SUCCESS = 0
    FAILED = -255
    TIMEOUT = -254
    UNKNOWN = -253
    TOO_FREQUENT = -252
    DEPRECATED = -251

    NOT_FOUND = -249
    ALREADY_EXISTS = -248

    PERMISSION_DENIED = -239
    INVALID_ROLE = -238

    CHECK_FAILURE = -229
    PARAM_REQUIRED = -228
    POSTDATA_REQUIRED = -227

    INVALID_PARAMS = -219
    INVALID_POSTDATA = -218

    CONNET_FAILED = -209

    WS_DONE = 1

    _lang_cn = {
        SUCCESS: '成功',
        FAILED: '失败',
        TIMEOUT: '超时',
        UNKNOWN: '未知错误',
        TOO_FREQUENT: '请求过于频繁',
        DEPRECATED: '此接口已不推荐使用',

        NOT_FOUND: '未找到',
        ALREADY_EXISTS: '已存在',

        PERMISSION_DENIED: '无权访问',
        INVALID_ROLE: '权限申请失败',

        CHECK_FAILURE: '校验失败',
        PARAM_REQUIRED: '缺少参数',
        POSTDATA_REQUIRED: '缺少提交内容',

        INVALID_PARAMS: '非法参数',
        INVALID_POSTDATA: '非法提交内容',

        CONNET_FAILED: '连接失败',

        WS_DONE: 'Websocket 请求完成'
    }

    _lang_cn = {
        SUCCESS: 'success',
        FAILED: 'failed',
        TIMEOUT: 'timeout',
        UNKNOWN: 'unknown',
        TOO_FREQUENT: 'request too frequent',
        DEPRECATED: 'interface deprecated',

        NOT_FOUND: 'not found',
        ALREADY_EXISTS: 'already exists',

        PERMISSION_DENIED: 'permission denied',
        INVALID_ROLE: 'acquire role failed',

        CHECK_FAILURE: 'check failure',
        PARAM_REQUIRED: 'parameter(s) required',
        POSTDATA_REQUIRED: 'post data item(s) required',

        INVALID_PARAMS: 'invalid parameter(s)',
        INVALID_POSTDATA: 'invalid post',

        CONNET_FAILED: 'connection failed',

        WS_DONE: 'Websocket request done'
    }


if __name__ == '__main__':
    print(R.to_dict())
    print(R.text(R.FAILED))
    print(R.group_to_dict(R.SUCCESS))
    print(R.group_to_list(R.CONNET_FAILED))