"""Use Cases for eShopOnContainers"""
import time
import requests
import jwt # type: ignore

HOST = 'http://localhost'

PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCqdOSwF3E6I6Wy
    ZE136YxLYzejUgOkri4CvRPj9io7fNgcAYBZPCyriaz41bKepjkdoHgROE3G6rYZ
    YLkkqk7ViKs6vBL3sHnH0snIdc+x0lxKKQQj0HE6SXpYtDRTM/Ed1hMulHj877Qg
    sCVfDw1Tj6MHgA/xKf1gZgnnDR8vDliZaKhd5a+hzPXAetl0k/FLxeeodfAxSjNX
    NCP7Hp1o6/kWasdTWv39tunRrUYu/gFtO1KHiQzLPWFfKWGjQS8+Dmn1ggpK1s0B
    b141a+/lHwc3s896LbUCxSrF6QrShb2OcR0d7ByROhfvHnNQtYrDBkiSyWXRedVz
    NWDLt8IXAgMBAAECggEAG7UKMpjE5hNC96c33nIp71vOgJowDxXkUxFNSTn2LcWX
    0p7ohYNzVrjM0y/YASjPfOzcx3PJqg1J51XNEn7VIf7n/RFIMKx7ccs7fdMEnTOD
    8+a3OQ5vRpmzV6Ax0dp4wDBQMuXzGq4+BILiuDvCn0loUdZJARr3CDMzOzRAqY2y
    Lkdv5wlJzSA0t9+QNFECPx8oTkUoqgvhN89uNp7nngbSvW1NWlJjOnk4LiO4VgEM
    G03hjRnEVkWMIFGH2CtPZTzsZKzF0CX+d9AZsZE68BoaySz/IMJuv3KPyPV8yOMN
    HtUpW34qPrrWnWrlgvtp8dlMdxB5fgts7ksaSBA1yQKBgQDr0Vyzr7Hll71GUqNt
    a1B2WtEbcMKAPtHnF0AabEQWkzqZxIJpWGpELRMH9s6/9H/mX3UhGnCQZHFZ1r0M
    nCfkv2aCW7aEekp3t1UGY3vnYPCfNTDOnEzhGC1pWQ0A9I1aSbOlSCHr4oUVKC7K
    I4S3GaZUXQktDLLJ6ydO87JlyQKBgQC5C4Db6boXXqF6Y/AZo+Uf1gDrT8fv/P+e
    dsC1z+tOhwEV17hfyJntleGXMIPDYeYEjVwloqMv9BdMKDj/Zl7iOfN80N/cg1IW
    OnLvDFTIp05JTJvqmYUnGWDHWCuPUK3Qm+4vzU9t42rcxxWHFEe7+Pv18o+pUnmq
    T+fEJ7RY3wKBgQDJNNOyBSD20ueOTwheXghDU+3DSgzKu88BLBdn9CSMVobTmJXl
    KKlTDlqEmxOBOS6/84bO/e45ZVpJ2y1myv5G8QCYDYTHuEg9qVGEp/GaVF46mXnR
    cA8wqB5nGrI7tG2/Mc90IP3AdIA0sxppIrEkQWBn7xHbPFB4dIoPlWML8QKBgEuf
    Tt8QqrNoQffBpdrkpvuWurNv3FbQfyqkf2cN/K0P8Tqa+UdztKxqx1HBSufrN1R+
    7LyYtbYgO/EssvZ1QKuVYVOODR6SMFbTNitJT9Dcxtqfy0xZxxfOgEWXW93q683I
    G9Q/RIm1GfP2DG8ys4o3W8kMgveAtCYNF7uLOmHjAoGAEOzdfKcjO09FhlSbGodC
    tXBigUXIbBAVVCTYHXUpF7e58uHsiRG9Joqi7nKdoh1QZI72EvFS50WzU581ufol
    xZtBymNaL0VW+3pHW5MigZ7R2U0/Lbc9m1WC+JUh1/LNTVPocRjBO0iaof5Z/NPL
    qQRQI5jEo+ztHsmhVL+myQQ=
    -----END PRIVATE KEY-----"""

JWT_HEADER = {
    "kid": "6B7ACC520305BFDB4F7252DAEB2177CC091FAAE1",
    "typ": "at+jwt",
    "x5t": "a3rMUgMFv9tPclLa6yF3zAkfquE"
}

CHECKOUT_HEADERS = {
    'Host': 'localhost',
    'User-Agent':
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/json',
    'Origin': 'http://localhost',
    'Connection': 'keep-alive',
    'Referer': 'http://localhost/order',
}


def unauth_use_cases():
    """Use cases which do not require login"""
    print('get webmvc')
    req = requests.get(f'{HOST}/webmvc')
    assert req.status_code == 200

    print('get mobile catalog')
    req = requests.get(f'{HOST}/mobileshoppingapigw/catalog-api/api/v1/Catalog/items')
    assert req.json()['count'] == 12

    print('get mobile home')
    req = requests.get(f'{HOST}/mobileshoppingapigw/')
    assert req.status_code == 200

    print('get configuration')
    req = requests.get(f'{HOST}/Home/Configuration')
    assert req.json()['identityUrl'] == 'http://localhost/identity'

    print('get brands')
    req = requests.get(f'{HOST}/webshoppingapigw/c/api/v1/catalog/catalogbrands')
    assert req.json()[0]['brand'] == 'Azure'

    print('get types')
    req = requests.get(f'{HOST}/webshoppingapigw/c/api/v1/catalog/catalogtypes')
    assert req.json()[0]['type'] == 'Mug'

    print('get items')
    req = requests.get(f'{HOST}/webshoppingapigw/c/api/v1/catalog/items')
    assert req.json()['count'] == 12

    print('get userinfo (fail case)')
    req = requests.get(f'{HOST}/identity/connect/userinfo')
    assert req.status_code == 401


def auth_use_cases():
    """Use cases which require an authenticated user"""
    buyer_id = "d25861fe-ed1b-440f-97c2-9aae20585518"

    jwt_payload = {
      "nbf": int(time.time()),
      "exp": int(time.time() + 3600),
      "iss": "null",
      "aud": [
        "orders",
        "basket",
        "webshoppingagg",
        "orders.signalrhub"
      ],
      "client_id": "js",
      "sub": buyer_id,
      "auth_time": int(time.time()),
      "idp": "local",
      "preferred_username": "demouser@microsoft.com",
      "unique_name": "demouser@microsoft.com",
      "name": "DemoUser",
      "last_name": "DemoLastName",
      "card_number": "4012888888881881",
      "card_holder": "DemoUser",
      "card_security_number": "535",
      "card_expiration": "12/21",
      "address_city": "Redmond",
      "address_country": "U.S.",
      "address_state": "WA",
      "address_street": "15703 NE 61st Ct",
      "address_zip_code": "98052",
      "email": "demouser@microsoft.com",
      "email_verified": False,
      "phone_number": "1234567890",
      "phone_number_verified": False,
      "scope": [
        "openid",
        "profile",
        "orders",
        "basket",
        "webshoppingagg",
        "orders.signalrhub"
      ],
      "amr": [
        "pwd"
      ]
    }

    encoded_jwt = jwt.encode(jwt_payload, PRIVATE_KEY, algorithm="RS256",
        headers=JWT_HEADER).decode('utf8')
    headers = {"Authorization": f"Bearer {encoded_jwt}"}

    print('get userinfo')
    req = requests.get(f'{HOST}/identity/connect/userinfo', headers=headers)
    assert req.status_code == 200
    assert req.json()['unique_name'] == 'demouser@microsoft.com'

    print('add item')
    product_id = '08ca23aa-4e71-4bed-b97b-f88b522b99aa'
    payload = {
        "buyerId": buyer_id,
        "items": [
            {
                "pictureUrl":"http://localhost/webshoppingapigw/c/api/v1/catalog/items/2/pic/",
                "productId":2,
                "productName":".NET Black & White Mug",
                "quantity":1,
                "unitPrice":8.5,
                "id": product_id,
                "oldUnitPrice":0
            }
        ]
    }

    req = requests.post(f'{HOST}/webshoppingapigw/api/v1/basket/', headers=headers, json=payload)
    assert req.status_code == 200
    assert req.json()['items'][0]['productId'] == 2

    print('get basket')
    req = requests.get(f'{HOST}/webshoppingapigw/b/api/v1/basket/{buyer_id}', headers=headers)
    assert req.json()['buyerId'] == buyer_id

    print('get basket mobile')
    req = requests.get(f'{HOST}/mobileshoppingapigw/api/v1/Order/draft/{buyer_id}', headers=headers)
    assert req.json()['buyer'] == buyer_id

    print('checkout')
    payload = {
        "street":"15703 NE 61st Ct",
        "city":"Redmond",
        "country":"U.S.",
        "state":"WA",
        "zipcode":"98052",
        "cardexpiration":"2022-01-01T08:00:00.000Z",
        "cardnumber":"4012888888881881",
        "cardsecuritynumber":"535",
        "cardtypeid":1,
        "cardholdername":"DemoUser",
        "total":0,
        "expiration":"12/21"
    }

    req = requests.post(f'{HOST}/webshoppingapigw/b/api/v1/basket/checkout',
            headers={**headers, **CHECKOUT_HEADERS}, json=payload)
    assert req.status_code == 202

    print('get orders')
    req = requests.get(f'{HOST}/webshoppingapigw/o/api/v1/orders', headers=headers)
    assert req.json()[0]['ordernumber'] == 1

    print('get order detail')
    req = requests.get(f'{HOST}/webshoppingapigw/o/api/v1/orders/1', headers=headers)

    assert req.json()['status'] == 'paid'

    # wait for grace period
    time.sleep(90)

if __name__ == "__main__":
    unauth_use_cases()
    auth_use_cases()
