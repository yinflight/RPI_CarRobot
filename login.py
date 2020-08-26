#!/usr/bin/env python3

# -*- coding:utf-8 -*-

from bottle import get, post, run, request, route, template

import RPi.GPIO as GPIO

import time

import sys



#define

Serve=0

Moter_PWMA=0

Moter_PWMB=0

PWM_pin = [11,18,23]

inx_pin = [22, 27, 15, 24]

#MoterA 正反转

AIN1 = inx_pin[0] 

AIN2 = inx_pin[1]

#MoterB 正反转

BIN1 = inx_pin[2]

BIN2 = inx_pin[3]







#setup

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

for pin in PWM_pin:

    GPIO.setup(pin, GPIO.OUT)

Serve=GPIO.PWM(PWM_pin[0] , 50)# 在pin脚上产生频率为50HZ的PWM信号

Moter_PWMA=GPIO.PWM(PWM_pin[1] , 100)

Moter_PWMB=GPIO.PWM(PWM_pin[2] , 100)

    ####  初始化PWMspeed 100hz

Serve.start(7) #angle=90度

    # Initial duty Cycle = 0

Moter_PWMA.start(0)# 在引脚上设置一个初始PWM信号。

Moter_PWMB.start(0)# 在引脚上设置一个初始PWM信号。       

pin = None#计数清零

for pin in inx_pin:#初始化控制端pin，设置成低电平

    GPIO.setup(pin, GPIO.OUT)

    GPIO.output(pin, GPIO.LOW)



####  front函数，小车前进

def front():

    Serve.ChangeDutyCycle(7)

    Moter_PWMA.ChangeDutyCycle(20)#speed[0 - 100]

    GPIO.output(AIN1,GPIO.LOW) #AIN1

    GPIO.output(AIN2,GPIO.HIGH)#AIN2



    Moter_PWMB.ChangeDutyCycle(20)#speed[0 - 100]

    GPIO.output(BIN1,GPIO.LOW) #BIN1

    GPIO.output(BIN2,GPIO.HIGH)#BIN2

 



####  leftFront函数，小车左拐弯

def leftFront():

    Serve.ChangeDutyCycle(7)

    Moter_PWMA.ChangeDutyCycle(40)#speed[0 - 100]

    GPIO.output(AIN1,GPIO.LOW) #AIN1

    GPIO.output(AIN2,GPIO.HIGH)#AIN2



    Moter_PWMB.ChangeDutyCycle(40)#speed[0 - 100]

    GPIO.output(BIN1,GPIO.HIGH) #BIN1

    GPIO.output(BIN2,GPIO.LOW)#BIN2







####  rightFront函数，小车右拐弯

def rightFront():

    Serve.ChangeDutyCycle(7)

    Moter_PWMA.ChangeDutyCycle(40)#speed[0 - 100]

    GPIO.output(AIN1,GPIO.HIGH) #AIN1

    GPIO.output(AIN2,GPIO.LOW)#AIN2



    Moter_PWMB.ChangeDutyCycle(40)#speed[0 - 100]

    GPIO.output(BIN1,GPIO.LOW) #BIN1

    GPIO.output(BIN2,GPIO.HIGH)#BIN2





####  rear函数，小车后退

def rear():

    Serve.ChangeDutyCycle(7)

    Moter_PWMA.ChangeDutyCycle(20)#speed[0 - 100]

    GPIO.output(AIN1,GPIO.HIGH) #AIN1

    GPIO.output(AIN2,GPIO.LOW)#AIN2



    Moter_PWMB.ChangeDutyCycle(20)#speed[0 - 100]

    GPIO.output(BIN1,GPIO.HIGH) #BIN1

    GPIO.output(BIN2,GPIO.LOW)#BIN2





####  stop函数，小车stop

def stop():

    

    Moter_PWMA.ChangeDutyCycle(0)#speed[0 - 100]

    GPIO.output(AIN1,GPIO.LOW) #AIN1

    GPIO.output(AIN2,GPIO.LOW)#AIN2



    Moter_PWMB.ChangeDutyCycle(0)#speed[0 - 100]

    GPIO.output(BIN1,GPIO.LOW) #BIN1

    GPIO.output(BIN2,GPIO.LOW)#BIN2

 







####  leftRear函数，舵机左退

def leftRear():

    Serve.ChangeDutyCycle(12)



####  rightRear函数，舵机右退

def rightRear():

    Serve.ChangeDutyCycle(3)





####  定义main主函数

def main(status):

    #setup()#setup函数初始化端口

    if status == "front":

        front()

    elif status == "leftFront":

        leftFront()

    elif status == "rightFront":

        rightFront()

    elif status == "rear":

        rear()

    elif status == "stop":

        stop()

    elif status == "leftRear":

        leftRear()

    elif status == "rightRear":

        rightRear()

    







#### 收到浏览器请求，返回一个HTML文件。

@get('/')

def login():

    return template("/home/pi/Desktop/CarMaster/login.html") #### 此处输入html文件的具体目录。



#### 收到浏览器发来的指令。

@post("/cmd")

def cmd():

    adss = request.body.read().decode()

    print("Push the button:" + adss)

    main(adss)

    return "OK"







#### 开启服务器，端口默认8080。

run(host="0.0.0.0", port=8080, debug=True) 

