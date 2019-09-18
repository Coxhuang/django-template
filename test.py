import requests
import datetime


while 1:
    r = requests.post(
        'https://search.readmorejoy.com/dream',
        data={
            "title": datetime.datetime.now(),
            "user": "1",
            "input": "*" * 1024
        })
    print(r.status_code)