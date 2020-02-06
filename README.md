源工具链接：https://github.com/rabbitmask/WeblogicScan

# weblogicScaner

原作者已经写的非常好了，在这里做了部分的 bug 修改，部分脚本 poc 未生效，配置错误。之前在做一次内网渗透，扫了一圈，发现 CVE-2017-10271 与 CVE-2019-2890，当时就郁闷了，怎么跨度这么大，中间的漏洞一个都没有，难道还有修一半，漏一半的，查了一下发现部分 poc 无法使用。在这个项目里面对脚本做了一些修改，提高准确率。

# 快速开始

### 依赖

+ python >= 3.6

进入项目目录，使用以下命令安装依赖库

```
$ pip3 install requests
```

### 使用说明

```
usage: ws.py [-h] -t TARGETS [TARGETS ...] [-o OUTPUT]

optional arguments:
  -h, --help            帮助信息
  -t TARGETS [TARGETS ...], --targets TARGETS [TARGETS ...]
                        直接填入目标或文件列表（默认使用端口7001）. 例子：
                        127.0.0.1:7001
  -o OUTPUT, --output OUTPUT
                        输出 json 结果的路径。默认不输出结果
```