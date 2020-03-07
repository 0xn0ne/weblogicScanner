source: https://github.com/rabbitmask/WeblogicScan

# weblogicScaner

[简体中文](./README.md) | English

As of March 7, 2020, weblogic Vulnerability Scanning Tool. If there is an unrecorded and open POC vulnerability, please submit issue.

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
```

# Example

```
(venv) ~/weblogicScanner$ python ws.py -t 192.168.124.129
[*] Start to detect weblogic administrator console for 192.168.124.129:7001.
[+] Found a module with weblogic administrator console at 192.168.124.129:7001!
[*] Please verify weblogic administrator console vulnerability manually!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2014-4210 for 192.168.124.129:7001.
[+] Found a module with CVE-2014-4210 at 192.168.124.129:7001!
[*] Please verify CVE-2014-4210 vulnerability manually!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2016-0638 for 192.168.124.129:7001.
[+] Target 192.168.124.129:7001 has a CVE-2016-0638 vulnerability!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2016-3510 for 192.168.124.129:7001.
[+] Target 192.168.124.129:7001 has a CVE-2016-3510 vulnerability!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2017-3248 for 192.168.124.129:7001.
[+] Target 192.168.124.129:7001 has a CVE-2017-3248 vulnerability!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2017-3506 for 192.168.124.129:7001.
[+] Target 192.168.124.129:7001 has a CVE-2017-3506 vulnerability!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2017-10271 for 192.168.124.129:7001.
[+] Target 192.168.124.129:7001 has a CVE-2017-10271 vulnerability!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2018-2628 for 192.168.124.129:7001.
[+] Target 192.168.124.129:7001 has a CVE-2018-2628 vulnerability!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2018-2893 for 192.168.124.129:7001.
[+] Target 192.168.124.129:7001 has a CVE-2018-2893 vulnerability!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2018-2894 for 192.168.124.129:7001.
[-] Target 192.168.124.129:7001 does not detect CVE-2018-2894!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2018-3191 for 192.168.124.129:7001.
[+] Target 192.168.124.129:7001 has a CVE-2018-3191 vulnerability!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2018-3245 for 192.168.124.129:7001.
[-] Target 192.168.124.129:7001 does not detect CVE-2018-3245 vulnerability!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2018-3252 for 192.168.124.129:7001.
[+] Found a module with CVE-2018-3252 at 192.168.124.129:7001!
[*] Please verify CVE-2018-3252 vulnerability manually!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2019-2618 for 192.168.124.129:7001.
[+] Found a module with CVE-2019-2618 at 192.168.124.129:7001!
[*] Please verify CVE-2019-2618 vulnerability manually!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2018-2725 for 192.168.124.129:7001.
[+] Target 192.168.124.129:7001 has a CVE-2018-2725 vulnerability!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2019-2729 for 192.168.124.129:7001.
[+] Target 192.168.124.129:7001 has a CVE-2019-2729 vulnerability!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2019-2890 for 192.168.124.129:7001.
[-] Target 192.168.124.129:7001 does not detect CVE-2019-2890 vulnerability!
---------------- Heartless Split Line ----------------
[*] Start to detect CVE-2020-2551 for 192.168.124.129:7001.
[+] Target 192.168.124.129:7001 has a CVE-2020-2551 vulnerability!
---------------- Heartless Split Line ----------------

```