#! /usr/bin/python
# -*- coding: utf-8 -*-
#
#   pa_api.py
#
# ------------------------------------------------------------------
import sys
import requests
import hmac
import hashlib
import base64
import urllib.parse
from datetime import datetime
#
# ------------------------------------------------------------------
sys.stderr.write("*** 開始 ***\n")
# Amazon Product Advertising APIの設定
hash_func = hashlib.sha256
encode_func = base64.b64encode
#id関係の設定
access_key = "AK******************"
secret_key = "mn**************************************"
associate_id = "w**********"
#
# メッセージの生成
time_stamp = urllib.parse.quote(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
#
# 商品のASINコード
asin_code = "487311778X"    # (ASINコードがない場合は変わりにISBN-10)
#
query="AWSAccessKeyId=" + access_key + \
    "&AssociateTag=" + associate_id + \
    "&ItemId=" + asin_code + \
    "&Operation=ItemLookup" + \
    "&ResponseGroup=Images%2CItemAttributes%2COffers%2CReviews" + \
    "&Service=AWSECommerceService" + \
    "&Timestamp=" + time_stamp + \
    "&Version=2013-08-01"
api_domain = "webservices.amazon.co.jp"
api_page = "/onca/xml"
message = "\n".join(["GET", api_domain, api_page, query])
#
# HMACのSignature生成
#
sing_gen = hmac.new(secret_key.encode('utf8'), message.encode('utf8'), hash_func)
raw_sign = sing_gen.digest()
sign = urllib.parse.quote(encode_func(raw_sign))

# APIの呼び出し
url = "http://" + api_domain + api_page + "?" + query + "&Signature=" + sign
res = requests.get(url)
with open(asin_code + ".xml", "wb") as ff:
    ff.write(res.content)
sys.stderr.write("*** 終了 ***\n")
# ------------------------------------------------------------------