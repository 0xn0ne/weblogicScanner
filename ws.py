#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import stars
import stars._import

if __name__ == '__main__':
    dip = '10.0.179.247'
    dport = '8001'
    for group_name in stars.universe.actived:
        for star in stars.universe.actived[group_name]:
            instance = star()
            instance.light_and_msg(dip, dport)
