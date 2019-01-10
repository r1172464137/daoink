#!/usr/bin/env python
#coding:utf-8
"""
file:.py
date:2019/1/7 18:41
author:    peak
description:
"""
from flask import Flask, Blueprint, render_template, request, flash, session, redirect, url_for, g
import json
from app.models import db, User, Order
daoinkpay = Blueprint(
    'daoinkpay',
    __name__,
)

from alipay import AliPay


app_private_key_string = open("D:\Develop_Program\python\\rooprint\\app\controllers\private.pem").read()
alipay_public_key_string = open("D:\Develop_Program\python\\rooprint\\app\controllers\public.pem").read()


alipay = AliPay(
    appid="2018122662657935",
    app_notify_url=None,  # 默认回调url
    app_private_key_string=app_private_key_string,
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_string=alipay_public_key_string,
    # sign_type="RSA",    # RSA 或者 RSA2
    debug=False          # 默认False
)

# 手机网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string

@daoinkpay.route('/pay', methods=['POST', 'GET'])
def pay():
    cost = request.form.get("cost")
    cost = float(cost)
    tradeid = request.form.get("tradeid")

    order_string = alipay.api_alipay_trade_wap_pay(
        out_trade_no=tradeid,
        total_amount=cost,
        subject="道墨云印订单",
        return_url="http://www.daoink.com/alipayresult",
        notify_url="" # 可选, 不填则使用默认notify url
    )
    url = "https://openapi.alipay.com/gateway.do?" + order_string
    return redirect(url)

@daoinkpay.route('/alipayresult', methods=['GET', 'POST'])
def alipayresult():
    trade_out_id = request.args.get("out_trade_no")
    data = request.form.to_dict()
    # sign 不能参与签名验证
    signature = data.pop("sign")

    print(json.dumps(data))
    print(signature)

    # verify
    success = alipay.verify(data, signature)
    if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED" ):
        result_order = Order.query.filter(Order.File_Dir == trade_out_id).first()
        result_order.Print_Status = 1
        db.session.add(result_order)
        db.session.commit()
        result = 1
        return render_template('result.html', result=result)
