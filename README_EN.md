source: https://github.com/rabbitmask/WeblogicScan

# weblogicScaner

[简体中文](./README.md) | English

As of November 27, 2020, weblogic Vulnerability Scanning Tool. If there is an unrecorded and open POC vulnerability, please submit issue.

Some bug fixes were made, some POC did not take effect, or configuration errors. I checked before and found that some POC could not be used. In this project, some modifications have been made to the script to improve the accuracy.

**Note**：Some vulnerabilities require multiple tests to verify due to stability reasons.

Currently detectable vulnerabilitys are (some non-principles detection, manual verification required):

+ weblogic administrator console
+ CVE-2014-4210
+ CVE-2016-0638
+ CVE-2016-3510
+ CVE-2017-3248
+ CVE-2017-3506
+ CVE-2017-10271
+ CVE-2018-2628
+ CVE-2018-2893
+ CVE-2018-2894
+ CVE-2018-3191
+ CVE-2018-3245
+ CVE-2018-3252
+ CVE-2019-2618
+ CVE-2019-2725
+ CVE-2019-2729
+ CVE-2019-2890
+ CVE-2020-2551
+ CVE-2020-14882
+ CVE-2020-14883

# Quick start

### Required

+ python >= 3.6

In the project directory and use the following command to install the dependent libraries

```
$ pip3 install requests
```

### Usage

```
usage: ws.py [-h] -t TARGETS [TARGETS ...]
             [-v VULNERABILITY [VULNERABILITY ...]] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGETS [TARGETS ...], --targets TARGETS [TARGETS ...]
                        target, or targets file(default port 7001). eg.
                        127.0.0.1:7001
  -v VULNERABILITY [VULNERABILITY ...], --vulnerability VULNERABILITY [VULNERABILITY ...]
                        vulnerability name. eg. "weblogic administrator
                        console"
  -o OUTPUT, --output OUTPUT
                        Path to json output(default without output).
  -s, --ssl             Forcing the use of the https protocol.
```

# Example

```
(venv) ~/weblogicScanner$ python ws.py -t 192.168.124.129
[23:03:04][INFO] [*][Weblogic Console][192.168.56.129:7001] Start...
[23:03:04][INFO] [+][Weblogic Console][192.168.56.129:7001] Found module!
[23:03:04][INFO] [*][Weblogic Console][192.168.56.129:7001] Please verify manually!
[23:03:04][INFO] [*][CVE-2014-4210][192.168.56.129:7001] Start...
[23:03:04][INFO] [-][CVE-2014-4210][192.168.56.129:7001] Not found.
[23:03:04][INFO] [*][CVE-2016-0638][192.168.56.129:7001] Start...
[23:03:06][INFO] [-][CVE-2016-0638][192.168.56.129:7001] Not vulnerability.
[23:03:06][INFO] [*][CVE-2016-3510][192.168.56.129:7001] Start...
[23:03:08][INFO] [-][CVE-2016-3510][192.168.56.129:7001] Not vulnerability.
[23:03:08][INFO] [*][CVE-2017-3248][192.168.56.129:7001] Start...
[23:03:10][INFO] [-][CVE-2017-3248][192.168.56.129:7001] Not vulnerability.
[23:03:10][INFO] [*][CVE-2017-3506][192.168.56.129:7001] Start...
[23:03:10][INFO] [-][CVE-2017-3506][192.168.56.129:7001] Not vulnerability.
[23:03:10][INFO] [*][CVE-2017-10271][192.168.56.129:7001] Start...
[23:03:10][INFO] [-][CVE-2017-10271][192.168.56.129:7001] Not vulnerability.
[23:03:10][INFO] [*][CVE-2018-2628][192.168.56.129:7001] Start...
[23:03:14][INFO] [+][CVE-2018-2628][192.168.56.129:7001] Exists vulnerability!
[23:03:14][INFO] [*][CVE-2018-2893][192.168.56.129:7001] Start...
[23:03:18][INFO] [+][CVE-2018-2893][192.168.56.129:7001] Exists vulnerability!
[23:03:18][INFO] [*][CVE-2018-2894][192.168.56.129:7001] Start...
[23:03:19][INFO] [+][CVE-2018-2894][192.168.56.129:7001] Found module!
[23:03:19][INFO] [*][CVE-2018-2894][192.168.56.129:7001] Please verify manually!
[23:03:19][INFO] [*][CVE-2018-3191][192.168.56.129:7001] Start...
[23:03:23][INFO] [+][CVE-2018-3191][192.168.56.129:7001] Exists vulnerability!
[23:03:23][INFO] [*][CVE-2018-3245][192.168.56.129:7001] Start...
[23:03:29][INFO] [-][CVE-2018-3245][192.168.56.129:7001] Not vulnerability.
[23:03:29][INFO] [*][CVE-2018-3252][192.168.56.129:7001] Start...
[23:03:36][INFO] [+][CVE-2018-3252][192.168.56.129:7001] Found module!
[23:03:36][INFO] [*][CVE-2018-3252][192.168.56.129:7001] Please verify manually!
[23:03:36][INFO] [*][CVE-2019-2618][192.168.56.129:7001] Start...
[23:03:36][INFO] [+][CVE-2019-2618][192.168.56.129:7001] Found module!
[23:03:36][INFO] [*][CVE-2019-2618][192.168.56.129:7001] Please verify manually!
[23:03:36][INFO] [*][CVE-2019-2725][192.168.56.129:7001] Start...
[23:03:46][INFO] [-][CVE-2019-2725][192.168.56.129:7001] Not vulnerability.
[23:03:46][INFO] [*][CVE-2019-2729][192.168.56.129:7001] Start...
[23:03:54][INFO] [-][CVE-2019-2729][192.168.56.129:7001] Not vulnerability.
[23:03:54][INFO] [*][CVE-2019-2888][192.168.56.129:7001] Start...
[23:03:56][INFO] [+][CVE-2019-2888][192.168.56.129:7001] Found module!
[23:03:56][INFO] [*][CVE-2019-2888][192.168.56.129:7001] Please verify manually!
[23:03:56][INFO] [*][CVE-2019-2890][192.168.56.129:7001] Start...
[23:03:58][INFO] [-][CVE-2019-2890][192.168.56.129:7001] Not vulnerability.
[23:03:58][INFO] [*][CVE-2020-2551][192.168.56.129:7001] Start...
[23:03:58][INFO] [+][CVE-2020-2551][192.168.56.129:7001] Found module!
[23:03:58][INFO] [*][CVE-2020-2551][192.168.56.129:7001] Please verify manually!
[23:03:58][INFO] [*][CVE-2020-2555][192.168.56.129:7001] Start...
[23:04:02][INFO] [+][CVE-2020-2555][192.168.56.129:7001] Exists vulnerability!
[23:04:02][INFO] [*][CVE-2020-2883][192.168.56.129:7001] Start...
[23:04:06][INFO] [+][CVE-2020-2883][192.168.56.129:7001] Exists vulnerability!
[23:04:06][INFO] [*][CVE-2020-14882][192.168.56.129:7001] Start...
[23:04:23][INFO] [-][CVE-2020-14882][192.168.56.129:7001] Not vulnerability.
[23:04:23][INFO] [*][CVE-2020-14883][192.168.56.129:7001] Start...
[23:04:23][INFO] [+][CVE-2020-14883][192.168.56.129:7001] Exists vulnerability!
```