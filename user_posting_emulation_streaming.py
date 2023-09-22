import requests
from time import sleep
import random
from multiprocessing import Process
import boto3
import json
import sqlalchemy
from sqlalchemy import text

invoke_url = "https://9024l19ao4.execute-api.us-east-1.amazonaws.com/stream_deploy"

random.seed(100)

class AWSDBConnector:

    def __init__(self):

        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine


new_connector = AWSDBConnector()

def send_data_to_api(stream_name, payload):
    try:
        payload = {
            "StreamName": stream_name,
            "Data": payload,
            "PartitionKey": str(random.randint(1, 10000))  # You can choose your partition key logic
        }

        headers = {'Content-Type': 'application/json'}

        response = requests.request("PUT", f"{invoke_url}/{stream_name}/record", headers=headers, data=payload)
        response.raise_for_status()

        print(f"Data sent to API for stream {stream_name}")
        print("Response status code:", response.status_code)
        print("Response content:", response.content)
    except Exception as e:
        print(f"Failed to send data to API for stream {stream_name}: {str(e)}")


def run_infinite_post_data_loop():
    while True:
        sleep(random.randrange(0, 2))
        random_row = random.randint(0, 11000)
        engine = new_connector.create_db_connector()

        with engine.connect() as connection:

            pin_string = text(f"SELECT * FROM pinterest_data LIMIT {random_row}, 1")
            pin_selected_row = connection.execute(pin_string)
            
            for row in pin_selected_row:
                pin_result = dict(row._mapping)
                pin_payload = json.dumps({
                    "records": [
                        {      
                        "value": {"index": pin_result["index"], "unique_id": pin_result["unique_id"], "title": pin_result["title"], "description": pin_result["description"], "poster_name": pin_result["poster_name"], "follower_count": pin_result["follower_count"], "tag_list": pin_result["tag_list"], "is_image_or_video": pin_result["is_image_or_video"], "image_src": pin_result["image_src"], "downloaded": pin_result["downloaded"], "save_location": pin_result["save_location"], "category": pin_result["category"]}
                        }
                    ]
                })
            
            
            
            send_data_to_api("streaming-12a3410ba3cf-pin", pin_payload)

            geo_string = text(f"SELECT * FROM geolocation_data LIMIT {random_row}, 1")
            geo_selected_row = connection.execute(geo_string)
            
            for row in geo_selected_row:
                geo_result = dict(row._mapping)
                geo_result['timestamp'] = geo_result['timestamp'].isoformat()
                geo_payload = json.dumps({
                    "records": [
                        {     
                        "value": {"ind": geo_result["ind"], "timestamp": geo_result["timestamp"], "latitude": geo_result["latitude"], "longitude": geo_result["longitude"], "country": geo_result["country"]}
                        }
                    ]
                })
                

            
            send_data_to_api("streaming-12a3410ba3cf-geo", geo_payload)

            user_string = text(f"SELECT * FROM user_data LIMIT {random_row}, 1")
            user_selected_row = connection.execute(user_string)
            
            for row in user_selected_row:
                user_result = dict(row._mapping)
                user_result['date_joined'] = user_result['date_joined'].isoformat()
                user_payload = json.dumps({
                    "records": [
                        {
                        #Data should be send as pairs of column_name:value, with different columns separated by commas       
                        "value": {"ind": user_result["ind"], "first_name": user_result["first_name"], "last_name": user_result["last_name"], "age": user_result["age"], "date_joined": user_result["date_joined"]}
                        }
                    ]
                })
                
            
            send_data_to_api("streaming-12a3410ba3cf-user", user_payload)
            
            


if __name__ == "__main__":
    print('Working')
    run_infinite_post_data_loop()
