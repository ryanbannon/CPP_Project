import boto3
from botocore.exceptions import ClientError
import uuid
from datetime import date

def db_put_team_item(team, email, table):
    """
    Function to put an item into the Teams table in DynamoDB
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        dynamoTable = dynamodb.Table(table)
        
        return dynamoTable.put_item(
            Item={
                'ID': str(uuid.uuid4()),
                'Email': email,
                'Datetime': date.today().strftime("%d/%m/%Y"),
                'Team':team
            }
        )
    except Exception as e:
        pass
    
    
def db_put_player_item(player, email, table):
    """
    Function to put an item into the Players table in DynamoDB
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        dynamoTable = dynamodb.Table(table)
        
        return dynamoTable.put_item(
            Item={
                'ID': str(uuid.uuid4()),
                'Email': email,
                'Datetime': date.today().strftime("%d/%m/%Y"),
                'Player':player
            }
        )
    except Exception as e:
        pass
    

def db_scan_items(table):
    """
    Function to retrieve all items in a DynamoDB table
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        dynamoTable = dynamodb.Table(table)
        return dynamoTable.scan()
    except ClientError as err:
        if err.response['Error']['Code'] == 'ExpiredToken':
            print("AWS Token Expired. Renew and retry")
            return