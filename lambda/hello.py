import json, time

def handler(event, context):
    print ('request:{}'.format(json.dumps(event)))
    cur_time = time.ctime()
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Night, CDK. you hit {}\nTime: {}\n'.format(event['path'], cur_time)
    }
