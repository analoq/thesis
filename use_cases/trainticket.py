"""Use cases for TrainTicket"""
import sys
import time
from datetime import date, timedelta, datetime

import requests
import jwt # type: ignore

HOST = sys.argv[1]

def unauth_use_cases():
    """Use Cases which require no authentication"""
    print('get news')
    req = requests.get(f'{HOST}/news-service/news')
    assert req.json()[0]['Title'] == 'News Service Complete'

    print('get office')
    req = requests.get(f'{HOST}/office/getRegionList')
    assert req.json()[0]['province'] == 'Shanghai'

    print('get captcha')
    req = requests.get(f'{HOST}/api/v1/verifycode/generate')
    assert req.status_code == 200

    print('attempt login')
    payload = {"username":"fdse_microservice","password":"111111","verificationCode":"O8KU"}
    req = requests.post(f'{HOST}/api/v1/users/login', json=payload)
    assert req.json()['status'] == 0


def admin_use_cases():
    """Use Cases which require an admin login"""
    admin_jwt_payload = {
      "sub": "admin",
      "roles": [
        "ROLE_ADMIN"
      ],
      "id": "ad8c8b1a-b11a-4a37-a3d8-c700c39a4eec",
      "iat": int(time.time()),
      "exp": int(time.time() + timedelta(days=1).total_seconds()),
    }
    admin_encoded_jwt = jwt.encode(admin_jwt_payload, "secret", algorithm="HS256").decode('utf8')
    admin_headers = {"Authorization": f"Bearer {admin_encoded_jwt}"}

    print('requires admin')
    req = requests.get(f'{HOST}/api/v1/adminorderservice/adminorder', headers=admin_headers)
    assert req.json()['status'] == 1
    req = requests.get(f'{HOST}/api/v1/adminrouteservice/adminroute', headers=admin_headers)
    assert req.json()['status'] == 1
    req = requests.get(f'{HOST}/api/v1/admintravelservice/admintravel', headers=admin_headers)
    assert req.json()['status'] == 1
    req = requests.get(f'{HOST}/api/v1/adminuserservice/users', headers=admin_headers)
    assert req.json()['status'] == 1
    req = requests.get(f'{HOST}/api/v1/adminbasicservice/adminbasic/contacts',
        headers=admin_headers)
    assert req.json()['status'] == 1


