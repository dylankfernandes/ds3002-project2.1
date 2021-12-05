import schedule
import threading
import boto3
import requests
import json
from collections import defaultdict
import pandas as pd
from decimal import Decimal
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DS3002Streaming')
url = 'https://4feaquhyai.execute-api.us-east-1.amazonaws.com/api/pi'
records = defaultdict(list)
minute = 0

def query_api():
    response = requests.get(url)
    data = json.loads(response.text, parse_float=Decimal)
    return data['factor'], data['pi'], data['time']

def job():
    global minute
    minute += 1

    [factor, pi, time] = query_api()
    records['factor'].append(factor)
    records['pi'].append(pi)
    records['time'].append(time)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Current Time = {current_time}")
    print(f"Inserted: {[factor, pi, time]}")

    response = table.put_item(
        Item={
            'factor': factor,
            'time': time,
            'pi': pi
        }
    )

    return response

def run_thread(function):
    thread = threading.Thread(target=function)
    thread.start()

schedule.every(1).minute.do(run_thread, job)

while True and minute < 60:
    schedule.run_pending()

df = pd.DataFrame(records)
print(df.head())
df.to_csv('streamed.csv')