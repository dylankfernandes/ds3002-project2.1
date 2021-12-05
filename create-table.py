import boto3

dynamodb = boto3.resource('dynamodb')

table = dynamodb.create_table(
    TableName='DS3002Streaming',
    KeySchema=[
        {
            'AttributeName': 'time',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'factor',
            'KeyType': 'RANGE'
        }
    ],
    BillingMode='PAY_PER_REQUEST',
    AttributeDefinitions=[
        {
            'AttributeName': 'time',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'factor',
            'AttributeType': 'N'
        }
    ]
)

table.meta.client.get_waiter('table_exists').wait(TableName='DS3002Streaming')
print(f'Table has been created: {table}')