def auth_use_cases(): # pylint: disable=too-many-statements
    """Use Cases which require authentication"""
    jwt_payload = {
      "sub": "fdse_microservice",
      "roles": ["ROLE_USER"],
      "id": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
      "iat": int(time.time()),
      "exp": int(time.time() + timedelta(days=1).total_seconds()),
    }
    encoded_jwt = jwt.encode(jwt_payload, "secret", algorithm="HS256").decode('utf8')
    headers = {"Authorization": f"Bearer {encoded_jwt}"}

    now = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    trip_id = 'D1345'
    trip_other_id = 'Z1235'

    print('assurances')
    req = requests.get(f'{HOST}/api/v1/assuranceservice/assurances/types', headers=headers)
    assert req.json()['status'] == 1

    print('search')
    payload = {
        "startingPlace": "Shang Hai",
        "endPlace": "Su Zhou",
        "departureTime": tomorrow
    }
    req = requests.post(f'{HOST}/api/v1/travelservice/trips/left', headers=headers, json=payload)
    assert req.json()['status'] == 1

    print('advanced search')
    payload = {"startingPlace":"Nan Jing", "endPlace": "Shang Hai", "departureTime": tomorrow}
    req = requests.post(f'{HOST}/api/v1/travelplanservice/travelPlan/cheapest',
        headers=headers, json=payload)
    assert req.json()['status'] == 1

    print('get Foods')
    req = requests.get(f'{HOST}/api/v1/foodservice/foods/2021-03-09/Shang Hai/Su Zhou/{trip_id}',
        headers=headers)
    assert req.json()['status'] == 1

    #### sequence matters

    account_id = '4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f'

    print('contacts')
    req = requests.get(f'{HOST}/api/v1/contactservice/contacts/account/{account_id}',
        headers=headers)
    assert req.json()['status'] == 1
    contact_id = req.json()['data'][0]['id']

    print('get other order list')
    payload = {
        "loginId": account_id, "enableStateQuery": False,
        "enableTravelDateQuery": False,"enableBoughtDateQuery": False,
        "travelDateStart": None, "travelDateEnd": None, "boughtDateStart": None,
        "boughtDateEnd": None
    }
    req = requests.post(f'{HOST}/api/v1/orderOtherService/orderOther/refresh',
        headers=headers, json=payload)
    assert req.json()['status'] == 1

    print('preserveOther')
    payload = {
        "accountId": account_id, "contactsId": contact_id,
        "tripId":"Z1235","seatType":"2","date": tomorrow,
        "from":"nanjing","to":"beijing","assurance":"0","foodType":1,
        "foodName":"Bone Soup","foodPrice":2.5,"stationName":"","storeName":""
    }
    req = requests.post(f'{HOST}/api/v1/preserveotherservice/preserveOther',
        headers=headers, json=payload)
    assert req.json()['status'] == 1

    print('preserve')
    payload = {
        "accountId": account_id, "contactsId": contact_id,
        "tripId":"D1345", "seatType":"2", "date": tomorrow, "from":"Shang Hai",
        "to":"Su Zhou", "assurance":"1", "foodType":2, "stationName":"suzhou",
        "storeName":"Roman Holiday","foodName":"Spicy hot noodles","foodPrice":5,
        "handleDate": tomorrow, "consigneeName":"Doof", "consigneePhone":"123",
        "consigneeWeight":321,"isWithin":False
    }
    req = requests.post(f'{HOST}/api/v1/preserveservice/preserve', headers=headers, json=payload)
    assert req.json()['status'] == 1

    print('consigns for account')
    req = requests.get(f'{HOST}/api/v1/consignservice/consigns/account/{account_id}',
        headers=headers)
    assert req.json()['status'] == 1

    print('get order list')
    payload = {
        "loginId": account_id, "enableStateQuery": False,
        "enableTravelDateQuery": False, "enableBoughtDateQuery": False,
        "travelDateStart": None,"travelDateEnd": None,"boughtDateStart": None,
        "boughtDateEnd": None
    }
    req = requests.post(f'{HOST}/api/v1/orderservice/order/refresh', headers=headers, json=payload)
    assert req.json()['status'] == 1
    order_id = None
    for order in req.json()['data']:
        train_number = order['trainNumber']
        if train_number == trip_id and order['status'] == 0:
            order_id = order['id']

    print('get order Other list')
    req = requests.post(f'{HOST}/api/v1/orderOtherService/orderOther/refresh',
        headers=headers, json=payload)
    assert req.json()['status'] == 1
    order_other_id = None
    for order in req.json()['data']:
        train_number = order['trainNumber']
        if train_number == trip_other_id and order['status'] == 0:
            order_other_id = order['id']


    print('cancel')
    req = requests.get(f'{HOST}/api/v1/cancelservice/cancel/{order_other_id}/{account_id}',
        headers=headers)
    assert req.json()['status'] == 1

    print('pay')
    payload = {
        "orderId": order_id,
        "tripId": trip_id
    }
    req = requests.post(f'{HOST}/api/v1/inside_pay_service/inside_payment',
        headers=headers, json=payload)
    assert req.json()['status'] == 1

    print('collect')
    req = requests.get(f'{HOST}/api/v1/executeservice/execute/collected/{order_id}',
        headers=headers)
    assert req.json()['status'] == 1

    print('enter')
    req = requests.get(f'{HOST}/api/v1/executeservice/execute/execute/{order_id}', headers=headers)
    assert req.json()['status'] == 1

    print('voucher')
    payload = {"orderId": order_id,"type":1}
    req = requests.post(f'{HOST}/getVoucher', headers=headers, json=payload)
    assert req.json()['order_id'] == order_id

    print('rebook')
    payload = {
      "date": now,
      "loginId": account_id,
      "oldTripId": trip_id,
      "orderId": order_id,
      "seatType": 2,
      "tripId": trip_id
    }
    req = requests.post(f'{HOST}/api/v1/rebookservice/rebook', headers=headers, json=payload)
    print(req.json())

if __name__ == "__main__":
    unauth_use_cases()
    admin_use_cases()
    auth_use_cases()
