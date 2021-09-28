import json
import os
import requests
from datetime import date
from datetime import timedelta
from requests.exceptions import HTTPError



def app():
    start_date = date(date.today().year, 1, 1)
    end_date = date.today()
    url = 'https://robot-dreams-de-api.herokuapp.com/auth'
    headers = {'content-type': 'application/json'}
    payload = {"username": "rd_dreams", "password": "djT6LasE"}
    try:
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        token ="JWT " + (r.json())['access_token']
        url = 'https://robot-dreams-de-api.herokuapp.com/out_of_stock'
        headers = {'content-type': 'application/json', 'Authorization':token}
        data = {"date": start_date}
        while start_date <=end_date:
            data = {"date": str(start_date)}
            dir = os.path.join('.', 'partitioned_data', str(start_date))
            os.makedirs(dir, exist_ok=True)
            r = requests.get(url, data=json.dumps(data), headers=headers )
            with open (os.path.join(dir,'products.json'),'w') as json_file:
                json.dump(r.json(),json_file)
            print ('data for '+str(start_date)+' loaded')
            start_date=start_date + timedelta(days=1)
    except HTTPError:
        print ('HTTP Error!!')

if __name__ == '__main__':
    app()