from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
import os
from dotenv import load_dotenv


load_dotenv()
dynamodb = resource(
    'dynamodb',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_DEFAULT_REGION")
)
table = dynamodb.Table('confitec')

def dynamo_insert(item):

    response = table.put_item(Item=item)
    print("PutItem succeeded:")
    print(response)
    return response

def check_artist_dynamo(id: str) -> bool:

    response = table.get_item(
            Key={"artist_id": id},
            ConsistentRead=True
            )
    return 'Item' in response

def delete_artist(id: str):
    
    table.delete_item(
            Key={'artist_id': id}
        )