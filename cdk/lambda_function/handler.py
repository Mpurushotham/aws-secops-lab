import boto3, os, json

def lambda_handler(event, context):
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table(os.environ['TABLE_NAME'])
    body = json.loads(event.get('body', '{}'))
    if 'id' not in body:
        return {'statusCode': 400, 'body': 'Missing id'}
    table.put_item(Item={'id': body['id'], 'message': body.get('message', 'Hello!')})
    return {'statusCode': 200, 'body': json.dumps({'msg': 'Stored successfully'})}
