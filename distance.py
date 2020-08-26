#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time
from bottle import run, request, route, template
class Ranger(object):
    def setup(self): # 确定输入输出 GPIO 口。
        # 初始化gpio口。
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(29, GPIO.OUT)
        GPIO.setup(31, GPIO.IN)


    # trigger_pin 脚发送开始测量信号。
    def send_trigger_pulse(self):
        self.setup()
        GPIO.output(29,True)
        time.sleep(0.00001)
        GPIO.output(29,False)


    def wait_for_echo(self,value,timeout):
        count = timeout
        while GPIO.input(31) != value and count > 0:
            count = count - 1

    # 根据返回高电平时间计算距离，声速取340m/s。
    def get_distance(self):
        self.send_trigger_pulse()
        self.wait_for_echo(True, 10000)
        start = time.time()
        self.wait_for_echo(False, 10000)
        finish = time.time()
        pulse_len = finish - start
        distance_cm = pulse_len / 0.000058
        return distance_cm

# 将测得的距离返回给html模板。
@route("/")  #如果没有规定方式，默认get。
def distance():
    ranger = Ranger()
    dis = ranger.get_distance()
    return template("distance", dist=dis)


run(host="0.0.0.0", port=8081, debug=True) 