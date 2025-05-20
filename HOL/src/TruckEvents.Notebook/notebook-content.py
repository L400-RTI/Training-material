# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "jupyter",
# META     "jupyter_kernel_name": "python3.11"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

! pip install azure-eventhub==5.11.5

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# MARKDOWN ********************

# ## I created a new event hub to capture these events called rti-iad-trucks
# ## Replace event hub connection information with Cloud Labs Event hub

# CELL ********************

import json
import pandas as pd
import concurrent.futures
import time
import requests
from azure.eventhub import EventHubProducerClient, EventData

eventHubConnString = "Endpoint=sb://esehdb0nsbwvuvh00virk1.servicebus.windows.net/;SharedAccessKeyName=key_f8d784ad-675a-4f1d-973a-fda81b57e75f;SharedAccessKey=3a3jDGblfKoSuWPb5H2aH4ZiJmidG7klU+AEhCZc3+s=;EntityPath=es_1e3d1005-327d-4c71-8cb4-ca75cd93c788"
eventHubNameevents = "es_1e3d1005-327d-4c71-8cb4-ca75cd93c788" 

producer_events = EventHubProducerClient.from_connection_string(conn_str=eventHubConnString, eventhub_name=eventHubNameevents)

url = "https://raw.githubusercontent.com/L400-RTI/Training-material/refs/heads/main/HOL/assets/truck_location.csv"

dtype_dict = {
    "TruckID": "int64",
    "latitude": "float64",
    "longitude": "float64",
    "Order": "int64",
}

df_trucks_location = pd.read_csv(url,dtype=dtype_dict)

SLEEP_TIMER = 10

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

def sendToEventsHub(jsonEvent, producer,process_id):
    eventString = jsonEvent
    # print(f"Process: {process_id} - Event: {process_id}")
    event_data_batch = producer.create_batch() 
    event_data_batch.add(EventData(eventString)) 
    producer.send_batch(event_data_batch)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

def sendCarEvents(df_truck,producer_events,process_id):
    for index, row in df_truck.iterrows():
        event = row.to_json()
        sendToEventsHub(event,producer_events,index)
        time.sleep(SLEEP_TIMER)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }

# CELL ********************

while True:
    trucks = df_trucks_location["TruckID"].unique()

    max_parallel = 20

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_parallel) as executor:
        futures = {}
        
        for i,truck in enumerate(trucks[:max_parallel]):
            df_truck = df_trucks_location[df_trucks_location["TruckID"]==truck]
            df_truck = df_truck.set_index(["Order"])
            future = executor.submit(sendCarEvents,
                    df_truck,
                    producer_events,
                    i
                    )
            futures[future] = i

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "jupyter_python"
# META }
