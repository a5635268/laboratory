#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__= 'luhj'

from abc import ABCMeta,abstractmethod

class Payment(metaclass=ABCMeta):
    #抽象产品
    @abstractmethod
    def pay(self,money):
        pass


class AliPay(Payment):
    #具体产品
    def pay(self,money):
        print('使用支付宝支付%s元'%money)

class ApplePay(Payment):
    def pay(self,money):
        print('使用苹果支付支付%s元'%money)

class PaymentFactory(metaclass=ABCMeta):
    #抽象工厂
    @abstractmethod
    def create_payment(self):
        pass

class AliPayFactory(PaymentFactory):
    #具体工厂
    def create_payment(self):
        return AliPay()

class ApplePayFactory(PaymentFactory):
    def create_payment(self):
        return ApplePay()

af = AliPayFactory()
ali = af.create_payment()
ali.pay(100)

#如果要新增支付方式
class WechatPay(Payment):
    def pay(self,money):
        print('使用微信支付%s元'%money)

class WechatPayFactory(PaymentFactory):
    def create_payment(self):
        return WechatPay()

w = WechatPayFactory()
wc = w.create_payment()
wc.pay(200)